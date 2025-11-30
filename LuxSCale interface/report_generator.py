"""
Report Generator
===============

Generates lighting design reports similar to Dialux format.
Calculates lighting parameters based on room dimensions and luminaire specifications.
"""

import json
import math
from typing import Dict, Any
from pathlib import Path

class ReportGenerator:
    """
    Generates lighting design reports with calculated parameters.
    
    This class creates a report structure similar to Dialux reports,
    including metadata, lighting setup, rooms, luminaires, and scenes.
    """
    
    def __init__(self, standards_path: str):
        """
        Initialize the report generator.
        
        Args:
            standards_path: Path to standards_filtered.json file
        """
        self.standards_path = standards_path
        self.standards_data = self._load_standards()
    
    def _load_standards(self) -> Dict:
        """Load standards data for reference"""
        try:
            with open(self.standards_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return {'standards': data}
                elif isinstance(data, dict) and 'standards' in data:
                    return data
                else:
                    return {'standards': []}
        except Exception as e:
            print(f"Warning: Could not load standards: {e}")
            return {'standards': []}
    
    def generate_report(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete lighting design report.
        
        Args:
            input_data: Dictionary containing user input parameters
            
        Returns:
            Complete report data structure similar to Dialux format
        """
        # Calculate derived parameters
        room_area = input_data['room_length'] * input_data['room_width']
        total_power = input_data['luminaire_count'] * input_data['luminaire_power']
        
        # Calculate luminous flux if not provided
        if input_data.get('luminous_flux'):
            luminous_flux_per_luminaire = input_data['luminous_flux']
            efficacy = luminous_flux_per_luminaire / input_data['luminaire_power']
        elif input_data.get('efficacy'):
            efficacy = input_data['efficacy']
            luminous_flux_per_luminaire = input_data['luminaire_power'] * efficacy
        else:
            # Default efficacy if neither provided
            efficacy = 100.0
            luminous_flux_per_luminaire = input_data['luminaire_power'] * efficacy
        
        total_luminous_flux = input_data['luminaire_count'] * luminous_flux_per_luminaire
        
        # Calculate illuminance (simplified calculation)
        # Using basic formula: E = (Φ × n × UF × MF) / A
        # Where: Φ = luminous flux, n = number of luminaires, UF = utilization factor, MF = maintenance factor
        # Simplified: assuming UF = 0.5 and MF = 0.8 (typical values)
        utilization_factor = 0.5
        maintenance_factor = 0.8
        average_lux = (total_luminous_flux * utilization_factor * maintenance_factor) / room_area
        
        # Estimate min/max lux (assuming uniformity of 0.6)
        uniformity = 0.6  # Estimated
        min_lux = average_lux * uniformity
        max_lux = average_lux * (1.0 + (1.0 - uniformity))
        
        # Generate room layout (simple grid)
        layout = self._generate_room_layout(
            input_data['room_length'],
            input_data['room_width'],
            input_data['room_height'],
            input_data['luminaire_count'],
            input_data['mounting_height']
        )
        
        # Build report structure
        report = {
            "metadata": {
                "company_name": input_data.get('company_name', 'Not specified'),
                "project_name": input_data['project_name'],
                "engineer": "LuxSCale Generator",
                "email": "",
                "report_title": f"LuxSCale_Report_{input_data['project_name'].replace(' ', '_')}"
            },
            "lighting_setup": {
                "average_lux": round(average_lux, 1),
                "min_lux": round(min_lux, 1),
                "max_lux": round(max_lux, 1),
                "uniformity": round(uniformity, 2),
                "power_w": round(input_data['luminaire_power'], 1),
                "power_total_w": round(total_power, 1),
                "luminous_flux_lm": round(luminous_flux_per_luminaire, 1),
                "luminous_flux_total": round(total_luminous_flux, 1),
                "luminous_efficacy_lm_per_w": round(efficacy, 1),
                "mounting_height_m": round(input_data['mounting_height'], 2),
                "work_plane_height": round(input_data.get('work_plane_height', 0.75), 2),
                "quantity": input_data['luminaire_count']
            },
            "rooms": [
                {
                    "name": f"Room 1 - {input_data['project_name']}",
                    "arrangement": "Grid",
                    "utilisation_profile": input_data['room_type'],
                    "layout": layout
                }
            ],
            "luminaires": [
                {
                    "quantity": input_data['luminaire_count'],
                    "manufacturer": input_data.get('manufacturer', 'Not specified'),
                    "article_no": input_data.get('article_no', 'Not specified'),
                    "power_w": round(input_data['luminaire_power'], 1),
                    "luminous_flux_lm": round(luminous_flux_per_luminaire, 1),
                    "luminous_efficacy_lm_per_w": round(efficacy, 1)
                }
            ],
            "scenes": [
                {
                    "scene_name": input_data['project_name'],
                    "average_lux": round(average_lux, 1),
                    "min_lux": round(min_lux, 1),
                    "max_lux": round(max_lux, 1),
                    "uniformity": round(uniformity, 2),
                    "utilisation_profile": input_data['room_type']
                }
            ]
        }
        
        return report
    
    def _generate_room_layout(self, length: float, width: float, height: float, 
                              num_luminaires: int, mounting_height: float) -> list:
        """
        Generate a simple grid layout for luminaires.
        
        Args:
            length: Room length in meters
            width: Room width in meters
            height: Room height in meters
            num_luminaires: Number of luminaires
            mounting_height: Mounting height in meters
            
        Returns:
            List of coordinate points for luminaire positions
        """
        layout = []
        
        # Calculate grid dimensions
        # Try to create a roughly square grid
        cols = int(math.ceil(math.sqrt(num_luminaires)))
        rows = int(math.ceil(num_luminaires / cols))
        
        # Calculate spacing
        spacing_x = length / (cols + 1) if cols > 0 else length / 2
        spacing_y = width / (rows + 1) if rows > 0 else width / 2
        
        # Generate positions
        luminaire_index = 0
        for row in range(rows):
            for col in range(cols):
                if luminaire_index >= num_luminaires:
                    break
                
                x = spacing_x * (col + 1)
                y = spacing_y * (row + 1)
                z = mounting_height
                
                layout.append({
                    "X": round(x, 3),
                    "Y": round(y, 3),
                    "Z": round(z, 3)
                })
                
                luminaire_index += 1
            
            if luminaire_index >= num_luminaires:
                break
        
        return layout


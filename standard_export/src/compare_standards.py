#!/usr/bin/env python3
"""
Standards Comparison Utility

This script compares project report data against the extracted EN 12464-1 standards.
"""

import json
import os
from typing import Dict, List, Any, Optional

def load_standards(standards_path: str = "output/final_standards.json") -> List[Dict[str, Any]]:
    """Load standards from JSON file."""
    if not os.path.exists(standards_path):
        raise FileNotFoundError(f"Standards file not found: {standards_path}")
    
    with open(standards_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Handle both old format (list) and new format (dict with metadata)
        if isinstance(data, dict) and 'standards' in data:
            return data['standards']
        return data

def find_matching_standard(standards: List[Dict[str, Any]], 
                          utilisation_profile: str) -> Optional[Dict[str, Any]]:
    """Find matching standard based on utilisation profile."""
    profile_lower = utilisation_profile.lower()
    
    for standard in standards:
        if standard["category"] and standard["task_or_activity"]:
            category_lower = standard["category"].lower()
            activity_lower = standard["task_or_activity"].lower()
            
            # Check if profile contains category or activity
            if (category_lower in profile_lower or 
                activity_lower in profile_lower or
                profile_lower in category_lower or
                profile_lower in activity_lower):
                return standard
    
    return None

def compare_project_to_standard(project_data: Dict[str, Any], 
                               standard: Dict[str, Any]) -> Dict[str, Any]:
    """Compare project data against standard requirements."""
    comparison = {
        "project_data": project_data,
        "standard": standard,
        "compliance": {},
        "recommendations": []
    }
    
    # Compare illuminance values
    if "average_lux" in project_data and standard["Em_r_lx"]:
        project_lux = project_data["average_lux"]
        required_lux = standard["Em_r_lx"]
        
        if project_lux >= required_lux:
            comparison["compliance"]["illuminance"] = "PASS"
        else:
            comparison["compliance"]["illuminance"] = "FAIL"
            comparison["recommendations"].append(
                f"Insufficient illuminance: {project_lux} lx (required: {required_lux} lx)"
            )
    
    # Compare uniformity
    if "uniformity" in project_data and standard["Uo"]:
        project_uniformity = project_data["uniformity"]
        required_uniformity = standard["Uo"]
        
        if project_uniformity >= required_uniformity:
            comparison["compliance"]["uniformity"] = "PASS"
        else:
            comparison["compliance"]["uniformity"] = "FAIL"
            comparison["recommendations"].append(
                f"Insufficient uniformity: {project_uniformity} (required: {required_uniformity})"
            )
    
    # Compare color rendering
    if "Ra" in project_data and standard["Ra"]:
        project_ra = project_data["Ra"]
        required_ra = standard["Ra"]
        
        if project_ra >= required_ra:
            comparison["compliance"]["color_rendering"] = "PASS"
        else:
            comparison["compliance"]["color_rendering"] = "FAIL"
            comparison["recommendations"].append(
                f"Insufficient color rendering: Ra {project_ra} (required: Ra {required_ra})"
            )
    
    return comparison

def main():
    """Main function to demonstrate comparison."""
    try:
        # Load standards
        standards = load_standards()
        print(f"Loaded {len(standards)} standards")
        
        # Example project data
        project_data = {
            "utilisation_profile": "Traffic zones inside buildings - Corridors and circulation areas",
            "average_lux": 120,
            "uniformity": 0.45,
            "Ra": 80
        }
        
        print(f"\nProject data: {project_data}")
        
        # Find matching standard
        standard = find_matching_standard(standards, project_data["utilisation_profile"])
        
        if standard:
            print(f"\nFound matching standard: {standard['ref_no']} - {standard['task_or_activity']}")
            
            # Compare
            comparison = compare_project_to_standard(project_data, standard)
            
            print("\nCompliance Results:")
            for key, result in comparison["compliance"].items():
                print(f"  {key}: {result}")
            
            if comparison["recommendations"]:
                print("\nRecommendations:")
                for rec in comparison["recommendations"]:
                    print(f"  - {rec}")
            else:
                print("\nAll requirements met!")
        else:
            print("No matching standard found")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

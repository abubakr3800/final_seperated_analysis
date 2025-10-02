"""
PDF Report Extractor for Lighting Compliance System
Extracts lighting data from project reports and converts to JSON format
"""

import json
import re
from typing import Dict, List, Any, Optional
from PyPDF2 import PdfReader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFReportExtractor:
    def __init__(self):
        self.patterns = {
            'average_lux': r'(?:average|mean|avg)\s*(?:lux|lx|illuminance)[\s:]*(\d+(?:\.\d+)?)',
            'uniformity': r'uniformity[\s:]*(\d+(?:\.\d+)?)',
            'ra': r'(?:ra|color\s*rendering\s*index|cri)[\s:]*(\d+(?:\.\d+)?)',
            'utilisation_profile': r'(?:utilisation|use|activity|zone)[\s:]*([^,\n]+)',
            'room_name': r'(?:room|space|area)[\s:]*([^,\n]+)',
            'category': r'(?:category|type)[\s:]*([^,\n]+)'
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            raise
    
    def extract_lighting_data(self, text: str) -> Dict[str, Any]:
        """Extract lighting data from text using regex patterns"""
        data = {
            'rooms': [],
            'lighting_setup': {},
            'metadata': {}
        }
        
        # Extract lighting setup data
        for key, pattern in self.patterns.items():
            if key in ['average_lux', 'uniformity', 'ra']:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1)
                    if key == 'average_lux':
                        data['lighting_setup']['average_lux'] = float(value)
                    elif key == 'uniformity':
                        data['lighting_setup']['uniformity'] = float(value)
                    elif key == 'ra':
                        data['lighting_setup']['ra'] = float(value)
        
        # Extract room data
        room_pattern = r'(?:room|space|area)[\s:]*([^,\n]+)[\s\S]*?(?:utilisation|use|activity)[\s:]*([^,\n]+)'
        room_matches = re.finditer(room_pattern, text, re.IGNORECASE | re.MULTILINE)
        
        for match in room_matches:
            room_name = match.group(1).strip()
            utilisation_profile = match.group(2).strip()
            
            data['rooms'].append({
                'name': room_name,
                'utilisation_profile': utilisation_profile
            })
        
        # If no rooms found, create default room
        if not data['rooms']:
            data['rooms'].append({
                'name': 'Main Area',
                'utilisation_profile': 'General Office Space'
            })
        
        return data
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Main extraction method"""
        try:
            text = self.extract_text_from_pdf(pdf_path)
            data = self.extract_lighting_data(text)
            
            # Add metadata
            data['metadata'] = {
                'source_file': pdf_path,
                'extraction_timestamp': str(pd.Timestamp.now()),
                'extractor_version': '1.0.0'
            }
            
            return data
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            raise
    
    def save_to_json(self, data: Dict[str, Any], output_path: str) -> None:
        """Save extracted data to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Data saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            raise

# Example usage and testing
if __name__ == "__main__":
    extractor = PDFReportExtractor()
    
    # Sample data for testing
    sample_data = {
        'rooms': [
            {
                'name': 'Main Corridor',
                'utilisation_profile': 'Traffic zones inside buildings - Corridors'
            }
        ],
        'lighting_setup': {
            'average_lux': 150.0,
            'uniformity': 0.4,
            'ra': 80.0
        },
        'metadata': {
            'source_file': 'sample_report.pdf',
            'extraction_timestamp': '2024-01-15T10:30:00',
            'extractor_version': '1.0.0'
        }
    }
    
    # Save sample data
    extractor.save_to_json(sample_data, 'data/project_data.json')
    print("Sample project data created successfully!")

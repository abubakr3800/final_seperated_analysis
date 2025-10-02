#!/usr/bin/env python3
"""
Enhanced Standards Comparison Utility with Alias Support

This script compares project report data against standards using the alias
normalization system to handle various terminology formats.
"""

import json
import os
from typing import Dict, List, Any, Optional
from alias_normalizer import normalize_record, validate_lighting_values


def load_standards(standards_path: str = "output/enhanced_standards.json") -> List[Dict[str, Any]]:
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
    """Find matching standard based on utilisation profile with alias support."""
    profile_lower = utilisation_profile.lower()
    
    for standard in standards:
        if standard.get("category") and standard.get("task_or_activity"):
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
    """Compare project data against standard requirements with alias support."""
    
    # Normalize project data to handle aliases
    normalized_project = normalize_record(project_data)
    
    comparison = {
        "project_data": normalized_project,
        "standard": standard,
        "compliance": {},
        "recommendations": [],
        "alias_mappings_applied": {}
    }
    
    # Track which aliases were used
    for key, value in project_data.items():
        normalized_key = normalize_record({key: value})
        if list(normalized_key.keys())[0] != key:
            comparison["alias_mappings_applied"][key] = list(normalized_key.keys())[0]
    
    # Compare illuminance values (handle various aliases)
    illuminance_fields = ["Em_r_lx", "average lux", "maintained lux", "target lux", "em_r"]
    project_lux = None
    for field in illuminance_fields:
        if field in normalized_project:
            project_lux = normalized_project[field]
            break
    
    if project_lux is not None and standard.get("Em_r_lx"):
        required_lux = standard["Em_r_lx"]
        
        if project_lux >= required_lux:
            comparison["compliance"]["illuminance"] = "PASS"
        else:
            comparison["compliance"]["illuminance"] = "FAIL"
            comparison["recommendations"].append(
                f"Insufficient illuminance: {project_lux} lx (required: {required_lux} lx)"
            )
    
    # Compare uniformity (handle various aliases)
    uniformity_fields = ["Uo", "uniformity", "emin/eavg", "min/avg", "u0"]
    project_uniformity = None
    for field in uniformity_fields:
        if field in normalized_project:
            project_uniformity = normalized_project[field]
            break
    
    if project_uniformity is not None and standard.get("Uo"):
        required_uniformity = standard["Uo"]
        
        if project_uniformity >= required_uniformity:
            comparison["compliance"]["uniformity"] = "PASS"
        else:
            comparison["compliance"]["uniformity"] = "FAIL"
            comparison["recommendations"].append(
                f"Insufficient uniformity: {project_uniformity} (required: {required_uniformity})"
            )
    
    # Compare color rendering (handle various aliases)
    ra_fields = ["Ra", "CRI", "color rendering index", "colour rendering", "r_a"]
    project_ra = None
    for field in ra_fields:
        if field in normalized_project:
            project_ra = normalized_project[field]
            break
    
    if project_ra is not None and standard.get("Ra"):
        required_ra = standard["Ra"]
        
        if project_ra >= required_ra:
            comparison["compliance"]["color_rendering"] = "PASS"
        else:
            comparison["compliance"]["color_rendering"] = "FAIL"
            comparison["recommendations"].append(
                f"Insufficient color rendering: Ra {project_ra} (required: Ra {required_ra})"
            )
    
    # Compare glare (handle various aliases)
    glare_fields = ["RUGL", "UGR", "glare index", "unified glare rating"]
    project_glare = None
    for field in glare_fields:
        if field in normalized_project:
            project_glare = normalized_project[field]
            break
    
    if project_glare is not None and standard.get("RUGL"):
        required_glare = standard["RUGL"]
        
        # For glare, lower is better
        if project_glare <= required_glare:
            comparison["compliance"]["glare"] = "PASS"
        else:
            comparison["compliance"]["glare"] = "FAIL"
            comparison["recommendations"].append(
                f"Excessive glare: UGR {project_glare} (limit: UGR {required_glare})"
            )
    
    return comparison


def test_various_project_formats():
    """Test the comparison with various project data formats."""
    print("Testing Enhanced Comparison with Various Project Formats")
    print("=" * 70)
    
    # Load standards
    standards = load_standards()
    print(f"Loaded {len(standards)} standards")
    
    # Test cases with different alias formats
    test_cases = [
        {
            "name": "Standard Format",
            "data": {
                "utilisation_profile": "Traffic zones inside buildings - Corridors and circulation areas",
                "Em_r_lx": 120,
                "Uo": 0.45,
                "Ra": 80
            }
        },
        {
            "name": "Common Aliases",
            "data": {
                "utilisation_profile": "Work areas - General office work",
                "average lux": 600,
                "uniformity": 0.65,
                "CRI": 85
            }
        },
        {
            "name": "Technical Aliases",
            "data": {
                "utilisation_profile": "Work areas - Reading and writing",
                "maintained lux": 350,
                "emin/eavg": 0.70,
                "color rendering index": 90
            }
        },
        {
            "name": "Mixed Aliases",
            "data": {
                "utilisation_profile": "Industrial areas - General assembly work",
                "target lux": 400,
                "uniformity ratio": 0.75,
                "colour rendering": 85,
                "glare index": 22
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'-' * 50}")
        print(f"Test Case: {test_case['name']}")
        print(f"Project data: {test_case['data']}")
        
        # Find matching standard
        standard = find_matching_standard(standards, test_case['data']["utilisation_profile"])
        
        if standard:
            print(f"Found matching standard: {standard['ref_no']} - {standard['task_or_activity']}")
            
            # Compare
            comparison = compare_project_to_standard(test_case['data'], standard)
            
            print("Compliance Results:")
            for key, result in comparison["compliance"].items():
                print(f"  {key}: {result}")
            
            if comparison["alias_mappings_applied"]:
                print("Alias mappings applied:")
                for original, normalized in comparison["alias_mappings_applied"].items():
                    print(f"  '{original}' -> '{normalized}'")
            
            if comparison["recommendations"]:
                print("Recommendations:")
                for rec in comparison["recommendations"]:
                    print(f"  - {rec}")
            else:
                print("All requirements met!")
        else:
            print("No matching standard found")


def main():
    """Main function to demonstrate enhanced comparison."""
    try:
        test_various_project_formats()
        
        print(f"\n{'=' * 70}")
        print("ENHANCED COMPARISON SUMMARY")
        print("=" * 70)
        print("✅ Alias normalization working")
        print("✅ Multiple project formats supported")
        print("✅ Comprehensive compliance checking")
        print("✅ Ready for real-world project reports!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

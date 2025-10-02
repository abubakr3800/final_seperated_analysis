#!/usr/bin/env python3
"""
Lighting Standards Alias Normalizer

This module implements the alias mapping system from alias.txt to normalize
lighting terminology across different reports and standards.
"""

from typing import Dict, List, Any, Optional, Union
import re


# Comprehensive alias mapping based on alias.txt
ALIASES = {
    # Illuminance
    "Em_r_lx": [
        "em_r_lx", "em", "e_m", "average lux", "maintained lux", "target lux",
        "maintained illuminance", "required illuminance", "reference illuminance",
        "illuminance", "lux", "lx", "em_r", "em_r_lx", "maintained_illuminance"
    ],
    "Em_u_lx": [
        "em_u_lx", "upper lux", "max lux", "maximum lux", "recommended lux",
        "upper illuminance", "max illuminance", "em_u", "em_u_lx"
    ],
    
    # Uniformity
    "Uo": [
        "uo", "u0", "uniformity", "emin/eavg", "min/avg", "illuminance uniformity",
        "uniformity ratio", "uniformity factor", "u_o", "uniformity_index"
    ],
    
    # Glare
    "RUGL": [
        "rugl", "ugr", "glare index", "unified glare rating", "glare rating",
        "ugr limit", "glare limit", "unified_glare_rating", "glare_rating"
    ],
    
    # Color Rendering
    "Ra": [
        "ra", "cri", "color rendering index", "r_a", "colour rendering index",
        "color rendering", "colour rendering", "cri_ra", "rendering_index"
    ],
    "R9": [
        "r9", "cri_r9", "red rendering", "red color rendering", "r_9",
        "red_rendering", "cri_red"
    ],
    
    # Color Temperature
    "CCT": [
        "cct", "ct", "colour temperature", "k", "kelvin", "color temperature",
        "correlated colour temperature", "correlated color temperature",
        "colour_temp", "color_temp", "kelvin_temp"
    ],
    
    # Luminance / Luminous Parameters
    "Ez_lx": [
        "ez_lx", "background lux", "surround illuminance", "e_z", "ez",
        "background illuminance", "surround lux", "ambient illuminance"
    ],
    "luminous_flux_lm": [
        "luminous flux", "flux", "lm", "φ", "phi", "luminous output",
        "light flux", "light output", "luminous_flux", "light_flux"
    ],
    "power_w": [
        "power", "wattage", "lamp power", "p", "w", "watts", "electrical power",
        "lamp wattage", "fixture power", "luminous_power"
    ],
    
    # Geometry
    "mounting_height_m": [
        "mounting height", "suspension height", "hm", "height", "mounting_height",
        "suspension_height", "fixture height", "lamp height", "h_m"
    ],
    
    # Efficiency / Efficacy
    "luminous_efficacy_lm_per_w": [
        "lm/w", "efficacy", "η", "eta", "luminous efficiency", "efficiency",
        "luminous_efficacy", "light_efficiency", "lm_per_w", "lumens_per_watt"
    ],
    
    # Additional common aliases
    "Em_wall_lx": [
        "em_wall_lx", "wall lux", "wall illuminance", "wall lighting",
        "wall_illuminance", "em_wall", "wall_lux"
    ],
    "Em_ceiling_lx": [
        "em_ceiling_lx", "ceiling lux", "ceiling illuminance", "ceiling lighting",
        "ceiling_illuminance", "em_ceiling", "ceiling_lux"
    ],
    "specific_requirements": [
        "specific requirements", "requirements", "notes", "comments",
        "additional requirements", "special requirements", "remarks",
        "specific_reqs", "additional_notes"
    ],
    "ref_no": [
        "ref_no", "reference", "ref", "reference number", "standard ref",
        "table ref", "clause ref", "reference_no", "standard_reference"
    ],
    "category": [
        "category", "type", "classification", "group", "area type",
        "space type", "zone type", "category_type"
    ],
    "task_or_activity": [
        "task_or_activity", "task", "activity", "description", "task description",
        "activity description", "space description", "task_description",
        "activity_description", "space_type"
    ]
}


def normalize_key(key: str) -> str:
    """
    Normalize a field key using the alias mapping.
    
    Args:
        key: The field key to normalize
        
    Returns:
        The canonical field name or original key if no match found
    """
    if not key:
        return key
    
    key_lower = key.strip().lower()
    
    # Direct lookup first
    for canonical, aliases in ALIASES.items():
        if key_lower in [a.lower() for a in aliases]:
            return canonical
    
    # Fuzzy matching for common variations
    key_clean = re.sub(r'[_\-\s]+', '_', key_lower)
    for canonical, aliases in ALIASES.items():
        for alias in aliases:
            alias_clean = re.sub(r'[_\-\s]+', '_', alias.lower())
            if key_clean == alias_clean:
                return canonical
    
    # Return original key if no match found
    return key


def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize all keys in a record using the alias mapping.
    
    Args:
        record: Dictionary with potentially non-standard keys
        
    Returns:
        Dictionary with normalized keys
    """
    normalized = {}
    
    for key, value in record.items():
        normalized_key = normalize_key(key)
        normalized[normalized_key] = value
    
    return normalized


def find_aliases_for_field(field_name: str) -> List[str]:
    """
    Find all aliases for a given canonical field name.
    
    Args:
        field_name: The canonical field name
        
    Returns:
        List of all aliases for the field
    """
    return ALIASES.get(field_name, [])


def get_all_canonical_fields() -> List[str]:
    """
    Get all canonical field names.
    
    Returns:
        List of all canonical field names
    """
    return list(ALIASES.keys())


def detect_field_type(field_name: str) -> str:
    """
    Detect the type/category of a field based on its name.
    
    Args:
        field_name: The field name to categorize
        
    Returns:
        The field type category
    """
    field_lower = field_name.lower()
    
    if any(term in field_lower for term in ['lux', 'lx', 'illuminance', 'em_']):
        return "illuminance"
    elif any(term in field_lower for term in ['uniformity', 'uo', 'u0']):
        return "uniformity"
    elif any(term in field_lower for term in ['glare', 'ugr', 'rugl']):
        return "glare"
    elif any(term in field_lower for term in ['ra', 'cri', 'rendering']):
        return "color_rendering"
    elif any(term in field_lower for term in ['cct', 'temperature', 'kelvin']):
        return "color_temperature"
    elif any(term in field_lower for term in ['flux', 'lm', 'luminous']):
        return "luminous_parameters"
    elif any(term in field_lower for term in ['power', 'watt', 'w']):
        return "power"
    elif any(term in field_lower for term in ['height', 'mounting']):
        return "geometry"
    elif any(term in field_lower for term in ['efficacy', 'efficiency', 'lm/w']):
        return "efficiency"
    else:
        return "other"


def validate_lighting_values(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate lighting values with enhanced range checking.
    
    Args:
        record: Dictionary with lighting values
        
    Returns:
        Dictionary with validation results
    """
    validation_issues = []
    
    # Ra must be ≤ 100
    if record.get("Ra") is not None:
        ra_value = float(record["Ra"])
        if ra_value > 100:
            validation_issues.append(f"Ra {ra_value} > 100")
            record["Ra"] = None
    
    # Uo must be ≤ 1
    if record.get("Uo") is not None:
        uo_value = float(record["Uo"])
        if uo_value > 1:
            validation_issues.append(f"Uo {uo_value} > 1")
            record["Uo"] = None
    
    # Em_r_lx should be within reasonable range (20-20000 lux)
    if record.get("Em_r_lx") is not None:
        em_value = float(record["Em_r_lx"])
        if em_value < 20 or em_value > 20000:
            validation_issues.append(f"Em_r_lx {em_value} outside range 20-20000")
            record["Em_r_lx"] = None
    
    # RUGL should be within reasonable range (10-40)
    if record.get("RUGL") is not None:
        rugl_value = float(record["RUGL"])
        if rugl_value < 10 or rugl_value > 40:
            validation_issues.append(f"RUGL {rugl_value} outside range 10-40")
            record["RUGL"] = None
    
    # CCT should be within reasonable range (2000-10000 K)
    if record.get("CCT") is not None:
        cct_value = float(record["CCT"])
        if cct_value < 2000 or cct_value > 10000:
            validation_issues.append(f"CCT {cct_value} outside range 2000-10000 K")
            record["CCT"] = None
    
    # Add validation info
    if validation_issues:
        record["validation_issues"] = validation_issues
        record["needs_review"] = True
    else:
        record["needs_review"] = False
    
    return record


def create_alias_report(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a report showing alias usage in the dataset.
    
    Args:
        records: List of records to analyze
        
    Returns:
        Dictionary with alias usage statistics
    """
    field_usage = {}
    alias_mappings = {}
    
    for record in records:
        for key in record.keys():
            canonical = normalize_key(key)
            if canonical != key:
                # This was an alias
                if canonical not in alias_mappings:
                    alias_mappings[canonical] = []
                if key not in alias_mappings[canonical]:
                    alias_mappings[canonical].append(key)
            
            field_usage[canonical] = field_usage.get(canonical, 0) + 1
    
    return {
        "total_records": len(records),
        "field_usage": field_usage,
        "alias_mappings": alias_mappings,
        "canonical_fields_found": list(field_usage.keys())
    }


if __name__ == "__main__":
    # Test the alias system
    print("Testing Alias Normalization System")
    print("=" * 50)
    
    # Test normalize_key function
    test_keys = [
        "average lux", "uniformity", "UGR", "CRI", "colour temperature",
        "lm/w", "mounting height", "wall lux", "specific requirements"
    ]
    
    print("Key normalization tests:")
    for key in test_keys:
        normalized = normalize_key(key)
        print(f"  '{key}' -> '{normalized}'")
    
    # Test record normalization
    test_record = {
        "average lux": 500,
        "uniformity": 0.6,
        "UGR": 19,
        "CRI": 80,
        "colour temperature": 4000,
        "lm/w": 100,
        "mounting height": 2.5,
        "wall lux": 100,
        "specific requirements": "Test requirements"
    }
    
    print(f"\nOriginal record: {test_record}")
    normalized_record = normalize_record(test_record)
    print(f"Normalized record: {normalized_record}")
    
    # Test validation
    validated_record = validate_lighting_values(normalized_record)
    print(f"Validation result: needs_review = {validated_record.get('needs_review', False)}")
    
    print(f"\nAll canonical fields: {get_all_canonical_fields()}")

# Aliases.json Usage Map

## 📋 Overview

This document maps all locations where `aliases.json` is used in the system for parameter detection and field recognition.

**Aliases File Location**: `report_export/extractors/aliases.json`

---

## 🔍 Current Usage Locations

### **1. Report Extraction (PDF → JSON)**

#### **File**: `report_export/extractors/final_extractor.py`

**Line**: 76-119
```python
def __init__(self, alias_file: str = "aliases.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    alias_path = os.path.join(base_dir, alias_file)
    
    # Load aliases.json
    with open(alias_path, "r", encoding="utf-8") as f:
        self.aliases = json.load(f)
```

**Usage Points**:
- **Line 375-397**: `_extract_lighting_setup()` - Uses aliases to extract lighting parameters
  - Searches for parameter aliases in PDF text
  - Maps aliases to standard parameter names
  - Example: Finds "ē", "lux", "average lux" → maps to "average_lux"

- **Line 250-272**: `_normalize_parameter_name()` - Normalizes parameter names using aliases
  - Converts various parameter name variations to standard names

- **Line 273-295**: `_normalize_place_name()` - Normalizes place names using aliases
  - Converts various place name variations to standard names

- **Line 898-918**: `_extract_scenes()` - Fallback alias-based scene extraction
  - Uses aliases to find scene parameters when main extraction fails

**Purpose**: Extract parameters from PDF text using alias recognition

---

#### **File**: `report_export/api/api_server.py`

**Line**: 52
```python
extractor = FinalPDFExtractor("aliases.json")
```

**Usage**: Initializes the extractor with aliases.json for API requests

**Purpose**: API server uses extractor with aliases for PDF processing

---

### **2. Compliance Checking (JSON → Standards Comparison)**

#### **File**: `final project/src/compliance_checker.py`

**Line**: 40-48 (Updated)
```python
def _load_parameter_mapping(self) -> Dict:
    """Load parameter mapping from aliases.json file"""
    aliases_file = Path(__file__).parent.parent.parent / "report_export" / "extractors" / "aliases.json"
    with open(aliases_file, 'r', encoding='utf-8') as f:
        aliases = json.load(f)
        return aliases
```

**Usage Points**:
- **Line 174-190**: `_find_parameter_value()` - Finds parameter values using aliases
  - Searches for parameter aliases in extracted report data
  - Maps aliases to standard parameter names
  - Example: Finds "lux", "ē", "average lux" → maps to "average_lux"

- **Line 311-313**: `_perform_room_compliance_check()` - Uses aliases to find parameters
  - Finds average_lux using aliases
  - Finds uniformity using aliases
  - Finds Ra/CRI using aliases

**Purpose**: Match extracted report parameters to standard parameter names for comparison

---

## 📊 Parameter Detection Flow

### **Step 1: PDF Extraction (Uses aliases.json)**

```
PDF Text
    ↓
final_extractor.py uses aliases.json
    ↓
Searches for aliases: ["lux", "ē", "average lux", ...]
    ↓
Maps to standard: "average_lux"
    ↓
Extracted JSON: {"average_lux": 213.0}
```

**Code Path**: `report_export/extractors/final_extractor.py`
- Method: `_extract_lighting_setup()` (line 369)
- Uses: `self.aliases.get("parameters", {})`

---

### **Step 2: Compliance Checking (Uses aliases.json)**

```
Extracted JSON: {"lux": 213.0, "uniformity": 0.57}
    ↓
compliance_checker.py uses aliases.json
    ↓
Searches for aliases: ["lux", "ē", "average lux", ...]
    ↓
Maps to standard: "average_lux"
    ↓
Comparison: average_lux (213.0) vs Em_r_lx (100.0)
```

**Code Path**: `final project/src/compliance_checker.py`
- Method: `_find_parameter_value()` (line 174)
- Uses: `self.parameter_mapping['parameters'].get(parameter_type, [])`

---

## 🔧 Integration Points

### **1. Report Extraction API**

**File**: `report_export/api/api_server.py`
- **Line 52**: Initializes extractor with aliases.json
- **Purpose**: Extract parameters from uploaded PDFs

**Flow**:
```
User uploads PDF
    ↓
API Server calls FinalPDFExtractor("aliases.json")
    ↓
Extractor uses aliases to find parameters
    ↓
Returns JSON with standardized parameter names
```

---

### **2. Compliance Checking API**

**File**: `final project/src/api_server.py`
- **Line 47**: Initializes ComplianceChecker
- **Purpose**: Compare extracted data to standards

**Flow**:
```
Extracted JSON received
    ↓
ComplianceChecker loads aliases.json
    ↓
Uses aliases to find parameters in extracted data
    ↓
Compares to standards
    ↓
Returns compliance results
```

---

### **3. Compliance Checker**

**File**: `final project/src/compliance_checker.py`
- **Line 40-48**: Loads aliases.json
- **Line 174-190**: Uses aliases to find parameters
- **Line 311-313**: Uses aliases in compliance checks

**Flow**:
```
Report data: {"lux": 213.0, "uo": 0.57}
    ↓
_find_parameter_value(data, "average_lux")
    ↓
Searches aliases: ["lux", "ē", "average lux", ...]
    ↓
Finds "lux" → maps to "average_lux"
    ↓
Returns: {"found": True, "value": 213.0, "source": "lux"}
```

---

## 📝 Alias Mapping Structure

### **Parameters Section**

```json
{
  "parameters": {
    "average_lux": ["lux", "ē", "avg lux", "average lux", "avr.lux", ...],
    "min_lux": ["emin", "e_min", "minimum lux", ...],
    "max_lux": ["emax", "e_max", "maximum lux", ...],
    "uniformity": ["uniformity", "uo", "uo (g1)", "uniformity ratio", ...],
    "color_rendering_ra": ["ra", "cri", "color rendering", ...],
    ...
  }
}
```

### **Places Section**

```json
{
  "places": {
    "Factory": ["factory", "the factory", "industrial hall", ...],
    "Office": ["office", "workplace", "working place", ...],
    ...
  }
}
```

---

## 🎯 Key Methods Using Aliases

### **1. Extraction Methods**

#### **`_extract_lighting_setup()`** - `final_extractor.py:369`
- **Purpose**: Extract lighting parameters from PDF text
- **Uses Aliases**: Yes
- **Alias Section**: `parameters`
- **Example**: Finds "lux" → maps to "average_lux"

#### **`_normalize_parameter_name()`** - `final_extractor.py:250`
- **Purpose**: Normalize parameter names
- **Uses Aliases**: Yes
- **Alias Section**: `parameters`

#### **`_normalize_place_name()`** - `final_extractor.py:273`
- **Purpose**: Normalize place/room names
- **Uses Aliases**: Yes
- **Alias Section**: `places`

---

### **2. Compliance Methods**

#### **`_find_parameter_value()`** - `compliance_checker.py:174`
- **Purpose**: Find parameter value in extracted data using aliases
- **Uses Aliases**: Yes
- **Alias Section**: `parameters`
- **Example**: 
  ```python
  _find_parameter_value(data, "average_lux")
  # Searches for: ["lux", "ē", "avg lux", "average lux", ...]
  # Returns: {"found": True, "value": 213.0, "source": "lux"}
  ```

#### **`_perform_room_compliance_check()`** - `compliance_checker.py:296`
- **Purpose**: Perform compliance check using alias-found parameters
- **Uses Aliases**: Yes (via `_find_parameter_value()`)
- **Alias Section**: `parameters`

---

## 🔄 Complete Workflow with Aliases

### **End-to-End Flow**

```
1. PDF Upload
   ↓
2. final_extractor.py loads aliases.json
   ↓
3. Extracts text from PDF
   ↓
4. Uses aliases to find parameters:
   - Searches for "lux", "ē", "average lux" → finds "average_lux"
   - Searches for "uo", "uniformity" → finds "uniformity"
   ↓
5. Returns JSON: {"average_lux": 213.0, "uniformity": 0.57}
   ↓
6. compliance_checker.py loads aliases.json
   ↓
7. Uses aliases to find parameters in JSON:
   - If JSON has "lux" instead of "average_lux"
   - Searches aliases → maps "lux" to "average_lux"
   ↓
8. Compares to standards:
   - average_lux (213.0) vs Em_r_lx (100.0)
   - uniformity (0.57) vs Uo (0.4)
   ↓
9. Returns compliance results
```

---

## 📁 File Locations

### **Aliases File**
- **Path**: `report_export/extractors/aliases.json`
- **Used By**: 
  - `report_export/extractors/final_extractor.py`
  - `final project/src/compliance_checker.py`

### **Code Files Using Aliases**

1. **`report_export/extractors/final_extractor.py`**
   - Line 76: `__init__()` - Loads aliases.json
   - Line 250: `_normalize_parameter_name()` - Uses aliases
   - Line 273: `_normalize_place_name()` - Uses aliases
   - Line 369: `_extract_lighting_setup()` - Uses aliases
   - Line 898: `_extract_scenes()` - Uses aliases

2. **`report_export/api/api_server.py`**
   - Line 52: Initializes extractor with aliases.json

3. **`final project/src/compliance_checker.py`**
   - Line 40: `_load_parameter_mapping()` - Loads aliases.json
   - Line 174: `_find_parameter_value()` - Uses aliases
   - Line 311: `_perform_room_compliance_check()` - Uses aliases

---

## ✅ Benefits of Using Aliases

### **1. Flexible Parameter Recognition**
- Handles different naming conventions
- Example: "lux", "ē", "average lux" all map to "average_lux"

### **2. Better Extraction Accuracy**
- Finds parameters even with different names
- Reduces "parameter not found" errors

### **3. Consistent Standardization**
- All parameters mapped to standard names
- Easier comparison and analysis

### **4. Easy Maintenance**
- Add new aliases to one file
- Automatically used by all components

---

## 🔧 Adding New Aliases

### **To Add New Parameter Alias**

Edit `report_export/extractors/aliases.json`:

```json
{
  "parameters": {
    "average_lux": [
      "lux",
      "ē",
      "avg lux",
      "average lux",
      "NEW_ALIAS_HERE"  // Add here
    ]
  }
}
```

### **To Add New Place Alias**

```json
{
  "places": {
    "Factory": [
      "factory",
      "the factory",
      "NEW_FACTORY_ALIAS"  // Add here
    ]
  }
}
```

**No code changes needed** - aliases are automatically loaded!

---

## 📊 Alias Usage Statistics

### **Current Aliases in aliases.json**

- **Parameters**: 15+ parameter types with 100+ aliases
- **Places**: 17+ place types with 50+ aliases

### **Usage Frequency**

- **Extraction**: Used in every PDF extraction
- **Compliance**: Used in every compliance check
- **API Calls**: Used in every API request

---

## 🎯 Summary

### **Files Using aliases.json**

1. ✅ `report_export/extractors/final_extractor.py` - PDF extraction
2. ✅ `report_export/api/api_server.py` - API server initialization
3. ✅ `final project/src/compliance_checker.py` - Compliance checking

### **Key Methods**

1. ✅ `_extract_lighting_setup()` - Extract parameters from PDF
2. ✅ `_find_parameter_value()` - Find parameters in JSON
3. ✅ `_normalize_parameter_name()` - Normalize parameter names
4. ✅ `_normalize_place_name()` - Normalize place names

### **Purpose**

- **Extraction**: Find parameters in PDF text using various names
- **Compliance**: Find parameters in extracted JSON using various names
- **Standardization**: Map all variations to standard names

---

**Last Updated**: 2024  
**Aliases File**: `report_export/extractors/aliases.json`  
**Status**: ✅ Integrated and Active


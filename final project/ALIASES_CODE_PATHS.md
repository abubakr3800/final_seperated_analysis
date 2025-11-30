# Aliases.json Code Paths Reference

## 📍 Quick Reference: Where aliases.json is Used

### **Aliases File Location**
```
report_export/extractors/aliases.json
```

---

## 🔍 Code Files Using aliases.json

### **1. PDF Extraction**

#### **File**: `report_export/extractors/final_extractor.py`

**Line 76**: `__init__(self, alias_file: str = "aliases.json")`
- **Purpose**: Load aliases.json during initialization
- **Path**: `report_export/extractors/aliases.json`
- **Usage**: Loads aliases for parameter and place recognition

**Line 369-397**: `_extract_lighting_setup(self, text: str)`
- **Purpose**: Extract lighting parameters from PDF text
- **Uses**: `self.aliases.get("parameters", {})`
- **Example**: Searches for "lux", "ē", "average lux" → maps to "average_lux"

**Line 250-272**: `_normalize_parameter_name(self, param_name: str)`
- **Purpose**: Normalize parameter names using aliases
- **Uses**: `self.aliases["parameters"]`
- **Example**: "lux" → "average_lux"

**Line 273-295**: `_normalize_place_name(self, place_name: str)`
- **Purpose**: Normalize place/room names using aliases
- **Uses**: `self.aliases["places"]`
- **Example**: "the factory" → "Factory"

**Line 898-918**: `_extract_scenes(self, text: str, data: Dict)`
- **Purpose**: Fallback alias-based scene extraction
- **Uses**: `self.aliases["parameters"]`
- **Example**: Finds scene parameters using aliases when main extraction fails

---

### **2. API Server (Report Extraction)**

#### **File**: `report_export/api/api_server.py`

**Line 52**: `extractor = FinalPDFExtractor("aliases.json")`
- **Purpose**: Initialize extractor with aliases for API requests
- **Path**: `report_export/extractors/aliases.json` (relative to extractor)
- **Usage**: All PDF extraction requests use aliases

---

### **3. Compliance Checking**

#### **File**: `final project/src/compliance_checker.py`

**Line 40-48**: `_load_parameter_mapping(self) -> Dict`
- **Purpose**: Load aliases.json for compliance checking
- **Path**: `report_export/extractors/aliases.json` (absolute path)
- **Usage**: Loads aliases once during initialization
- **Code**:
  ```python
  aliases_file = Path(__file__).parent.parent.parent / "report_export" / "extractors" / "aliases.json"
  with open(aliases_file, 'r', encoding='utf-8') as f:
      aliases = json.load(f)
      return aliases
  ```

**Line 188-210**: `_find_parameter_value(self, data: Dict, parameter_type: str) -> Dict`
- **Purpose**: Find parameter value using aliases
- **Uses**: `self.parameter_mapping['parameters'].get(parameter_type, [])`
- **Example**: 
  ```python
  _find_parameter_value(data, "average_lux")
  # Searches for: ["lux", "ē", "avg lux", "average lux", ...]
  # Returns: {"found": True, "value": 213.0, "source": "lux"}
  ```

**Line 324-332**: `_perform_room_compliance_check()` - Parameter Detection
- **Purpose**: Use aliases to find parameters in extracted data
- **Uses**: `_find_parameter_value()` with aliases
- **Code**:
  ```python
  # Find average_lux using aliases
  avg_lux_result = self._find_parameter_value(lighting_setup, 'average_lux')
  average_lux = avg_lux_result['value'] if avg_lux_result['found'] else lighting_setup.get('average_lux', 0)
  
  # Find uniformity using aliases
  uniformity_result = self._find_parameter_value(lighting_setup, 'uniformity')
  uniformity = uniformity_result['value'] if uniformity_result['found'] else lighting_setup.get('uniformity', 0)
  ```

**Line 329**: `_find_parameter_value()` for Ra/CRI
- **Purpose**: Find color rendering index using aliases
- **Uses**: Aliases for "color_rendering_ra": ["ra", "cri", "color rendering", ...]

---

## 📊 Usage Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│              aliases.json                                │
│  report_export/extractors/aliases.json                  │
└──────────────┬──────────────────────────────────────────┘
               │
               ├──────────────────────────────────────────┐
               │                                           │
               ▼                                           ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│  final_extractor.py          │        │  compliance_checker.py        │
│  (PDF Extraction)            │        │  (Compliance Checking)        │
│                               │        │                               │
│  Line 76: Load aliases        │        │  Line 40: Load aliases        │
│  Line 369: Extract params    │        │  Line 188: Find params        │
│  Line 250: Normalize params   │        │  Line 324: Use aliases        │
│  Line 273: Normalize places  │        │                               │
│  Line 898: Fallback extract   │        │                               │
└──────────────────────────────┘        └──────────────────────────────┘
               │                                           │
               │                                           │
               ▼                                           ▼
┌──────────────────────────────┐        ┌──────────────────────────────┐
│  Extracted JSON               │        │  Compliance Results          │
│  {"lux": 213.0, ...}          │───────▶│  {"average_lux": 213.0, ...} │
└──────────────────────────────┘        └──────────────────────────────┘
```

---

## 🎯 Key Methods Summary

| Method | File | Line | Purpose | Uses Aliases |
|--------|------|------|---------|--------------|
| `__init__()` | `final_extractor.py` | 76 | Load aliases.json | ✅ Yes |
| `_extract_lighting_setup()` | `final_extractor.py` | 369 | Extract parameters | ✅ Yes |
| `_normalize_parameter_name()` | `final_extractor.py` | 250 | Normalize params | ✅ Yes |
| `_normalize_place_name()` | `final_extractor.py` | 273 | Normalize places | ✅ Yes |
| `_extract_scenes()` | `final_extractor.py` | 898 | Fallback extraction | ✅ Yes |
| `_load_parameter_mapping()` | `compliance_checker.py` | 40 | Load aliases.json | ✅ Yes |
| `_find_parameter_value()` | `compliance_checker.py` | 188 | Find parameters | ✅ Yes |
| `_perform_room_compliance_check()` | `compliance_checker.py` | 324 | Use aliases | ✅ Yes |

---

## 🔧 How to Add New Aliases

### **Step 1: Edit aliases.json**

**File**: `report_export/extractors/aliases.json`

**Example**: Add new alias for "average_lux"
```json
{
  "parameters": {
    "average_lux": [
      "lux",
      "ē",
      "avg lux",
      "average lux",
      "NEW_ALIAS_HERE"  // Add your new alias
    ]
  }
}
```

### **Step 2: No Code Changes Needed!**

The aliases are automatically loaded by:
- ✅ `final_extractor.py` (line 76)
- ✅ `compliance_checker.py` (line 40)

**Both will automatically use the new alias!**

---

## 📝 Verification Commands

### **Check if aliases.json is loaded**

**In final_extractor.py**:
```python
extractor = FinalPDFExtractor("aliases.json")
print(extractor.aliases)  # Should show loaded aliases
```

**In compliance_checker.py**:
```python
checker = ComplianceChecker(standards_path, api_url)
print(checker.parameter_mapping)  # Should show loaded aliases
```

### **Test parameter detection**

```python
# Test data with alias name
test_data = {"lux": 213.0, "uo": 0.57}

# Should find using aliases
checker = ComplianceChecker(standards_path, api_url)
result = checker._find_parameter_value(test_data, "average_lux")
print(result)  # Should show: {"found": True, "value": 213.0, "source": "lux"}
```

---

## ✅ Summary

### **Files Using aliases.json**

1. ✅ `report_export/extractors/final_extractor.py` - PDF extraction
2. ✅ `report_export/api/api_server.py` - API initialization  
3. ✅ `final project/src/compliance_checker.py` - Compliance checking

### **Key Integration Points**

- **Extraction**: Uses aliases to find parameters in PDF text
- **Compliance**: Uses aliases to find parameters in extracted JSON
- **Standardization**: Maps all variations to standard names

### **Result**

- ✅ Better parameter detection
- ✅ Handles different parameter names
- ✅ Consistent alias usage across system

---

**Aliases File**: `report_export/extractors/aliases.json`  
**Status**: ✅ Integrated and Active  
**All Components**: Using Same Aliases File


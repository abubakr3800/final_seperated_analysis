# Aliases.json Code Reference - Complete Paths

## 📍 Aliases File Location

```
report_export/extractors/aliases.json
```

---

## 🔍 All Code Paths Using aliases.json

### **1. PDF Extraction - final_extractor.py**

**File**: `report_export/extractors/final_extractor.py`

#### **Path 1.1: Load aliases.json**
- **Line**: 76-119
- **Method**: `__init__(self, alias_file: str = "aliases.json")`
- **Code**:
  ```python
  base_dir = os.path.dirname(os.path.abspath(__file__))
  alias_path = os.path.join(base_dir, alias_file)
  with open(alias_path, "r", encoding="utf-8") as f:
      self.aliases = json.load(f)
  ```
- **Purpose**: Load aliases during extractor initialization
- **Uses**: `self.aliases` (stored for later use)

---

#### **Path 1.2: Extract Lighting Parameters**
- **Line**: 369-397
- **Method**: `_extract_lighting_setup(self, text: str)`
- **Code**:
  ```python
  params = self.aliases.get("parameters", {})
  for standard, variations in params.items():
      for alias in variations:
          pattern = rf"(?<!\w){re.escape(alias)}(?!\w)\s*[:=]?\s*{number_pattern}"
          m = re.search(pattern, text, re.IGNORECASE)
          if m:
              lighting_setup[standard] = val
  ```
- **Purpose**: Find parameters in PDF text using aliases
- **Example**: Searches for "lux", "ē", "average lux" → finds and maps to "average_lux"

---

#### **Path 1.3: Normalize Parameter Names**
- **Line**: 250-272
- **Method**: `_normalize_parameter_name(self, param_name: str)`
- **Code**:
  ```python
  for standard, variations in self.aliases["parameters"].items():
      if param_name.lower() in [v.lower() for v in variations]:
          return standard
  ```
- **Purpose**: Convert parameter name variations to standard names
- **Example**: "lux" → "average_lux"

---

#### **Path 1.4: Normalize Place Names**
- **Line**: 273-295
- **Method**: `_normalize_place_name(self, place_name: str)`
- **Code**:
  ```python
  for standard, variations in self.aliases["places"].items():
      if place_name.lower() in [v.lower() for v in variations]:
          return standard
  ```
- **Purpose**: Convert place name variations to standard names
- **Example**: "the factory" → "Factory"

---

#### **Path 1.5: Fallback Scene Extraction**
- **Line**: 898-918
- **Method**: `_extract_scenes(self, text: str, data: Dict)`
- **Code**:
  ```python
  for standard, variations in self.aliases["parameters"].items():
      for alias in variations:
          match = re.search(rf"{alias}\s*[:=]?\s*([\d.]+)", text, re.IGNORECASE)
          if match:
              alias_scene[standard] = float(match.group(1))
  ```
- **Purpose**: Fallback extraction when main scene extraction fails
- **Example**: Finds scene parameters using aliases

---

### **2. API Server - api_server.py**

**File**: `report_export/api/api_server.py`

#### **Path 2.1: Initialize Extractor with Aliases**
- **Line**: 52
- **Code**:
  ```python
  extractor = FinalPDFExtractor("aliases.json")
  ```
- **Purpose**: API server uses extractor with aliases for all PDF processing
- **Usage**: Every PDF upload uses aliases for extraction

---

### **3. Compliance Checking - compliance_checker.py**

**File**: `final project/src/compliance_checker.py`

#### **Path 3.1: Load aliases.json**
- **Line**: 40-48
- **Method**: `_load_parameter_mapping(self) -> Dict`
- **Code**:
  ```python
  aliases_file = Path(__file__).parent.parent.parent / "report_export" / "extractors" / "aliases.json"
  if aliases_file.exists():
      with open(aliases_file, 'r', encoding='utf-8') as f:
          aliases = json.load(f)
          print(f"✓ Loaded aliases from {aliases_file}")
          return aliases
  ```
- **Purpose**: Load aliases for compliance checking
- **Stored As**: `self.parameter_mapping`

---

#### **Path 3.2: Find Parameter Values Using Aliases**
- **Line**: 188-210
- **Method**: `_find_parameter_value(self, data: Dict, parameter_type: str) -> Dict`
- **Code**:
  ```python
  parameter_aliases = self.parameter_mapping['parameters'].get(parameter_type, [])
  
  # Try direct match first
  if parameter_type in data and data[parameter_type] is not None:
      return {'found': True, 'source': parameter_type, 'value': data[parameter_type]}
  
  # Try all aliases
  for alias in parameter_aliases:
      if alias in data and data[alias] is not None:
          return {'found': True, 'source': alias, 'value': data[alias]}
      
      # Try case-insensitive match
      for key in data.keys():
          if key.lower() == alias.lower() and data[key] is not None:
              return {'found': True, 'source': key, 'value': data[key]}
  ```
- **Purpose**: Find parameter values in extracted JSON using aliases
- **Example**: 
  - Input: `data = {"lux": 213.0}`, `parameter_type = "average_lux"`
  - Searches aliases: `["lux", "ē", "avg lux", "average lux", ...]`
  - Finds: `"lux"` → Returns: `{"found": True, "value": 213.0, "source": "lux"}`

---

#### **Path 3.3: Use Aliases in Compliance Checks**
- **Line**: 349-354
- **Method**: `_perform_room_compliance_check()` - Parameter Detection
- **Code**:
  ```python
  # Try to find average_lux using aliases
  avg_lux_result = self._find_parameter_value(lighting_setup, 'average_lux')
  average_lux = avg_lux_result['value'] if avg_lux_result['found'] else lighting_setup.get('average_lux', 0)
  
  # Try to find uniformity using aliases
  uniformity_result = self._find_parameter_value(lighting_setup, 'uniformity')
  uniformity = uniformity_result['value'] if uniformity_result['found'] else lighting_setup.get('uniformity', 0)
  ```
- **Purpose**: Find parameters using aliases before comparison
- **Example**: 
  - If JSON has `{"lux": 213.0}` instead of `{"average_lux": 213.0}`
  - Uses aliases to find "lux" → maps to "average_lux" → uses 213.0 for comparison

---

#### **Path 3.4: Find Ra/CRI Using Aliases**
- **Line**: 357
- **Method**: `_perform_room_compliance_check()` - Ra Detection
- **Code**:
  ```python
  ra = self._find_parameter_value(lighting_setup, 'color_rendering_ra')
  ```
- **Purpose**: Find color rendering index using aliases
- **Aliases Used**: `["ra", "cri", "color rendering", "colour rendering index", ...]`

---

## 📊 Complete Usage Flow

```
┌─────────────────────────────────────────────────────────────┐
│  aliases.json                                                │
│  report_export/extractors/aliases.json                       │
└──────────────┬──────────────────────────────────────────────┘
               │
               ├──────────────────────────────┐
               │                              │
               ▼                              ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│  final_extractor.py       │    │  compliance_checker.py   │
│  (PDF Extraction)          │    │  (Compliance Checking)   │
│                            │    │                          │
│  Line 76: Load            │    │  Line 40: Load           │
│  Line 369: Extract        │    │  Line 188: Find          │
│  Line 250: Normalize      │    │  Line 349: Use            │
│  Line 273: Normalize      │    │  Line 353: Use            │
│  Line 898: Fallback       │    │  Line 357: Use            │
└──────────────────────────┘    └──────────────────────────┘
               │                              │
               │                              │
               ▼                              ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│  Extracted JSON           │    │  Compliance Results       │
│  (May have aliases)       │───▶│  (Using alias-found       │
│  {"lux": 213.0}           │    │   parameters)             │
└──────────────────────────┘    └──────────────────────────┘
```

---

## 🎯 Key Methods Summary

| # | Method | File | Line | Purpose | Alias Section |
|---|--------|------|------|---------|---------------|
| 1 | `__init__()` | `final_extractor.py` | 76 | Load aliases.json | Both |
| 2 | `_extract_lighting_setup()` | `final_extractor.py` | 369 | Extract parameters | parameters |
| 3 | `_normalize_parameter_name()` | `final_extractor.py` | 250 | Normalize params | parameters |
| 4 | `_normalize_place_name()` | `final_extractor.py` | 273 | Normalize places | places |
| 5 | `_extract_scenes()` | `final_extractor.py` | 898 | Fallback extract | parameters |
| 6 | `_load_parameter_mapping()` | `compliance_checker.py` | 40 | Load aliases.json | Both |
| 7 | `_find_parameter_value()` | `compliance_checker.py` | 188 | Find parameters | parameters |
| 8 | `_perform_room_compliance_check()` | `compliance_checker.py` | 349 | Use aliases | parameters |
| 9 | `_perform_room_compliance_check()` | `compliance_checker.py` | 353 | Use aliases | parameters |
| 10 | `_perform_room_compliance_check()` | `compliance_checker.py` | 357 | Use aliases | parameters |

---

## 📝 Detailed Code References

### **Extraction Phase**

**File**: `report_export/extractors/final_extractor.py`

1. **Line 76-119**: `__init__()` - Loads aliases.json
2. **Line 369-397**: `_extract_lighting_setup()` - Uses aliases to extract from PDF text
3. **Line 250-272**: `_normalize_parameter_name()` - Normalizes using aliases
4. **Line 273-295**: `_normalize_place_name()` - Normalizes using aliases
5. **Line 898-918**: `_extract_scenes()` - Fallback alias-based extraction

### **API Phase**

**File**: `report_export/api/api_server.py`

1. **Line 52**: `FinalPDFExtractor("aliases.json")` - Initializes with aliases

### **Compliance Phase**

**File**: `final project/src/compliance_checker.py`

1. **Line 40-48**: `_load_parameter_mapping()` - Loads aliases.json
2. **Line 188-210**: `_find_parameter_value()` - Uses aliases to find parameters
3. **Line 349**: Uses aliases to find `average_lux`
4. **Line 353**: Uses aliases to find `uniformity`
5. **Line 357**: Uses aliases to find `color_rendering_ra`

---

## ✅ Verification

### **Check if aliases.json is loaded correctly**

**In final_extractor.py**:
```python
extractor = FinalPDFExtractor("aliases.json")
print("Aliases loaded:", "parameters" in extractor.aliases)
print("Parameter aliases:", len(extractor.aliases.get("parameters", {})))
```

**In compliance_checker.py**:
```python
checker = ComplianceChecker(standards_path, api_url)
print("Aliases loaded:", "parameters" in checker.parameter_mapping)
print("Parameter aliases:", len(checker.parameter_mapping.get("parameters", {})))
```

### **Test parameter detection**

```python
# Test with alias name
test_data = {"lux": 213.0, "uo": 0.57}

checker = ComplianceChecker(standards_path, api_url)

# Should find using aliases
avg_lux = checker._find_parameter_value(test_data, "average_lux")
print(avg_lux)  # {"found": True, "value": 213.0, "source": "lux"}

uniformity = checker._find_parameter_value(test_data, "uniformity")
print(uniformity)  # {"found": True, "value": 0.57, "source": "uo"}
```

---

## 🎯 Summary

### **Files Using aliases.json**

1. ✅ `report_export/extractors/final_extractor.py` - 5 usage points
2. ✅ `report_export/api/api_server.py` - 1 usage point
3. ✅ `final project/src/compliance_checker.py` - 5 usage points

### **Total Usage Points**: 11

### **Purpose**

- **Extraction**: Find parameters in PDF text using various names
- **Compliance**: Find parameters in extracted JSON using various names
- **Standardization**: Map all variations to standard names

---

**Aliases File**: `report_export/extractors/aliases.json`  
**Status**: ✅ Fully Integrated  
**All Components**: Using Same File


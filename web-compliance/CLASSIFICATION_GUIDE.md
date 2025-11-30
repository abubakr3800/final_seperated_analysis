# Report Classification Guide

This document explains how the system classifies uploaded reports and matches them to lighting standards.

## Overview

The classification process works in **two main steps**:

1. **Determine Utilisation Profile**: Extract or infer the utilisation profile for each room
2. **Match to Standards Array**: Search through the `standards_filtered.json` array to find matching standard

---

## Step 1: Determining Utilisation Profile

The system tries to determine the utilisation profile for each room in this order:

### 1.1 From Room Data
```python
utilisation_profile = room.get('utilisation_profile', '')
```

### 1.2 From Scene Data (if room profile is empty)
The system checks the corresponding scene:
- If scene name contains: `factory`, `industrial`, `warehouse`, `manufacturing`, `production`
  → Sets profile to: **"Industrial activities and crafts"**
- If scene has `utilisation_profile` field → Uses that value
- If scene name contains: `working place` or `work`
  → Sets profile to: **"Industrial activities and crafts"**

### 1.3 From Room Name (if still empty)
The system analyzes the room name for keywords:

| Keyword in Room Name | Assigned Profile |
|---------------------|-----------------|
| `factory`, `industrial`, `warehouse`, `manufacturing`, `production`, `workshop` | **"Industrial activities and crafts"** |
| `office` | **"Offices"** |
| `corridor`, `hallway` | **"Traffic zones inside buildings"** |
| `storage`, `store` | **"General areas inside buildings – Store rooms, cold stores"** |
| `building`, `room` (generic) | Checks project name:<br>- If project contains factory/industrial → **"Industrial activities and crafts"**<br>- Otherwise → **"General areas inside buildings"** |
| (no match) | **"General areas inside buildings"** (default fallback) |

### 1.4 Example Flow

```
Room: "building 1 · storey 1 · room 1"
├─ Room has utilisation_profile? → NO
├─ Check scene name: "the factory"
│  └─ Contains "factory" → YES
│     └─ Profile: "Industrial activities and crafts"
└─ Result: "Industrial activities and crafts"
```

---

## Step 2: Matching to Standards Array

The system searches through the **`standards_filtered.json`** array, which contains all lighting standards.

### 2.1 Standards Array Structure

The `standards_filtered.json` file is an **array of standard objects**:

```json
[
  {
    "ref_no": "6.1.1",
    "category": "Traffic zones inside buildings",
    "task_or_activity": "Corridors and circulation areas",
    "Em_r_lx": 100.0,
    "Em_u_lx": 100.0,
    "Uo": 0.4,
    "Ra": 40.0,
    ...
  },
  {
    "ref_no": "6.1.2",
    "category": "Traffic zones inside buildings",
    "task_or_activity": "Stairs",
    "Em_r_lx": 100.0,
    ...
  },
  ...
]
```

### 2.2 Matching Algorithm

The system uses a **priority-based matching algorithm** that searches in this order:

#### **Priority 1: Exact Match with Uniformity**
```python
for standard in standards_array:
    if standard['task_or_activity'].lower() == utilisation_profile.lower():
        if standard has lighting requirements AND uniformity:
            return standard  # MATCH FOUND
```

**Example:**
- Utilisation Profile: `"Corridors and circulation areas"`
- Standard: `{"task_or_activity": "Corridors and circulation areas", "Uo": 0.4, ...}`
- Result: **MATCH** ✓

#### **Priority 2: Exact Match without Uniformity**
```python
for standard in standards_array:
    if standard['task_or_activity'].lower() == utilisation_profile.lower():
        if standard has lighting requirements:
            return standard  # MATCH FOUND
```

#### **Priority 3: Partial Match**
```python
for standard in standards_array:
    task_activity = standard['task_or_activity'].lower()
    category = standard['category'].lower()
    
    if (utilisation_profile.lower() in task_activity OR
        utilisation_profile.lower() in category OR
        any keyword from profile in task_activity):
        if standard has lighting requirements AND uniformity:
            return standard  # MATCH FOUND
```

**Example:**
- Utilisation Profile: `"Industrial activities and crafts"`
- Standard: `{"task_or_activity": "Industrial activities and crafts - General assembly work", ...}`
- Result: **MATCH** ✓ (partial match)

#### **Priority 4: Keyword-Based Match (Industrial)**
```python
if profile contains ['factory', 'industrial', 'warehouse', 'manufacturing']:
    for standard in standards_array:
        if standard['task_or_activity'] contains ['industrial', 'factory', 'warehouse', 'manufacturing']:
            if standard has lighting requirements:
                return standard  # MATCH FOUND
```

#### **Priority 5: General Work Standards**
```python
for standard in standards_array:
    if standard['task_or_activity'] contains ['general', 'work', 'office']:
        if standard has lighting requirements AND uniformity:
            return standard  # MATCH FOUND
```

#### **Priority 6: Fallback (Any Standard with Uniformity)**
```python
for standard in standards_array:
    if standard has lighting requirements AND uniformity:
        return standard  # MATCH FOUND (first one with uniformity)
```

---

## Complete Example

### Input Report:
```json
{
  "rooms": [
    {
      "name": "building 1 · storey 1 · room 1",
      "utilisation_profile": ""
    }
  ],
  "scenes": [
    {
      "scene_name": "the factory",
      "average_lux": 213.0,
      "uniformity": 0.57
    }
  ],
  "metadata": {
    "project_name": "Al amal factory"
  }
}
```

### Classification Process:

1. **Determine Profile:**
   - Room has no `utilisation_profile`
   - Scene name: "the factory" → contains "factory"
   - **Profile determined:** `"Industrial activities and crafts"`

2. **Match to Standards:**
   - Search `standards_filtered.json` array
   - Look for standard where `task_or_activity` matches or contains "Industrial activities and crafts"
   - **Example match found:**
     ```json
     {
       "ref_no": "6.2.1",
       "category": "Industrial activities and crafts",
       "task_or_activity": "Industrial activities and crafts - General assembly work",
       "Em_r_lx": 300.0,
       "Uo": 0.4,
       "Ra": 40.0
     }
     ```

3. **Compliance Check:**
   - Compare report values against standard:
     - Lux: 213.0 vs Required: 300.0 → **FAIL** (if this was the requirement)
     - Uniformity: 0.57 vs Required: 0.4 → **PASS**
     - Ra: (if found) vs Required: 40.0

---

## Key Fields Used for Matching

### From Standards Array:
- **`task_or_activity`**: Primary matching field (exact or partial match)
- **`category`**: Secondary matching field (partial match)
- **`Em_r_lx`** or **`Em_u_lx`**: Required illuminance (lux)
- **`Uo`**: Required uniformity ratio
- **`Ra`**: Required color rendering index

### From Report:
- **`room.utilisation_profile`**: Direct profile (if available)
- **`scene.scene_name`**: Used to infer profile
- **`scene.utilisation_profile`**: Alternative profile source
- **`room.name`**: Used to infer profile
- **`metadata.project_name`**: Context for generic room names

---

## Standards Array Location

The standards are loaded from:
```
../standard_export/output/standards_filtered.json
```

This file contains **73 standards** (as of current version), all with complete data (no null values).

---

## Matching Priority Summary

1. ✅ **Exact match** (`task_or_activity` == profile) **with uniformity**
2. ✅ **Exact match** (`task_or_activity` == profile) **without uniformity**
3. ✅ **Partial match** (profile substring in `task_or_activity` or `category`) **with uniformity**
4. ✅ **Keyword match** (industrial/factory keywords) **with lighting requirements**
5. ✅ **General match** (general/work/office keywords) **with uniformity**
6. ✅ **Fallback** (any standard with uniformity)

---

## Important Notes

1. **Case Insensitive**: All matching is case-insensitive
2. **Uniformity Priority**: Standards with uniformity requirements are preferred
3. **Lighting Requirements Check**: Only standards with actual lighting values (non-null, non-zero) are considered
4. **First Match Wins**: The algorithm returns the first matching standard found
5. **No Match Handling**: If no standard is found, the room gets status `NO_STANDARD_FOUND`

---

## Debugging Classification

To see which standard was matched for a room, check the compliance result:

```json
{
  "checks": [
    {
      "room": "building 1 · storey 1 · room 1",
      "utilisation_profile": "Industrial activities and crafts",
      "standard": {
        "ref_no": "6.2.1",
        "category": "Industrial activities and crafts",
        "task_or_activity": "Industrial activities and crafts - General assembly work"
      },
      "status": "PASS"
    }
  ]
}
```

The `standard` object shows which standard from the array was matched.

---

## Viewing All Available Standards

To see all standards in the array:

```bash
# Check standards info via API
curl http://localhost:8000/standards-info

# Or view the file directly
cat ../standard_export/output/standards_filtered.json
```

The API returns:
- Total number of standards
- Sample standards (first 5)
- Metadata (if available)


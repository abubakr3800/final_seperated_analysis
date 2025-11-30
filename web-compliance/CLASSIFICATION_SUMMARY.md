# Classification Process - Quick Summary

## How Reports Are Classified

### The Standards Array

The system uses **`standards_filtered.json`** which is an **array of 73 standard objects**.

Each standard object has this structure:
```json
{
  "ref_no": "6.1.1",                    // Standard reference number
  "category": "Traffic zones...",      // Category name
  "task_or_activity": "Corridors...",   // ⭐ PRIMARY MATCHING FIELD
  "Em_r_lx": 100.0,                     // Required illuminance
  "Em_u_lx": 150.0,                     // Upper illuminance
  "Uo": 0.4,                            // Uniformity requirement
  "Ra": 40.0,                           // Color rendering
  ...
}
```

---

## Classification Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. EXTRACT REPORT DATA                                 │
│    - Rooms, Scenes, Metadata                           │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ 2. FOR EACH ROOM: Determine Utilisation Profile        │
│                                                         │
│    Try in order:                                        │
│    a) room.utilisation_profile (if exists)              │
│    b) scene.scene_name → infer from keywords            │
│    c) scene.utilisation_profile (if exists)            │
│    d) room.name → infer from keywords                   │
│    e) project_name → context for generic names         │
│    f) Default: "General areas inside buildings"        │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ 3. SEARCH STANDARDS ARRAY                              │
│                                                         │
│    Search through standards_filtered.json array:        │
│                                                         │
│    Priority 1: Exact match (task_or_activity)          │
│                + Has uniformity                         │
│                                                         │
│    Priority 2: Exact match (task_or_activity)          │
│                + Has lighting requirements             │
│                                                         │
│    Priority 3: Partial match (substring)              │
│                + Has uniformity                        │
│                                                         │
│    Priority 4: Keyword match (industrial/factory)      │
│                + Has lighting requirements              │
│                                                         │
│    Priority 5: General match (general/work/office)    │
│                + Has uniformity                        │
│                                                         │
│    Priority 6: Fallback (any with uniformity)          │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ 4. COMPARE VALUES                                       │
│                                                         │
│    Report Value  vs  Standard Requirement              │
│    ────────────      ────────────────────             │
│    average_lux  vs   Em_r_lx or Em_u_lx               │
│    uniformity   vs   Uo                               │
│    Ra/CRI       vs   Ra                                │
└─────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────┐
│ 5. RESULT                                               │
│                                                         │
│    PASS: All requirements met                           │
│    FAIL: One or more requirements not met               │
│    NO_STANDARD_FOUND: No matching standard             │
└─────────────────────────────────────────────────────────┘
```

---

## Key Matching Field

**`task_or_activity`** is the PRIMARY field used for matching.

The system compares:
- **Utilisation Profile** (from report) 
- **vs**
- **`task_or_activity`** (from each standard in the array)

---

## Example Classification

### Input:
- Room: "building 1 · storey 1 · room 1"
- Scene: "the factory"
- Project: "Al amal factory"

### Process:

1. **Profile Determination:**
   ```
   Scene name: "the factory"
   → Contains "factory" keyword
   → Profile: "Industrial activities and crafts"
   ```

2. **Standards Array Search:**
   ```
   Search through 73 standards...
   Looking for: task_or_activity contains "Industrial activities and crafts"
   
   Found: {
     "ref_no": "6.2.1",
     "task_or_activity": "Industrial activities and crafts - General assembly work",
     "Em_r_lx": 300.0,
     "Uo": 0.4
   }
   ```

3. **Compliance Check:**
   ```
   Report: 213.0 lux, 0.57 uniformity
   Standard: 300.0 lux required, 0.4 uniformity required
   
   Lux: 213.0 < 300.0 → FAIL (if this was the requirement)
   Uniformity: 0.57 >= 0.4 → PASS
   ```

---

## Standards Array Location

```
web-compliance/
  └─ api_server.py
     └─ Loads: ../standard_export/output/standards_filtered.json
                ↑
                This is an ARRAY of 73 standard objects
```

---

## Important Points

1. ✅ The system searches through **ALL standards in the array** until it finds a match
2. ✅ Matching is **case-insensitive**
3. ✅ **`task_or_activity`** is the primary matching field
4. ✅ Standards with **uniformity requirements** are preferred
5. ✅ The **first matching standard** is used (priority order)
6. ✅ If no match found → Status: `NO_STANDARD_FOUND`

---

## Viewing the Classification

The matched standard is shown in the compliance result:

```json
{
  "standard": {
    "ref_no": "6.1.1",                    // Which standard was matched
    "category": "Traffic zones...",       // Category
    "task_or_activity": "Corridors..."   // The matching field
  },
  "utilisation_profile": "..."           // The profile that was matched
}
```

This tells you:
- **Which standard** from the array was selected
- **Why** it was selected (the matching field)
- **What profile** triggered the match


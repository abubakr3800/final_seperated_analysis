# LuxSCale Interface - Concept & Workflow

## 🎯 Concept

LuxSCale uses a **standards-first approach** to lighting design:

1. **User enters room dimensions and type**
2. **System looks up the lighting standard** for that room type
3. **System displays the required parameters** (lux, uniformity, Ra, etc.)
4. **User configures luminaires** to meet those requirements
5. **System generates report** and checks compliance

## 📋 Workflow

### Step 1: Room Information
User provides:
- Project Name
- Company Name (optional)
- **Room Type** (dropdown selection)
- **Room Dimensions**: Length, Width, Height

**Action**: Click "Get Standard Requirements"

**System Response**:
- Looks up matching standard from `standards_filtered.json`
- Displays required parameters:
  - Required Illuminance (Em,r)
  - Upper Illuminance (Em,u)
  - Uniformity (Uo)
  - Color Rendering (Ra)
  - Glare Rating (RUGL)
  - Specific Requirements

### Step 2: Configure Luminaires
Based on the standard requirements shown, user configures:
- Number of Luminaires
- Luminaire Power (W)
- Luminous Flux (lm) OR Efficacy (lm/W)
- Mounting Height
- Work Plane Height (optional)
- Manufacturer (optional)
- Article/Model Number (optional)

**Action**: Click "Generate Report"

**System Response**:
- Generates report with calculated parameters
- Checks compliance against the standard
- Displays results with pass/fail status
- Provides download option

## 🔄 Data Flow

```
User Input (Room Type + Dimensions)
    ↓
GET /get-standard-requirements?room_type=...
    ↓
Standards Lookup
    ↓
Display Required Parameters
    ↓
User Configures Luminaires
    ↓
POST /generate-report
    ↓
Report Generator + Compliance Check
    ↓
Display Results + Download
```

## ✨ Key Features

1. **Standards-Driven**: Requirements come from official lighting standards
2. **Two-Step Process**: Clear separation between requirements and configuration
3. **Visual Requirements**: Standard requirements displayed prominently
4. **Compliance Checking**: Automatic verification against standards
5. **Minimal Input**: Only essential information required

## 📊 Example Flow

### Input:
- Room Type: "Offices"
- Dimensions: 10m × 8m × 3m

### System Shows:
- Required Illuminance: 300 lx
- Uniformity: 0.6
- Color Rendering: 80

### User Configures:
- 12 luminaires
- 50W each
- Efficacy: 100 lm/W
- Mounting: 2.5m

### System Generates:
- Calculated average lux
- Uniformity check
- Compliance status (PASS/FAIL)

## 🎯 Benefits

- **User sees requirements first** - Knows what to aim for
- **Standards-based** - Uses official lighting standards
- **Guided design** - System shows what's needed
- **Compliance built-in** - Automatic verification
- **Simple workflow** - Two clear steps


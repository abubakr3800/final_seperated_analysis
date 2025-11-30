# LuxSCale Interface - Code Documentation

Complete documentation for all code components in the LuxSCale interface.

---

## 📄 index.html

**Purpose**: Dark-themed web interface for user input and report display.

**Key Features**:
- Modern dark theme UI
- Minimal form with essential questions
- Real-time form validation
- Report display with compliance summary
- Download functionality

**Structure**:
- **Header**: Title and description
- **Form Sections**:
  1. Project Information
  2. Room Information
  3. Luminaire Information
  4. Optional Information
- **Results Display**: Shows generated report and compliance status
- **Download Button**: Downloads report as JSON

**JavaScript Functions**:
- `form submission`: Collects form data and sends to API
- `displayResult()`: Displays generated report and compliance results
- `downloadReport()`: Downloads report JSON file

**API Integration**:
- Base URL: `http://localhost:8001`
- Endpoint: `POST /generate-report`
- Download: `GET /download-report/{report_id}`

---

## 📄 api_server.py

**Purpose**: FastAPI server that handles report generation requests.

**Main Components**:

### Class: FastAPI App
- **Port**: 8001
- **CORS**: Enabled for all origins
- **Documentation**: Available at `/docs`

### Endpoints:

#### `GET /`
- **Purpose**: API information and documentation
- **Returns**: API metadata and available endpoints

#### `GET /health`
- **Purpose**: Health check
- **Returns**: Status of components (report_generator, compliance_integration)

#### `POST /generate-report`
- **Purpose**: Generate lighting design report
- **Request Body**: `LightingDesignRequest` model
- **Response**: Complete report with compliance results
- **Process**:
  1. Validates input data
  2. Generates report using `ReportGenerator`
  3. Checks compliance using `ComplianceIntegration`
  4. Saves report to `reports/` folder
  5. Returns complete report with unique ID

#### `GET /download-report/{report_id}`
- **Purpose**: Download generated report
- **Parameters**: `report_id` (UUID string)
- **Returns**: JSON file download

### Request Model: `LightingDesignRequest`
```python
- project_name: str (required)
- company_name: Optional[str]
- room_type: str (required)
- room_length: float > 0 (required)
- room_width: float > 0 (required)
- room_height: float > 0 (required)
- luminaire_count: int > 0 (required)
- luminaire_power: float > 0 (required)
- luminous_flux: Optional[float] >= 0
- efficacy: Optional[float] >= 0
- mounting_height: float > 0 (required)
- work_plane_height: float >= 0 (default: 0.75)
- manufacturer: Optional[str]
- article_no: Optional[str]
```

### Dependencies:
- `ReportGenerator`: Generates report structure
- `ComplianceIntegration`: Checks compliance against standards
- `standards_filtered.json`: Lighting standards data

### Storage:
- Reports saved in `reports/` folder
- Filename format: `{report_id}.json`

---

## 📄 report_generator.py

**Purpose**: Generates lighting design reports with calculated parameters.

### Class: `ReportGenerator`

#### `__init__(standards_path: str)`
- **Purpose**: Initialize report generator
- **Parameters**: Path to standards file
- **Loads**: Standards data for reference

#### `generate_report(input_data: Dict) -> Dict`
- **Purpose**: Generate complete report structure
- **Process**:
  1. Calculates room area
  2. Calculates total power
  3. Determines luminous flux (from input or calculated from efficacy)
  4. Calculates illuminance using simplified formula
  5. Estimates min/max lux and uniformity
  6. Generates room layout (grid pattern)
  7. Builds complete report structure

**Calculations**:
- **Room Area**: `length × width`
- **Total Power**: `luminaire_count × luminaire_power`
- **Luminous Flux**: From input OR `power × efficacy`
- **Average Lux**: `(total_flux × UF × MF) / area`
  - UF (Utilization Factor) = 0.5
  - MF (Maintenance Factor) = 0.8
- **Uniformity**: Estimated as 0.6
- **Min/Max Lux**: Calculated from average and uniformity

#### `_generate_room_layout(...) -> list`
- **Purpose**: Generate grid layout for luminaires
- **Process**:
  1. Calculates grid dimensions (rows × cols)
  2. Calculates spacing between luminaires
  3. Generates coordinate points for each luminaire
- **Returns**: List of {X, Y, Z} coordinate dictionaries

**Report Structure Generated**:
```json
{
  "metadata": {...},
  "lighting_setup": {
    "average_lux": float,
    "min_lux": float,
    "max_lux": float,
    "uniformity": float,
    "power_w": float,
    "power_total_w": float,
    "luminous_flux_lm": float,
    "luminous_flux_total": float,
    "luminous_efficacy_lm_per_w": float,
    "mounting_height_m": float,
    "work_plane_height": float,
    "quantity": int
  },
  "rooms": [{...}],
  "luminaires": [{...}],
  "scenes": [{...}]
}
```

**Note**: Calculations are simplified. For production use, implement proper lighting calculation algorithms (point-by-point, zonal cavity method, etc.)

---

## 📄 compliance_integration.py

**Purpose**: Integrates compliance checking into report generation.

### Class: `ComplianceIntegration`

#### `__init__(standards_path: str, report_api_url: str)`
- **Purpose**: Initialize compliance integration
- **Parameters**:
  - `standards_path`: Path to standards file
  - `report_api_url`: Report API URL (required by ComplianceChecker, not used for generated reports)
- **Creates**: `ComplianceChecker` instance

#### `check_compliance(report_data: Dict) -> Dict`
- **Purpose**: Check generated report against lighting standards
- **Process**:
  1. Uses `ComplianceChecker.check_compliance()` method
  2. Returns compliance results
  3. Handles errors gracefully
- **Returns**: Compliance result dictionary with:
  - `overall_compliance`: PASS/FAIL/ERROR
  - `checks`: List of room compliance checks
  - `summary`: Statistics (total_rooms, passed, failed, pass_rate)
  - `error`: Error message if check failed

**Integration**:
- Imports `ComplianceChecker` from:
  1. `../web-compliance/compliance_checker.py` (preferred)
  2. `../final project/src/compliance_checker.py` (fallback)

**Error Handling**:
- Returns error result if compliance check fails
- Preserves report generation even if compliance check fails

---

## 🔄 Data Flow

```
User Input (Form)
    ↓
index.html (JavaScript)
    ↓
POST /generate-report
    ↓
api_server.py
    ├─→ report_generator.py (Generate report structure)
    └─→ compliance_integration.py (Check compliance)
    ↓
Complete Report (JSON)
    ↓
Save to reports/ folder
    ↓
Return to user
    ↓
Display results + Download option
```

---

## 📊 Report Format

The generated report follows this structure (similar to Dialux):

```json
{
  "generated_at": "ISO timestamp",
  "report_id": "UUID",
  "report_data": {
    "metadata": {...},
    "lighting_setup": {...},
    "rooms": [...],
    "luminaires": [...],
    "scenes": [...]
  },
  "compliance_result": {
    "overall_compliance": "PASS/FAIL",
    "checks": [...],
    "summary": {...}
  },
  "input_parameters": {...}
}
```

---

## 🔧 Configuration

### Paths (in api_server.py):
- **Standards**: `../standard_export/output/standards_filtered.json`
- **Reports Storage**: `reports/` folder (created automatically)
- **Compliance Checker**: From `../web-compliance/` or `../final project/src/`

### Ports:
- **API Server**: 8001
- **Web Interface**: Can be served on any port (3000 suggested)

### Defaults:
- **Work Plane Height**: 0.75m
- **Utilization Factor**: 0.5
- **Maintenance Factor**: 0.8
- **Estimated Uniformity**: 0.6

---

## 🎯 Key Design Decisions

1. **Minimal Questions**: Only essential parameters required
2. **Automatic Calculations**: System calculates derived parameters
3. **Simplified Formulas**: Uses basic lighting calculations (suitable for estimates)
4. **Standards Integration**: Uses existing compliance checker
5. **Dark Theme**: Modern, professional UI
6. **JSON Format**: Easy to parse and integrate

---

## 📝 Notes

- **Simplified Calculations**: For production, replace with professional lighting calculation software
- **Grid Layout**: Simple grid pattern for luminaire placement
- **Standards Matching**: Uses existing compliance checker logic
- **Error Handling**: Graceful degradation if compliance check fails
- **Storage**: Reports stored locally (consider database for production)

---

## 🔍 Future Enhancements

1. **Advanced Calculations**: Implement proper lighting calculation methods
2. **Database Storage**: Store reports in database instead of files
3. **PDF Export**: Generate PDF reports
4. **Visualization**: Add room layout visualization
5. **Multiple Rooms**: Support multiple rooms in one report
6. **Template System**: Pre-defined room templates
7. **Export Formats**: Support multiple export formats (Excel, PDF, etc.)


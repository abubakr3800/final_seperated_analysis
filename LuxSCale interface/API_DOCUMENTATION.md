# LuxSCale API Documentation

Complete API reference for the LuxSCale lighting design report generator.

## Base URL

```
http://localhost:8001
```

## Endpoints

### 1. GET `/` - API Information

Get API documentation and available endpoints.

**Request:**
```bash
curl http://localhost:8001/
```

**Response:**
```json
{
  "message": "LuxSCale API - Lighting Design Report Generator",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "POST /generate-report": "Generate lighting design report",
    "GET /download-report/{report_id}": "Download generated report",
    "GET /health": "Health check"
  },
  "timestamp": "2025-11-30T12:00:00"
}
```

---

### 2. GET `/health` - Health Check

Check API health and component status.

**Request:**
```bash
curl http://localhost:8001/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-30T12:00:00",
  "components": {
    "report_generator": "ready",
    "compliance_integration": "ready"
  }
}
```

---

### 3. POST `/generate-report` - Generate Report

Generate a lighting design report based on user input.

**Request:**
```bash
curl -X POST http://localhost:8001/generate-report \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "Office Building",
    "company_name": "My Company",
    "room_type": "Offices",
    "room_length": 10.0,
    "room_width": 8.0,
    "room_height": 3.0,
    "luminaire_count": 12,
    "luminaire_power": 50.0,
    "efficacy": 100.0,
    "mounting_height": 2.5,
    "work_plane_height": 0.75
  }'
```

**Request Body (LightingDesignRequest):**
```json
{
  "project_name": "string (required)",
  "company_name": "string (optional)",
  "room_type": "string (required)",
  "room_length": "float > 0 (required)",
  "room_width": "float > 0 (required)",
  "room_height": "float > 0 (required)",
  "luminaire_count": "integer > 0 (required)",
  "luminaire_power": "float > 0 (required)",
  "luminous_flux": "float >= 0 (optional, if efficacy not provided)",
  "efficacy": "float >= 0 (optional, if luminous_flux not provided)",
  "mounting_height": "float > 0 (required)",
  "work_plane_height": "float >= 0 (default: 0.75)",
  "manufacturer": "string (optional)",
  "article_no": "string (optional)"
}
```

**Response:**
```json
{
  "generated_at": "2025-11-30T12:00:00",
  "report_id": "550e8400-e29b-41d4-a716-446655440000",
  "report_data": {
    "metadata": {
      "company_name": "My Company",
      "project_name": "Office Building",
      "engineer": "LuxSCale Generator",
      "email": "",
      "report_title": "LuxSCale_Report_Office_Building"
    },
    "lighting_setup": {
      "average_lux": 300.0,
      "min_lux": 180.0,
      "max_lux": 420.0,
      "uniformity": 0.6,
      "power_w": 50.0,
      "power_total_w": 600.0,
      "luminous_flux_lm": 5000.0,
      "luminous_flux_total": 60000.0,
      "luminous_efficacy_lm_per_w": 100.0,
      "mounting_height_m": 2.5,
      "work_plane_height": 0.75,
      "quantity": 12
    },
    "rooms": [
      {
        "name": "Room 1 - Office Building",
        "arrangement": "Grid",
        "utilisation_profile": "Offices",
        "layout": [
          {"X": 2.5, "Y": 2.0, "Z": 2.5},
          ...
        ]
      }
    ],
    "luminaires": [
      {
        "quantity": 12,
        "manufacturer": "Not specified",
        "article_no": "Not specified",
        "power_w": 50.0,
        "luminous_flux_lm": 5000.0,
        "luminous_efficacy_lm_per_w": 100.0
      }
    ],
    "scenes": [
      {
        "scene_name": "Office Building",
        "average_lux": 300.0,
        "min_lux": 180.0,
        "max_lux": 420.0,
        "uniformity": 0.6,
        "utilisation_profile": "Offices"
      }
    ]
  },
  "compliance_result": {
    "overall_compliance": "PASS",
    "checks": [
      {
        "room": "Room 1 - Office Building",
        "utilisation_profile": "Offices",
        "standard": {
          "ref_no": "6.3.1",
          "category": "Offices",
          "task_or_activity": "Offices"
        },
        "checks": {
          "lux": {
            "required": 300.0,
            "actual": 300.0,
            "compliant": true,
            "margin": 0.0
          },
          "uniformity": {
            "required": 0.6,
            "actual": 0.6,
            "compliant": true,
            "margin": 0.0
          }
        },
        "status": "PASS"
      }
    ],
    "summary": {
      "total_rooms": 1,
      "passed": 1,
      "failed": 0,
      "no_standard_found": 0,
      "pass_rate": 100.0
    },
    "timestamp": "2025-11-30T12:00:00"
  },
  "input_parameters": {
    "project_name": "Office Building",
    ...
  }
}
```

**Error Responses:**

**400 Bad Request:**
```json
{
  "detail": "Either luminous_flux or efficacy must be provided"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Failed to generate report: [error message]"
}
```

---

### 4. GET `/download-report/{report_id}` - Download Report

Download a generated report by its unique ID.

**Request:**
```bash
curl http://localhost:8001/download-report/550e8400-e29b-41d4-a716-446655440000 \
  --output report.json
```

**Parameters:**
- `report_id` (path parameter): UUID of the report

**Response:**
- Content-Type: `application/json`
- File download with filename: `luxscale_report_{report_id}.json`

**Error Responses:**

**404 Not Found:**
```json
{
  "detail": "Report not found"
}
```

---

## Using with JavaScript

### Generate Report

```javascript
async function generateReport(formData) {
    const response = await fetch('http://localhost:8001/generate-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to generate report');
    }
    
    return await response.json();
}

// Usage
const report = await generateReport({
    project_name: "Office Building",
    room_type: "Offices",
    room_length: 10.0,
    room_width: 8.0,
    room_height: 3.0,
    luminaire_count: 12,
    luminaire_power: 50.0,
    efficacy: 100.0,
    mounting_height: 2.5
});
```

### Download Report

```javascript
async function downloadReport(reportId) {
    const response = await fetch(`http://localhost:8001/download-report/${reportId}`);
    
    if (!response.ok) {
        throw new Error('Failed to download report');
    }
    
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `luxscale_report_${reportId}.json`;
    a.click();
    window.URL.revokeObjectURL(url);
}
```

---

## Using with Python

```python
import requests

def generate_report(input_data):
    url = "http://localhost:8001/generate-report"
    response = requests.post(url, json=input_data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.json()}")

# Usage
report = generate_report({
    "project_name": "Office Building",
    "room_type": "Offices",
    "room_length": 10.0,
    "room_width": 8.0,
    "room_height": 3.0,
    "luminaire_count": 12,
    "luminaire_power": 50.0,
    "efficacy": 100.0,
    "mounting_height": 2.5
})

print(f"Report ID: {report['report_id']}")
print(f"Compliance: {report['compliance_result']['overall_compliance']}")
```

---

## Room Types

Available room types (utilisation profiles):

- `"Offices"`
- `"Industrial activities and crafts"`
- `"Traffic zones inside buildings"`
- `"General areas inside buildings – Store rooms, cold stores"`
- `"General areas inside buildings"`
- `"Health care premises - Operating areas"`
- `"Educational buildings"`
- `"Retail"`

These match the `task_or_activity` field in the standards file.

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

These interfaces allow you to:
- Test endpoints directly
- View request/response schemas
- See example requests
- Try the API without writing code

---

## Best Practices

1. **Validate Input**: Check all required fields before sending
2. **Handle Errors**: Always check response status codes
3. **Store Report ID**: Save the report_id for later download
4. **Check Compliance**: Review compliance_result before using report
5. **Use Appropriate Room Type**: Select correct room type for accurate standards matching

---

## Notes

- Reports are stored in the `reports/` folder
- Each report has a unique UUID
- Reports include both generated data and compliance results
- The system uses simplified calculations (suitable for estimates)
- For production use, integrate with professional lighting calculation software


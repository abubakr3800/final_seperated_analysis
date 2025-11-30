# API Usage Guide - Web Compliance

Complete guide to using the Compliance API endpoints.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. GET `/` - API Information

Get API documentation and available endpoints.

**Request:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "Lighting Compliance Checker API",
  "version": "2.0.0",
  "status": "running",
  "endpoints": { ... },
  "timestamp": "2025-11-30T12:00:00"
}
```

---

### 2. GET `/health` - Health Check

Check API health and component status.

**Request:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-30T12:00:00",
  "components": {
    "compliance_checker": "ready",
    "standards_loaded": true,
    "report_api_available": "unknown"
  }
}
```

---

### 3. GET `/standards-info` - Standards Information

Get information about loaded lighting standards.

**Request:**
```bash
curl http://localhost:8000/standards-info
```

**Response:**
```json
{
  "total_standards": 73,
  "metadata": {},
  "sample_standards": [ ... ],
  "timestamp": "2025-11-30T12:00:00"
}
```

---

### 4. POST `/check-compliance` - Basic Compliance Check

Upload a PDF and get basic compliance results.

**Request:**
```bash
curl -X POST \
  http://localhost:8000/check-compliance \
  -F "file=@report.pdf"
```

**Response:**
```json
{
  "report_data": { ... },
  "compliance_result": {
    "overall_compliance": "PASS",
    "checks": [ ... ],
    "summary": { ... }
  },
  "file_info": {
    "filename": "report.pdf",
    "size": 123456,
    "upload_time": "2025-11-30T12:00:00"
  },
  "timestamp": "2025-11-30T12:00:00"
}
```

---

### 5. POST `/check-compliance-detailed` - Detailed Compliance Check

**Recommended endpoint** - Upload a PDF and get detailed results with all extracted parameters.

**Request:**
```bash
curl -X POST \
  http://localhost:8000/check-compliance-detailed \
  -F "file=@report.pdf"
```

**Response:**
```json
{
  "file_info": {
    "filename": "report.pdf",
    "size": 123456,
    "upload_time": "2025-11-30T12:00:00"
  },
  "extracted_report_data": {
    "metadata": { ... },
    "lighting_setup": { ... },
    "rooms": [ ... ],
    "luminaires": [ ... ],
    "scenes": [ ... ]
  },
  "compliance_result": {
    "overall_compliance": "PASS",
    "checks": [
      {
        "room": "Room 1",
        "utilisation_profile": "...",
        "standard": {
          "ref_no": "6.1.1",
          "category": "...",
          "task_or_activity": "..."
        },
        "checks": {
          "lux": {
            "required": 100.0,
            "actual": 213.0,
            "compliant": true,
            "margin": 113.0
          },
          "uniformity": {
            "required": 0.4,
            "actual": 0.57,
            "compliant": true,
            "margin": 0.17
          },
          "ra": { ... }
        },
        "status": "PASS"
      }
    ],
    "summary": {
      "total_rooms": 4,
      "passed": 4,
      "failed": 0,
      "no_standard_found": 0,
      "pass_rate": 100.0
    },
    "timestamp": "2025-11-30T12:00:00"
  },
  "timestamp": "2025-11-30T12:00:00"
}
```

---

### 6. GET `/test-connection` - Test Report API Connection

Test connection to the Report API.

**Request:**
```bash
curl http://localhost:8000/test-connection
```

**Response:**
```json
{
  "status": "connected",
  "report_api_status": { ... },
  "timestamp": "2025-11-30T12:00:00"
}
```

---

### 7. GET `/proxy/report-health` - Proxy Report API Health

CORS-friendly proxy to check Report API health.

**Request:**
```bash
curl http://localhost:8000/proxy/report-health
```

**Response:**
```json
{
  "status": "healthy",
  "report_api": { ... },
  "timestamp": "2025-11-30T12:00:00"
}
```

---

## Using with JavaScript/Fetch

### Upload and Check Compliance

```javascript
async function checkCompliance(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('http://localhost:8000/check-compliance-detailed', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to process file');
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Usage
const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener('change', async (e) => {
    if (e.target.files.length > 0) {
        const result = await checkCompliance(e.target.files[0]);
        console.log('Compliance Result:', result);
    }
});
```

---

## Using with Python Requests

```python
import requests

def check_compliance(pdf_path):
    url = "http://localhost:8000/check-compliance-detailed"
    
    with open(pdf_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.json()}")

# Usage
result = check_compliance('report.pdf')
print(f"Overall Compliance: {result['compliance_result']['overall_compliance']}")
```

---

## Response Structure

### Compliance Result Structure

```json
{
  "overall_compliance": "PASS" | "FAIL" | "PARTIAL" | "UNKNOWN" | "ERROR",
  "checks": [
    {
      "room": "Room name",
      "utilisation_profile": "Profile name",
      "standard": {
        "ref_no": "Standard reference",
        "category": "Category",
        "task_or_activity": "Activity"
      },
      "checks": {
        "lux": {
          "required": 100.0,
          "actual": 213.0,
          "compliant": true,
          "margin": 113.0
        },
        "uniformity": { ... },
        "ra": { ... }
      },
      "status": "PASS" | "FAIL"
    }
  ],
  "summary": {
    "total_rooms": 4,
    "passed": 4,
    "failed": 0,
    "no_standard_found": 0,
    "pass_rate": 100.0
  },
  "timestamp": "ISO timestamp"
}
```

### Extracted Report Data Structure

```json
{
  "metadata": {
    "company_name": "...",
    "project_name": "...",
    "engineer": "...",
    "email": "..."
  },
  "lighting_setup": {
    "average_lux": 213.0,
    "uniformity": 0.57,
    "min_lux": 121.0,
    "max_lux": 266.0,
    ...
  },
  "rooms": [ ... ],
  "luminaires": [ ... ],
  "scenes": [ ... ]
}
```

---

## Error Handling

### Common Error Responses

**400 Bad Request:**
```json
{
  "detail": "Only PDF files are allowed"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Processing failed: [error message]"
}
```

**503 Service Unavailable:**
```json
{
  "detail": "Compliance checker not initialized"
}
```

---

## Best Practices

1. **Use `/check-compliance-detailed`** for complete information
2. **Check `/health`** before processing files
3. **Handle errors gracefully** - check response status codes
4. **Validate file type** before uploading (PDF only)
5. **Monitor file size** - large files may take longer
6. **Use async/await** for better error handling

---

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to:
- Test endpoints directly
- View request/response schemas
- See example requests

---

## Rate Limiting

Currently, there is no rate limiting implemented. For production use, consider:
- Implementing request throttling
- Adding authentication
- Setting up rate limits per IP/user

---

## CORS

CORS is enabled for all origins. For production:
- Restrict allowed origins
- Configure credentials properly
- Set appropriate headers


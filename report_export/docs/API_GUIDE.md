# PDF Report Extraction API Guide

## 🚀 **Simple API Interface**

A Flask-based API that accepts PDF file uploads and returns extracted JSON data. This is completely separate from the existing command-line tools and doesn't interfere with current functionality.

### 📁 **API Files Created:**

1. **`api_server.py`** - Main Flask API server
2. **`api_client.py`** - Python client for testing
3. **`api_interface.html`** - Web interface for easy testing

### 🎯 **API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API documentation and usage |
| GET | `/health` | Health check |
| POST | `/extract` | Upload PDF and extract data |
| GET | `/files` | List all processed files |
| GET | `/download/<file_id>` | Download extracted JSON file |

### 🚀 **Quick Start:**

#### **1. Start the API Server:**
```bash
py api/api_server.py
# or
api/start_api.bat
```
Server will start on `http://localhost:5000`

#### **2. Test with Web Interface:**
Open `http://localhost:5000` in your browser and use the HTML interface

#### **3. Test with Python Client:**
```bash
py api/api_client.py
```

### 📊 **API Usage Examples:**

#### **Upload PDF and Extract Data:**
```bash
curl -X POST -F "file=@report.pdf" http://localhost:5000/extract
```

#### **Check API Health:**
```bash
curl http://localhost:5000/health
```

#### **List Processed Files:**
```bash
curl http://localhost:5000/files
```

#### **Download Extracted Data:**
```bash
curl http://localhost:5000/download/file_id -o extracted_data.json
```

### 🐍 **Python Client Usage:**

```python
from api_client import PDFExtractionClient

# Initialize client
client = PDFExtractionClient("http://localhost:5000")

# Check health
health = client.health_check()
print(health)

# Extract PDF
result = client.extract_pdf("report.pdf")
print(result)

# List files
files = client.list_files()
print(files)

# Download file
download_result = client.download_file("file_id", "output.json")
print(download_result)
```

### 📋 **API Response Format:**

#### **Successful Extraction:**
```json
{
  "success": true,
  "message": "PDF processed successfully",
  "file_id": "report_20241201_143022_a1b2c3d4",
  "original_filename": "report.pdf",
  "extracted_data": {
    "metadata": {
      "company_name": "Short Cicuit Company",
      "project_name": "Lighting study...",
      "engineer": "Eng.Mostafa Emad",
      "email": "mostafaattalla122@gmail.com"
    },
    "lighting_setup": { ... },
    "luminaires": [ ... ],
    "rooms": [ ... ],
    "scenes": [ ... ]
  },
  "download_url": "/download/report_20241201_143022_a1b2c3d4",
  "timestamp": "2024-12-01T14:30:22.123456"
}
```

#### **Error Response:**
```json
{
  "error": "Processing failed",
  "message": "Error details here",
  "timestamp": "2024-12-01T14:30:22.123456"
}
```

### 🔧 **Configuration:**

- **Max file size:** 50MB
- **Allowed formats:** PDF only
- **Upload folder:** `api_uploads/` (auto-created)
- **Output folder:** `api_outputs/` (auto-created)
- **Port:** 5000 (configurable)

### 🛡️ **Security Features:**

- File type validation
- Secure filename handling
- File size limits
- Automatic cleanup of uploaded files
- Unique filename generation

### 📁 **File Management:**

- Uploaded files are automatically deleted after processing
- Extracted JSON files are saved with unique IDs
- Files can be downloaded using the file ID
- Batch summary available via `/files` endpoint

### 🎯 **Integration Examples:**

#### **JavaScript/Frontend:**
```javascript
const formData = new FormData();
formData.append('file', pdfFile);

fetch('/extract', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Extracted data:', data.extracted_data);
        // Use the extracted data
    }
});
```

#### **Python Script:**
```python
import requests

with open('report.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/extract', files=files)
    data = response.json()
    
    if data['success']:
        print("Company:", data['extracted_data']['metadata']['company_name'])
```

#### **Using the API Client:**
```python
from api.api_client import PDFExtractionClient

client = PDFExtractionClient("http://localhost:5000")
result = client.extract_pdf("report.pdf")
print(result)
```

### 🎉 **Features:**

✅ **Simple REST API** - Easy to integrate  
✅ **File Upload Support** - Direct PDF upload  
✅ **JSON Response** - Structured data output  
✅ **File Management** - Download and list files  
✅ **Error Handling** - Comprehensive error responses  
✅ **Web Interface** - HTML interface for testing  
✅ **Python Client** - Ready-to-use client library  
✅ **Separate from CLI** - Doesn't interfere with existing tools  

### 🚀 **Ready to Use:**

The API is now ready for integration with any application that needs PDF report extraction functionality! 🎉

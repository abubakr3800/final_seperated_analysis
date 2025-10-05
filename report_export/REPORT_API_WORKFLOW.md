# Report API Workflow in Web Application

## 📋 Overview

The Report API is an advanced Flask-based service that handles PDF file uploads and data extraction using the comprehensive Final PDF Extractor with alias mapping. It works as part of a larger system where the web interface communicates with both the Report API (port 5000) and the Compliance API (port 8000).

**Key Features:**
- Uses Final PDF Extractor with alias-based parameter mapping
- Enhanced room layout extraction with 3D coordinates
- Comprehensive metadata, lighting setup, luminaire, and scene extraction
- Robust error handling and fallback mechanisms
- Automatic cleanup of temporary files

## 🏗️ System Architecture

```
Web Interface (Port 3000)
    ↓
Compliance API (Port 8000)
    ↓
Report API (Port 5000)
    ↓
Final PDF Extractor with Alias Mapping
    ↓
Extracted JSON Data
```

## 🔄 Complete Workflow

### 1. **User Uploads PDF**
- User selects PDF file in web interface
- File is validated (PDF format, size limits)
- Upload button triggers `uploadFile()` function

### 2. **Web Interface Processing**
```javascript
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Send directly to Compliance API
    const response = await fetch(`${API_BASE}/check-compliance-detailed`, {
        method: 'POST',
        body: formData
    });
}
```

### 3. **Compliance API Receives Request**
- Compliance API (port 8000) receives the PDF file
- Internally calls Report API (port 5000) for extraction
- Processes extracted data for compliance checking

### 4. **Report API Processing**
```python
@app.route('/extract', methods=['POST'])
def extract_pdf():
    # 1. Validate uploaded file
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    # 2. Check file type and size
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    # 3. Generate unique filename
    unique_filename = generate_unique_filename(original_filename)
    
    # 4. Save uploaded file temporarily
    upload_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(upload_path)
    
    # 5. Extract data using Final PDF Extractor
    if extractor:
        result = extractor.process_report(upload_path)
    else:
        # Fallback to enhanced parser
        result = process_report(upload_path)
    
    # 6. Save extracted data to JSON
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    # 7. Clean up uploaded file
    os.remove(upload_path)
    
    # 8. Return extracted data
    return jsonify({
        "success": True,
        "extracted_data": result,
        "file_id": file_id
    })
```

## 📁 File Structure

### **Report API Directories**
```
report_export/api/
├── api_server.py          # Main Flask API server
├── api_uploads/           # Temporary PDF storage (cleaned after processing)
├── api_outputs/           # Extracted JSON files (persistent)
└── api_interface.html     # Web interface for testing
```

### **File Naming Convention**
- **Uploaded files**: `{original_name}_{timestamp}_{uuid}.pdf`
- **Extracted files**: `{original_name}_{timestamp}_{uuid}_extracted.json`

## 🔧 API Endpoints

### **1. Health Check**
```http
GET /health
```
**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2024-01-01T12:00:00",
    "extractor": "ready"
}
```

### **2. Extract PDF Data**
```http
POST /extract
Content-Type: multipart/form-data
```
**Request Body:**
- `file`: PDF file (max 50MB)

**Response:**
```json
{
    "success": true,
    "message": "PDF processed successfully",
    "file_id": "report_20240101_120000_abc12345",
    "original_filename": "report.pdf",
    "extracted_data": {
        "metadata": {...},
        "lighting_setup": {...},
        "luminaires": [...],
        "rooms": [...],
        "scenes": [...]
    },
    "download_url": "/download/report_20240101_120000_abc12345",
    "timestamp": "2024-01-01T12:00:00"
}
```

### **3. List Processed Files**
```http
GET /files
```
**Response:**
```json
{
    "success": true,
    "files": [
        {
            "file_id": "report_20240101_120000_abc12345",
            "filename": "report_20240101_120000_abc12345_extracted.json",
            "size": 1024,
            "created": "2024-01-01T12:00:00",
            "download_url": "/download/report_20240101_120000_abc12345"
        }
    ],
    "count": 1
}
```

### **4. Download Extracted Data**
```http
GET /download/{file_id}
```
**Response:**
- Downloads the JSON file directly

## 🛠️ Processing Pipeline

### **1. File Validation**
```python
def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### **2. Unique Filename Generation**
```python
def generate_unique_filename(original_filename):
    """Generate unique filename to avoid conflicts"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    name, ext = os.path.splitext(original_filename)
    return f"{name}_{timestamp}_{unique_id}{ext}"
```

### **3. Final PDF Extractor Integration**
```python
# Import the Final PDF Extractor
from extractors.final_extractor import FinalPDFExtractor

# Initialize extractor with alias mapping
extractor = FinalPDFExtractor("aliases.json")

# Process the PDF
result = extractor.process_report(upload_path)
```

### **4. Data Structure**
The extracted data follows this structure:
```json
{
    "metadata": {
        "company_name": "Company Name",
        "project_name": "Project Name",
        "engineer": "Eng. Name",
        "email": "email@domain.com",
        "report_title": "report.pdf"
    },
    "lighting_setup": {
        "number_of_fixtures": 36,
        "fixture_type": "HighBay 150 watt",
        "mounting_height_m": 11.5,
        "average_lux": 673.0,
        "uniformity": 0.41,
        "total_power_w": 5400.0,
        "luminous_efficacy_lm_per_w": 145.0
    },
    "luminaires": [
        {
            "quantity": 36,
            "manufacturer": "Philips",
            "article_no": "BY698P LED265CW G2 WB",
            "power_w": 150.0,
            "luminous_flux_lm": 21750.0,
            "efficacy_lm_per_w": 145.0
        }
    ],
    "rooms": [
        {
            "name": "Building 1 · Storey 1 · Room 1",
            "arrangement": "X",
            "layout": [
                {
                    "x_m": 7.0,
                    "y_m": 4.0,
                    "z_m": 36.002
                }
            ]
        }
    ],
    "scenes": [
        {
            "scene_name": "the factory",
            "average_lux": 673.0,
            "min_lux": 277.0,
            "max_lux": 949.0,
            "uniformity": 0.41,
            "utilisation_profile": "Health care premises - Operating areas"
        }
    ]
}
```

## 🔒 Security Features

### **1. File Validation**
- Only PDF files allowed
- Maximum file size: 50MB
- Secure filename handling

### **2. CORS Support**
```python
from flask_cors import CORS
CORS(app)  # Enable CORS for all routes
```

### **3. Error Handling**
- Comprehensive error responses
- File cleanup on errors
- Graceful failure handling

## 📊 Performance Features

### **1. Temporary File Management**
- Uploaded files are deleted after processing
- Only extracted JSON files are kept
- Unique filenames prevent conflicts

### **2. Memory Efficiency**
- Files are processed one at a time
- No file caching in memory
- Stream processing for large files

### **3. Concurrent Processing**
- Flask handles multiple requests
- Each request is independent
- No shared state between requests

## 🚀 Usage Examples

### **1. Direct API Usage**
```bash
# Upload PDF file
curl -X POST -F "file=@report.pdf" http://localhost:5000/extract

# Check health
curl http://localhost:5000/health

# List files
curl http://localhost:5000/files

# Download extracted data
curl http://localhost:5000/download/report_20240101_120000_abc12345
```

### **2. Web Interface Integration**
```javascript
// The web interface uses the Compliance API which internally calls Report API
const response = await fetch('http://localhost:8000/check-compliance-detailed', {
    method: 'POST',
    body: formData
});
```

### **3. Python Client Usage**
```python
import requests

# Upload and extract
with open('report.pdf', 'rb') as f:
    response = requests.post('http://localhost:5000/extract', 
                           files={'file': f})
    data = response.json()
    print(data['extracted_data'])
```

## 🔧 Configuration

### **Environment Variables**
```python
# Flask configuration
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

# Directory configuration
UPLOAD_FOLDER = 'api_uploads'
OUTPUT_FOLDER = 'api_outputs'
ALLOWED_EXTENSIONS = {'pdf'}
```

### **Server Startup**
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📝 Error Handling

### **Common Error Responses**
```json
{
    "error": "No file provided",
    "message": "Please upload a PDF file using the 'file' field"
}

{
    "error": "Invalid file type",
    "message": "Only PDF files are allowed"
}

{
    "error": "File too large",
    "message": "File size exceeds 50MB limit"
}

{
    "error": "Processing failed",
    "message": "Detailed error message"
}
```

## 🎯 Key Benefits

1. **Separation of Concerns**: Report extraction is separate from compliance checking
2. **Reusability**: Report API can be used by other applications
3. **Scalability**: Can handle multiple concurrent requests
4. **Reliability**: Comprehensive error handling and file cleanup
5. **Flexibility**: Supports both direct API usage and web interface integration

---

**The Report API serves as the core PDF processing engine, providing reliable and efficient extraction of lighting report data for the entire web application system.**

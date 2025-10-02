# Quick Start Guide

## 🚀 **Get Started in 3 Steps**

### **Step 1: Installation**
```bash
# Install dependencies
py -m pip install -r requirements.txt

# Or use the installation script
core/install_and_run.bat
```

### **Step 2: Choose Your Method**

#### **Option A: Command Line (Recommended for single files)**
```bash
# Extract data from a PDF file
py extractors/layout_enhanced_extractor.py "your_report.pdf"
```

#### **Option B: Batch Processing (For multiple files)**
```bash
# Process all PDFs in a folder
py batch_processing/process_folder.py input_folder output_folder
```

#### **Option C: API Server (For web integration)**
```bash
# Start API server
py api/api_server.py

# Open browser to http://localhost:5000
```

### **Step 3: View Results**
- **Command line**: JSON file created in same directory
- **Batch processing**: Files saved to output folder
- **API**: JSON response or download link

## 🎯 **Common Use Cases**

### **Single PDF File**
```bash
py extractors/layout_enhanced_extractor.py "report.pdf"
```
**Output**: `report_extracted.json`

### **Multiple PDF Files**
```bash
py batch_processing/process_folder.py "C:\reports" "C:\extracted"
```
**Output**: All files in `C:\extracted\` folder

### **Web Integration**
```bash
# Start server
py api/api_server.py

# Upload via browser
# http://localhost:5000
```

### **Python Integration**
```python
from api.api_client import PDFExtractionClient

client = PDFExtractionClient("http://localhost:5000")
result = client.extract_pdf("report.pdf")
print(result['extracted_data'])
```

## 📊 **What You'll Get**

Each extraction produces structured JSON data:

```json
{
  "metadata": {
    "company_name": "Short Cicuit Company",
    "project_name": "Lighting study for nesstra factory",
    "engineer": "Eng.Mostafa Emad",
    "email": "mostafaattalla122@gmail.com"
  },
  "lighting_setup": {
    "number_of_fixtures": 36,
    "fixture_type": "HighBay 150 watt",
    "average_lux": 673,
    "uniformity": 0.41
  },
  "luminaires": [...],
  "rooms": [...],
  "scenes": [...]
}
```

## 🔧 **Troubleshooting**

### **Python not found**
```bash
# Install Python from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH"
```

### **Dependencies missing**
```bash
py -m pip install -r requirements_minimal.txt
```

### **PDF not processing**
- Check if PDF is not password protected
- Ensure PDF contains text (not just images)
- Try different extractor: `py extractors/final_extractor.py`

### **API not starting**
```bash
# Install Flask
py -m pip install Flask requests

# Start server
py api/api_server.py
```

## 📚 **Next Steps**

- **Read full documentation**: `docs/README.md`
- **Try examples**: `examples/example_usage.py`
- **Run tests**: `tests/test_layout.py`
- **Explore API**: `docs/API_GUIDE.md`

## 🎉 **You're Ready!**

The system is now ready to extract data from your PDF reports. Choose the method that best fits your workflow! 🚀

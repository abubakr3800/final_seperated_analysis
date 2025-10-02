# PDF Report Extractor

A comprehensive Python system for extracting structured data from PDF lighting analysis reports. Supports both command-line and API interfaces with advanced room layout extraction capabilities.

## 🚀 **Quick Start**

### **Installation:**
```bash
py -m pip install -r requirements.txt
```

### **Basic Usage:**
```bash
# Single file extraction
py extractors/layout_enhanced_extractor.py "report.pdf"

# Batch processing
py batch_processing/process_folder.py input_folder output_folder

# API server
py api/api_server.py
```

## 📁 **Project Structure**

```
├── core/                    # Core installation scripts
├── extractors/              # PDF extraction engines
├── api/                     # Web API interface
├── batch_processing/        # Batch processing tools
├── docs/                    # Documentation
├── examples/                # Usage examples
├── tests/                   # Test scripts
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## 🎯 **Features**

✅ **Hybrid PDF Processing** - Text-based + OCR fallback  
✅ **Advanced Layout Extraction** - X/Y/Z coordinates & arrangements  
✅ **Multiple Extraction Engines** - 4 different extractors  
✅ **Batch Processing** - Process entire folders  
✅ **REST API** - Web interface for integration  
✅ **Command Line Tools** - Direct file processing  
✅ **Comprehensive Testing** - Full test suite  

## 📊 **Extraction Capabilities**

- **Metadata**: Company, project, engineer, email
- **Lighting Setup**: Fixtures, power, lux levels, uniformity
- **Luminaires**: Manufacturer, specifications, quantities
- **Room Layouts**: Spatial coordinates, arrangements
- **Scenes**: Performance metrics, utilization profiles

## 🛠 **Usage Options**

### **1. Command Line (Recommended)**
```bash
# Layout Enhanced Extractor (best results)
py extractors/layout_enhanced_extractor.py "report.pdf"

# Final Extractor (comprehensive)
py extractors/final_extractor.py "report.pdf"

# Enhanced Parser (fast)
py extractors/enhanced_parser.py "report.pdf"

# Original Extractor (basic)
py extractors/pdf_report_extractor.py "report.pdf"
```

### **2. Batch Processing**
```bash
# Process all PDFs in a folder
py batch_processing/process_folder.py input_folder output_folder

# Windows batch file
batch_processing/process_folder.bat input_folder output_folder
```

### **3. API Server**
```bash
# Start API server
py api/api_server.py

# Access web interface
# http://localhost:5000
```

### **4. Examples & Testing**
```bash
# Run examples
py examples/example_usage.py

# Run tests
py tests/test_layout.py
```

## 📋 **Output Format**

All extractors produce structured JSON data:

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

## 🔧 **Requirements**

- Python 3.6+
- pdfplumber, PyMuPDF
- pdf2image, pytesseract (for OCR)
- Flask, requests (for API)

## 📚 **Documentation**

- [Quick Start Guide](docs/QUICK_START.md) - Get started in 3 steps
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Directory organization
- [API Guide](docs/API_GUIDE.md) - Web API documentation
- [Folder Processing Guide](docs/FOLDER_PROCESSING_GUIDE.md) - Batch processing
- [Layout Enhancement Summary](docs/LAYOUT_ENHANCEMENT_SUMMARY.md) - Advanced features

## 🎉 **Ready to Use**

The system is production-ready with comprehensive error handling, logging, and multiple interface options. Choose the approach that best fits your needs!

---

**📁 All files are organized in logical directories for easy navigation and maintenance.**
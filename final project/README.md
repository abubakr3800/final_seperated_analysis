# Lighting Compliance Checker - Final Project

A comprehensive web-based system for checking lighting compliance against standards by extracting data from PDF reports.

## 🏗️ Project Structure

```
final project/
├── 📂 src/                    # Core application code
│   ├── api_server.py         # FastAPI compliance checker server
│   ├── compliance_checker.py # Core compliance logic
│   ├── parameter_mapping.json # Parameter aliases mapping
│   └── pdf_extractor.py      # PDF extraction utilities
├── 📂 scripts/               # Utility scripts
│   ├── process_reports_enhanced.py # Enhanced batch processing
│   ├── process_reports.bat   # Batch processing script
│   ├── demo.py              # Demo script
│   └── minimal_api.py       # Minimal API for testing
├── 📂 tests/                 # Test files
│   ├── test_*.py            # Various test scripts
│   ├── debug_*.py           # Debug utilities
│   └── simple_*.py          # Simple test scripts
├── 📂 docs/                  # Documentation
│   └── README.md            # This file
├── 📂 temp/                  # Temporary files
│   ├── debug_*.json         # Debug output files
│   └── *_test_result.json   # Test result files
├── 📂 data/                  # Data files
├── 📄 web_interface.html     # Web interface (main UI)
├── 📄 web_server.py         # Web server for the interface
├── 📄 requirements.txt      # Python dependencies
└── 📄 *.bat                 # Service management scripts
```

## 🚀 Quick Start

### 1. Start All Services
```bash
restart_services.bat
```

### 2. Access the System
- **Web Interface**: http://localhost:3000 (or 3001)
- **API Documentation**: http://localhost:8000/docs
- **Report API**: http://localhost:5000

### 3. Upload PDF Report
1. Open the web interface
2. Upload a PDF lighting report
3. View compliance results

## 🔧 Individual Services

### Start Services Individually
```bash
# Report API (PDF extraction)
start_report_api.bat

# Compliance API (standards checking)
start_api.bat

# Web Interface
start_web_interface.bat
```

## 📊 Features

- **PDF Report Extraction**: Extracts lighting data from PDF reports
- **Standards Compliance**: Compares against lighting standards
- **Web Interface**: User-friendly web interface
- **Room Analysis**: Detailed room-by-room compliance checking
- **Visual Reports**: Room diagrams and comparison tables

## 🛠️ Development

### Running Tests
```bash
cd tests
py test_direct_compliance.py
```

### Batch Processing
```bash
cd scripts
py process_reports_enhanced.py
```

### Debugging
```bash
cd tests
py debug_uniformity_issue.py
```

## 📋 API Endpoints

### Compliance API (Port 8000)
- `GET /health` - Health check
- `GET /standards-info` - Standards information
- `POST /check-compliance-detailed` - Detailed compliance check

### Report API (Port 5000)
- `GET /health` - Health check
- `POST /extract` - Extract data from PDF
- `GET /files` - List processed files

## 🔍 Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure ports 3000, 5000, 8000 are available
2. **Python not found**: Install Python and ensure it's in PATH
3. **Dependencies**: Run `py -m pip install -r requirements.txt`

### Debug Mode
- Check console output in service windows
- Review debug files in `temp/` directory
- Use test scripts in `tests/` directory

## 📝 Notes

- Uses `py` command instead of `python`
- Enhanced parser for better uniformity extraction
- Realistic lighting standards (enhanced_standards.json)
- CORS enabled for cross-origin requests
- Automatic service management with batch scripts

## 🎯 Key Components

1. **Report Extraction**: Uses enhanced_parser.py for PDF processing
2. **Standards Matching**: Intelligent matching based on room types
3. **Compliance Checking**: Comprehensive LUX, Uniformity, Ra/CRI checks
4. **Web Interface**: Modern, responsive UI with detailed results
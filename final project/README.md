# 🏗️ Lighting Compliance Checker - Final Project

A comprehensive web-based system for checking lighting compliance against standards by extracting data from PDF reports.

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🏗️ Project Structure](#️-project-structure)
- [🔧 Service Management](#-service-management)
- [📊 Features](#-features)
- [🛠️ Development](#️-development)
- [📋 API Endpoints](#-api-endpoints)
- [🔍 Troubleshooting](#-troubleshooting)
- [📚 Additional Resources](#-additional-resources)

---

## 🚀 Quick Start

### 1. One-Command Setup
```bash
start_all_services.bat
```

### 2. Access the System
- **🌐 Web Interface**: http://localhost:3000
- **📖 API Documentation**: http://localhost:8000/docs
- **🔧 Report API**: http://localhost:5000

### 3. Upload and Analyze
1. Open http://localhost:3000
2. Upload a PDF lighting report
3. View compliance results and analysis

---

## 🏗️ Project Structure

```
final project/
├── 📂 src/                           # Core application code
│   ├── api_server.py                # FastAPI compliance server
│   ├── compliance_checker.py        # Core compliance logic
│   ├── parameter_mapping.json       # Parameter aliases mapping
│   └── pdf_extractor.py             # PDF extraction utilities
│
├── 📂 scripts/                       # Utility scripts
│   ├── process_reports_enhanced.py  # Enhanced batch processing
│   ├── process_reports.bat          # Batch processing script
│   ├── demo.py                      # Demo script
│   └── minimal_api.py               # Minimal API for testing
│
├── 📂 tests/                         # Test files
│   ├── test_direct_compliance.py    # Direct compliance testing
│   ├── test_uniformity_extraction.py # Uniformity testing
│   ├── debug_uniformity_issue.py    # Debug utilities
│   ├── simple_debug_test.py         # Simple debugging
│   └── [other test files...]        # Various test scripts
│
├── 📂 docs/                          # Documentation
│   └── README.md                    # Main documentation
│
├── 📂 temp/                          # Temporary files
│   ├── debug_*.json                 # Debug output files
│   └── *_test_result.json           # Test result files
│
├── 📂 data/                          # Data files
│
├── 📄 web_interface.html             # Web interface (main UI)
├── 📄 web_server.py                  # Web server for the interface
├── 📄 requirements.txt               # Python dependencies
│
├── 🚀 Service Management Scripts:
│   ├── start_all_services.bat       # Master startup script
│   ├── restart_services.bat         # Restart all services
│   ├── start_api.bat                # Start compliance API only
│   ├── start_report_api.bat         # Start report API only
│   └── start_web_interface.bat      # Start web interface only
│
└── 🛠️ Utility Scripts:
    ├── organize_project.bat         # Organize project structure
    └── cleanup_project.bat          # Clean temporary files
```

---

## 🔧 Service Management

### Master Scripts
| Script | Purpose | Description |
|--------|---------|-------------|
| `start_all_services.bat` | **Master startup** | Starts all services with organized info |
| `restart_services.bat` | **Restart all** | Restarts all services |
| `cleanup_project.bat` | **Cleanup** | Cleans temporary files and cache |

### Individual Services
| Script | Service | Port | Description |
|--------|---------|------|-------------|
| `start_api.bat` | Compliance API | 8000 | Standards checking |
| `start_report_api.bat` | Report API | 5000 | PDF extraction |
| `start_web_interface.bat` | Web Interface | 3000 | User interface |

### Usage Examples
```bash
# Start everything
start_all_services.bat

# Start individual services
start_api.bat
start_report_api.bat
start_web_interface.bat

# Restart all services
restart_services.bat

# Clean up project
cleanup_project.bat
```

---

## 📊 Features

### 🔍 PDF Report Extraction
- **Advanced OCR**: Tesseract-based text recognition
- **Layout Analysis**: Room dimensions and layouts
- **Luminaire Detection**: Fixture specifications
- **Parameter Extraction**: LUX, Uniformity, Ra/CRI values
- **Scene Analysis**: Multiple lighting scenarios

### 📏 Standards Compliance
- **EN 12464-1**: European lighting standards
- **Room Type Matching**: Automatic classification
- **Parameter Comparison**: LUX, Uniformity, Ra/CRI checking
- **Pass/Fail Analysis**: Detailed compliance results
- **Margin Calculations**: Performance vs requirements

### 🎨 Web Interface
- **Modern UI**: Responsive CSS Grid design
- **Visual Reports**: Room diagrams and tables
- **Real-time Processing**: Live status updates
- **Detailed Results**: Comprehensive analysis
- **Export Options**: JSON and visual reports

### 🔧 Advanced Features
- **Batch Processing**: Multiple PDF processing
- **Parameter Mapping**: Alias recognition
- **Error Handling**: Robust error management
- **Debug Tools**: Comprehensive debugging
- **API Integration**: RESTful endpoints

---

## 🛠️ Development

### Running Tests
```bash
cd tests

# Direct compliance testing
py test_direct_compliance.py

# Uniformity extraction testing
py test_uniformity_extraction.py

# Debug utilities
py debug_uniformity_issue.py

# Simple debugging
py simple_debug_test.py
```

### Batch Processing
```bash
cd scripts
py process_reports_enhanced.py
```

### Debugging
```bash
# Check service health
curl http://localhost:5000/health
curl http://localhost:8000/health

# View debug files
cd temp
# Check debug_*.json files
```

### Adding New Standards
1. Update `../standard_export/output/enhanced_standards.json`
2. Modify `src/parameter_mapping.json` for aliases
3. Test with `tests/test_enhanced_standards.py`

---

## 📋 API Endpoints

### Compliance API (Port 8000)
- `GET /health` - Health check
- `GET /standards-info` - Standards information
- `POST /check-compliance-detailed` - Detailed compliance check
- `GET /docs` - Interactive API documentation

### Report API (Port 5000)
- `GET /health` - Health check
- `POST /extract` - Extract data from PDF
- `GET /files` - List processed files
- `GET /files/{filename}` - Download extracted data

### Web Interface (Port 3000)
- **File Upload**: Drag-and-drop PDF upload
- **Progress Tracking**: Real-time processing status
- **Results Display**: Comprehensive compliance analysis
- **Visual Reports**: Room diagrams and tables
- **Export Options**: Download results

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Conflicts
**Problem**: Services won't start
**Solution**:
```bash
# Check port usage
netstat -ano | findstr :3000
netstat -ano | findstr :5000
netstat -ano | findstr :8000

# Kill Python processes
taskkill /f /im python.exe
```

#### 2. Python Not Found
**Problem**: `py` command not recognized
**Solution**:
- Install Python from python.org
- Ensure Python is in PATH
- Use `python` instead of `py` if needed

#### 3. Dependencies Issues
**Problem**: Import errors
**Solution**:
```bash
py -m pip install -r requirements.txt --force-reinstall
```

#### 4. PDF Processing Fails
**Problem**: Empty extraction results
**Solution**:
- Check PDF is not password-protected
- Ensure PDF contains text (not just images)
- Try different PDF format

#### 5. Compliance Shows "NO_CHECKS"
**Problem**: No compliance checks performed
**Solution**:
- Verify all services are running
- Check extracted data contains room information
- Ensure standards database is loaded

### Debug Tools

#### Service Health Checks
```bash
curl http://localhost:5000/health
curl http://localhost:8000/health
```

#### Debug Files Location
- `temp/debug_*.json` - Debug output
- `temp/*_test_result.json` - Test results
- Console output in service windows

#### Test Scripts
```bash
cd tests
py simple_debug_test.py
py test_direct_compliance.py
```

---

## 📚 Additional Resources

### Documentation Links
- [Main Project README](../README.md) - Complete project guide
- [Project Structure](PROJECT_STRUCTURE.md) - Detailed structure
- [Report Export Guide](../report_export/docs/README.md) - PDF extraction
- [Standards Export Guide](../standard_export/README.md) - Standards database

### API Documentation
- [Compliance API Docs](http://localhost:8000/docs) (when running)
- [Report API Interface](../report_export/api/api_interface.html)

### Test Files
- [Direct Compliance Test](tests/test_direct_compliance.py)
- [Uniformity Extraction Test](tests/test_uniformity_extraction.py)
- [System Integration Test](tests/test_complete_system.py)

### Utility Scripts
- [Batch Processing](scripts/process_reports_enhanced.py)
- [Project Organization](organize_project.bat)
- [Cleanup Utility](cleanup_project.bat)

### Configuration Files
- [Parameter Mapping](src/parameter_mapping.json)
- [Enhanced Standards](../standard_export/output/enhanced_standards.json)
- [Requirements](requirements.txt)

---

## 🎯 Quick Reference

### Start Everything
```bash
start_all_services.bat
```

### Access Points
- **Web Interface**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Report API**: http://localhost:5000

### Key Commands
```bash
# Restart services
restart_services.bat

# Clean up
cleanup_project.bat

# Run tests
cd tests && py test_direct_compliance.py
```

### File Locations
- **Main App**: Current directory
- **PDF Extraction**: `../report_export/`
- **Standards**: `../standard_export/`
- **Tests**: `tests/`
- **Scripts**: `scripts/`

---

## 📝 Technical Notes

- **Python Command**: Uses `py` instead of `python`
- **Enhanced Parser**: Better uniformity extraction
- **Standards**: Realistic lighting standards (enhanced_standards.json)
- **CORS**: Enabled for cross-origin requests
- **Service Management**: Automatic with batch scripts

## 🎯 Key Components

1. **Report Extraction**: Uses enhanced_parser.py for PDF processing
2. **Standards Matching**: Intelligent matching based on room types
3. **Compliance Checking**: Comprehensive LUX, Uniformity, Ra/CRI checks
4. **Web Interface**: Modern, responsive UI with detailed results

---

**🎉 Ready for Lighting Analysis!** 

*This system provides comprehensive lighting compliance checking with modern web interface and robust PDF processing capabilities.*
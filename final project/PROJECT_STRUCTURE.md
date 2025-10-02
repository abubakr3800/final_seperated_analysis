# Final Project Structure - Organized

## 📁 Directory Organization

```
final project/
├── 📂 src/                           # Core application code
│   ├── api_server.py                # FastAPI compliance checker server
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

## 🚀 Quick Start Commands

### Start All Services
```bash
start_all_services.bat
```

### Individual Services
```bash
start_api.bat              # Compliance API (port 8000)
start_report_api.bat       # Report API (port 5000)
start_web_interface.bat    # Web Interface (port 3000)
```

### Maintenance
```bash
organize_project.bat       # Organize files
cleanup_project.bat        # Clean temporary files
restart_services.bat       # Restart all services
```

## 🔧 Path Configuration

All .bat files use relative paths that work from the project root:

- **Report API**: `..\report_export\api\api_server.py`
- **Compliance API**: `src\api_server.py`
- **Web Interface**: `web_server.py`
- **Tests**: `tests\test_*.py`
- **Scripts**: `scripts\*.py`

## 📊 Key Features

✅ **Organized Structure**: Clean separation of concerns
✅ **Working Paths**: All .bat files use correct relative paths
✅ **Easy Maintenance**: Utility scripts for organization and cleanup
✅ **Comprehensive Testing**: All test files in dedicated directory
✅ **Documentation**: Clear README and structure documentation
✅ **Service Management**: Multiple startup options for different needs

## 🎯 Usage

1. **Development**: Use individual service scripts for debugging
2. **Production**: Use `start_all_services.bat` for full system
3. **Testing**: Run tests from `tests/` directory
4. **Maintenance**: Use utility scripts for cleanup and organization

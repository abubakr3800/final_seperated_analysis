# Project Structure Overview

## 📁 **Directory Organization**

The PDF Report Extractor project is organized into logical directories for easy navigation and maintenance.

```
PDF Report Extractor/
├── 📁 core/                    # Core installation and setup
│   └── install_and_run.bat     # Main installation script
│
├── 📁 extractors/              # PDF extraction engines
│   ├── layout_enhanced_extractor.py  # ⭐ Best extractor (recommended)
│   ├── final_extractor.py            # Comprehensive extractor
│   ├── enhanced_parser.py            # Fast parser
│   └── pdf_report_extractor.py       # Original extractor
│
├── 📁 api/                     # Web API interface
│   ├── api_server.py           # Flask API server
│   ├── api_client.py           # Python API client
│   ├── api_interface.html      # Web interface
│   └── start_api.bat           # API startup script
│
├── 📁 batch_processing/        # Batch processing tools
│   ├── process_folder.py       # Simple folder processor
│   ├── batch_processor.py      # Advanced batch processor
│   └── process_folder.bat      # Windows batch file
│
├── 📁 docs/                    # Documentation
│   ├── README.md               # Main documentation
│   ├── API_GUIDE.md            # API documentation
│   ├── FOLDER_PROCESSING_GUIDE.md  # Batch processing guide
│   ├── LAYOUT_ENHANCEMENT_SUMMARY.md  # Layout features
│   └── PROJECT_STRUCTURE.md    # This file
│
├── 📁 examples/                # Usage examples
│   ├── example_usage.py        # Comprehensive examples
│   └── usage_examples.py       # Command line examples
│
├── 📁 tests/                   # Test scripts
│   ├── test_layout.py          # Layout extraction tests
│   ├── test_enhanced.py        # Enhanced parser tests
│   ├── test_extractor.py       # Main extractor tests
│   ├── test_folder_processor.py # Batch processing tests
│   ├── debug_test.py           # Debug utilities
│   └── quick_test.py           # Quick validation tests
│
├── 📄 requirements.txt         # Full dependencies
├── 📄 requirements_minimal.txt # Minimal dependencies
├── 📄 README.md               # Project overview
└── 📄 NESSTRA Report With 150 watt.pdf  # Sample PDF
```

## 🎯 **File Categories**

### **Core Files**
- **Installation scripts** in `core/`
- **Dependencies** in root directory
- **Main README** in root directory

### **Extractors** (Choose one based on your needs)
1. **`layout_enhanced_extractor.py`** ⭐ **RECOMMENDED**
   - Best overall performance
   - Advanced room layout extraction
   - Comprehensive field detection
   - Most accurate results

2. **`final_extractor.py`**
   - Combines multiple approaches
   - Good for complex PDFs
   - Robust error handling

3. **`enhanced_parser.py`**
   - Fast processing
   - Good for simple PDFs
   - Based on added.txt specifications

4. **`pdf_report_extractor.py`**
   - Original implementation
   - Based on guide.txt specifications
   - Good for basic extraction

### **API Interface**
- **`api_server.py`** - Main Flask server
- **`api_client.py`** - Python client library
- **`api_interface.html`** - Web interface
- **`start_api.bat`** - Easy startup script

### **Batch Processing**
- **`process_folder.py`** - Simple folder processor
- **`batch_processor.py`** - Advanced with argparse
- **`process_folder.bat`** - Windows batch file

### **Documentation**
- **`README.md`** - Project overview and quick start
- **`API_GUIDE.md`** - Complete API documentation
- **`FOLDER_PROCESSING_GUIDE.md`** - Batch processing guide
- **`LAYOUT_ENHANCEMENT_SUMMARY.md`** - Advanced features
- **`PROJECT_STRUCTURE.md`** - This file

### **Examples & Tests**
- **`example_usage.py`** - Comprehensive usage examples
- **`usage_examples.py`** - Command line examples
- **`test_*.py`** - Various test scripts
- **`debug_test.py`** - Debug utilities

## 🚀 **Quick Navigation**

### **For New Users:**
1. Start with `README.md` (root directory)
2. Use `extractors/layout_enhanced_extractor.py` (recommended)
3. Check `examples/example_usage.py` for usage patterns

### **For API Integration:**
1. Read `docs/API_GUIDE.md`
2. Use `api/api_server.py` to start server
3. Use `api/api_client.py` for Python integration

### **For Batch Processing:**
1. Read `docs/FOLDER_PROCESSING_GUIDE.md`
2. Use `batch_processing/process_folder.py`
3. Check `tests/test_folder_processor.py` for examples

### **For Development:**
1. Check `tests/` directory for test scripts
2. Use `extractors/` for different extraction approaches
3. Refer to `docs/` for detailed documentation

## 📋 **File Naming Conventions**

- **Extractors**: `*_extractor.py` or `*_parser.py`
- **Tests**: `test_*.py`
- **Examples**: `example_*.py` or `usage_*.py`
- **Documentation**: `*.md`
- **Batch files**: `*.bat`
- **Configuration**: `requirements*.txt`

## 🎉 **Benefits of This Structure**

✅ **Clear separation** of concerns  
✅ **Easy navigation** for different use cases  
✅ **Modular design** for easy maintenance  
✅ **Comprehensive documentation** in dedicated folder  
✅ **Multiple interfaces** (CLI, API, Batch)  
✅ **Extensive testing** and examples  
✅ **Scalable architecture** for future enhancements  

This organization makes the project easy to understand, use, and maintain! 🚀

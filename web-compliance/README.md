# Web Compliance - Lighting Compliance Checker

A modern, dark-themed web interface for checking lighting compliance against standards. This application provides a comprehensive view of all extracted parameters and compliance results.

## 🌟 Features

- **Dark Theme UI**: Modern, professional dark theme interface
- **Complete Parameter Display**: View all extracted parameters from PDF reports
- **Comprehensive Compliance Results**: Detailed room-by-room compliance analysis
- **Multiple Views**: 
  - Overview with summary statistics
  - All extracted parameters
  - Compliance results with pass/fail indicators
  - Room details
  - Luminaire information
  - Scene information
  - Raw JSON data viewer
- **Drag & Drop**: Easy file upload with drag-and-drop support
- **Real-time Processing**: Live status updates during processing

## 📁 Structure

```
web-compliance/
├── api_server.py          # FastAPI server for compliance checking
├── compliance_checker.py  # Core compliance checking logic
├── index.html            # Dark-themed web interface
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── SETUP.md             # Setup instructions
└── API_USAGE.md         # API usage documentation
```

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Report API** (if not already running)
   ```bash
   cd ../report_export/api
   python api_server.py
   ```
   The Report API should run on `http://localhost:5000`

3. **Start the Compliance API**
   ```bash
   cd web-compliance
   python api_server.py
   ```
   The Compliance API will run on `http://localhost:8000`

4. **Open the Web Interface**
   - Open `index.html` in your web browser
   - Or serve it using a local web server:
     ```bash
     python -m http.server 3000
     ```
   - Then navigate to `http://localhost:3000`

## 📋 Requirements

- Python 3.7+
- FastAPI
- uvicorn
- requests
- Report API running on port 5000
- Standards file: `../standard_export/output/standards_filtered.json`
- Aliases file: `../report_export/extractors/aliases.json`

## 🔗 API Endpoints

### GET `/`
API documentation and information

### GET `/health`
Health check endpoint

### GET `/standards-info`
Get information about loaded standards

### POST `/check-compliance`
Basic compliance check (returns summary)

### POST `/check-compliance-detailed`
**Recommended**: Detailed compliance check with all extracted parameters

### GET `/test-connection`
Test connection to Report API

## 📖 Documentation

- [SETUP.md](SETUP.md) - Detailed setup instructions
- [API_USAGE.md](API_USAGE.md) - API usage guide

## 🎨 Features Overview

### Web Interface Tabs

1. **Overview**: Summary statistics and report metadata
2. **Parameters**: All extracted lighting parameters
3. **Compliance**: Room-by-room compliance results with pass/fail indicators
4. **Rooms**: Detailed room information
5. **Luminaires**: Luminaire specifications
6. **Scenes**: Scene configurations
7. **Raw Data**: Complete JSON data viewer

### Compliance Display

- **Status Indicators**: Color-coded pass/fail status
- **Check Details**: Required vs actual values with margins
- **Standard Matching**: Shows matched standard reference
- **Utilisation Profile**: Displays inferred or extracted profiles

## 🔧 Configuration

The API server automatically resolves paths to:
- Standards: `../standard_export/output/standards_filtered.json`
- Aliases: `../report_export/extractors/aliases.json`
- Report API: `http://localhost:5000`

## 📝 Notes

- The old version in `final project/` remains unchanged
- This is a standalone web-compliance system
- All extracted parameters are displayed
- All compliance results are visible
- Dark theme for comfortable viewing

## 🐛 Troubleshooting

### API Connection Issues
- Ensure Report API is running on port 5000
- Check firewall settings
- Verify CORS is enabled

### File Not Found Errors
- Verify standards file exists
- Check aliases.json path
- Ensure relative paths are correct

### Browser Issues
- Use modern browser (Chrome, Firefox, Edge)
- Enable JavaScript
- Check browser console for errors

## 📄 License

Part of the final_comparator project.


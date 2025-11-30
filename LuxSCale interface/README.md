# LuxSCale Interface - Lighting Design Report Generator

A simple, user-friendly web interface for generating lighting design reports similar to Dialux. The system asks minimal questions and automatically generates standards-compliant reports.

## 🌟 Features

- **Simple Form Interface**: Minimal questions to generate complete reports
- **Dark Theme Design**: Modern, professional dark-themed UI
- **Standards Compliance**: Automatically checks reports against lighting standards
- **Dialux-like Reports**: Generates reports in a format similar to Dialux
- **Automatic Calculations**: Calculates lighting parameters from basic inputs
- **Compliance Checking**: Verifies generated designs meet standard requirements

## 📁 Project Structure

```
LuxSCale interface/
├── index.html                    # Dark-themed web interface
├── api_server.py                # FastAPI server (main API)
├── report_generator.py          # Report generation logic
├── compliance_integration.py    # Compliance checking integration
├── requirements.txt             # Python dependencies
├── start_server.bat            # Windows startup script
├── start_server.sh             # Linux/Mac startup script
├── reports/                    # Generated reports storage (created automatically)
├── README.md                   # This file
├── DOCUMENTATION.md            # Complete code documentation
└── API_DOCUMENTATION.md        # API usage guide
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd "LuxSCale interface"
pip install -r requirements.txt
```

### 2. Start the API Server

**Windows:**
```bash
start_server.bat
```

**Linux/Mac:**
```bash
chmod +x start_server.sh
./start_server.sh
```

**Or manually:**
```bash
python api_server.py
```

The API will start on `http://localhost:8001`

### 3. Open the Web Interface

Open `index.html` in your web browser, or serve it using:

```bash
python -m http.server 3000
```

Then navigate to `http://localhost:3000`

## 📋 Required Information

The form asks for minimal information:

### Project Information
- Project Name (required)
- Company Name (optional)

### Room Information
- Room Type / Utilisation Profile (required) - Determines lighting standard
- Room Dimensions: Length, Width, Height (required)

### Luminaire Information
- Number of Luminaires (required)
- Luminaire Power in Watts (required)
- Luminous Flux OR Efficacy (one required)
- Mounting Height (required)
- Work Plane Height (optional, defaults to 0.75m)

### Optional Information
- Manufacturer
- Article/Model Number

## 🔄 How It Works

1. **User fills form** → Minimal questions
2. **System generates report** → Calculates all lighting parameters
3. **System checks compliance** → Verifies against standards
4. **User downloads report** → JSON format similar to Dialux

## 📊 Report Structure

Generated reports include:
- **Metadata**: Project and company information
- **Lighting Setup**: Calculated illuminance, uniformity, power, etc.
- **Rooms**: Room dimensions and layout
- **Luminaires**: Luminaire specifications
- **Scenes**: Lighting scene data
- **Compliance Results**: Pass/fail status against standards

## 🔗 Dependencies

- Uses `standards_filtered.json` from `../standard_export/output/`
- Uses compliance checker from `../web-compliance/` or `../final project/src/`
- No external services required (standalone)

## 📖 Documentation

- [DOCUMENTATION.md](DOCUMENTATION.md) - Complete code documentation
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API usage guide

## 🎯 Key Features

- ✅ **Minimal Questions**: Only essential information required
- ✅ **Automatic Calculations**: System calculates all parameters
- ✅ **Standards Compliance**: Built-in compliance checking
- ✅ **Dark Theme**: Modern, professional interface
- ✅ **Simple Workflow**: Fill form → Generate → Download

## 🐛 Troubleshooting

### API Not Starting
- Check if port 8001 is available
- Verify Python dependencies are installed
- Check standards file path is correct

### Compliance Check Fails
- Ensure standards file exists at `../standard_export/output/standards_filtered.json`
- Check compliance checker can be imported

### Report Generation Errors
- Verify all required fields are filled
- Check numeric values are positive
- Ensure either luminous flux OR efficacy is provided

## 📝 Notes

- Reports are saved in the `reports/` folder
- Each report has a unique ID
- Reports can be downloaded as JSON files
- The system uses simplified calculations (for production, use professional lighting calculation software)


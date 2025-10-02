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

All extractors produce structured JSON data with comprehensive layout information:

### **Complete Data Structure**

```json
{
  "metadata": {
    "company_name": "Short Cicuit Company",
    "project_name": "Lighting study for nesstra factory",
    "engineer": "Eng.Mostafa Emad",
    "email": "mostafaattalla122@gmail.com",
    "report_title": "Report.pdf"
  },
  "lighting_setup": {
    "number_of_fixtures": 36,
    "fixture_type": "HighBay 150 watt",
    "mounting_height_m": 11.5,
    "average_lux": 673.0,
    "min_lux": 277.0,
    "max_lux": 949.0,
    "uniformity": 0.41,
    "total_power_w": 5400.0,
    "luminous_efficacy_lm_per_w": 145.0,
    "g1": 1.64,
    "index": "WP1"
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
        },
        {
          "x_m": 8.0,
          "y_m": 36.002,
          "z_m": 7.0
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
      "utilisation_profile": "Health care premises - Operating areas (5.46.1 Pre-op and recovery rooms)"
    }
  ]
}
```

### **Layout Data Structure**

The **`layout`** array contains detailed spatial coordinates for each room:

```json
"layout": [
  {
    "x_m": 7.0,      // X coordinate in meters
    "y_m": 4.0,      // Y coordinate in meters  
    "z_m": 36.002    // Z coordinate in meters (height)
  }
]
```

**Layout Properties:**
- **`x_m`**: X-axis coordinate (horizontal position)
- **`y_m`**: Y-axis coordinate (vertical position)
- **`z_m`**: Z-axis coordinate (height/elevation)
- **Units**: All coordinates in meters
- **Purpose**: Defines luminaire positions and room boundaries

### **Room Structure**

```json
"rooms": [
  {
    "name": "Building 1 · Storey 1 · Room 1",  // Hierarchical room name
    "arrangement": "X",                        // Layout arrangement type
    "layout": [...]                           // Array of coordinate points
  }
]
```

**Room Properties:**
- **`name`**: Hierarchical room identifier (Building · Storey · Room)
- **`arrangement`**: Layout pattern (X, Grid, Linear, etc.)
- **`layout`**: Array of 3D coordinate points defining the space

### **Scene Structure**

```json
"scenes": [
  {
    "scene_name": "the factory",              // Scene identifier
    "average_lux": 673.0,                    // Average illuminance
    "min_lux": 277.0,                        // Minimum illuminance
    "max_lux": 949.0,                        // Maximum illuminance
    "uniformity": 0.41,                      // Uniformity ratio
    "utilisation_profile": "Health care..."  // Standards profile
  }
]
```

**Scene Properties:**
- **`scene_name`**: Descriptive scene name
- **`average_lux`**: Mean illuminance level
- **`min_lux`**: Minimum illuminance point
- **`max_lux`**: Maximum illuminance point
- **`uniformity`**: Uniformity ratio (min/max)
- **`utilisation_profile`**: Standards compliance profile

### **Luminaire Structure**

```json
"luminaires": [
  {
    "quantity": 36,                           // Number of fixtures
    "manufacturer": "Philips",                // Manufacturer name
    "article_no": "BY698P LED265CW G2 WB",   // Product code
    "power_w": 150.0,                        // Power consumption (Watts)
    "luminous_flux_lm": 21750.0,             // Light output (Lumens)
    "efficacy_lm_per_w": 145.0               // Efficiency (Lumens/Watt)
  }
]
```

### **Lighting Setup Structure**

```json
"lighting_setup": {
  "number_of_fixtures": 36,                  // Total fixture count
  "fixture_type": "HighBay 150 watt",        // Fixture description
  "mounting_height_m": 11.5,                 // Installation height
  "average_lux": 673.0,                      // Overall average illuminance
  "min_lux": 277.0,                          // Overall minimum illuminance
  "max_lux": 949.0,                          // Overall maximum illuminance
  "uniformity": 0.41,                        // Overall uniformity ratio
  "total_power_w": 5400.0,                   // Total power consumption
  "luminous_efficacy_lm_per_w": 145.0,       // Overall efficiency
  "g1": 1.64,                                // Glare index
  "index": "WP1"                             // Working plane index
}
```

### **Layout Visualization**

The layout data can be used to create visual representations:

```python
# Example: Extract room dimensions from layout
def get_room_dimensions(layout_points):
    x_coords = [point['x_m'] for point in layout_points]
    y_coords = [point['y_m'] for point in layout_points]
    z_coords = [point['z_m'] for point in layout_points]
    
    return {
        'width': max(x_coords) - min(x_coords),
        'length': max(y_coords) - min(y_coords),
        'height': max(z_coords) - min(z_coords),
        'area': (max(x_coords) - min(x_coords)) * (max(y_coords) - min(y_coords))
    }

# Example: Count luminaires in room
def count_luminaires_in_room(layout_points):
    return len(layout_points)

# Example: Calculate luminaire density
def calculate_luminaire_density(layout_points):
    dimensions = get_room_dimensions(layout_points)
    luminaire_count = count_luminaires_in_room(layout_points)
    return luminaire_count / dimensions['area']  # luminaires per m²
```

### **Data Usage Examples**

#### **1. Room Analysis**
```python
# Access room data
room = extracted_data['rooms'][0]
room_name = room['name']           # "Building 1 · Storey 1 · Room 1"
arrangement = room['arrangement']  # "X"
layout_points = room['layout']     # Array of coordinate points

# Calculate room area
x_coords = [p['x_m'] for p in layout_points]
y_coords = [p['y_m'] for p in layout_points]
room_area = (max(x_coords) - min(x_coords)) * (max(y_coords) - min(y_coords))
```

#### **2. Lighting Performance**
```python
# Access lighting data
lighting = extracted_data['lighting_setup']
avg_lux = lighting['average_lux']      # 673.0
uniformity = lighting['uniformity']    # 0.41
total_power = lighting['total_power_w'] # 5400.0

# Access scene data
scene = extracted_data['scenes'][0]
scene_name = scene['scene_name']       # "the factory"
scene_lux = scene['average_lux']       # 673.0
scene_uniformity = scene['uniformity'] # 0.41
```

#### **3. Luminaire Specifications**
```python
# Access luminaire data
luminaire = extracted_data['luminaires'][0]
quantity = luminaire['quantity']           # 36
manufacturer = luminaire['manufacturer']   # "Philips"
power = luminaire['power_w']              # 150.0
flux = luminaire['luminous_flux_lm']      # 21750.0
efficacy = luminaire['efficacy_lm_per_w'] # 145.0
```

### **Layout Coordinate System**

The layout uses a 3D coordinate system:

- **X-axis**: Horizontal position (left-right)
- **Y-axis**: Vertical position (front-back)  
- **Z-axis**: Height/elevation (up-down)
- **Origin**: Typically bottom-left corner of the room
- **Units**: All measurements in meters

**Coordinate Examples:**
```json
{
  "x_m": 7.0,    // 7 meters from left edge
  "y_m": 4.0,    // 4 meters from front edge
  "z_m": 36.002  // 36.002 meters height (mounting height)
}
```

### **Arrangement Types**

Common arrangement patterns detected:

- **"X"**: Cross or diagonal arrangement
- **"Grid"**: Regular grid pattern
- **"Linear"**: Straight line arrangement
- **"Circular"**: Circular or curved arrangement
- **"Random"**: Irregular or custom arrangement

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
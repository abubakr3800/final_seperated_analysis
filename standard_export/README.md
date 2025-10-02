# EN 12464-1 Standards Extractor

This project extracts lighting standards from the prEN 12464-1 PDF document and converts them into a structured JSON format for easy comparison with project reports.

## Project Structure

```
exporter/
├── data/                           # Input files
│   ├── prEN 12464-1.pdf          # Source PDF with lighting standards
│   └── NESSTRA Report With 150 watt.pdf  # Sample project report
├── src/                           # Source code
│   └── extract_standards.py      # Main extraction script
├── output/                        # Generated files
│   └── standards.json            # Extracted standards (generated)
├── docs/                          # Documentation
│   └── standard-export.txt       # Project requirements
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## Features

- **Comprehensive Extraction**: Extracts all tables from Clause 6 (Tables 6.1 – 6.54) of prEN 12464-1
- **Consistent Schema**: Uses a fixed JSON schema with standardized variable names
- **Data Cleaning**: Handles various data formats and cleans inconsistent entries
- **Numeric Parsing**: Properly parses numeric values from text
- **Category Detection**: Automatically detects table categories from headings

## JSON Schema

The extracted data follows this consistent schema:

```json
{
  "ref_no": "6.1.1",
  "category": "Traffic zones inside buildings",
  "task_or_activity": "Corridors and circulation areas",
  "Em_r_lx": 100,
  "Em_u_lx": 150,
  "Uo": 0.40,
  "Ra": 40,
  "RUGL": 28,
  "Ez_lx": 50,
  "Em_wall_lx": 50,
  "Em_ceiling_lx": 30,
  "specific_requirements": "Illuminance at floor level..."
}
```

### Field Descriptions

- `ref_no`: Reference number (e.g., "6.1.1")
- `category`: Table category from heading
- `task_or_activity`: Specific task or activity description
- `Em_r_lx`: Maintained illuminance on reference plane (lux)
- `Em_u_lx`: Maintained illuminance on working plane (lux)
- `Uo`: Uniformity ratio
- `Ra`: Color rendering index
- `RUGL`: Unified glare rating
- `Ez_lx`: Cylindrical illuminance (lux)
- `Em_wall_lx`: Wall illuminance (lux)
- `Em_ceiling_lx`: Ceiling illuminance (lux)
- `specific_requirements`: Additional requirements and notes

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the extraction script:

```bash
python src/extract_standards.py
```

This will:
1. Process the PDF file in `data/prEN 12464-1.pdf`
2. Extract all tables from Clause 6
3. Generate `output/standards.json` with structured data

## Output

The script generates a comprehensive JSON file containing all lighting standards with:
- Consistent variable names for easy comparison
- Proper data types (numbers vs strings)
- Cleaned and normalized text
- Complete coverage of all tables in the standard

## Use Cases

This structured data can be used to:
- Compare project reports against official standards
- Build compliance checking tools
- Create lighting design validation systems
- Generate standardized reports

## Example Comparison

With the extracted standards, you can compare project data:

```python
# Project report data
project_data = {
    "utilisation_profile": "Traffic zones inside buildings - Corridors and circulation areas",
    "average_lux": 120,
    "uniformity": 0.45,
    "Ra": 80
}

# Find matching standard
standard = find_matching_standard(project_data["utilisation_profile"])
# Compare values against standard requirements
```

## Dependencies

- `pdfplumber`: PDF text and table extraction
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `camelot-py`: Alternative table extraction (optional)

## License

This project is for educational and research purposes. The prEN 12464-1 standard is subject to its own copyright and licensing terms.

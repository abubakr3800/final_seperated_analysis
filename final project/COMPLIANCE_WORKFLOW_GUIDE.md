# Compliance Workflow Guide

## 📋 Overview

This guide provides step-by-step commands for the complete compliance checking workflow using `standards_filtered.json`.

## 🎯 Workflow Steps

1. **Extract Parameters** - Extract data from PDF report
2. **Compare to Standards** - Compare extracted data against standards
3. **Generate Compliance Sheet** - Create compliance report

---

## 🚀 Quick Start

### **Single Command (All Steps)**
```cmd
py "final project\scripts\compliance_workflow.py" "path\to\report.pdf"
```

### **With Custom Output File**
```cmd
py "final project\scripts\compliance_workflow.py" "path\to\report.pdf" --output "my_compliance.json"
```

### **Using Batch File (Windows)**
```cmd
cd "final project"
scripts\compliance_workflow.bat "path\to\report.pdf"
```

---

## 📝 Step-by-Step Commands

### **Prerequisites**

1. **Start Report API** (Port 5000):
   ```cmd
   cd report_export
   py api\api_server.py
   ```
   Keep this terminal open.

2. **Start Compliance API** (Port 8000):
   ```cmd
   cd "final project"
   py src\api_server.py
   ```
   Keep this terminal open.

### **Step 1: Extract Parameters from Report**

**Command:**
```cmd
cd "final project"
py -c "import sys; sys.path.append('src'); from compliance_checker import ComplianceChecker; import os; checker = ComplianceChecker(os.path.join('..', 'standard_export', 'output', 'standards_filtered.json'), 'http://localhost:5000'); data = checker.extract_report_data('path\to\report.pdf'); print('Extracted:', len(data.get('rooms', [])))"
```

**Or use the workflow script:**
```cmd
cd "final project"
py scripts\compliance_workflow.py "path\to\report.pdf"
```

**Expected Output:**
```
STEP 1: EXTRACTING PARAMETERS FROM REPORT
📄 PDF File: path\to\report.pdf
🔄 Extracting data from PDF...
✅ Extraction successful!
   - Company: Company Name
   - Project: Project Name
   - Rooms: 1
   - Scenes: 2
   - Average Lux: 213.0
   - Uniformity: 0.57
```

### **Step 2: Compare to Standards**

**Command:**
```cmd
cd "final project"
py -c "import sys; sys.path.append('src'); from compliance_checker import ComplianceChecker; import os, json; checker = ComplianceChecker(os.path.join('..', 'standard_export', 'output', 'standards_filtered.json'), 'http://localhost:5000'); report_data = checker.extract_report_data('path\to\report.pdf'); result = checker.check_compliance(report_data); print('Overall:', result.get('overall_compliance')); print('Passed:', result.get('summary', {}).get('passed', 0))"
```

**Or use the workflow script (includes Step 1):**
```cmd
cd "final project"
py scripts\compliance_workflow.py "path\to\report.pdf"
```

**Expected Output:**
```
STEP 2: COMPARING TO STANDARDS
🔄 Comparing against standards...
✅ Comparison complete!
   - Overall Compliance: PASS
   - Total Rooms Checked: 1
   - Passed: 1
   - Failed: 0
   - No Standard Found: 0
   - Pass Rate: 100.0%
```

### **Step 3: Generate Compliance Sheet**

**Command:**
```cmd
cd "final project"
py scripts\compliance_workflow.py "path\to\report.pdf" --output "compliance_report.json"
```

**Expected Output:**
```
STEP 3: GENERATING COMPLIANCE SHEET
💾 Saving compliance sheet...
✅ Compliance sheet generated!
   📄 File: temp\compliance_report.json
   📊 Size: 45.2 KB
```

---

## 🔧 Complete Workflow Example

### **Example 1: Basic Usage**

```cmd
REM Navigate to project root
cd E:\AI_projects\final_comparator

REM Run complete workflow
cd "final project"
py scripts\compliance_workflow.py "..\report_export\NESSTRA Report With 150 watt.pdf"
```

### **Example 2: With Custom Output**

```cmd
cd E:\AI_projects\final_comparator
cd "final project"
py scripts\compliance_workflow.py "..\report_export\NESSTRA Report With 150 watt.pdf" --output "nesstra_compliance.json"
```

### **Example 3: Using Batch File**

```cmd
cd E:\AI_projects\final_comparator\final project
scripts\compliance_workflow.bat "..\report_export\NESSTRA Report With 150 watt.pdf"
```

---

## 📊 Output Files

### **Compliance Sheet Structure**

The generated compliance sheet contains:

```json
{
  "generated_at": "2024-01-01T12:00:00",
  "report_metadata": {
    "company_name": "...",
    "project_name": "...",
    "engineer": "...",
    "email": "..."
  },
  "lighting_setup": {
    "average_lux": 213.0,
    "uniformity": 0.57,
    ...
  },
  "compliance_summary": {
    "overall_compliance": "PASS",
    "total_rooms": 1,
    "passed": 1,
    "failed": 0,
    "pass_rate": 100.0
  },
  "room_compliance_details": [
    {
      "room": "Building 1 · Storey 1 · Room 1",
      "status": "PASS",
      "utilisation_profile": "...",
      "checks": {
        "illuminance": "PASS",
        "uniformity": "PASS"
      }
    }
  ],
  "full_report_data": {...},
  "full_compliance_result": {...}
}
```

### **Output Location**

- **Default**: `final project/temp/compliance_sheet_YYYYMMDD_HHMMSS.json`
- **Custom**: Specified with `--output` parameter

---

## 🌐 Website Integration

The website uses the **same files and workflow**:

### **Website Workflow**

1. **User uploads PDF** → Web interface
2. **Web interface calls** → Compliance API (Port 8000)
3. **Compliance API**:
   - Uses `standards_filtered.json` (same as CLI)
   - Calls Report API (Port 5000) for extraction
   - Performs comparison
   - Returns compliance sheet

### **API Endpoints**

**Compliance API** (`final project/src/api_server.py`):
- `POST /check-compliance` - Basic compliance check
- `POST /check-compliance-detailed` - Detailed compliance check with full data

**Report API** (`report_export/api/api_server.py`):
- `POST /extract` - Extract data from PDF

### **Configuration**

Both CLI and website use:
- **Standards File**: `standard_export/output/standards_filtered.json`
- **Report API**: `http://localhost:5000`
- **Compliance API**: `http://localhost:8000`

---

## 🔍 Verification Commands

### **Check Standards File**
```cmd
py -c "import json; data = json.load(open('standard_export/output/standards_filtered.json', 'r', encoding='utf-8')); print(f'Standards loaded: {len(data)} entries')"
```

### **Test Report API**
```cmd
curl http://localhost:5000/health
```

### **Test Compliance API**
```cmd
curl http://localhost:8000/health
```

### **Check Standards Info**
```cmd
curl http://localhost:8000/standards-info
```

---

## 📋 Command Reference

### **Workflow Script**
```cmd
py scripts\compliance_workflow.py <pdf_file> [--output <output_file>]
```

### **Batch File**
```cmd
scripts\compliance_workflow.bat <pdf_file> [output_file]
```

### **Python Direct**
```python
from compliance_checker import ComplianceChecker
checker = ComplianceChecker("standards_filtered.json", "http://localhost:5000")
report_data = checker.extract_report_data("report.pdf")
result = checker.check_compliance(report_data)
```

---

## 🎯 Quick Command List

### **1. Extract Parameters**
```cmd
cd "final project"
py scripts\compliance_workflow.py "report.pdf"
```

### **2. Compare to Standards**
```cmd
cd "final project"
py scripts\compliance_workflow.py "report.pdf"
```

### **3. Generate Compliance Sheet**
```cmd
cd "final project"
py scripts\compliance_workflow.py "report.pdf" --output "compliance.json"
```

### **All-in-One**
```cmd
cd "final project"
py scripts\compliance_workflow.py "report.pdf" --output "compliance.json"
```

---

## ✅ Verification Checklist

- [ ] Report API running on port 5000
- [ ] Compliance API running on port 8000
- [ ] `standards_filtered.json` exists and has 73 entries
- [ ] PDF file path is correct
- [ ] Output directory (`temp/`) exists

---

## 🐛 Troubleshooting

### **Error: Standards file not found**
```cmd
REM Check if file exists
dir "standard_export\output\standards_filtered.json"
```

### **Error: Report API not responding**
```cmd
REM Check if Report API is running
curl http://localhost:5000/health
```

### **Error: Compliance API not responding**
```cmd
REM Check if Compliance API is running
curl http://localhost:8000/health
```

### **Error: No standard found**
- Check if `standards_filtered.json` has 73 entries
- Verify the utilisation_profile in the report
- Check matching logic in compliance_checker.py

---

## 📚 Additional Resources

- **Standards File**: `standard_export/output/standards_filtered.json`
- **Workflow Script**: `final project/scripts/compliance_workflow.py`
- **Compliance Checker**: `final project/src/compliance_checker.py`
- **API Server**: `final project/src/api_server.py`

---

**Last Updated**: 2024  
**Standards File**: `standards_filtered.json` (73 entries)  
**Status**: Production Ready


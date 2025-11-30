# Quick Commands Reference

## 🚀 Complete Workflow (All Steps)

### **Single Command - All Steps**
```cmd
cd "final project"
py scripts\compliance_workflow.py "path\to\report.pdf"
```

### **With Custom Output File**
```cmd
cd "final project"
py scripts\compliance_workflow.py "path\to\report.pdf" --output "my_compliance.json"
```

### **Using Batch File**
```cmd
cd "final project"
scripts\compliance_workflow.bat "path\to\report.pdf"
```

---

## 📋 Step-by-Step Commands

### **Step 1: Extract Parameters from Report**

```cmd
cd "final project"
py scripts\compliance_workflow.py "path\to\report.pdf"
```
*(This runs all steps, but Step 1 output is shown first)*

### **Step 2: Compare to Standards**

```cmd
cd "final project"
py scripts\compliance_workflow.py "path\to\report.pdf"
```
*(This runs all steps, but Step 2 output is shown second)*

### **Step 3: Generate Compliance Sheet**

```cmd
cd "final project"
py scripts\compliance_workflow.py "path\to\report.pdf" --output "compliance.json"
```
*(This runs all steps, compliance sheet is generated in Step 3)*

---

## 🔧 Prerequisites (Start Services)

### **1. Start Report API (Port 5000)**
```cmd
cd report_export
py api\api_server.py
```
*Keep this terminal open*

### **2. Start Compliance API (Port 8000)**
```cmd
cd "final project"
py src\api_server.py
```
*Keep this terminal open*

---

## 📊 Example Commands

### **Example 1: Process NESSTRA Report**
```cmd
cd E:\AI_projects\final_comparator
cd "final project"
py scripts\compliance_workflow.py "..\report_export\NESSTRA Report With 150 watt.pdf"
```

### **Example 2: Process with Custom Output**
```cmd
cd E:\AI_projects\final_comparator
cd "final project"
py scripts\compliance_workflow.py "..\report_export\NESSTRA Report With 150 watt.pdf" --output "nesstra_compliance.json"
```

### **Example 3: Process from Output Folder**
```cmd
cd E:\AI_projects\final_comparator
cd "final project"
py scripts\compliance_workflow.py "..\report_export\output\Al amal factory _Report_extracted.json"
```

---

## ✅ Verification Commands

### **Check Standards File**
```cmd
py -c "import json; data = json.load(open('standard_export/output/standards_filtered.json', 'r', encoding='utf-8')); print(f'Standards: {len(data)} entries')"
```

### **Test Report API**
```cmd
curl http://localhost:5000/health
```

### **Test Compliance API**
```cmd
curl http://localhost:8000/health
```

---

## 📁 Output Location

**Default**: `final project/temp/compliance_sheet_YYYYMMDD_HHMMSS.json`

**Custom**: Use `--output` parameter

---

## 🌐 Website Uses Same Files

The website automatically uses:
- ✅ `standards_filtered.json` (same as CLI)
- ✅ Same compliance checker
- ✅ Same comparison logic

**No changes needed** - website will use the updated standards file automatically!

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| **All Steps** | `py scripts\compliance_workflow.py "report.pdf"` |
| **Custom Output** | `py scripts\compliance_workflow.py "report.pdf" --output "output.json"` |
| **Batch File** | `scripts\compliance_workflow.bat "report.pdf"` |
| **Start Report API** | `cd report_export && py api\api_server.py` |
| **Start Compliance API** | `cd "final project" && py src\api_server.py` |

---

**Standards File**: `standard_export/output/standards_filtered.json` (73 entries)  
**Status**: ✅ Ready to Use


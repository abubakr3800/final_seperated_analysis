# Folder Processing Guide

## 🚀 **Batch PDF Processing**

Process all PDF files in a folder and save each report with the same name in an output folder.

### 📁 **Files Created:**

1. **`process_folder.py`** - Simple folder processor
2. **`batch_processor.py`** - Advanced batch processor with argparse
3. **`process_folder.bat`** - Windows batch file for easy usage

### 🎯 **Usage Options:**

#### **Option 1: Python Script (Recommended)**
```bash
# Process current directory, save to "output" folder
py batch_processing/process_folder.py

# Process specific folder, save to "output" folder
py batch_processing/process_folder.py "C:\path\to\pdf\files"

# Process specific folder, save to specific output folder
py batch_processing/process_folder.py "C:\input\folder" "C:\output\folder"
```

#### **Option 2: Windows Batch File**
```bash
# Process current directory, save to "output" folder
batch_processing/process_folder.bat

# Process specific folder, save to "output" folder
batch_processing/process_folder.bat "C:\path\to\pdf\files"

# Process specific folder, save to specific output folder
batch_processing/process_folder.bat "C:\input\folder" "C:\output\folder"
```

#### **Option 3: Advanced Batch Processor**
```bash
# Process current directory
py batch_processing/batch_processor.py

# Process specific folder
py batch_processing/batch_processor.py "C:\path\to\pdf\files"

# Process with custom output folder
py batch_processing/batch_processor.py "C:\input" -o "C:\output"
```

### 📊 **Output Structure:**

```
output/
├── report1_extracted.json
├── report2_extracted.json
├── report3_extracted.json
└── batch_summary.json
```

### 📋 **Features:**

✅ **Automatic PDF Detection** - Finds all .pdf files in input folder  
✅ **Same Name Output** - Each report saved with same name + "_extracted.json"  
✅ **Batch Summary** - Complete processing summary in batch_summary.json  
✅ **Error Handling** - Continues processing even if some files fail  
✅ **Progress Tracking** - Shows processing status for each file  
✅ **Output Folder Creation** - Automatically creates output folder  

### 🎯 **Example Output:**

```
Found 3 PDF files to process
Input folder: C:\reports
Output folder: C:\extracted
============================================================
Processing: report1.pdf
✓ Saved: C:\extracted\report1_extracted.json
Processing: report2.pdf
✓ Saved: C:\extracted\report2_extracted.json
Processing: report3.pdf
✗ Error processing report3.pdf: File corrupted
============================================================
FOLDER PROCESSING COMPLETED
============================================================
Total files: 3
Successful: 2
Failed: 1
Summary saved to: C:\extracted\batch_summary.json
```

### 📄 **Batch Summary Format:**

```json
{
  "batch_summary": {
    "total_files": 3,
    "successful": 2,
    "failed": 1,
    "input_folder": "C:\\reports",
    "output_folder": "C:\\extracted"
  },
  "results": [
    {
      "file": "report1.pdf",
      "status": "success",
      "output": "C:\\extracted\\report1_extracted.json"
    },
    {
      "file": "report2.pdf",
      "status": "success", 
      "output": "C:\\extracted\\report2_extracted.json"
    },
    {
      "file": "report3.pdf",
      "status": "failed",
      "error": "File corrupted"
    }
  ]
}
```

### 🔧 **Requirements:**

- Python 3.6+
- All dependencies from `requirements_minimal.txt`
- PDF files in input folder

### 🎉 **Ready to Use:**

The folder processor is now ready to handle multiple PDF files efficiently! 🚀

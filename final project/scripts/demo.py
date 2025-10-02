"""
Simple demo script to show how the system works
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking project files...")
    
    files_to_check = [
        "src/compliance_checker.py",
        "src/api_server.py", 
        "requirements.txt",
        "README.md",
        "start_api.bat",
        "start_report_api.bat"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def check_dependencies():
    """Check if required dependencies are available"""
    print("\n🔍 Checking dependencies...")
    
    try:
        import fastapi
        print("✅ fastapi")
    except ImportError:
        print("❌ fastapi - Install with: pip install fastapi")
    
    try:
        import uvicorn
        print("✅ uvicorn")
    except ImportError:
        print("❌ uvicorn - Install with: pip install uvicorn")
    
    try:
        import requests
        print("✅ requests")
    except ImportError:
        print("❌ requests - Install with: pip install requests")

def check_external_projects():
    """Check if external projects exist"""
    print("\n🔍 Checking external projects...")
    
    # Check report_export
    report_export_path = "../report_export"
    if os.path.exists(report_export_path):
        print("✅ report_export project found")
        
        # Check for API server
        api_server = os.path.join(report_export_path, "api", "api_server.py")
        if os.path.exists(api_server):
            print("✅ report_export API server found")
        else:
            print("❌ report_export API server not found")
    else:
        print("❌ report_export project not found")
    
    # Check standard_export
    standard_export_path = "../standard_export"
    if os.path.exists(standard_export_path):
        print("✅ standard_export project found")
        
        # Check for standards file
        standards_file = os.path.join(standard_export_path, "output", "complete_standards.json")
        if os.path.exists(standards_file):
            print("✅ complete_standards.json found")
            
            # Check file size
            file_size = os.path.getsize(standards_file)
            print(f"📊 Standards file size: {file_size:,} bytes")
        else:
            print("❌ complete_standards.json not found")
    else:
        print("❌ standard_export project not found")

def show_usage_instructions():
    """Show how to use the system"""
    print("\n" + "="*60)
    print("🚀 HOW TO USE THE LIGHTING COMPLIANCE CHECKER")
    print("="*60)
    print()
    print("1️⃣  Start the Report Extraction API:")
    print("    Run: start_report_api.bat")
    print("    This starts the API on http://localhost:5000")
    print()
    print("2️⃣  Start the Compliance Checker API:")
    print("    Run: start_api.bat") 
    print("    This starts the API on http://localhost:8000")
    print()
    print("3️⃣  Test the system:")
    print("    Open browser: http://localhost:8000/docs")
    print("    Upload a PDF file and get compliance results")
    print()
    print("4️⃣  API Endpoints:")
    print("    POST /check-compliance - Upload PDF, get PASS/FAIL results")
    print("    GET  /health - Check system health")
    print("    GET  /standards-info - View loaded standards")
    print()
    print("🎯 FINAL RESULT:")
    print("   You get a simple API that takes a PDF report and returns")
    print("   compliance results with PASS/FAIL status for each room.")
    print("="*60)

def main():
    """Main demo function"""
    print("🎯 LIGHTING COMPLIANCE CHECKER - FINAL PROJECT")
    print("="*60)
    
    # Check all components
    files_ok = check_files()
    check_dependencies()
    check_external_projects()
    
    print("\n" + "="*60)
    if files_ok:
        print("✅ Project setup complete!")
        show_usage_instructions()
    else:
        print("❌ Some files are missing. Please check the errors above.")

if __name__ == "__main__":
    main()

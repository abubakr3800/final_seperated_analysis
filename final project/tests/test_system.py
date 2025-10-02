"""
Test script for the Lighting Compliance Checker system
"""

import requests
import json
import os
from pathlib import Path

def test_api_health():
    """Test if the compliance checker API is running"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Compliance Checker API is running")
            return True
        else:
            print(f"❌ Compliance Checker API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Compliance Checker API: {e}")
        return False

def test_report_api_health():
    """Test if the report extraction API is running"""
    try:
        response = requests.get("http://localhost:5000/health")
        if response.status_code == 200:
            print("✅ Report Extraction API is running")
            return True
        else:
            print(f"❌ Report Extraction API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Report Extraction API: {e}")
        return False

def test_standards_loaded():
    """Test if standards are loaded"""
    try:
        response = requests.get("http://localhost:8000/standards-info")
        if response.status_code == 200:
            data = response.json()
            total_standards = data.get('total_standards', 0)
            print(f"✅ Standards loaded: {total_standards} standards available")
            return True
        else:
            print(f"❌ Failed to get standards info: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking standards: {e}")
        return False

def test_with_sample_pdf():
    """Test the system with a sample PDF if available"""
    # Look for sample PDFs in the parent directories
    sample_paths = [
        "../report_export/NESSTRA Report With 150 watt.pdf",
        "../standard_export/data/NESSTRA Report With 150 watt.pdf"
    ]
    
    sample_pdf = None
    for path in sample_paths:
        if os.path.exists(path):
            sample_pdf = path
            break
    
    if not sample_pdf:
        print("⚠️  No sample PDF found for testing")
        return False
    
    try:
        print(f"🧪 Testing with sample PDF: {sample_pdf}")
        
        with open(sample_pdf, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/check-compliance", files=files)
        
        if response.status_code == 200:
            result = response.json()
            compliance = result.get('compliance_result', {}).get('overall_compliance', 'UNKNOWN')
            print(f"✅ Test successful! Compliance result: {compliance}")
            
            # Print summary
            summary = result.get('compliance_result', {}).get('summary', {})
            if summary:
                print(f"📊 Summary: {summary.get('passed', 0)}/{summary.get('total_rooms', 0)} rooms passed")
            
            return True
        else:
            print(f"❌ Test failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Lighting Compliance Checker System")
    print("=" * 50)
    
    tests = [
        ("Compliance Checker API", test_api_health),
        ("Report Extraction API", test_report_api_health),
        ("Standards Loading", test_standards_loaded),
        ("Sample PDF Test", test_with_sample_pdf)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📋 Test Results Summary:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! System is ready to use.")
        print("🌐 API available at: http://localhost:8000")
        print("📖 API docs at: http://localhost:8000/docs")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("💡 Make sure both APIs are running:")
        print("   1. Run start_report_api.bat (port 5000)")
        print("   2. Run start_api.bat (port 8000)")

if __name__ == "__main__":
    main()

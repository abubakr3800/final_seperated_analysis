"""
Test the complete system - all APIs and web interface
"""

import requests
import json
import time
import webbrowser
from pathlib import Path

def test_report_api():
    """Test the report extraction API"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Report API (port 5000): ONLINE")
            return True
        else:
            print(f"❌ Report API (port 5000): ERROR - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Report API (port 5000): OFFLINE - {e}")
        return False

def test_compliance_api():
    """Test the compliance checker API"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Compliance API (port 8000): ONLINE")
            return True
        else:
            print(f"❌ Compliance API (port 8000): ERROR - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Compliance API (port 8000): OFFLINE - {e}")
        return False

def test_standards():
    """Test if standards are loaded"""
    try:
        response = requests.get("http://localhost:8000/standards-info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            total_standards = data.get('total_standards', 0)
            print(f"✅ Standards: {total_standards} standards loaded")
            return True
        else:
            print(f"❌ Standards: ERROR - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Standards: OFFLINE - {e}")
        return False

def test_web_interface():
    """Test if web interface is accessible"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Web Interface (port 3000): ONLINE")
            return True
        else:
            print(f"❌ Web Interface (port 3000): ERROR - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Web Interface (port 3000): OFFLINE - {e}")
        return False

def test_with_sample_pdf():
    """Test the complete system with a sample PDF"""
    # Look for sample PDFs
    sample_paths = [
        "../report_export/NESSTRA Report With 150 watt.pdf",
        "../standard_export/data/NESSTRA Report With 150 watt.pdf"
    ]
    
    sample_pdf = None
    for path in sample_paths:
        if Path(path).exists():
            sample_pdf = path
            break
    
    if not sample_pdf:
        print("⚠️  No sample PDF found for testing")
        return False
    
    try:
        print(f"🧪 Testing with sample PDF: {sample_pdf}")
        
        with open(sample_pdf, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/check-compliance", files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            compliance = result.get('compliance_result', {}).get('overall_compliance', 'UNKNOWN')
            print(f"✅ End-to-end test successful! Compliance result: {compliance}")
            
            # Print summary
            summary = result.get('compliance_result', {}).get('summary', {})
            if summary:
                print(f"📊 Summary: {summary.get('passed', 0)}/{summary.get('total_rooms', 0)} rooms passed")
            
            return True
        else:
            print(f"❌ End-to-end test failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during end-to-end test: {e}")
        return False

def main():
    """Run complete system test"""
    print("🧪 TESTING COMPLETE LIGHTING COMPLIANCE SYSTEM")
    print("=" * 60)
    
    # Test all components
    tests = [
        ("Report API", test_report_api),
        ("Compliance API", test_compliance_api),
        ("Standards", test_standards),
        ("Web Interface", test_web_interface),
        ("End-to-End Test", test_with_sample_pdf)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # Small delay between tests
    
    print("\n" + "=" * 60)
    print("📋 COMPLETE SYSTEM TEST RESULTS:")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! System is fully operational!")
        print("\n🌐 Access Points:")
        print("   📱 Web Interface: http://localhost:3000")
        print("   📖 API Docs: http://localhost:8000/docs")
        print("   🔧 Report API: http://localhost:5000")
        
        # Try to open the web interface
        try:
            webbrowser.open('http://localhost:3000')
            print("\n🚀 Web interface opened in your browser!")
        except:
            print("\n💡 Please open your browser and go to http://localhost:3000")
            
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n💡 Make sure all services are running:")
        print("   1. Run start_report_api.bat (port 5000)")
        print("   2. Run start_api.bat (port 8000)")
        print("   3. Run start_web_interface.bat (port 3000)")

if __name__ == "__main__":
    main()

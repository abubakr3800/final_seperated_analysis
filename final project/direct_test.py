"""
Direct test to see what's happening with PDF processing
"""

import requests
import json

def test_direct():
    """Direct test of the API"""
    print("🧪 DIRECT API TEST")
    print("=" * 30)
    
    # Test 1: Check if APIs are running
    print("1. Testing API health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"   Compliance API: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Standards loaded: {data.get('components', {}).get('standards_loaded')}")
    except Exception as e:
        print(f"   Compliance API error: {e}")
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        print(f"   Report API: {response.status_code}")
    except Exception as e:
        print(f"   Report API error: {e}")
    
    # Test 2: Try a simple upload
    print("\n2. Testing PDF upload...")
    pdf_path = "../report_export/NESSTRA Report With 150 watt.pdf"
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            print("   Uploading...")
            response = requests.post("http://localhost:8000/check-compliance", files=files, timeout=30)
        
        print(f"   Response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Upload successful!")
            
            # Check what we got
            if 'compliance_result' in result:
                compliance = result['compliance_result']
                print(f"   Overall: {compliance.get('overall_compliance')}")
                print(f"   Checks: {len(compliance.get('checks', []))}")
                
                if compliance.get('checks'):
                    for i, check in enumerate(compliance['checks'][:2]):
                        print(f"     Room {i+1}: {check.get('room')} - {check.get('status')}")
                else:
                    print("   ❌ No room checks found")
            else:
                print("   ❌ No compliance result")
                
        else:
            print(f"   ❌ Upload failed: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Upload error: {e}")

if __name__ == "__main__":
    test_direct()

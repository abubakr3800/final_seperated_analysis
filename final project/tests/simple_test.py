"""
Simple test to upload PDF and see what happens
"""

import requests
import json

def test_upload():
    """Test PDF upload with detailed output"""
    pdf_path = "../report_export/NESSTRA Report With 150 watt.pdf"
    
    print(f"🧪 Testing upload of: {pdf_path}")
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            print("📤 Uploading file...")
            response = requests.post("http://localhost:8000/check-compliance", files=files, timeout=120)
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Upload successful!")
            
            # Print the full response structure
            print("\n📋 Response structure:")
            print(f"Keys in response: {list(result.keys())}")
            
            if 'compliance_result' in result:
                compliance = result['compliance_result']
                print(f"Compliance keys: {list(compliance.keys())}")
                print(f"Overall compliance: {compliance.get('overall_compliance', 'UNKNOWN')}")
                print(f"Number of checks: {len(compliance.get('checks', []))}")
                
                if compliance.get('checks'):
                    print("\n🏠 Room details:")
                    for i, check in enumerate(compliance['checks'][:3]):
                        print(f"  Room {i+1}: {check.get('room', 'Unknown')} - {check.get('status', 'Unknown')}")
            else:
                print("❌ No compliance_result in response")
                
            # Save full response for debugging
            with open('debug_response.json', 'w') as f:
                json.dump(result, f, indent=2)
            print("💾 Full response saved to debug_response.json")
            
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_upload()

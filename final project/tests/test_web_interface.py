"""
Test what the web interface receives from the API
"""

import requests
import json
from pathlib import Path

def test_web_interface_data():
    """Test what data the web interface receives"""
    
    pdf_path = "../report_export/NESSTRA Report With 150 watt.pdf"
    if not Path(pdf_path).exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print("🧪 TESTING WEB INTERFACE DATA")
    print("=" * 50)
    
    # Test the same endpoint the web interface uses
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/check-compliance-detailed", files=files, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response received!")
            
            # Check the structure
            print(f"📋 Response keys: {list(result.keys())}")
            
            if 'compliance_result' in result:
                compliance = result['compliance_result']
                print(f"\n📊 COMPLIANCE RESULT:")
                print(f"   Overall: {compliance.get('overall_compliance', 'UNKNOWN')}")
                print(f"   Checks: {len(compliance.get('checks', []))}")
                
                if compliance.get('checks'):
                    print(f"\n🔍 ROOM CHECKS:")
                    for i, check in enumerate(compliance['checks']):
                        print(f"   Check {i+1}:")
                        print(f"     Room: {check.get('room', 'Unknown')}")
                        print(f"     Status: {check.get('status', 'Unknown')}")
                        print(f"     Profile: {check.get('utilisation_profile', 'Unknown')}")
                        if check.get('standard'):
                            std = check['standard']
                            print(f"     Standard: {std.get('ref_no', 'N/A')} - {std.get('task_or_activity', 'N/A')}")
                        
                        if check.get('checks'):
                            print(f"     Detailed Checks:")
                            for check_type, check_data in check['checks'].items():
                                print(f"       {check_type}: {check_data.get('actual', 'N/A')} / {check_data.get('required', 'N/A')} ({'PASS' if check_data.get('compliant') else 'FAIL'})")
                        else:
                            print(f"     No detailed checks found!")
                else:
                    print("❌ No room checks found!")
                    
                # Check summary
                if compliance.get('summary'):
                    summary = compliance['summary']
                    print(f"\n📈 SUMMARY:")
                    print(f"   Total Rooms: {summary.get('total_rooms', 0)}")
                    print(f"   Passed: {summary.get('passed', 0)}")
                    print(f"   Failed: {summary.get('failed', 0)}")
                    print(f"   Pass Rate: {summary.get('pass_rate', 0)}%")
                else:
                    print("❌ No summary found!")
            
            # Save the full response for debugging
            with open('web_interface_test_result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full response saved to: web_interface_test_result.json")
            
            return True
            
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API request error: {e}")
        return False

if __name__ == "__main__":
    success = test_web_interface_data()
    print("\n" + "=" * 50)
    if success:
        print("🎉 WEB INTERFACE DATA TEST COMPLETED!")
        print("💡 Check the saved JSON file for details")
    else:
        print("❌ WEB INTERFACE DATA TEST FAILED")
"""
Test the compliance fix
"""

import requests
import json
from pathlib import Path

def test_compliance_fix():
    """Test if the compliance fix works"""
    
    pdf_path = "../report_export/NESSTRA Report With 150 watt.pdf"
    if not Path(pdf_path).exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print("🧪 Testing Compliance Fix")
    print("=" * 30)
    
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/check-compliance-detailed", files=files, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            compliance = result.get('compliance_result', {})
            
            print(f"Overall Compliance: {compliance.get('overall_compliance', 'UNKNOWN')}")
            print(f"Checks: {len(compliance.get('checks', []))}")
            
            if compliance.get('checks'):
                print("\n🏠 Room Checks:")
                for i, check in enumerate(compliance['checks']):
                    print(f"   Room {i+1}: {check.get('room', 'Unknown')}")
                    print(f"   Status: {check.get('status', 'Unknown')}")
                    print(f"   Profile: {check.get('utilisation_profile', 'Unknown')}")
                    if check.get('standard'):
                        std = check['standard']
                        print(f"   Standard: {std.get('ref_no', 'N/A')} - {std.get('task_or_activity', 'N/A')}")
            else:
                print("❌ No room checks found")
            
            # Save result for debugging
            with open('test_compliance_result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Result saved to: test_compliance_result.json")
            
            return len(compliance.get('checks', [])) > 0
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_compliance_fix()
    if success:
        print("\n🎉 Compliance fix working! You should now see room checks in the web interface.")
    else:
        print("\n⚠️  Compliance fix needs more work. Check the debug files.")

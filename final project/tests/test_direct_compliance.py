"""
Test the compliance API directly to see what's happening
"""

import requests
import json
from pathlib import Path

def test_direct_compliance():
    """Test the compliance API directly"""
    
    pdf_path = "../report_export/NESSTRA Report With 150 watt.pdf"
    if not Path(pdf_path).exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print("🧪 TESTING COMPLIANCE API DIRECTLY")
    print("=" * 50)
    
    # Test 1: Check API health
    print("1. Testing API health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data.get('status')}")
            print(f"   Standards loaded: {data.get('components', {}).get('standards_loaded')}")
        else:
            print(f"❌ API Health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health error: {e}")
        return False
    
    # Test 2: Test standards info
    print("\n2. Testing standards info...")
    try:
        response = requests.get("http://localhost:8000/standards-info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Standards: {data.get('total_standards', 0)} standards loaded")
        else:
            print(f"❌ Standards info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Standards info error: {e}")
    
    # Test 3: Test PDF upload and compliance
    print("\n3. Testing PDF upload and compliance...")
    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/check-compliance-detailed", files=files, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ PDF upload successful!")
            
            # Check extracted data
            if 'extracted_report_data' in result:
                extracted = result['extracted_report_data']
                print(f"📋 Extracted data keys: {list(extracted.keys())}")
                
                if 'rooms' in extracted:
                    rooms = extracted['rooms']
                    print(f"🏠 Rooms found: {len(rooms)}")
                    for i, room in enumerate(rooms):
                        print(f"   Room {i+1}: {room.get('name', 'Unnamed')}")
                
                if 'scenes' in extracted:
                    scenes = extracted['scenes']
                    print(f"🎬 Scenes found: {len(scenes)}")
                    for i, scene in enumerate(scenes):
                        print(f"   Scene {i+1}: {scene.get('utilisation_profile', 'No profile')}")
            
            # Check compliance result
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
                else:
                    print("❌ No room checks found!")
                    
                    # Debug why no checks
                    if compliance.get('overall_compliance') == 'NO_CHECKS':
                        print("🔍 Debugging NO_CHECKS...")
                        print(f"   Summary: {compliance.get('summary', {})}")
            
            # Save full result for debugging
            with open('direct_test_result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full result saved to: direct_test_result.json")
            
            return len(compliance.get('checks', [])) > 0
            
        else:
            print(f"❌ PDF upload failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ PDF upload error: {e}")
        return False

if __name__ == "__main__":
    success = test_direct_compliance()
    print("\n" + "=" * 50)
    if success:
        print("🎉 COMPLIANCE API IS WORKING!")
        print("💡 The issue might be in the web interface")
    else:
        print("❌ COMPLIANCE API HAS ISSUES")
        print("💡 Check the debug files for details")

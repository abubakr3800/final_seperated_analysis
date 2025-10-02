#!/usr/bin/env python3
"""
Test the fixes for room duplication and uniformity reading
"""

import requests
import json
import time

def test_fixes():
    """Test if the fixes work"""
    
    print("🧪 TESTING FIXES")
    print("=" * 50)
    
    # Wait for APIs to start
    print("⏳ Waiting for APIs to start...")
    time.sleep(8)
    
    # Test Report API
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Report API is running")
        else:
            print(f"❌ Report API health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Report API not accessible: {e}")
        return
    
    # Test Compliance API
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Compliance API is running")
        else:
            print(f"❌ Compliance API health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Compliance API not accessible: {e}")
        return
    
    # Test with a PDF upload
    print("\n📄 Testing PDF upload and compliance check...")
    
    # Use the existing extracted file for testing
    test_file = "../../report_export/output/Al amal factory _Report_extracted.json"
    
    try:
        # Upload the file to Report API
        with open(test_file, 'rb') as f:
            files = {'file': ('test.pdf', f, 'application/pdf')}
            response = requests.post("http://localhost:5000/extract", files=files, timeout=30)
        
        if response.status_code == 200:
            print("✅ PDF upload successful")
            extracted_data = response.json()
            
            # Check uniformity in extracted data
            lighting_setup = extracted_data.get('lighting_setup', {})
            uniformity = lighting_setup.get('uniformity')
            print(f"📊 Extracted uniformity: {uniformity}")
            
            scenes = extracted_data.get('scenes', [])
            print(f"📊 Scenes with uniformity:")
            for i, scene in enumerate(scenes):
                print(f"  Scene {i+1}: {scene.get('uniformity', 'NOT FOUND')}")
            
            # Test compliance check
            print("\n🔍 Testing compliance check...")
            compliance_response = requests.post("http://localhost:8000/check-compliance-detailed", 
                                              files={'file': ('test.pdf', open(test_file, 'rb'), 'application/pdf')}, 
                                              timeout=30)
            
            if compliance_response.status_code == 200:
                compliance_data = compliance_response.json()
                print(f"✅ Compliance check successful")
                print(f"📊 Overall compliance: {compliance_data.get('overall_compliance', 'UNKNOWN')}")
                print(f"📊 Number of checks: {len(compliance_data.get('checks', []))}")
                
                # Check for duplicates
                room_names = [check.get('room', '') for check in compliance_data.get('checks', [])]
                unique_rooms = set(room_names)
                print(f"📊 Unique rooms: {len(unique_rooms)}")
                print(f"📊 Total checks: {len(room_names)}")
                
                if len(unique_rooms) < len(room_names):
                    print("❌ DUPLICATE ROOMS DETECTED!")
                else:
                    print("✅ No duplicate rooms")
                
                # Check uniformity in results
                for i, check in enumerate(compliance_data.get('checks', [])[:3]):  # Show first 3
                    print(f"\nCheck {i+1}:")
                    print(f"  Room: {check.get('room', 'Unknown')}")
                    print(f"  Status: {check.get('status', 'Unknown')}")
                    
                    checks = check.get('checks', {})
                    if 'uniformity' in checks:
                        uniformity_check = checks['uniformity']
                        print(f"  Uniformity: {uniformity_check.get('required', 'N/A')} / {uniformity_check.get('actual', 'N/A')}")
                    else:
                        print(f"  Uniformity: NOT CHECKED")
            else:
                print(f"❌ Compliance check failed: {compliance_response.status_code}")
                print(f"Response: {compliance_response.text}")
        else:
            print(f"❌ PDF upload failed: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_fixes()

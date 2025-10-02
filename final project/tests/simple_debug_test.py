#!/usr/bin/env python3
"""
Simple debug test to see what's happening
"""

import json
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_data_flow():
    """Test the data flow step by step"""
    
    print("🔍 DEBUGGING DATA FLOW")
    print("=" * 50)
    
    # Load the extracted data
    json_path = "../report_export/output/Al amal factory _Report_extracted.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        report_data = json.load(f)
    
    print("📊 EXTRACTED DATA:")
    print(f"Rooms: {len(report_data.get('rooms', []))}")
    for i, room in enumerate(report_data.get('rooms', [])):
        print(f"  Room {i+1}: {room.get('name', 'Unknown')}")
    
    print(f"\nScenes: {len(report_data.get('scenes', []))}")
    for i, scene in enumerate(report_data.get('scenes', [])):
        print(f"  Scene {i+1}: {scene.get('scene_name', 'Unknown')}")
        print(f"    Uniformity: {scene.get('uniformity', 'NOT FOUND')}")
    
    lighting_setup = report_data.get('lighting_setup', {})
    print(f"\nLighting Setup Uniformity: {lighting_setup.get('uniformity', 'NOT FOUND')}")
    
    # Test compliance checker directly
    print("\n🧪 TESTING COMPLIANCE CHECKER:")
    try:
        from compliance_checker import ComplianceChecker
        standards_path = "../standard_export/output/enhanced_standards.json"
        checker = ComplianceChecker(standards_path)
        
        print("✅ Compliance checker imported successfully")
        
        # Test the check_compliance method
        result = checker.check_compliance(report_data)
        
        print(f"Overall Compliance: {result.get('overall_compliance', 'UNKNOWN')}")
        print(f"Number of checks: {len(result.get('checks', []))}")
        
        # Check for duplicates
        room_names = [check.get('room', '') for check in result.get('checks', [])]
        unique_rooms = set(room_names)
        print(f"Unique rooms: {len(unique_rooms)}")
        print(f"Total checks: {len(room_names)}")
        
        if len(unique_rooms) < len(room_names):
            print("❌ DUPLICATE ROOMS DETECTED!")
            print("Room names:")
            for name in room_names:
                print(f"  - {name}")
        else:
            print("✅ No duplicate rooms")
        
        # Check uniformity in first few results
        for i, check in enumerate(result.get('checks', [])[:3]):
            print(f"\nCheck {i+1}:")
            print(f"  Room: {check.get('room', 'Unknown')}")
            print(f"  Status: {check.get('status', 'Unknown')}")
            
            checks = check.get('checks', {})
            if 'uniformity' in checks:
                uniformity_check = checks['uniformity']
                print(f"  Uniformity: {uniformity_check.get('required', 'N/A')} / {uniformity_check.get('actual', 'N/A')}")
            else:
                print(f"  Uniformity: NOT CHECKED")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_data_flow()

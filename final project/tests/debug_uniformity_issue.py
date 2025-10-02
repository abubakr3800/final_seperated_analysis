#!/usr/bin/env python3
"""
Debug uniformity reading issue
"""

import json
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from compliance_checker import ComplianceChecker

def debug_uniformity_issue():
    """Debug why uniformity is not being read"""
    
    print("🔍 DEBUGGING UNIFORMITY ISSUE")
    print("=" * 50)
    
    # Load the extracted data
    json_path = "../../report_export/output/Al amal factory _Report_extracted.json"
    if not os.path.exists(json_path):
        print(f"❌ File not found: {json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        report_data = json.load(f)
    
    print("📊 EXTRACTED DATA ANALYSIS:")
    print(f"Lighting Setup Uniformity: {report_data.get('lighting_setup', {}).get('uniformity', 'NOT FOUND')}")
    
    scenes = report_data.get('scenes', [])
    print(f"Scenes found: {len(scenes)}")
    for i, scene in enumerate(scenes):
        print(f"  Scene {i+1}: {scene.get('scene_name', 'Unknown')}")
        print(f"    Uniformity: {scene.get('uniformity', 'NOT FOUND')}")
        print(f"    Average Lux: {scene.get('average_lux', 'NOT FOUND')}")
        print(f"    Utilisation Profile: {scene.get('utilisation_profile', 'NOT FOUND')}")
    
    rooms = report_data.get('rooms', [])
    print(f"\nRooms found: {len(rooms)}")
    for i, room in enumerate(rooms):
        print(f"  Room {i+1}: {room.get('name', 'Unknown')}")
    
    # Test compliance checker
    print("\n🧪 TESTING COMPLIANCE CHECKER:")
    try:
        checker = ComplianceChecker()
        result = checker.check_compliance(report_data)
        
        print(f"Overall Compliance: {result.get('overall_compliance', 'UNKNOWN')}")
        print(f"Number of checks: {len(result.get('checks', []))}")
        
        for i, check in enumerate(result.get('checks', [])):
            print(f"\nCheck {i+1}:")
            print(f"  Room: {check.get('room', 'Unknown')}")
            print(f"  Status: {check.get('status', 'Unknown')}")
            print(f"  Standard: {check.get('standard', {}).get('ref_no', 'Unknown')}")
            
            checks = check.get('checks', {})
            if 'uniformity' in checks:
                uniformity_check = checks['uniformity']
                print(f"  Uniformity: {uniformity_check.get('required', 'N/A')} / {uniformity_check.get('actual', 'N/A')}")
                print(f"  Uniformity Found: {uniformity_check.get('actual', 'N/A') != 'N/A'}")
            else:
                print(f"  Uniformity: NOT CHECKED")
            
            if 'lux' in checks:
                lux_check = checks['lux']
                print(f"  LUX: {lux_check.get('required', 'N/A')} / {lux_check.get('actual', 'N/A')}")
        
    except Exception as e:
        print(f"❌ Error testing compliance checker: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    debug_uniformity_issue()

#!/usr/bin/env python3
"""
Test uniformity extraction from Report API
"""

import requests
import json
import os

def test_uniformity_extraction():
    """Test if the Report API can extract uniformity values"""
    
    print("🧪 TESTING UNIFORMITY EXTRACTION")
    print("=" * 50)
    
    # Test Report API health
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
    
    # Test with a sample PDF file
    pdf_path = "../../report_export/output/Al amal factory _Report_extracted.json"
    if os.path.exists(pdf_path):
        print(f"📄 Found test file: {pdf_path}")
        
        # Read the extracted data to see what uniformity values are available
        with open(pdf_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("\n📊 EXTRACTED DATA ANALYSIS:")
        print(f"Lighting Setup Uniformity: {data.get('lighting_setup', {}).get('uniformity', 'NOT FOUND')}")
        
        scenes = data.get('scenes', [])
        print(f"Scenes found: {len(scenes)}")
        for i, scene in enumerate(scenes):
            print(f"  Scene {i+1}: {scene.get('scene_name', 'Unknown')}")
            print(f"    Uniformity: {scene.get('uniformity', 'NOT FOUND')}")
            print(f"    Average Lux: {scene.get('average_lux', 'NOT FOUND')}")
        
        rooms = data.get('rooms', [])
        print(f"Rooms found: {len(rooms)}")
        for i, room in enumerate(rooms):
            print(f"  Room {i+1}: {room.get('name', 'Unknown')}")
    else:
        print("❌ No test file found")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_uniformity_extraction()

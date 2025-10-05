#!/usr/bin/env python3
"""
Test Script for Final PDF Extractor API
=======================================

This script tests the updated Report API that now uses the Final PDF Extractor
with alias mapping for improved data extraction.
"""

import requests
import json
import os
import sys
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:5000"
TEST_PDF_PATH = "NESSTRA Report With 150 watt.pdf"  # Adjust path as needed

def test_api_health():
    """Test API health endpoint"""
    print("🔍 Testing API Health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"📊 Extractor: {data['extractor']}")
            print(f"🔢 Version: {data['version']}")
            print(f"🎯 Features: {', '.join(data['features'])}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_api_documentation():
    """Test API documentation endpoint"""
    print("\n📚 Testing API Documentation...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Documentation: {data['message']}")
            print(f"🔢 Version: {data['version']}")
            print(f"🔧 Extractor: {data['extractor']}")
            print(f"🎯 Features: {len(data['features'])} features available")
            return True
        else:
            print(f"❌ Documentation check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Documentation check error: {e}")
        return False

def test_pdf_extraction():
    """Test PDF extraction with Final PDF Extractor"""
    print("\n📄 Testing PDF Extraction...")
    
    # Check if test PDF exists
    if not os.path.exists(TEST_PDF_PATH):
        print(f"⚠️ Test PDF not found: {TEST_PDF_PATH}")
        print("Please provide a valid PDF file path in the script")
        return False
    
    try:
        # Upload and extract PDF
        with open(TEST_PDF_PATH, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{API_BASE_URL}/extract", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ PDF Extraction: {data['message']}")
            print(f"📁 Original File: {data['original_filename']}")
            print(f"🆔 File ID: {data['file_id']}")
            
            # Analyze extracted data
            extracted_data = data['extracted_data']
            print(f"\n📊 Extracted Data Analysis:")
            print(f"  🏢 Company: {extracted_data['metadata']['company_name']}")
            print(f"  📋 Project: {extracted_data['metadata']['project_name']}")
            print(f"  👨‍💼 Engineer: {extracted_data['metadata']['engineer']}")
            print(f"  📧 Email: {extracted_data['metadata']['email']}")
            
            # Lighting setup
            lighting = extracted_data['lighting_setup']
            if lighting:
                print(f"\n💡 Lighting Setup:")
                print(f"  🔢 Fixtures: {lighting.get('number_of_fixtures', 'N/A')}")
                print(f"  🔌 Type: {lighting.get('fixture_type', 'N/A')}")
                print(f"  💡 Average Lux: {lighting.get('average_lux', 'N/A')}")
                print(f"  📐 Uniformity: {lighting.get('uniformity', 'N/A')}")
                print(f"  ⚡ Power: {lighting.get('total_power_w', 'N/A')} W")
                print(f"  🎯 Efficacy: {lighting.get('luminous_efficacy_lm_per_w', 'N/A')} lm/W")
            
            # Luminaires
            luminaires = extracted_data['luminaires']
            print(f"\n🔦 Luminaires: {len(luminaires)} found")
            for i, lum in enumerate(luminaires[:3]):  # Show first 3
                print(f"  {i+1}. {lum.get('manufacturer', 'Unknown')} - {lum.get('article_no', 'Unknown')}")
                print(f"     Quantity: {lum.get('quantity', 'N/A')}, Power: {lum.get('power_w', 'N/A')} W")
            
            # Rooms
            rooms = extracted_data['rooms']
            print(f"\n🏠 Rooms: {len(rooms)} found")
            for i, room in enumerate(rooms[:3]):  # Show first 3
                print(f"  {i+1}. {room['name']}")
                print(f"     Arrangement: {room.get('arrangement', 'N/A')}")
                print(f"     Layout Points: {len(room.get('layout', []))}")
            
            # Scenes
            scenes = extracted_data['scenes']
            print(f"\n🎬 Scenes: {len(scenes)} found")
            for i, scene in enumerate(scenes[:3]):  # Show first 3
                print(f"  {i+1}. {scene.get('scene_name', 'Unknown')}")
                print(f"     Average Lux: {scene.get('average_lux', 'N/A')}")
                print(f"     Uniformity: {scene.get('uniformity', 'N/A')}")
            
            return True
        else:
            print(f"❌ PDF extraction failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ PDF extraction error: {e}")
        return False

def test_file_listing():
    """Test file listing endpoint"""
    print("\n📁 Testing File Listing...")
    try:
        response = requests.get(f"{API_BASE_URL}/files")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ File Listing: {data['count']} files found")
            for file_info in data['files'][:3]:  # Show first 3
                print(f"  📄 {file_info['filename']}")
                print(f"     Size: {file_info['size']} bytes")
                print(f"     Created: {file_info['created']}")
            return True
        else:
            print(f"❌ File listing failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ File listing error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Final PDF Extractor API")
    print("=" * 50)
    
    # Test sequence
    tests = [
        ("API Health", test_api_health),
        ("API Documentation", test_api_documentation),
        ("PDF Extraction", test_pdf_extraction),
        ("File Listing", test_file_listing)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Final PDF Extractor API is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the API server and configuration.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

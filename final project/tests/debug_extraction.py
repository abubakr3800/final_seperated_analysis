"""
Debug tool to see what's being extracted from the PDF
"""

import requests
import json
from pathlib import Path

def debug_pdf_extraction():
    """Debug what's being extracted from the PDF"""
    
    pdf_path = "../report_export/NESSTRA Report With 150 watt.pdf"
    if not Path(pdf_path).exists():
        print(f"❌ PDF not found: {pdf_path}")
        return
    
    print("🔍 DEBUGGING PDF EXTRACTION")
    print("=" * 40)
    print(f"📄 Testing with: {pdf_path}")
    
    try:
        # Step 1: Test direct report extraction
        print("\n1️⃣ Testing Report API extraction...")
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:5000/extract", files=files, timeout=120)
        
        if response.status_code == 200:
            report_data = response.json()['extracted_data']
            print("✅ Report extraction successful!")
            
            # Show what was extracted
            print(f"\n📋 EXTRACTED DATA STRUCTURE:")
            print(f"Keys: {list(report_data.keys())}")
            
            # Show lighting setup
            if 'lighting_setup' in report_data:
                lighting = report_data['lighting_setup']
                print(f"\n💡 LIGHTING SETUP:")
                for key, value in lighting.items():
                    print(f"   {key}: {value}")
            else:
                print("❌ No lighting_setup found")
            
            # Show rooms
            if 'rooms' in report_data:
                rooms = report_data['rooms']
                print(f"\n🏠 ROOMS ({len(rooms)} found):")
                for i, room in enumerate(rooms):
                    print(f"   Room {i+1}:")
                    for key, value in room.items():
                        print(f"     {key}: {value}")
            else:
                print("❌ No rooms found")
            
            # Save extracted data
            with open('debug_extracted_data.json', 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Raw extracted data saved to: debug_extracted_data.json")
            
        else:
            print(f"❌ Report extraction failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        # Step 2: Test compliance checking
        print(f"\n2️⃣ Testing Compliance API...")
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/check-compliance-detailed", files=files, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Compliance check successful!")
            
            compliance = result.get('compliance_result', {})
            print(f"\n📊 COMPLIANCE RESULT:")
            print(f"Overall: {compliance.get('overall_compliance', 'UNKNOWN')}")
            print(f"Checks: {len(compliance.get('checks', []))}")
            
            if compliance.get('checks'):
                print(f"\n🔍 ROOM CHECKS:")
                for i, check in enumerate(compliance['checks']):
                    print(f"   Check {i+1}:")
                    print(f"     Room: {check.get('room', 'Unknown')}")
                    print(f"     Status: {check.get('status', 'Unknown')}")
                    print(f"     Profile: {check.get('utilisation_profile', 'Unknown')}")
            else:
                print("❌ No room checks found")
                
            # Save full result
            with open('debug_compliance_result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full compliance result saved to: debug_compliance_result.json")
            
        else:
            print(f"❌ Compliance check failed: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_pdf_extraction()

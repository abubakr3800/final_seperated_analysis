"""
Test PDF upload and processing
"""

import requests
import os
from pathlib import Path

def find_sample_pdf():
    """Find a sample PDF to test with"""
    sample_paths = [
        "../report_export/NESSTRA Report With 150 watt.pdf",
        "../standard_export/data/NESSTRA Report With 150 watt.pdf"
    ]
    
    for path in sample_paths:
        if Path(path).exists():
            return path
    return None

def test_pdf_upload():
    """Test uploading a PDF and getting compliance results"""
    sample_pdf = find_sample_pdf()
    
    if not sample_pdf:
        print("❌ No sample PDF found")
        return False
    
    print(f"🧪 Testing with PDF: {sample_pdf}")
    
    try:
        with open(sample_pdf, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/check-compliance", files=files, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ PDF upload successful!")
            
            # Check if we got compliance results
            compliance_result = result.get('compliance_result', {})
            if compliance_result:
                overall = compliance_result.get('overall_compliance', 'UNKNOWN')
                checks = compliance_result.get('checks', [])
                summary = compliance_result.get('summary', {})
                
                print(f"📊 Overall Compliance: {overall}")
                print(f"📋 Total Rooms: {summary.get('total_rooms', 0)}")
                print(f"✅ Passed: {summary.get('passed', 0)}")
                print(f"❌ Failed: {summary.get('failed', 0)}")
                print(f"📈 Pass Rate: {summary.get('pass_rate', 0):.1f}%")
                
                if checks:
                    print("\n🏠 Room Details:")
                    for i, check in enumerate(checks[:3]):  # Show first 3 rooms
                        room_name = check.get('room', f'Room {i+1}')
                        status = check.get('status', 'UNKNOWN')
                        profile = check.get('utilisation_profile', 'Unknown')
                        print(f"   {room_name}: {status} ({profile})")
                
                return True
            else:
                print("⚠️  No compliance results found in response")
                return False
        else:
            print(f"❌ Upload failed: Status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return False

def main():
    print("🧪 Testing PDF Upload and Processing")
    print("=" * 40)
    
    # Test the upload
    success = test_pdf_upload()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 PDF processing test successful!")
        print("💡 Your web interface should now show real data")
        print("🌐 Go to http://localhost:3000 to see the results")
    else:
        print("⚠️  PDF processing test failed")
        print("💡 Check if all APIs are running properly")

if __name__ == "__main__":
    main()

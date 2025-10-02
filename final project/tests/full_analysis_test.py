"""
Full analysis test to get complete report analysis and standards comparison
"""

import requests
import json
import time
from pathlib import Path

def test_full_analysis():
    """Test complete PDF analysis and standards comparison"""
    
    # Find sample PDF
    pdf_path = "../report_export/NESSTRA Report With 150 watt.pdf"
    if not Path(pdf_path).exists():
        print(f"❌ PDF not found: {pdf_path}")
        return False
    
    print("🔍 FULL LIGHTING COMPLIANCE ANALYSIS TEST")
    print("=" * 50)
    print(f"📄 Testing with: {pdf_path}")
    
    try:
        # Step 1: Upload PDF and get detailed results
        print("\n📤 Step 1: Uploading PDF for analysis...")
        with open(pdf_path, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/check-compliance-detailed", files=files, timeout=180)
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ PDF analysis successful!")
            
            # Step 2: Show extracted report data
            print("\n📋 Step 2: EXTRACTED REPORT DATA")
            print("-" * 30)
            
            if 'extracted_report_data' in result:
                report_data = result['extracted_report_data']
                print(f"Report structure: {list(report_data.keys())}")
                
                # Show lighting setup
                if 'lighting_setup' in report_data:
                    lighting = report_data['lighting_setup']
                    print(f"\n💡 LIGHTING SETUP:")
                    for key, value in lighting.items():
                        print(f"   {key}: {value}")
                
                # Show rooms
                if 'rooms' in report_data:
                    rooms = report_data['rooms']
                    print(f"\n🏠 ROOMS FOUND: {len(rooms)}")
                    for i, room in enumerate(rooms):
                        print(f"   Room {i+1}: {room.get('name', 'Unknown')}")
                        print(f"     - Utilisation Profile: {room.get('utilisation_profile', 'Unknown')}")
                        print(f"     - Area: {room.get('area', 'Unknown')}")
                        print(f"     - Other data: {list(room.keys())}")
            else:
                print("❌ No extracted report data found")
            
            # Step 3: Show compliance results
            print("\n📊 Step 3: COMPLIANCE ANALYSIS")
            print("-" * 30)
            
            if 'compliance_result' in result:
                compliance = result['compliance_result']
                print(f"Overall Compliance: {compliance.get('overall_compliance', 'UNKNOWN')}")
                
                # Show summary
                if 'summary' in compliance:
                    summary = compliance['summary']
                    print(f"\n📈 SUMMARY:")
                    print(f"   Total Rooms: {summary.get('total_rooms', 0)}")
                    print(f"   Passed: {summary.get('passed', 0)}")
                    print(f"   Failed: {summary.get('failed', 0)}")
                    print(f"   No Standard Found: {summary.get('no_standard_found', 0)}")
                    print(f"   Pass Rate: {summary.get('pass_rate', 0):.1f}%")
                
                # Show detailed checks
                if 'checks' in compliance and compliance['checks']:
                    print(f"\n🔍 DETAILED ROOM CHECKS:")
                    for i, check in enumerate(compliance['checks']):
                        print(f"\n   Room {i+1}: {check.get('room', 'Unknown')}")
                        print(f"   Status: {check.get('status', 'UNKNOWN')}")
                        print(f"   Utilisation Profile: {check.get('utilisation_profile', 'Unknown')}")
                        
                        if 'standard' in check:
                            std = check['standard']
                            print(f"   Matched Standard:")
                            print(f"     - Ref No: {std.get('ref_no', 'Unknown')}")
                            print(f"     - Category: {std.get('category', 'Unknown')}")
                            print(f"     - Task/Activity: {std.get('task_or_activity', 'Unknown')}")
                        
                        if 'checks' in check:
                            print(f"   Compliance Checks:")
                            for check_type, check_data in check['checks'].items():
                                required = check_data.get('required', 0)
                                actual = check_data.get('actual', 0)
                                compliant = check_data.get('compliant', False)
                                margin = check_data.get('margin', 0)
                                
                                status_icon = "✅" if compliant else "❌"
                                print(f"     {status_icon} {check_type.upper()}:")
                                print(f"       Required: {required}")
                                print(f"       Actual: {actual}")
                                print(f"       Margin: {margin}")
                                print(f"       Compliant: {compliant}")
                else:
                    print("❌ No room checks found")
            else:
                print("❌ No compliance results found")
            
            # Save full results
            with open('full_analysis_results.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full analysis saved to: full_analysis_results.json")
            
            return True
            
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return False

def main():
    print("🚀 Starting Full Lighting Compliance Analysis...")
    success = test_full_analysis()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 FULL ANALYSIS COMPLETE!")
        print("📊 You now have complete report analysis and standards comparison")
        print("💾 Check 'full_analysis_results.json' for detailed data")
    else:
        print("⚠️  Analysis failed - check the errors above")

if __name__ == "__main__":
    main()

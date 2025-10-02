"""
Test if standards are being loaded and matched correctly
"""

import json
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from compliance_checker import ComplianceChecker

def test_standards():
    """Test standards loading and matching"""
    
    print("🧪 Testing Standards Loading and Matching")
    print("=" * 50)
    
    # Initialize compliance checker
    standards_path = os.path.join(os.path.dirname(__file__), "..", "standard_export", "output", "complete_standards.json")
    
    try:
        checker = ComplianceChecker(standards_path, "http://localhost:5000")
        print(f"✅ Compliance checker initialized")
        print(f"📁 Standards path: {standards_path}")
        
        # Check if standards are loaded
        if checker.standards_data and 'standards' in checker.standards_data:
            standards = checker.standards_data['standards']
            print(f"📊 Total standards loaded: {len(standards)}")
            
            # Test matching with the utilisation profile from the PDF
            test_profiles = [
                "Health care premises - Operating areas (5.46.1 Pre-op and recovery rooms)",
                "Industrial work",
                "Factory work",
                "General lighting"
            ]
            
            print(f"\n🔍 Testing standard matching:")
            for profile in test_profiles:
                standard = checker.find_matching_standard(profile)
                if standard:
                    print(f"✅ '{profile}' -> {standard.get('ref_no', 'N/A')} - {standard.get('task_or_activity', 'N/A')}")
                else:
                    print(f"❌ '{profile}' -> No match found")
            
            # Show some sample standards
            print(f"\n📋 Sample standards:")
            for i, std in enumerate(standards[:5]):
                print(f"   {i+1}. {std.get('ref_no', 'N/A')} - {std.get('task_or_activity', 'N/A')}")
            
            return True
        else:
            print("❌ No standards loaded")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_standards()

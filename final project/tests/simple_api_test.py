"""
Simple test to start the API and see what happens
"""

import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all imports work"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        import requests
        print("✅ requests imported")
        
        import json
        print("✅ json imported")
        
        from datetime import datetime
        print("✅ datetime imported")
        
        # Test compliance checker import
        from compliance_checker import ComplianceChecker
        print("✅ ComplianceChecker imported")
        
        # Test standards path
        standards_path = os.path.join(os.path.dirname(__file__), "..", "standard_export", "output", "complete_standards.json")
        print(f"Standards path: {standards_path}")
        print(f"Standards file exists: {os.path.exists(standards_path)}")
        
        # Try to initialize compliance checker
        checker = ComplianceChecker(standards_path, "http://localhost:5000")
        print("✅ ComplianceChecker initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()

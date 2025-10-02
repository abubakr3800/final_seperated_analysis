#!/usr/bin/env python3
"""
Test script to verify enhanced standards are being loaded correctly
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.compliance_checker import ComplianceChecker

def test_enhanced_standards():
    print("🧪 TESTING ENHANCED STANDARDS LOADING")
    print("=" * 50)
    
    # Test with enhanced standards
    enhanced_path = os.path.join(os.path.dirname(__file__), "..", "standard_export", "output", "enhanced_standards.json")
    print(f"📁 Enhanced standards path: {enhanced_path}")
    print(f"📁 File exists: {os.path.exists(enhanced_path)}")
    
    try:
        checker = ComplianceChecker(enhanced_path, "http://localhost:5000")
        print(f"✅ Enhanced standards loaded successfully")
        print(f"📊 Standards count: {len(checker.standards_data.get('standards', []))}")
        
        # Show the standards
        for i, standard in enumerate(checker.standards_data.get('standards', [])):
            print(f"  {i+1}. {standard.get('ref_no', 'N/A')} - {standard.get('task_or_activity', 'N/A')}")
            print(f"     LUX: {standard.get('Em_r_lx', 'N/A')} / {standard.get('Em_u_lx', 'N/A')}")
            print(f"     Uniformity: {standard.get('Uo', 'N/A')}")
            print(f"     Ra: {standard.get('Ra', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"❌ Error loading enhanced standards: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_enhanced_standards()

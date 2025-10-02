#!/usr/bin/env python3
"""
Test script to verify standard matching logic
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.compliance_checker import ComplianceChecker

def test_standard_matching():
    print("🧪 TESTING STANDARD MATCHING LOGIC")
    print("=" * 50)
    
    # Test with enhanced standards
    enhanced_path = os.path.join(os.path.dirname(__file__), "..", "standard_export", "output", "enhanced_standards.json")
    checker = ComplianceChecker(enhanced_path, "http://localhost:5000")
    
    # Test different utilisation profiles
    test_profiles = [
        "Industrial work",
        "General assembly work", 
        "General lighting",
        "factory",
        "the factory",
        "Health care premises - Operating areas (5.46.1 Pre-op and recovery rooms)"
    ]
    
    for profile in test_profiles:
        print(f"🔍 Testing profile: '{profile}'")
        standard = checker.find_matching_standard(profile)
        if standard:
            print(f"  ✅ Matched: {standard.get('ref_no', 'N/A')} - {standard.get('task_or_activity', 'N/A')}")
            print(f"     LUX: {standard.get('Em_r_lx', 'N/A')} / {standard.get('Em_u_lx', 'N/A')}")
            print(f"     Uniformity: {standard.get('Uo', 'N/A')}")
            print(f"     Ra: {standard.get('Ra', 'N/A')}")
        else:
            print(f"  ❌ No match found")
        print()
    
    print("=" * 50)

if __name__ == "__main__":
    test_standard_matching()

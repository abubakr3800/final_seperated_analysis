#!/usr/bin/env python3
"""
Test script to test the Al amal factory report directly
"""

import sys
import os
import json
sys.path.append(os.path.dirname(__file__))

from src.compliance_checker import ComplianceChecker

def test_al_amal_report():
    print("🧪 TESTING AL AMAL FACTORY REPORT")
    print("=" * 50)
    
    # Load the extracted report data
    report_path = os.path.join(os.path.dirname(__file__), "..", "report_export", "output", "Al amal factory _Report_extracted.json")
    print(f"📁 Report path: {report_path}")
    print(f"📁 File exists: {os.path.exists(report_path)}")
    
    if not os.path.exists(report_path):
        print("❌ Report file not found!")
        return
    
    # Load the report data
    with open(report_path, 'r', encoding='utf-8') as f:
        report_data = json.load(f)
    
    print(f"📋 Report data keys: {list(report_data.keys())}")
    print(f"🏠 Rooms found: {len(report_data.get('rooms', []))}")
    print(f"🎬 Scenes found: {len(report_data.get('scenes', []))}")
    
    # Show the lighting setup data
    lighting_setup = report_data.get('lighting_setup', {})
    print(f"💡 Lighting setup:")
    print(f"   Average LUX: {lighting_setup.get('average_lux', 'N/A')}")
    print(f"   Uniformity: {lighting_setup.get('uniformity', 'N/A')}")
    
    # Show the scenes data
    scenes = report_data.get('scenes', [])
    for i, scene in enumerate(scenes):
        print(f"🎬 Scene {i+1}:")
        print(f"   Name: {scene.get('scene_name', 'N/A')}")
        print(f"   Average LUX: {scene.get('average_lux', 'N/A')}")
        print(f"   Uniformity: {scene.get('uniformity', 'N/A')}")
        print(f"   Profile: {scene.get('utilisation_profile', 'N/A')}")
    
    # Test compliance checking
    enhanced_path = os.path.join(os.path.dirname(__file__), "..", "standard_export", "output", "enhanced_standards.json")
    checker = ComplianceChecker(enhanced_path, "http://localhost:5000")
    
    print(f"\n🔍 Testing compliance check...")
    result = checker.check_compliance(report_data)
    
    print(f"📊 Compliance Result:")
    print(f"   Overall: {result.get('overall_compliance', 'N/A')}")
    print(f"   Checks: {len(result.get('checks', []))}")
    
    for i, check in enumerate(result.get('checks', [])):
        print(f"   Check {i+1}:")
        print(f"     Room: {check.get('room', 'N/A')}")
        print(f"     Status: {check.get('status', 'N/A')}")
        print(f"     Standard: {check.get('standard', {}).get('ref_no', 'N/A')} - {check.get('standard', {}).get('task_or_activity', 'N/A')}")
        
        # Show the checks
        checks = check.get('checks', {})
        for check_type, check_data in checks.items():
            print(f"     {check_type.upper()}:")
            print(f"       Required: {check_data.get('required', 'N/A')}")
            print(f"       Actual: {check_data.get('actual', 'N/A')}")
            print(f"       Compliant: {check_data.get('compliant', 'N/A')}")
    
    print("=" * 50)

if __name__ == "__main__":
    test_al_amal_report()

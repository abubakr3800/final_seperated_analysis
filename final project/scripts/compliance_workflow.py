#!/usr/bin/env python3
"""
Compliance Workflow Script
==========================

Command-line tool for the complete compliance checking workflow:
1. Extract parameters from PDF report
2. Compare to standards
3. Generate compliance sheet

Usage:
    py scripts/compliance_workflow.py <pdf_file> [--output <output_file>]
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from compliance_checker import ComplianceChecker

# Configuration
STANDARDS_PATH = os.path.join(
    os.path.dirname(__file__), 
    "..", "..", 
    "standard_export", 
    "output", 
    "standards_filtered.json"
)
REPORT_API_URL = "http://localhost:5000"


def extract_report_data(pdf_path: str) -> dict:
    """
    Step 1: Extract parameters from PDF report
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted report data
    """
    print("=" * 60)
    print("STEP 1: EXTRACTING PARAMETERS FROM REPORT")
    print("=" * 60)
    print(f"📄 PDF File: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: PDF file not found: {pdf_path}")
        return None
    
    # Initialize compliance checker
    checker = ComplianceChecker(STANDARDS_PATH, REPORT_API_URL)
    
    # Extract data
    print("🔄 Extracting data from PDF...")
    report_data = checker.extract_report_data(pdf_path)
    
    if not report_data:
        print("❌ Error: Failed to extract report data")
        return None
    
    print("✅ Extraction successful!")
    print(f"   - Company: {report_data.get('metadata', {}).get('company_name', 'N/A')}")
    print(f"   - Project: {report_data.get('metadata', {}).get('project_name', 'N/A')}")
    print(f"   - Rooms: {len(report_data.get('rooms', []))}")
    print(f"   - Scenes: {len(report_data.get('scenes', []))}")
    print(f"   - Average Lux: {report_data.get('lighting_setup', {}).get('average_lux', 'N/A')}")
    print(f"   - Uniformity: {report_data.get('lighting_setup', {}).get('uniformity', 'N/A')}")
    
    return report_data


def compare_to_standards(report_data: dict) -> dict:
    """
    Step 2: Compare extracted data to standards
    
    Args:
        report_data: Extracted report data
        
    Returns:
        Compliance check results
    """
    print("\n" + "=" * 60)
    print("STEP 2: COMPARING TO STANDARDS")
    print("=" * 60)
    
    # Initialize compliance checker
    checker = ComplianceChecker(STANDARDS_PATH, REPORT_API_URL)
    
    # Check compliance
    print("🔄 Comparing against standards...")
    compliance_result = checker.check_compliance(report_data)
    
    if not compliance_result:
        print("❌ Error: Failed to perform compliance check")
        return None
    
    # Display results
    overall = compliance_result.get('overall_compliance', 'UNKNOWN')
    checks = compliance_result.get('checks', [])
    summary = compliance_result.get('summary', {})
    
    print("✅ Comparison complete!")
    print(f"   - Overall Compliance: {overall}")
    print(f"   - Total Rooms Checked: {summary.get('total_rooms', 0)}")
    print(f"   - Passed: {summary.get('passed', 0)}")
    print(f"   - Failed: {summary.get('failed', 0)}")
    print(f"   - No Standard Found: {summary.get('no_standard', 0)}")
    print(f"   - Pass Rate: {summary.get('pass_rate', 0):.1f}%")
    
    # Show room details
    if checks:
        print("\n📋 Room Details:")
        for i, check in enumerate(checks[:5], 1):  # Show first 5
            room = check.get('room', f'Room {i}')
            status = check.get('status', 'UNKNOWN')
            profile = check.get('utilisation_profile', 'Unknown')
            print(f"   {i}. {room}: {status}")
            print(f"      Profile: {profile}")
    
    return compliance_result


def generate_compliance_sheet(report_data: dict, compliance_result: dict, output_file: str = None) -> str:
    """
    Step 3: Generate compliance sheet
    
    Args:
        report_data: Extracted report data
        compliance_result: Compliance check results
        output_file: Output file path (optional)
        
    Returns:
        Path to generated compliance sheet
    """
    print("\n" + "=" * 60)
    print("STEP 3: GENERATING COMPLIANCE SHEET")
    print("=" * 60)
    
    # Generate output filename if not provided
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"compliance_sheet_{timestamp}.json"
    
    # Create output directory if needed
    output_dir = os.path.join(os.path.dirname(__file__), "..", "temp")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)
    
    # Prepare compliance sheet
    compliance_sheet = {
        "generated_at": datetime.now().isoformat(),
        "report_metadata": report_data.get('metadata', {}),
        "lighting_setup": report_data.get('lighting_setup', {}),
        "compliance_summary": {
            "overall_compliance": compliance_result.get('overall_compliance', 'UNKNOWN'),
            "total_rooms": compliance_result.get('summary', {}).get('total_rooms', 0),
            "passed": compliance_result.get('summary', {}).get('passed', 0),
            "failed": compliance_result.get('summary', {}).get('failed', 0),
            "no_standard_found": compliance_result.get('summary', {}).get('no_standard', 0),
            "pass_rate": compliance_result.get('summary', {}).get('pass_rate', 0)
        },
        "room_compliance_details": compliance_result.get('checks', []),
        "full_report_data": report_data,
        "full_compliance_result": compliance_result
    }
    
    # Save to file
    print(f"💾 Saving compliance sheet...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(compliance_sheet, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Compliance sheet generated!")
    print(f"   📄 File: {output_path}")
    print(f"   📊 Size: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    return output_path


def main():
    """Main workflow function"""
    if len(sys.argv) < 2:
        print("Usage: py scripts/compliance_workflow.py <pdf_file> [--output <output_file>]")
        print("\nExample:")
        print("  py scripts/compliance_workflow.py report.pdf")
        print("  py scripts/compliance_workflow.py report.pdf --output my_compliance.json")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_file = None
    
    # Parse output file if provided
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    print("\n" + "=" * 60)
    print("LIGHTING COMPLIANCE CHECKER - WORKFLOW")
    print("=" * 60)
    print(f"📁 Standards: {STANDARDS_PATH}")
    print(f"🔗 Report API: {REPORT_API_URL}")
    print()
    
    try:
        # Step 1: Extract parameters
        report_data = extract_report_data(pdf_path)
        if not report_data:
            print("\n❌ Workflow failed at Step 1")
            sys.exit(1)
        
        # Step 2: Compare to standards
        compliance_result = compare_to_standards(report_data)
        if not compliance_result:
            print("\n❌ Workflow failed at Step 2")
            sys.exit(1)
        
        # Step 3: Generate compliance sheet
        output_path = generate_compliance_sheet(report_data, compliance_result, output_file)
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ WORKFLOW COMPLETE")
        print("=" * 60)
        print(f"📄 Compliance Sheet: {output_path}")
        print(f"📊 Overall Status: {compliance_result.get('overall_compliance', 'UNKNOWN')}")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()


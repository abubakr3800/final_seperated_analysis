#!/usr/bin/env python3
"""
Usage Examples for PDF Report Extractors
========================================

This script demonstrates how to use the PDF extractors with command line arguments.
"""

import os
import sys

def show_usage():
    """Show usage examples for all extractors"""
    print("PDF Report Extractor - Usage Examples")
    print("=" * 50)
    print()
    
    print("1. Layout Enhanced Extractor (Recommended):")
    print("   py layout_enhanced_extractor.py <pdf_file_path>")
    print("   Example: py layout_enhanced_extractor.py \"my_report.pdf\"")
    print()
    
    print("2. Final Extractor:")
    print("   py final_extractor.py <pdf_file_path>")
    print("   Example: py final_extractor.py \"my_report.pdf\"")
    print()
    
    print("3. Enhanced Parser:")
    print("   py enhanced_parser.py <pdf_file_path>")
    print("   Example: py enhanced_parser.py \"my_report.pdf\"")
    print()
    
    print("4. Original PDF Report Extractor:")
    print("   py pdf_report_extractor.py <pdf_file_path>")
    print("   Example: py pdf_report_extractor.py \"my_report.pdf\"")
    print()
    
    print("5. Without arguments (uses default file):")
    print("   py layout_enhanced_extractor.py")
    print("   (Will use 'NESSTRA Report With 150 watt.pdf' as default)")
    print()
    
    print("=" * 50)
    print("All extractors now accept file paths as command line arguments!")
    print("The fixed file path is commented out in the code for easy modification.")

def test_with_current_file():
    """Test with the current PDF file"""
    pdf_file = "NESSTRA Report With 150 watt.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"Error: {pdf_file} not found in current directory")
        return
    
    print(f"Testing with current file: {pdf_file}")
    print("=" * 50)
    
    # Test layout enhanced extractor
    print("Testing Layout Enhanced Extractor...")
    os.system(f'py layout_enhanced_extractor.py "{pdf_file}"')
    
    print("\n" + "=" * 50)
    print("Test completed! Check the output files for results.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_with_current_file()
    else:
        show_usage()

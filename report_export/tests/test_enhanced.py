#!/usr/bin/env python3
"""
Test script for the enhanced parser
"""

import os
import sys

print("Testing Enhanced Parser...")
print("=" * 40)

# Check if PDF exists
pdf_file = "NESSTRA Report With 150 watt.pdf"
if not os.path.exists(pdf_file):
    print(f"ERROR: PDF file not found: {pdf_file}")
    sys.exit(1)

print(f"✓ PDF file found: {pdf_file}")

# Test imports
try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from extractors.enhanced_parser import process_report
    print("✓ Enhanced parser imported successfully")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test processing
try:
    print("Processing PDF...")
    result = process_report(pdf_file)
    print("✓ Processing completed")
    
    # Print results
    print("\nResults:")
    print(f"Company: {result['metadata']['company_name']}")
    print(f"Project: {result['metadata']['project_name']}")
    print(f"Engineer: {result['metadata']['engineer']}")
    print(f"Email: {result['metadata']['email']}")
    print(f"Luminaires: {len(result['luminaires'])}")
    print(f"Rooms: {len(result['rooms'])}")
    print(f"Scenes: {len(result['scenes'])}")
    
    # Save results
    import json
    with open("enhanced_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    print("✓ Results saved to enhanced_output.json")
    
except Exception as e:
    print(f"✗ Processing failed: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed!")

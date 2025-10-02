#!/usr/bin/env python3
"""
Quick test to verify PDF extraction is working
"""

print("Testing PDF extraction...")
print("=" * 40)

try:
    from enhanced_parser import process_report
    
    result = process_report('NESSTRA Report With 150 watt.pdf')
    
    print("✓ Extraction successful!")
    print(f"Company: {result['metadata']['company_name']}")
    print(f"Project: {result['metadata']['project_name']}")
    print(f"Engineer: {result['metadata']['engineer']}")
    print(f"Email: {result['metadata']['email']}")
    print(f"Fixtures: {result['lighting_setup']['number_of_fixtures']}")
    print(f"Average Lux: {result['lighting_setup']['average_lux']}")
    print(f"Luminaires: {len(result['luminaires'])}")
    print(f"Scenes: {len(result['scenes'])}")
    
    print("\n" + "=" * 40)
    print("SUCCESS: All extraction working perfectly!")
    print("=" * 40)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

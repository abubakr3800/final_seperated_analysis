#!/usr/bin/env python3
"""
Test script for layout enhanced extraction
"""

print("Testing Layout Enhanced Extraction...")
print("=" * 50)

try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from extractors.layout_enhanced_extractor import LayoutEnhancedExtractor
    
    extractor = LayoutEnhancedExtractor()
    result = extractor.process_report('NESSTRA Report With 150 watt.pdf')
    
    print("✓ Layout enhanced extraction successful!")
    print(f"Company: {result['metadata']['company_name']}")
    print(f"Project: {result['metadata']['project_name']}")
    print(f"Engineer: {result['metadata']['engineer']}")
    print(f"Email: {result['metadata']['email']}")
    print(f"Fixtures: {result['lighting_setup']['number_of_fixtures']}")
    print(f"Average Lux: {result['lighting_setup']['average_lux']}")
    print(f"Luminaires: {len(result['luminaires'])}")
    print(f"Rooms: {len(result['rooms'])}")
    
    # Show detailed room layout information
    print("\nRoom Layout Details:")
    for i, room in enumerate(result['rooms'], 1):
        print(f"  Room {i}: {room['name']}")
        print(f"    Arrangement: {room['arrangement']}")
        print(f"    Layout points: {len(room['layout'])}")
        if room['layout']:
            for j, coord in enumerate(room['layout'][:5]):  # Show first 5 coordinates
                print(f"      Point {j+1}: X={coord['x_m']}, Y={coord['y_m']}, Z={coord['z_m']}")
            if len(room['layout']) > 5:
                print(f"      ... and {len(room['layout']) - 5} more points")
    
    print(f"Scenes: {len(result['scenes'])}")
    
    # Save results
    import json
    with open("layout_enhanced_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    print("\n✓ Results saved to layout_enhanced_output.json")
    print("=" * 50)
    print("SUCCESS: Layout enhanced extraction working perfectly!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

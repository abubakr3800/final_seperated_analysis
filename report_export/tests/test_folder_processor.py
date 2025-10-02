#!/usr/bin/env python3
"""
Test script for folder processor
"""

print("Testing Folder Processor...")
print("=" * 40)

try:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from batch_processing.process_folder import process_folder
    
    # Test with current directory
    print("Testing with current directory...")
    process_folder(".", "test_output")
    
    print("\n✓ Folder processor test completed!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

#!/usr/bin/env python3
"""
Fix Import Paths Script
======================

This script fixes import paths in all files after the directory reorganization.
"""

import os
import re

def fix_imports_in_file(file_path):
    """Fix import paths in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix common import patterns
        patterns = [
            (r'from layout_enhanced_extractor import', 'from extractors.layout_enhanced_extractor import'),
            (r'from enhanced_parser import', 'from extractors.enhanced_parser import'),
            (r'from final_extractor import', 'from extractors.final_extractor import'),
            (r'from pdf_report_extractor import', 'from extractors.pdf_report_extractor import'),
            (r'from process_folder import', 'from batch_processing.process_folder import'),
            (r'from batch_processor import', 'from batch_processing.batch_processor import'),
            (r'from api_client import', 'from api.api_client import'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed imports in: {file_path}")
            return True
        else:
            print(f"- No changes needed: {file_path}")
            return False
            
    except Exception as e:
        print(f"✗ Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all import paths"""
    print("Fixing Import Paths After Directory Reorganization")
    print("=" * 50)
    
    # Files to check and fix
    files_to_fix = [
        'api/api_client.py',
        'batch_processing/process_folder.py',
        'batch_processing/batch_processor.py',
        'tests/test_layout.py',
        'tests/test_enhanced.py',
        'tests/test_extractor.py',
        'tests/test_folder_processor.py',
        'examples/example_usage.py',
        'examples/usage_examples.py'
    ]
    
    fixed_count = 0
    total_count = len(files_to_fix)
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_imports_in_file(file_path):
                fixed_count += 1
        else:
            print(f"- File not found: {file_path}")
    
    print("\n" + "=" * 50)
    print(f"Import fixing completed!")
    print(f"Files processed: {total_count}")
    print(f"Files fixed: {fixed_count}")
    print("=" * 50)

if __name__ == "__main__":
    main()

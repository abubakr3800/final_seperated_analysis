#!/usr/bin/env python3
"""
Test Organization Script
========================

Test that all files work correctly after the directory reorganization.
"""

import os
import sys

def test_imports():
    """Test that all imports work correctly"""
    print("Testing Import Paths After Reorganization")
    print("=" * 50)
    
    # Test extractor imports
    try:
        sys.path.append('.')
        from extractors.layout_enhanced_extractor import LayoutEnhancedExtractor
        print("✓ Layout Enhanced Extractor import successful")
    except ImportError as e:
        print(f"✗ Layout Enhanced Extractor import failed: {e}")
    
    try:
        from extractors.final_extractor import FinalPDFExtractor
        print("✓ Final Extractor import successful")
    except ImportError as e:
        print(f"✗ Final Extractor import failed: {e}")
    
    try:
        from extractors.enhanced_parser import process_report
        print("✓ Enhanced Parser import successful")
    except ImportError as e:
        print(f"✗ Enhanced Parser import failed: {e}")
    
    try:
        from extractors.pdf_report_extractor import PDFReportExtractor
        print("✓ PDF Report Extractor import successful")
    except ImportError as e:
        print(f"✗ PDF Report Extractor import failed: {e}")
    
    # Test batch processing imports
    try:
        from batch_processing.process_folder import process_folder
        print("✓ Process Folder import successful")
    except ImportError as e:
        print(f"✗ Process Folder import failed: {e}")
    
    try:
        from batch_processing.batch_processor import BatchProcessor
        print("✓ Batch Processor import successful")
    except ImportError as e:
        print(f"✗ Batch Processor import failed: {e}")
    
    # Test API imports
    try:
        from api.api_client import PDFExtractionClient
        print("✓ API Client import successful")
    except ImportError as e:
        print(f"✗ API Client import failed: {e}")

def test_file_structure():
    """Test that all expected files exist"""
    print("\nTesting File Structure")
    print("=" * 30)
    
    expected_files = [
        'extractors/layout_enhanced_extractor.py',
        'extractors/final_extractor.py',
        'extractors/enhanced_parser.py',
        'extractors/pdf_report_extractor.py',
        'api/api_server.py',
        'api/api_client.py',
        'api/api_interface.html',
        'batch_processing/process_folder.py',
        'batch_processing/batch_processor.py',
        'docs/README.md',
        'docs/API_GUIDE.md',
        'docs/QUICK_START.md',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (missing)")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\nMissing files: {len(missing_files)}")
    else:
        print(f"\nAll expected files present!")

def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting Basic Functionality")
    print("=" * 30)
    
    # Test if we can create an extractor
    try:
        from extractors.layout_enhanced_extractor import LayoutEnhancedExtractor
        extractor = LayoutEnhancedExtractor()
        print("✓ Layout Enhanced Extractor can be instantiated")
    except Exception as e:
        print(f"✗ Layout Enhanced Extractor instantiation failed: {e}")
    
    # Test if we can create a batch processor
    try:
        from batch_processing.process_folder import process_folder
        print("✓ Process Folder function can be imported")
    except Exception as e:
        print(f"✗ Process Folder import failed: {e}")
    
    # Test if we can create an API client
    try:
        from api.api_client import PDFExtractionClient
        client = PDFExtractionClient()
        print("✓ API Client can be instantiated")
    except Exception as e:
        print(f"✗ API Client instantiation failed: {e}")

def main():
    """Main test function"""
    print("PDF Report Extractor - Organization Test")
    print("=" * 50)
    
    test_file_structure()
    test_imports()
    test_basic_functionality()
    
    print("\n" + "=" * 50)
    print("Organization test completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()

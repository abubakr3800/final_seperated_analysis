#!/usr/bin/env python3
"""
Debug test script to check if everything is working
"""

print("Starting debug test...")

try:
    import sys
    print(f"Python version: {sys.version}")
    
    import os
    print(f"Current directory: {os.getcwd()}")
    
    pdf_file = "NESSTRA Report With 150 watt.pdf"
    print(f"PDF file exists: {os.path.exists(pdf_file)}")
    
    if os.path.exists(pdf_file):
        print(f"PDF file size: {os.path.getsize(pdf_file)} bytes")
    
    print("Testing imports...")
    
    try:
        import pdfplumber
        print("✓ pdfplumber imported successfully")
    except ImportError as e:
        print(f"✗ pdfplumber import failed: {e}")
    
    try:
        import fitz
        print("✓ PyMuPDF (fitz) imported successfully")
    except ImportError as e:
        print(f"✗ PyMuPDF import failed: {e}")
    
    try:
        from pdf2image import convert_from_path
        print("✓ pdf2image imported successfully")
    except ImportError as e:
        print(f"✗ pdf2image import failed: {e}")
    
    try:
        import pytesseract
        print("✓ pytesseract imported successfully")
    except ImportError as e:
        print(f"✗ pytesseract import failed: {e}")
    
    print("Testing main extractor...")
    
    try:
        from pdf_report_extractor import PDFReportExtractor
        extractor = PDFReportExtractor()
        print("✓ PDFReportExtractor created successfully")
        
        if os.path.exists(pdf_file):
            print("Attempting to extract text...")
            text = extractor.extract_text(pdf_file)
            print(f"Extracted text length: {len(text)} characters")
            if text:
                print(f"First 200 characters: {text[:200]}...")
            else:
                print("No text extracted")
        
    except Exception as e:
        print(f"✗ PDFReportExtractor failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("Debug test completed!")
    
except Exception as e:
    print(f"Critical error: {e}")
    import traceback
    traceback.print_exc()

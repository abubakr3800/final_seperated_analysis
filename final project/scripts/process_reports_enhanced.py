#!/usr/bin/env python3
"""
Process Reports with Enhanced Layout Extractor
==============================================

This script processes PDF reports using the enhanced layout extractor
and saves them to the output folder for use with the compliance checker.
"""

import os
import sys
import json
from pathlib import Path

# Add the report_export directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "report_export"))

from batch_processing.process_folder import process_folder

def main():
    print("🚀 PROCESSING REPORTS WITH ENHANCED LAYOUT EXTRACTOR")
    print("=" * 60)
    
    # Get current directory
    current_dir = os.path.dirname(__file__)
    
    # Define paths
    input_folder = os.path.join(current_dir, "..", "input_pdfs")  # Where your PDF files are
    output_folder = os.path.join(current_dir, "..", "report_export", "output")  # Where to save extracted reports
    
    print(f"📁 Input folder: {input_folder}")
    print(f"📁 Output folder: {output_folder}")
    
    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"❌ Input folder does not exist: {input_folder}")
        print("💡 Please create the input_pdfs folder and add your PDF files there")
        return
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Process the folder
    try:
        process_folder(input_folder, output_folder)
        print("\n✅ Processing completed successfully!")
        print(f"📁 Extracted reports saved to: {output_folder}")
        print("\n💡 You can now use these reports with the compliance checker")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return

if __name__ == "__main__":
    main()

"""
Simple Folder Processor
======================

Processes all PDF files in a folder and saves each report with the same name
in an output folder.
"""

import os
import sys
import json
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from extractors.layout_enhanced_extractor import LayoutEnhancedExtractor


def process_folder(input_folder=".", output_folder="output"):
    """
    Process all PDF files in a folder
    
    Args:
        input_folder: Folder containing PDF files (default: current directory)
        output_folder: Folder to save extracted reports (default: output)
    """
    
    # Convert to Path objects
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Create output folder if it doesn't exist
    output_path.mkdir(exist_ok=True)
    
    # Get all PDF files
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in: {input_path}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    print(f"Input folder: {input_path}")
    print(f"Output folder: {output_path}")
    print("=" * 60)
    
    # Initialize extractor
    extractor = LayoutEnhancedExtractor()
    
    successful = 0
    failed = 0
    results = []
    
    for pdf_file in pdf_files:
        try:
            print(f"Processing: {pdf_file.name}")
            
            # Extract data
            result = extractor.process_report(str(pdf_file))
            
            # Create output filename (same name as PDF but with .json extension)
            output_filename = pdf_file.stem + "_extracted.json"
            output_file_path = output_path / output_filename
            
            # Save results
            with open(output_file_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            
            print(f"✓ Saved: {output_file_path}")
            successful += 1
            results.append({
                "file": pdf_file.name,
                "status": "success",
                "output": str(output_file_path)
            })
            
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {e}")
            failed += 1
            results.append({
                "file": pdf_file.name,
                "status": "failed",
                "error": str(e)
            })
    
    # Save batch summary
    summary = {
        "batch_summary": {
            "total_files": len(pdf_files),
            "successful": successful,
            "failed": failed,
            "input_folder": str(input_path),
            "output_folder": str(output_path)
        },
        "results": results
    }
    
    summary_file = output_path / "batch_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("FOLDER PROCESSING COMPLETED")
    print("=" * 60)
    print(f"Total files: {len(pdf_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Summary saved to: {summary_file}")
    print("=" * 60)


def main():
    """Main function"""
    # Get input folder from command line or use current directory
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
    else:
        input_folder = "."  # Current directory
    
    # Get output folder from command line or use default
    if len(sys.argv) > 2:
        output_folder = sys.argv[2]
    else:
        output_folder = "output"
    
    print("PDF Folder Processor")
    print("=" * 30)
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    print()
    
    # Validate input folder
    if not os.path.exists(input_folder):
        print(f"Error: Input folder does not exist: {input_folder}")
        print("Usage: py process_folder.py [input_folder] [output_folder]")
        return
    
    if not os.path.isdir(input_folder):
        print(f"Error: Input path is not a directory: {input_folder}")
        return
    
    # Process the folder
    process_folder(input_folder, output_folder)


if __name__ == "__main__":
    main()

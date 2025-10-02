"""
Batch PDF Report Processor
=========================

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


class BatchProcessor:
    """Batch processor for multiple PDF files"""
    
    def __init__(self, input_folder=".", output_folder="output"):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.extractor = LayoutEnhancedExtractor()
        
        # Create output folder if it doesn't exist
        self.output_folder.mkdir(exist_ok=True)
    
    def get_pdf_files(self):
        """Get all PDF files from input folder"""
        pdf_files = list(self.input_folder.glob("*.pdf"))
        return pdf_files
    
    def process_single_file(self, pdf_path):
        """Process a single PDF file"""
        try:
            print(f"Processing: {pdf_path.name}")
            
            # Extract data
            result = self.extractor.process_report(str(pdf_path))
            
            # Create output filename (same name as PDF but with .json extension)
            output_filename = pdf_path.stem + "_extracted.json"
            output_path = self.output_folder / output_filename
            
            # Save results
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            
            print(f"✓ Saved: {output_path}")
            return True, str(output_path)
            
        except Exception as e:
            print(f"✗ Error processing {pdf_path.name}: {e}")
            return False, str(e)
    
    def process_all_files(self):
        """Process all PDF files in the input folder"""
        pdf_files = self.get_pdf_files()
        
        if not pdf_files:
            print(f"No PDF files found in: {self.input_folder}")
            return
        
        print(f"Found {len(pdf_files)} PDF files to process")
        print(f"Input folder: {self.input_folder}")
        print(f"Output folder: {self.output_folder}")
        print("=" * 60)
        
        results = []
        successful = 0
        failed = 0
        
        for pdf_file in pdf_files:
            success, result = self.process_single_file(pdf_file)
            results.append({
                "file": pdf_file.name,
                "success": success,
                "result": result
            })
            
            if success:
                successful += 1
            else:
                failed += 1
        
        # Save batch summary
        summary = {
            "batch_processing_summary": {
                "total_files": len(pdf_files),
                "successful": successful,
                "failed": failed,
                "input_folder": str(self.input_folder),
                "output_folder": str(self.output_folder)
            },
            "file_results": results
        }
        
        summary_path = self.output_folder / "batch_summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("BATCH PROCESSING COMPLETED")
        print("=" * 60)
        print(f"Total files: {len(pdf_files)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Summary saved to: {summary_path}")
        print("=" * 60)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch process PDF reports")
    parser.add_argument("input_folder", nargs="?", default=".", 
                       help="Input folder containing PDF files (default: current directory)")
    parser.add_argument("-o", "--output", default="output", 
                       help="Output folder for processed reports (default: output)")
    
    args = parser.parse_args()
    
    # Validate input folder
    input_path = Path(args.input_folder)
    if not input_path.exists():
        print(f"Error: Input folder does not exist: {input_path}")
        return
    
    if not input_path.is_dir():
        print(f"Error: Input path is not a directory: {input_path}")
        return
    
    # Create processor and run
    processor = BatchProcessor(args.input_folder, args.output)
    processor.process_all_files()


if __name__ == "__main__":
    main()

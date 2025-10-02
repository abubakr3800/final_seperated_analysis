"""
Example Usage of PDF Report Extractor
====================================

This script demonstrates various ways to use the PDF Report Extractor
for processing lighting analysis reports.
"""

import os
import json
from extractors.pdf_report_extractor import PDFReportExtractor, ReportData


def example_basic_usage():
    """Basic usage example"""
    print("=" * 60)
    print("BASIC USAGE EXAMPLE")
    print("=" * 60)
    
    # Initialize the extractor
    extractor = PDFReportExtractor()
    
    # Process the PDF report
    pdf_path = "NESSTRA Report With 150 watt.pdf"
    
    if os.path.exists(pdf_path):
        # Extract data
        report_data = extractor.process_report(pdf_path)
        
        # Save to JSON
        extractor.save_to_json(report_data, "basic_output.json")
        
        # Print summary
        print(f"✓ Processed: {pdf_path}")
        print(f"✓ Company: {report_data.metadata.company_name}")
        print(f"✓ Project: {report_data.metadata.project_name}")
        print(f"✓ Output saved to: basic_output.json")
    else:
        print(f"✗ PDF file not found: {pdf_path}")


def example_custom_output():
    """Example with custom output filename"""
    print("\n" + "=" * 60)
    print("CUSTOM OUTPUT EXAMPLE")
    print("=" * 60)
    
    extractor = PDFReportExtractor()
    pdf_path = "NESSTRA Report With 150 watt.pdf"
    
    if os.path.exists(pdf_path):
        report_data = extractor.process_report(pdf_path)
        
        # Custom output filename with timestamp
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"report_extracted_{timestamp}.json"
        
        extractor.save_to_json(report_data, output_file)
        print(f"✓ Custom output saved to: {output_file}")


def example_data_analysis():
    """Example of analyzing extracted data"""
    print("\n" + "=" * 60)
    print("DATA ANALYSIS EXAMPLE")
    print("=" * 60)
    
    extractor = PDFReportExtractor()
    pdf_path = "NESSTRA Report With 150 watt.pdf"
    
    if os.path.exists(pdf_path):
        report_data = extractor.process_report(pdf_path)
        
        # Analyze lighting setup
        if report_data.lighting_setup:
            setup = report_data.lighting_setup
            print("LIGHTING SETUP ANALYSIS:")
            print(f"  • Total fixtures: {setup.number_of_fixtures}")
            print(f"  • Fixture type: {setup.fixture_type}")
            print(f"  • Mounting height: {setup.mounting_height_m}m")
            print(f"  • Average lux: {setup.average_lux}")
            print(f"  • Uniformity: {setup.uniformity}")
            print(f"  • Total power: {setup.total_power_w}W")
            print(f"  • Efficacy: {setup.luminous_efficacy_lm_per_w} lm/W")
        
        # Analyze luminaires
        if report_data.luminaires:
            print(f"\nLUMINAIRE ANALYSIS:")
            for i, luminaire in enumerate(report_data.luminaires, 1):
                print(f"  Luminaire {i}:")
                print(f"    • Manufacturer: {luminaire.manufacturer}")
                print(f"    • Article No: {luminaire.article_no}")
                print(f"    • Power: {luminaire.power_w}W")
                print(f"    • Flux: {luminaire.luminous_flux_lm} lm")
                print(f"    • Efficacy: {luminaire.efficacy_lm_per_w} lm/W")
                print(f"    • Quantity: {luminaire.quantity}")
        
        # Analyze scenes
        if report_data.scenes:
            print(f"\nSCENE ANALYSIS:")
            for i, scene in enumerate(report_data.scenes, 1):
                print(f"  Scene {i}: {scene.scene_name}")
                print(f"    • Average lux: {scene.average_lux}")
                print(f"    • Min lux: {scene.min_lux}")
                print(f"    • Max lux: {scene.max_lux}")
                print(f"    • Uniformity: {scene.uniformity}")


def example_batch_processing():
    """Example of processing multiple PDF files"""
    print("\n" + "=" * 60)
    print("BATCH PROCESSING EXAMPLE")
    print("=" * 60)
    
    # List of PDF files to process
    pdf_files = [
        "NESSTRA Report With 150 watt.pdf",
        # Add more PDF files here
    ]
    
    extractor = PDFReportExtractor()
    results = []
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"Processing: {pdf_file}")
            try:
                report_data = extractor.process_report(pdf_file)
                
                # Create summary
                summary = {
                    "file": pdf_file,
                    "company": report_data.metadata.company_name,
                    "project": report_data.metadata.project_name,
                    "fixtures": report_data.lighting_setup.number_of_fixtures if report_data.lighting_setup else 0,
                    "average_lux": report_data.lighting_setup.average_lux if report_data.lighting_setup else 0
                }
                results.append(summary)
                
                # Save individual output
                output_file = f"batch_{pdf_file.replace('.pdf', '')}.json"
                extractor.save_to_json(report_data, output_file)
                print(f"  ✓ Saved to: {output_file}")
                
            except Exception as e:
                print(f"  ✗ Error processing {pdf_file}: {e}")
        else:
            print(f"✗ File not found: {pdf_file}")
    
    # Save batch summary
    if results:
        with open("batch_summary.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)
        print(f"\n✓ Batch summary saved to: batch_summary.json")


def example_custom_extraction():
    """Example of custom field extraction"""
    print("\n" + "=" * 60)
    print("CUSTOM EXTRACTION EXAMPLE")
    print("=" * 60)
    
    extractor = PDFReportExtractor()
    pdf_path = "NESSTRA Report With 150 watt.pdf"
    
    if os.path.exists(pdf_path):
        # Extract raw text first
        text = extractor.extract_text(pdf_path)
        
        # Custom extraction logic
        import re
        
        # Extract custom fields
        custom_fields = {}
        
        # Look for specific patterns
        patterns = {
            "report_date": r"date[:\-]?\s*(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4})",
            "client_name": r"client[:\-]?\s*([A-Za-z\s]+)",
            "project_code": r"project\s*code[:\-]?\s*([A-Z0-9]+)",
            "total_area": r"total\s*area[:\-]?\s*(\d+\.?\d*)\s*m²"
        }
        
        for field_name, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                custom_fields[field_name] = match.group(1).strip()
        
        print("CUSTOM EXTRACTED FIELDS:")
        for field, value in custom_fields.items():
            print(f"  • {field}: {value}")
        
        # Save custom extraction
        with open("custom_extraction.json", "w", encoding="utf-8") as f:
            json.dump(custom_fields, f, indent=4, ensure_ascii=False)
        print(f"\n✓ Custom extraction saved to: custom_extraction.json")


def main():
    """Run all examples"""
    print("PDF REPORT EXTRACTOR - EXAMPLE USAGE")
    print("=" * 60)
    
    # Run examples
    example_basic_usage()
    example_custom_output()
    example_data_analysis()
    example_batch_processing()
    example_custom_extraction()
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)
    print("Check the generated JSON files for results:")
    print("  • basic_output.json")
    print("  • report_extracted_*.json")
    print("  • batch_summary.json")
    print("  • custom_extraction.json")


if __name__ == "__main__":
    main()

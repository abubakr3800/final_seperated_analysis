#!/usr/bin/env python3
"""
EN 12464-1 Standards Extractor

This script extracts all lighting standards tables from prEN 12464-1.pdf
and converts them into a structured JSON format with consistent schema.

The output JSON follows a fixed schema that can be used for comparison
against project reports.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
import pdfplumber
from pathlib import Path


def clean_cell(cell: Any) -> Optional[str]:
    """Clean and normalize cell content."""
    if cell is None:
        return None
    
    # Convert to string and clean
    cell_str = str(cell).strip()
    if not cell_str or cell_str.lower() in ['', 'none', 'null', '-', 'n/a']:
        return None
    
    # Replace newlines with spaces and normalize whitespace
    cell_str = re.sub(r'\s+', ' ', cell_str.replace('\n', ' '))
    return cell_str


def parse_numeric_value(value: str) -> Optional[float]:
    """Parse numeric values from text, handling various formats."""
    if not value:
        return None
    
    # Remove common units and clean
    value = re.sub(r'[^\d.,\-]', '', str(value))
    if not value:
        return None
    
    # Handle different decimal separators
    value = value.replace(',', '.')
    
    try:
        return float(value)
    except ValueError:
        return None


def extract_table_category(page_text: str) -> Optional[str]:
    """Extract category from table heading."""
    lines = page_text.split('\n')
    for line in lines:
        if line.startswith('Table 6.'):
            # Extract category after the dash
            if '—' in line:
                return line.split('—', 1)[1].strip()
            elif '-' in line:
                return line.split('-', 1)[1].strip()
    return None


def create_standard_record(
    ref_no: str = None,
    category: str = None,
    task_or_activity: str = None,
    Em_r_lx: Any = None,
    Em_u_lx: Any = None,
    Uo: Any = None,
    Ra: Any = None,
    RUGL: Any = None,
    Ez_lx: Any = None,
    Em_wall_lx: Any = None,
    Em_ceiling_lx: Any = None,
    specific_requirements: str = None
) -> Dict[str, Any]:
    """Create a standardized record with the fixed schema."""
    
    # Parse numeric values
    def parse_numeric(val):
        if val is None:
            return None
        cleaned = clean_cell(val)
        if cleaned:
            return parse_numeric_value(cleaned)
        return None
    
    return {
        "ref_no": clean_cell(ref_no),
        "category": clean_cell(category),
        "task_or_activity": clean_cell(task_or_activity),
        "Em_r_lx": parse_numeric(Em_r_lx),
        "Em_u_lx": parse_numeric(Em_u_lx),
        "Uo": parse_numeric(Uo),
        "Ra": parse_numeric(Ra),
        "RUGL": parse_numeric(RUGL),
        "Ez_lx": parse_numeric(Ez_lx),
        "Em_wall_lx": parse_numeric(Em_wall_lx),
        "Em_ceiling_lx": parse_numeric(Em_ceiling_lx),
        "specific_requirements": clean_cell(specific_requirements)
    }


def extract_standards_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """Extract all standards from the PDF file."""
    output = []
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    print(f"Processing PDF: {pdf_path}")
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")
        
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"Processing page {page_num}/{total_pages}")
            
            # Extract text for category detection
            page_text = page.extract_text() or ""
            category = extract_table_category(page_text)
            
            # Extract tables from the page
            tables = page.extract_tables()
            
            if not tables:
                continue
                
            print(f"  Found {len(tables)} table(s) on page {page_num}")
            
            for table_idx, table in enumerate(tables):
                if not table or len(table) < 2:
                    continue
                
                # Skip header row and process data rows
                for row_idx, row in enumerate(table[1:], 1):
                    if not row or len(row) < 2:
                        continue
                    
                    # Create record with available data
                    record = create_standard_record(
                        ref_no=row[0] if len(row) > 0 else None,
                        category=category,
                        task_or_activity=row[1] if len(row) > 1 else None,
                        Em_r_lx=row[2] if len(row) > 2 else None,
                        Em_u_lx=row[3] if len(row) > 3 else None,
                        Uo=row[4] if len(row) > 4 else None,
                        Ra=row[5] if len(row) > 5 else None,
                        RUGL=row[6] if len(row) > 6 else None,
                        Ez_lx=row[7] if len(row) > 7 else None,
                        Em_wall_lx=row[8] if len(row) > 8 else None,
                        Em_ceiling_lx=row[9] if len(row) > 9 else None,
                        specific_requirements=row[10] if len(row) > 10 else None
                    )
                    
                    # Only add records with meaningful data
                    if record["ref_no"] or record["task_or_activity"]:
                        output.append(record)
                        print(f"    Added record: {record['ref_no']} - {record['task_or_activity']}")
    
    print(f"Extraction complete. Total records: {len(output)}")
    return output


def save_standards_json(standards: List[Dict[str, Any]], output_path: str):
    """Save standards to JSON file."""
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(standards, f, ensure_ascii=False, indent=2)
    
    print(f"Standards saved to: {output_path}")


def main():
    """Main execution function."""
    print("Starting EN 12464-1 Standards Extractor...")
    
    # Paths
    pdf_path = "data/prEN 12464-1.pdf"
    output_path = "output/standards.json"
    
    print(f"PDF path: {pdf_path}")
    print(f"Output path: {output_path}")
    
    try:
        # Extract standards
        print("Extracting standards from PDF...")
        standards = extract_standards_from_pdf(pdf_path)
        
        # Save to JSON
        print("Saving standards to JSON...")
        save_standards_json(standards, output_path)
        
        # Print summary
        print("\n" + "="*50)
        print("EXTRACTION SUMMARY")
        print("="*50)
        print(f"Total records extracted: {len(standards)}")
        print(f"Output file: {output_path}")
        
        # Show sample record
        if standards:
            print("\nSample record:")
            print(json.dumps(standards[0], indent=2, ensure_ascii=False))
        else:
            print("No records were extracted!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

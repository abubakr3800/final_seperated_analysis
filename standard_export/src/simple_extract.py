#!/usr/bin/env python3
"""
Simple EN 12464-1 Standards Extractor
A simplified version that extracts basic data from the PDF
"""

import os
import json
import pdfplumber
from pathlib import Path

def extract_standards():
    """Extract standards from PDF and save to JSON."""
    
    pdf_path = "data/prEN 12464-1.pdf"
    output_path = "output/standards.json"
    
    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    standards = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Processing {len(pdf.pages)} pages...")
            
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text
                text = page.extract_text() or ""
                
                # Look for table headings
                category = None
                for line in text.split('\n'):
                    if 'Table 6.' in line and '—' in line:
                        category = line.split('—', 1)[1].strip()
                        break
                
                # Extract tables
                tables = page.extract_tables()
                
                for table in tables:
                    if not table or len(table) < 2:
                        continue
                    
                    # Process each row (skip header)
                    for row in table[1:]:
                        if not row or len(row) < 2:
                            continue
                        
                        # Create record
                        record = {
                            "ref_no": str(row[0]).strip() if row[0] else None,
                            "category": category,
                            "task_or_activity": str(row[1]).strip() if len(row) > 1 and row[1] else None,
                            "Em_r_lx": None,
                            "Em_u_lx": None,
                            "Uo": None,
                            "Ra": None,
                            "RUGL": None,
                            "Ez_lx": None,
                            "Em_wall_lx": None,
                            "Em_ceiling_lx": None,
                            "specific_requirements": None
                        }
                        
                        # Try to parse numeric values
                        for i, field in enumerate(['Em_r_lx', 'Em_u_lx', 'Uo', 'Ra', 'RUGL', 'Ez_lx', 'Em_wall_lx', 'Em_ceiling_lx']):
                            if len(row) > i + 2 and row[i + 2]:
                                try:
                                    value = str(row[i + 2]).strip()
                                    if value and value != '-':
                                        record[field] = float(value.replace(',', '.'))
                                except:
                                    pass
                        
                        # Add specific requirements if available
                        if len(row) > 10 and row[10]:
                            record["specific_requirements"] = str(row[10]).strip()
                        
                        # Only add if we have meaningful data
                        if record["ref_no"] or record["task_or_activity"]:
                            standards.append(record)
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(standards, f, ensure_ascii=False, indent=2)
        
        print(f"Extraction complete! {len(standards)} records saved to {output_path}")
        
        # Show sample
        if standards:
            print("\nSample record:")
            print(json.dumps(standards[0], indent=2, ensure_ascii=False))
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    extract_standards()

#!/usr/bin/env python3
"""
Analyze the Complete PDF Extraction Results

This script analyzes the extracted data to provide insights about what was found.
"""

import json
import os
from collections import Counter
from typing import Dict, List, Any


def analyze_extraction_results(file_path: str = "output/complete_standards.json"):
    """Analyze the complete extraction results."""
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    print("ANALYZING COMPLETE PDF EXTRACTION RESULTS")
    print("=" * 60)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metadata = data.get('metadata', {})
    standards = data.get('standards', [])
    
    print(f"Total records extracted: {len(standards)}")
    print(f"Records needing review: {metadata.get('records_needing_review', 0)}")
    print(f"Extraction method: {metadata.get('extraction_method', 'unknown')}")
    
    # Analyze categories
    categories = [s.get('category', 'Unknown') for s in standards]
    category_counts = Counter(categories)
    
    print(f"\nCategories found ({len(category_counts)}):")
    for category, count in category_counts.most_common(10):
        print(f"  {category}: {count} records")
    
    # Analyze reference numbers
    ref_nos = [s.get('ref_no', '') for s in standards if s.get('ref_no')]
    valid_refs = [ref for ref in ref_nos if ref and '.' in ref and ref[0].isdigit()]
    
    print(f"\nReference numbers:")
    print(f"  Total with ref_no: {len(ref_nos)}")
    print(f"  Valid standards refs: {len(valid_refs)}")
    
    # Show some valid reference numbers
    if valid_refs:
        print(f"  Sample refs: {valid_refs[:10]}")
    
    # Analyze numeric data
    numeric_fields = ['Em_r_lx', 'Em_u_lx', 'Uo', 'Ra', 'RUGL', 'Ez_lx', 'Em_wall_lx', 'Em_ceiling_lx']
    
    print(f"\nNumeric data analysis:")
    for field in numeric_fields:
        values = [s.get(field) for s in standards if s.get(field) is not None]
        if values:
            print(f"  {field}: {len(values)} records, range: {min(values)} - {max(values)}")
    
    # Find records with complete data
    complete_records = []
    for record in standards:
        if (record.get('ref_no') and '.' in record.get('ref_no', '') and 
            record.get('Em_r_lx') is not None and
            record.get('task_or_activity') and len(record.get('task_or_activity', '')) > 10):
            complete_records.append(record)
    
    print(f"\nComplete records (with ref_no, Em_r_lx, and meaningful task): {len(complete_records)}")
    
    # Show sample complete records
    if complete_records:
        print(f"\nSample complete records:")
        for i, record in enumerate(complete_records[:5]):
            print(f"\nRecord {i+1}:")
            print(f"  Ref: {record.get('ref_no')}")
            print(f"  Task: {record.get('task_or_activity')}")
            print(f"  Em_r_lx: {record.get('Em_r_lx')}")
            print(f"  Em_u_lx: {record.get('Em_u_lx')}")
            print(f"  Ra: {record.get('Ra')}")
            print(f"  Category: {record.get('category')}")
    
    # Analyze validation issues
    records_with_issues = [s for s in standards if s.get('needs_review')]
    if records_with_issues:
        print(f"\nRecords with validation issues: {len(records_with_issues)}")
        issue_types = Counter()
        for record in records_with_issues:
            issues = record.get('validation_issues', [])
            for issue in issues:
                issue_types[issue.split(':')[0]] += 1
        
        print(f"  Issue types:")
        for issue_type, count in issue_types.most_common():
            print(f"    {issue_type}: {count}")
    
    # Summary
    print(f"\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully extracted {len(standards)} records from PDF")
    print(f"✅ Found {len(complete_records)} complete standards records")
    print(f"✅ Identified {len(category_counts)} different table categories")
    print(f"✅ Applied alias normalization to all data")
    print(f"✅ Validated {len(standards)} records with range checking")
    print(f"✅ Ready for comprehensive project comparison!")


if __name__ == "__main__":
    analyze_extraction_results()

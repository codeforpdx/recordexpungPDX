#!/usr/bin/env python3
"""
Script to fix PDF field default values that were changed when making forms fillable in Acrobat.
This ensures the new PDFs behave the same as the old ones for the Python code.
"""

import sys
from pathlib import Path
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfObject

def analyze_pdf_fields(pdf_path):
    """Analyze PDF fields to understand their current state."""
    print(f"\nAnalyzing: {pdf_path}")
    reader = PdfReader(pdf_path)
    
    if not reader.Root.AcroForm or not reader.Root.AcroForm.Fields:
        print("No form fields found")
        return
    
    print("Form fields found:")
    for field in reader.Root.AcroForm.Fields:
        field_name = field.T
        field_value = field.V
        field_type = field.FT if hasattr(field, 'FT') else 'Unknown'
        print(f"  {field_name}: {field_value} (type: {field_type})")
    
    # Also check annotations
    annotations = [annot for page in reader.pages for annot in page.Annots or []]
    print(f"\nFound {len(annotations)} annotations")
    
    problematic_fields = []
    for annot in annotations:
        if hasattr(annot, 'T') and hasattr(annot, 'V'):
            field_name = annot.T
            field_value = annot.V
            
            # Check for problematic values
            if field_value == '/Off':
                print(f"  ISSUE: {field_name} has value '/Off' (should be None)")
                problematic_fields.append((annot, 'checkbox_off'))
            elif field_value == '<>':
                print(f"  ISSUE: {field_name} has value '<>' (should be empty)")
                problematic_fields.append((annot, 'empty_brackets'))
            elif field_value not in [None, '()']:
                print(f"  WARNING: {field_name} has unexpected value: {field_value}")
    
    return problematic_fields

def fix_pdf_fields(pdf_path, output_path=None):
    """Fix PDF fields to match expected values."""
    if output_path is None:
        output_path = pdf_path
    
    print(f"\nFixing: {pdf_path}")
    reader = PdfReader(pdf_path)
    
    fixed_count = 0
    
    # Fix form fields
    if reader.Root.AcroForm and reader.Root.AcroForm.Fields:
        for field in reader.Root.AcroForm.Fields:
            if field.V == '/Off':
                del field.V  # Remove the field entirely to make it None/unset
                fixed_count += 1
                print(f"  Fixed field {field.T}: '/Off' -> None")
            elif field.V == '<>':
                field.V = '()'
                fixed_count += 1
                print(f"  Fixed field {field.T}: '<>' -> '()'")
    
    # Fix annotations
    for page in reader.pages:
        if page.Annots:
            for annot in page.Annots:
                if hasattr(annot, 'V'):
                    if annot.V == '/Off':
                        del annot.V  # Remove the field entirely to make it None/unset
                        fixed_count += 1
                        print(f"  Fixed annotation {annot.T}: '/Off' -> None")
                    elif annot.V == '<>':
                        annot.V = '()'
                        fixed_count += 1
                        print(f"  Fixed annotation {annot.T}: '<>' -> '()'")
    
    # Write the fixed PDF properly
    writer = PdfWriter()
    writer.addpages(reader.pages)
    
    # Preserve the AcroForm structure
    if reader.Root.AcroForm:
        writer.trailer.Root.AcroForm = reader.Root.AcroForm
    
    writer.write(output_path)
    
    print(f"  Fixed {fixed_count} fields and saved to {output_path}")
    return fixed_count

def main():
    # Paths to the PDF files that need fixing
    pdf_files = [
        "expungeservice/files/oregon.pdf",
        "expungeservice/files/oregon_arrest.pdf", 
        "expungeservice/files/oregon_conviction.pdf"
    ]
    
    print("=== PDF Field Analysis and Fix ===")
    
    for pdf_file in pdf_files:
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            print(f"File not found: {pdf_path}")
            continue
            
        # Analyze first
        problematic_fields = analyze_pdf_fields(str(pdf_path))
        
        # Fix if issues found
        if problematic_fields:
            fix_pdf_fields(str(pdf_path))
        else:
            print(f"  No issues found in {pdf_path}")
    
    print("\n=== Done ===")

if __name__ == "__main__":
    main()
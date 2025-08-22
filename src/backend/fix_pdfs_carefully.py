#!/usr/bin/env python3
"""
Carefully fix PDF fields without breaking structure
"""

from pathlib import Path
from pdfrw import PdfReader, PdfWriter

def fix_pdf_carefully(pdf_path):
    """Fix PDF fields without breaking structure"""
    print(f"\nFixing: {pdf_path}")
    reader = PdfReader(pdf_path)
    
    fixed_count = 0
    
    # Only fix the checkbox values, leave everything else alone
    if reader.Root.AcroForm and reader.Root.AcroForm.Fields:
        for field in reader.Root.AcroForm.Fields:
            if hasattr(field, 'V') and field.V == '/Off':
                field.V = None
                fixed_count += 1
                print(f"  Fixed field {field.T}: '/Off' -> None")
    
    # Also fix annotations to keep them in sync
    for page in reader.pages:
        if page.Annots:
            for annot in page.Annots:
                if hasattr(annot, 'V') and annot.V == '/Off':
                    annot.V = None
                    fixed_count += 1
                    print(f"  Fixed annotation {annot.T}: '/Off' -> None")
    
    # Write back more carefully
    writer = PdfWriter()
    for page in reader.pages:
        writer.addpage(page)
    
    # Preserve all the form structure exactly
    writer.trailer.Root = reader.Root
    
    writer.write(pdf_path)
    print(f"  Fixed {fixed_count} items in {pdf_path}")

def main():
    pdf_files = [
        "expungeservice/files/oregon.pdf",
        "expungeservice/files/oregon_arrest.pdf", 
        "expungeservice/files/oregon_conviction.pdf"
    ]
    
    for pdf_file in pdf_files:
        fix_pdf_carefully(pdf_file)

if __name__ == "__main__":
    main()
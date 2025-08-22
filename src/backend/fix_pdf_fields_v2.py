#!/usr/bin/env python3
"""
Script to fix PDF field default values to match old PDF behavior.
"""

from pathlib import Path
from pdfrw import PdfReader, PdfWriter

def fix_pdf_fields(pdf_path, output_path=None):
    """Fix PDF fields to match old PDF behavior."""
    if output_path is None:
        output_path = pdf_path
    
    print(f"\nFixing: {pdf_path}")
    reader = PdfReader(pdf_path)
    
    fixed_count = 0
    
    # Fix form fields
    if reader.Root.AcroForm and reader.Root.AcroForm.Fields:
        for field in reader.Root.AcroForm.Fields:
            if hasattr(field, 'V'):
                if field.V == '/Off':
                    field.V = None  # Set to None like old PDFs
                    fixed_count += 1
                    print(f"  Fixed field {field.T}: '/Off' -> None")
                elif field.V == '<>':
                    field.V = '()'  # Change to empty like old PDFs
                    fixed_count += 1
                    print(f"  Fixed field {field.T}: '<>' -> '()'")
                elif field.T == '(Charges list the charges you were arrested or cited for 2)' and field.V == '()':
                    field.V = ''  # New field should be empty string, not ()
                    fixed_count += 1
                    print(f"  Fixed new field {field.T}: '()' -> ''")
    
    # Fix annotations  
    for page in reader.pages:
        if page.Annots:
            for annot in page.Annots:
                if hasattr(annot, 'V'):
                    if annot.V == '/Off':
                        annot.V = None  # Set to None like old PDFs
                        fixed_count += 1
                        print(f"  Fixed annotation {annot.T}: '/Off' -> None")
                    elif annot.V == '<>':
                        annot.V = '()'  # Change to empty like old PDFs
                        fixed_count += 1
                        print(f"  Fixed annotation {annot.T}: '<>' -> '()'")
                    elif annot.T == '(Charges list the charges you were arrested or cited for 2)' and annot.V == '()':
                        annot.V = ''  # New field should be empty string, not ()
                        fixed_count += 1
                        print(f"  Fixed new annotation {annot.T}: '()' -> ''")
    
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
    
    print("=== PDF Field Fix to Match Old PDF Behavior ===")
    
    for pdf_file in pdf_files:
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            print(f"File not found: {pdf_path}")
            continue
            
        fix_pdf_fields(str(pdf_path))
    
    print("\n=== Done ===")

if __name__ == "__main__":
    main()
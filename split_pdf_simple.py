"""
CFA Level 2 PDF Splitter - Simple Version
Splits a textbook PDF into separate PDFs
"""

import os
from pathlib import Path

try:
    import pypdf
except ImportError:
    os.system("pip install pypdf")
    import pypdf


def split_pdf_by_count(pdf_path, num_readings, output_dir=None):
    """
    Split PDF into equal parts

    Args:
        pdf_path: Path to PDF
        num_readings: Number of parts to split into
        output_dir: Output directory
    """
    pdf_path = Path(pdf_path).resolve()

    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_split"

    output_dir.mkdir(exist_ok=True)

    pdf_reader = pypdf.PdfReader(pdf_path)
    total_pages = len(pdf_reader.pages)

    pages_per_reading = total_pages // num_readings
    remainder = total_pages % num_readings

    print("=" * 60)
    print("CFA Level 2 PDF Splitter")
    print("=" * 60)
    print(f"Input: {pdf_path.name}")
    print(f"Total pages: {total_pages}")
    print(f"Splitting into {num_readings} parts")
    print(f"Output: {output_dir}")
    print("=" * 60)
    print()

    start_page = 0
    for i in range(num_readings):
        # Add extra page to first readings if there's remainder
        extra = 1 if i < remainder else 0
        end_page = start_page + pages_per_reading + extra

        # Create PDF
        pdf_writer = pypdf.PdfWriter()
        for page_num in range(start_page, end_page):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        output_path = output_dir / f"Reading_{i+1:02d}.pdf"
        with open(output_path, 'wb') as f:
            pdf_writer.write(f)

        print(f"Reading {i+1}: pages {start_page+1}-{end_page} ({end_page-start_page} pages)")
        start_page = end_page

    print()
    print(f"Done! {num_readings} PDFs created in: {output_dir}")


def split_pdf_by_pages(pdf_path, pages_per_reading, output_dir=None):
    """
    Split PDF by fixed number of pages per reading

    Args:
        pdf_path: Path to PDF
        pages_per_reading: Pages per part
        output_dir: Output directory
    """
    pdf_path = Path(pdf_path).resolve()

    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_split"

    output_dir.mkdir(exist_ok=True)

    pdf_reader = pypdf.PdfReader(pdf_path)
    total_pages = len(pdf_reader.pages)

    print("=" * 60)
    print("CFA Level 2 PDF Splitter")
    print("=" * 60)
    print(f"Input: {pdf_path.name}")
    print(f"Total pages: {total_pages}")
    print(f"Pages per reading: {pages_per_reading}")
    print(f"Output: {output_dir}")
    print("=" * 60)
    print()

    reading_num = 1
    for start_page in range(0, total_pages, pages_per_reading):
        end_page = min(start_page + pages_per_reading, total_pages)

        pdf_writer = pypdf.PdfWriter()
        for page_num in range(start_page, end_page):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        output_path = output_dir / f"Reading_{reading_num:02d}.pdf"
        with open(output_path, 'wb') as f:
            pdf_writer.write(f)

        print(f"Reading {reading_num}: pages {start_page+1}-{end_page} ({end_page-start_page} pages)")
        reading_num += 1

    print()
    print(f"Done! {reading_num-1} PDFs created in: {output_dir}")


def main():
    """Main function"""
    pdf_path = r"C:\Users\Dell\Documents\CFA L2\CFA L2 2025 CBOK& Schweser\Book 1.pdf"

    # Get total pages first
    pdf_reader = pypdf.PdfReader(pdf_path)
    total_pages = len(pdf_reader.pages)

    print("=" * 60)
    print("CFA Level 2 PDF Splitter")
    print("=" * 60)
    print(f"PDF: Book 1.pdf")
    print(f"Total pages: {total_pages}")
    print()
    print("Choose split method:")
    print(f"  1. By number of readings (e.g., {total_pages // 20} readings of ~20 pages each)")
    print(f"  2. By pages per reading (e.g., 20 pages per reading)")
    print()

    choice = input("Enter choice (1 or 2) [1]: ").strip() or "1"

    if choice == "1":
        num = int(input(f"Enter number of readings: "))
        split_pdf_by_count(pdf_path, num)
    else:
        pages = int(input("Enter pages per reading: "))
        split_pdf_by_pages(pdf_path, pages)


if __name__ == "__main__":
    main()

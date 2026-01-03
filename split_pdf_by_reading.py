"""
CFA Level 2 PDF Splitter
Splits a textbook PDF into separate PDFs for each reading/chapter
"""

import os
import re
from pathlib import Path

try:
    import pypdf
except ImportError:
    print("Installing required library: pypdf")
    os.system("pip install pypdf")
    import pypdf


def clean_text(text):
    """Clean extracted text from PDF"""
    if not text:
        return ""
    # Remove null characters and other problematic characters
    text = text.replace('\x00', '')
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    return text


def extract_text_from_page(pdf_reader, page_num):
    """Extract text from a specific page"""
    try:
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        return clean_text(text)
    except:
        return ""


def find_reading_boundaries(pdf_reader, keywords=None):
    """
    Find the start pages of each reading/chapter

    Args:
        pdf_reader: PdfReader object
        keywords: List of keywords that indicate start of a new reading

    Returns:
        List of tuples: (reading_number, start_page, title)
    """
    if keywords is None:
        keywords = ['Reading', 'CHAPTER', 'Chapter', 'LESSON', 'Lesson']

    total_pages = len(pdf_reader.pages)
    boundaries = []

    print(f"Scanning {total_pages} pages for reading boundaries...")
    print(f"Looking for keywords: {keywords}")
    print()

    # Track found readings to avoid duplicates
    found_readings = set()

    for page_num in range(total_pages):
        text = extract_text_from_page(pdf_reader, page_num)

        # Look for reading/chapter markers
        for keyword in keywords:
            # More flexible pattern
            patterns = [
                rf'{keyword}\s+(\d+)[\.::\s]*(.{{0,80}})',
                rf'{keyword}\s+(\d+)',
            ]

            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)

                for match in matches:
                    reading_num = match.group(1)

                    # Skip if we already found this reading
                    key = f"{keyword.lower()}_{reading_num}"
                    if key in found_readings:
                        continue

                    # Get title if available
                    try:
                        title = match.group(2).strip() if len(match.groups()) > 1 else ""
                    except:
                        title = ""

                    # Clean up the title
                    title = re.sub(r'\n+', ' ', title)
                    title = re.sub(r'\s+', ' ', title)
                    title = clean_text(title)
                    title = title[:80]  # Limit length

                    found_readings.add(key)
                    boundaries.append((int(reading_num), page_num, keyword, title))

                    print(f"  Found: {keyword} {reading_num} - {title[:40]}... at page {page_num + 1}")
                    break

    # Sort by reading number
    boundaries.sort(key=lambda x: x[0])

    return boundaries


def split_pdf_by_readings(pdf_path, output_dir=None, keywords=None):
    """
    Split PDF into separate files for each reading

    Args:
        pdf_path: Path to the input PDF
        output_dir: Directory to save split PDFs
        keywords: Keywords to identify reading boundaries
    """
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        return

    # Set output directory
    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_split"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("CFA Level 2 PDF Splitter")
    print("=" * 70)
    print(f"Input file: {pdf_path.name}")
    print(f"Output directory: {output_dir}")
    print()

    # Open PDF
    pdf_reader = pypdf.PdfReader(pdf_path)
    total_pages = len(pdf_reader.pages)

    # Find reading boundaries
    boundaries = find_reading_boundaries(pdf_reader, keywords)

    if not boundaries:
        print("No reading boundaries found with default keywords.")
        print("Trying alternative method...")

        # Try with more specific CFA patterns
        alt_keywords = ['Learning Outcome', 'LEARNING OUTCOME',
                       'INTRODUCTION', 'Introduction',
                       'Topic', 'TOPIC',
                       'Unit', 'UNIT']
        boundaries = find_reading_boundaries(pdf_reader, alt_keywords)

    if len(boundaries) < 2:
        print()
        print("Warning: Could not detect enough reading boundaries automatically.")
        print()
        print("Options:")
        print("1. Try different keywords")
        print("2. Split by fixed page ranges")
        print("3. Manually specify page ranges")
        print()

        choice = input("Choose option [2]: ").strip() or "2"

        if choice == "1":
            custom_keywords = input("Enter keywords (comma-separated): ").strip()
            keywords = [k.strip() for k in custom_keywords.split(',')]
            split_pdf_by_readings(pdf_path, output_dir, keywords)
            return
        elif choice == "2":
            pages_per = int(input("Enter pages per reading: "))
            split_by_fixed_pages(pdf_path, pages_per, output_dir)
            return
        else:
            manual_split(pdf_reader, output_dir)
            return

    print()
    print(f"Found {len(boundaries)} readings")
    print()

    # Split the PDF
    for i, (reading_num, start_page, keyword, title) in enumerate(boundaries):
        # Determine end page
        if i + 1 < len(boundaries):
            end_page = boundaries[i + 1][1]
        else:
            end_page = total_pages

        # Create filename
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)[:40]
        safe_title = re.sub(r'\s+', '_', safe_title)

        if safe_title:
            filename = f"Reading_{reading_num:02d}_{safe_title}.pdf"
        else:
            filename = f"Reading_{reading_num:02d}.pdf"

        output_path = output_dir / filename

        # Create new PDF for this reading
        pdf_writer = pypdf.PdfWriter()
        for page_num in range(start_page, end_page):
            pdf_writer.add_page(pdf_reader.pages[page_num])

        # Save
        with open(output_path, 'wb') as f:
            pdf_writer.write(f)

        pages_in_reading = end_page - start_page
        print(f"  [{reading_num:02d}] {filename} ({pages_in_reading} pages: {start_page+1}-{end_page})")

    print()
    print(f"Done! {len(boundaries)} PDFs created in: {output_dir}")


def split_by_fixed_pages(pdf_path, pages_per_reading, output_dir=None):
    """Split PDF by fixed number of pages per reading"""
    pdf_path = Path(pdf_path).resolve()

    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_split"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)

    pdf_reader = pypdf.PdfReader(pdf_path)
    total_pages = len(pdf_reader.pages)

    print()
    print(f"Splitting {total_pages} pages into chunks of {pages_per_reading} pages...")
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

        print(f"  Created: Reading_{reading_num:02d}.pdf (pages {start_page+1}-{end_page})")
        reading_num += 1

    print()
    print(f"Done! {reading_num-1} PDFs created in: {output_dir}")


def manual_split(pdf_reader, output_dir):
    """Manually specify page ranges for each reading"""
    total_pages = len(pdf_reader.pages)
    print()
    print(f"PDF has {total_pages} pages")
    print("Enter page ranges for each reading (format: start-end)")
    print("Enter 'q' when done")
    print()

    reading_num = 1
    while True:
        page_range = input(f"Reading {reading_num} page range (or 'q' to finish): ").strip()

        if page_range.lower() == 'q':
            break

        try:
            if '-' in page_range:
                start, end = page_range.split('-')
                start_page = int(start.strip()) - 1  # Convert to 0-indexed
                end_page = int(end.strip())
            else:
                start_page = int(page_range) - 1
                # Ask for end page or use next reading start
                end_input = input(f"  End page for reading {reading_num}: ").strip()
                end_page = int(end_input) if end_input else start_page + 50

            end_page = min(end_page, total_pages)

            # Create PDF
            pdf_writer = pypdf.PdfWriter()
            for page_num in range(start_page, end_page):
                pdf_writer.add_page(pdf_reader.pages[page_num])

            output_path = output_dir / f"Reading_{reading_num:02d}.pdf"
            with open(output_path, 'wb') as f:
                pdf_writer.write(f)

            print(f"  Created: Reading_{reading_num:02d}.pdf (pages {start_page+1}-{end_page})")
            reading_num += 1

        except Exception as e:
            print(f"  Error: {e}")
            print("  Please try again")

    print()
    print(f"Done! {reading_num-1} PDFs created in: {output_dir}")


def main():
    """Main function"""
    import sys

    pdf_path = r"C:\Users\Dell\Documents\CFA L2\CFA L2 2025 CBOK& Schweser\Book 1.pdf"

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]

    split_pdf_by_readings(pdf_path)


if __name__ == "__main__":
    main()

# generate_statement.py — cleaned version with formatted values and nan handling
import argparse
import pandas as pd
import numpy as np
import os
import tempfile
import shutil
from jinja2 import Environment, FileSystemLoader
from PyPDF2 import PdfReader, PdfWriter

def clean_currency(x):
    try:
        f = float(x)
        if pd.isna(f):
            return ""
        return f"{f:,.2f}"
    except:
        return ""

def main():
    parser = argparse.ArgumentParser(description="Render statement HTML and optionally generate PDF")
    parser.add_argument('--input', required=True, help="CSV file with transaction data")
    parser.add_argument('--output', required=True, help="Output PDF or HTML file")
    parser.add_argument('--fonts-dir', default='../fonts/', help="Directory containing font files")
    args = parser.parse_args()

    header = {
        'name': "Your Name",
        'address_lines': ["111 Main St", "Ojai, CA 11111"],
        'account_number': "12345678910000",
        'statement_open': "April 1, 2025",
        'statement_close': "April 30, 2025",
        'customer_care': "support@taekus.com",
        'customer_phone': "(866) 282-3587",
        'beginning_balance': "200",
        'total_credits': "100.00",
        'total_debits': "100.00",
        'ending_balance': "200.00"
    }

    # Load and clean CSV
    df = pd.read_csv(args.input)
    for col in ["Credits", "Debit", "Balance"]:
        df[col] = df[col].apply(clean_currency)
    df["Type"] = df["Type"].replace("nan", "").fillna("")
    df["Description"] = df["Description"].replace("nan", "").fillna("")
    df["Posted_Date"] = df["Posted Date"].fillna("")

    # Render HTML
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("statement.html.j2")
    html = template.render(header=header, rows=df.to_dict(orient="records"))

    # Save HTML for inspection
    if args.output.endswith(".html"):
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\u2713 HTML written to {args.output}")
        return

    # Create temp directory for HTML and fonts
    temp_dir = tempfile.mkdtemp(dir=os.getcwd())
    temp_html = os.path.join(temp_dir, "statement.html")
    
    # Copy fonts and logo to temp directory
    font_regular = os.path.join(args.fonts_dir, "MonumentGrotesk-Regular.otf")
    font_bold = os.path.join(args.fonts_dir, "MonumentGrotesk-Bold.otf")
    logo_file = os.path.join(os.getcwd(), "logo.svg")
    
    if os.path.exists(font_regular):
        shutil.copy2(font_regular, temp_dir)
    if os.path.exists(font_bold):
        shutil.copy2(font_bold, temp_dir)
    if os.path.exists(logo_file):
        shutil.copy2(logo_file, temp_dir)
        
    # Save temp HTML
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html)
    
    # Run wkhtmltopdf
    print("Converting HTML to PDF...")
    import subprocess
    try:
        # Use specific paper size and margins to match original.pdf
        result = subprocess.run([
            "wkhtmltopdf",
            "--enable-local-file-access",
            "--allow", temp_dir,
            "--disable-javascript",
            "--load-error-handling", "ignore",
            "--page-size", "A4",
            "--margin-top", "0",
            "--margin-bottom", "0",
            "--margin-left", "0",
            "--margin-right", "0",
            temp_html, args.output
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Inject metadata
            reader = PdfReader(args.output)
            writer = PdfWriter()
            writer.append_pages_from_reader(reader)
            writer.append(os.path.join(os.getcwd(), "lastPageTaekus.pdf"))
            # Set PDF version to 1.4
            writer._header = b"%PDF-1.4"
            writer.add_metadata({
                '/Title': 'Taekus Account Statement',
                '/Creator': 'wkhtmltopdf 0.12.4',
                '/Producer': 'Qt 4.8.7',
                '/CreationDate': "D:20250503054520-05'00'"
            })
            with open(args.output, 'wb') as out_f:
                writer.write(out_f)
            print(f"\u2713 PDF written to {args.output}")
        else:
            print(f"Error: wkhtmltopdf failed: {result.stderr}")
            print("Saving HTML instead...")
            # Save HTML as the output file if PDF generation fails
            shutil.copy2(temp_html, args.output)
            print(f"\u2713 HTML written to {args.output} (wkhtmltopdf not available)")
    except FileNotFoundError:
        print("Error: wkhtmltopdf not found. Install with:\n  - Mac: brew install wkhtmltopdf\n  - Windows: Download from https://wkhtmltopdf.org/downloads.html\n  - Linux: apt-get install wkhtmltopdf")
        print("Saving HTML instead...")
        # Save HTML as the output file if wkhtmltopdf is not available
        shutil.copy2(temp_html, args.output)
        print(f"\u2713 HTML written to {args.output} (wkhtmltopdf not available)")
    # Clean up temp directory
    shutil.rmtree(temp_dir)

if __name__ == '__main__':
    main()

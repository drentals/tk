# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains a statement generation system that creates bank statements in HTML or PDF format from CSV transaction data. The main components are:

1. `generate_statement.py` - Main Python script that processes CSV data and generates the statement
2. `statement.html.j2` - Jinja2 HTML template for the statement appearance
3. `statement.csv` - Sample CSV data for testing

## Commands

### Running the Statement Generator

Generate HTML statement:
```bash
python generate_statement.py --input statement.csv --output statement.html
```

Generate PDF statement:
```bash
python generate_statement.py --input statement.csv --output statement.pdf
```

## Requirements

- Python 3.6+
- Required Python packages:
  - pandas
  - numpy
  - jinja2
  - PyPDF2
- wkhtmltopdf (for PDF generation)

## Project Architecture

The system follows a simple workflow:

1. Load transaction data from a CSV file
2. Clean and format the data (e.g., currency formatting, handling NaN values)
3. Render an HTML statement using Jinja2 templating
4. (Optional) Convert the HTML to PDF using wkhtmltopdf
5. Inject metadata into the PDF file

The header information (customer details, account number, etc.) is currently hardcoded in the `generate_statement.py` script.

## CSV Format

The input CSV must have these columns:
- Posted Date
- Description
- Type
- Credits
- Debit
- Balance
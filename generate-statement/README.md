# Statement Generator

This generates statements in HTML or PDF format from CSV transaction data.

## Components

1. **generate_statement.py** - Main Python script that processes CSV data and generates the statement
2. **statement.html.j2** - Jinja2 HTML template that defines the appearance of the statement
3. **statement.csv** - Sample CSV data with transaction information

## Requirements

- Python 3.6+
- Required Python packages:
  - pandas
  - numpy
  - jinja2
  - PyPDF2
- wkhtmltopdf (for PDF generation)

## Installation

1. Install required Python packages:
   ```
   pip install pandas numpy jinja2 PyPDF2
   ```

2. Install wkhtmltopdf:
   - Windows: Download and install from https://wkhtmltopdf.org/downloads.html
   - Mac: `brew install wkhtmltopdf`
   - Linux: `apt-get install wkhtmltopdf` or equivalent for your distribution

## Usage

### Generate HTML Statement

```
python generate_statement.py --input statement.csv --output statement.html
```

### Generate PDF Statement

```
python generate_statement.py --input statement.csv --output statement.pdf
```

## CSV Format

The input CSV must have the following columns:
- Posted Date
- Description
- Type
- Credits
- Debit
- Balance

## Customization

Update generate_statement.py with your name and account information.

To customize the appearance of the statement, edit the `statement.html.j2` file. This is a Jinja2 template that determines the structure and styling of the statement.

The header information (customer details, account number, etc.) is currently hardcoded in the `generate_statement.py` script. You'll need to modify this to read from a separate file or pass as arguments if you want to change these details.

## Example

The included `statement.csv` contains sample transaction data that demonstrates the formatting and structure expected by the generator.

## Issues and TODOs

- Header layout is off. Specifically the vertical alignment of Account Number, Statement Period, and Customer Care Information
- Account Number, Statement Period, and Customer Care need to be right aligned
- Logo is too small
- Once HTML layout is correct, need to work on PDF metadata


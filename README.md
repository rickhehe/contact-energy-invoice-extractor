# Contact Energy Invoice Extractor

I wanted to know some insights about my Contact Energy invoices, so I created this project to automate the extraction and processing of billing data from PDF invoices.

This project extracts and processes data from Contact Energy PDF invoices, converting them into structured CSV files for analysis and reporting.

## Overview

The Contact Energy Invoice Extractor automates the extraction of important billing information from Contact Energy PDF invoices. It parses various data elements such as:

- Basic invoice information (dates, customer numbers)
- Energy usage details (imported and exported)
- Daily charges
- Variable charges
- Broadband and fibre charges
- No-charge items

The extracted data is organized into pandas DataFrames and exported as CSV files for easy analysis and record-keeping.

## Project Structure

```plaintext
contact-energy-invoice-extractor/
│
├── data/
│   ├── raw/                # Raw PDF invoice files (excluded from git)
│   │   └── .gitkeep        # Placeholder to maintain directory in git
│   ├── processed/          # Generated CSV output files
│   └── README.md           # Data folder description
│
├── scripts/                # Scripts for setup and running the project
│   └── run.ps1             # PowerShell script to run the project
│
├── src/                    # Source code (Python)
│   ├── app.py              # Alternative application logic
│   ├── main.py             # Main entry point and processing logic
│   ├── extractor.py        # PDF extraction and regex parsing functions
│   └── __pycache__/        # Python bytecode cache (excluded from git)
│
├── .gitignore              # Git ignore configuration
├── requirements.txt        # Project dependencies
└── README.md               # Project description
```

## Installation

1. Clone the repository:

   ```bash
   git clone [repository URL]
   cd contact-energy-invoice-extractor
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
   - Linux/macOS: `source .venv/bin/activate`

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your Contact Energy PDF invoice files in the `data/raw/` directory.
   - Supported filename format: *YYYY-contactbill.pdf (e.g., 23-Dec-2024-ContactBill.pdf)

2. Run the project using the provided PowerShell script:

   ```powershell
   .\scripts\run.ps1
   ```
   
   Or run the main module directly:

   ```bash
   python -m src.main
   ```

3. The processed data will be saved as CSV files in the `data/processed/` directory:
   - `stg_contact_bill_basics.csv` - Basic invoice information
   - `stg_contact_bill_daily_charges.csv` - Daily charges
   - `stg_contact_bill_variable_charged.csv` - Variable charges
   - `stg_contact_bill_fibre.csv` - Fibre charges
   - `stg_contact_bill_exported.csv` - Exported energy details
   - `stg_contact_bill_no_charge.csv` - No-charge items

## Key Features

- **Robust PDF Text Extraction**: Extracts text from multi-page PDFs.
- **Pattern Recognition**: Uses regular expressions to identify and extract specific data points.
- **Structured Data Output**: Converts unstructured PDF data into organized DataFrames.
- **Error Handling**: Gracefully handles parsing errors without crashing.
- **Date Normalization**: Converts date strings to standardized format (YYYYMMDD).
- **Nested Data Support**: Properly handles nested data structures (lists of items within invoices).

## Dependencies

- Python 3.x
- pandas (>= 2.0.0)
- PyPDF2 (>= 3.0.0)

## Development Guidelines

- All code uses snake_case for consistency.
- Use virtual environment for isolation.
- Add new test cases in the appropriate test directory.
- Follow PEP 8 style guidelines.

## License

MIT License (MIT)

---

Feel free to update this file with more project-specific details.

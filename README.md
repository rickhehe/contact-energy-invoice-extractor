# Contact Energy Invoice Extractor

A Python tool to automatically extract, process, and analyze billing data from Contact Energy PDF invoices, generating structured CSV files for reporting and insights.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Overview

The Contact Energy Invoice Extractor transforms unstructured data from your electricity and broadband invoices into organized, analyzable datasets. This tool addresses the challenge of manually tracking energy consumption, costs, and patterns across multiple billing periods.

The tool parses various invoice elements including:

- Basic invoice information (dates, customer numbers, invoice numbers)
- Energy consumption details (imported, free, exported units)
- Daily charges with different rate periods
- Variable charges for different pricing components
- Broadband and fibre service charges

> **Note:** Tariff charges are not currently covered in the extraction process. This is a planned feature for future releases.

All CSV files are organized by billing aspect rather than by individual invoice. For example, every exported energy detail from all invoices is consolidated into a single CSV file dedicated to exported information. This structure makes it easy to analyze trends, totals, and patterns across all invoices for each category—such as energy usage, costs, and service charges—streamlining comprehensive reporting and insights. The resulting CSV files are ready for use in visualization or business intelligence platforms, enabling deeper analysis and data-driven decision making.


## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PowerShell (for Windows users)

### Installation and Use

```powershell
# Clone the repository
git clone https://github.com/rickhehe/contact-energy-invoice-extractor.git
cd contact-energy-invoice-extractor

> **Note:** The steps for setting up the virtual environment and installing dependencies are automated in `scripts/run.ps1`. You do not need to run them manually.

# Drop your Contact Energy PDFs into the data/raw folder
# Simply drag and drop your PDF invoices into this folder

# Run the extractor
.\scripts\run.ps1

# Find your results in data/processed folder
explorer .\data\processed
```

## 📂 File Processing

### How to Provide Input

1. **Drag-and-Drop Simplicity**: Place your Contact Energy PDF invoices into the `data/raw/` folder.
2. **Filename Pattern**: Invoices should use the default Contact Energy format: `*202Y-ContactBill.pdf` (e.g., `23-Dec-2024-ContactBill.pdf`).  
   *You can customize the filename matching by editing the `PATH_PATTERN` regex in `main.py` to suit your own naming scheme.*
3. **Automatic Discovery**: The extractor scans `data/raw/` and all subfolders, automatically finding and processing every valid invoice PDF.

### Output: Structured CSV Files

Processed invoice data is organized into distinct CSV files within the `data/processed/` directory. Each file corresponds to a specific billing aspect, making analysis straightforward:

- `stg_contact_bill_basics.csv` — Essential invoice details (dates, customer numbers, invoice totals)
- `stg_contact_bill_daily_charges.csv` — Daily charges, including rate periods and day counts
- `stg_contact_bill_variable_charged.csv` — Variable charges based on energy consumption (price converted from cents to dollars)
- `stg_contact_bill_fibre.csv` — Broadband and fibre service charges
- `stg_contact_bill_exported.csv` — Credits for exported energy (e.g., solar generation)
- `stg_contact_bill_no_charge.csv` — Allocations of free energy

CSV files are only generated for applicable topics found in your invoices; if a category is not present, its file will not be created. This ensures your output remains relevant and clutter-free.

## ✨ Key Features

- **Multi-Component Invoice Handling**: Extracts and separately processes different charge types from the same invoice, including support for multiple prices for the same item within a single invoice (e.g., price changes or hikes over time)
- **Category-Specific CSV Files**: Outputs specialized CSV files for each aspect of your bill for targeted analysis
- **Robust Pattern Recognition**: Uses advanced regular expressions to accurately identify and extract data points
- **Error Resilience**: Gracefully handles parsing challenges without failing
- **Date Standardization**: Converts various date formats to consistent YYYYMMDD format for easy sorting and analysis
- **Unit Conversion**: Automatically converts price units from cents to dollars for variable charges
- **Structured Data Model**: Converts unstructured PDF content into normalized, relational data tables
- **Multi-Invoice Processing**: Batch processes multiple invoices in a single run

## 📁 Project Structure

```plaintext
contact-energy-invoice-extractor/
│
├── data/
│   ├── raw/                # Place your PDF invoices here
│   └── processed/          # Generated CSV output files appear here
│
├── scripts/
│   └── run.ps1             # PowerShell script for easy execution
│
├── src/                    # Source code
│   ├── main.py             # Primary entry point and processing logic
│   └── extractor.py        # PDF extraction and regex parsing functions
│
├── .gitignore              # Git ignore configuration
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## 🔮 Roadmap

Future enhancements planned for this project:

- **Energy Usage Forecasting**: Predict future usage patterns and costs
- **Bash support**: Add a Bash script identical to `run.ps1` for Linux users

## 📄 License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

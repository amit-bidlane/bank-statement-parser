# Bank Statement Parser

A complete end-to-end Python project to parse bank statement PDFs, extract and automatically categorize transactions, store them in a local SQLite database using SQLAlchemy, and generate visual analytics.

## Features
- **PDF Parsing**: Extracts transactions (date, description, amount, type) from bank statements using regex and pdfplumber.
- **Auto Categorization**: Rule-based categorization for Food, Shopping, Transport, Bills, Salary, Transfer, etc.
- **Database**: Normalized SQLite schema using SQLAlchemy ORM.
- **Analytics**: Monthly summaries, spending trends, category breakdown using Pandas.
- **Visualizations**: Bar charts, pie charts, and line graphs saved to `reports/` using Matplotlib and Seaborn.
- **CLI Interface**: Simple terminal commands to use the tool.

## Requirements
- Python 3.11+
- dependencies from `requirements.txt`

## Setup Instructions

1. **Clone or download the repository**.
2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   # On macOS/Linux:
   source venv/bin/activate  
   # On Windows:
   venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Use the `main.py` entrypoint via the command line interface.

**1. Import a bank statement PDF:**
```bash
python main.py import path/to/statement.pdf
```
*(This will initialize the database `data/bank_statements.db` if it doesn't exist, parse the PDF, identify duplicate transactions, and store them securely).*

**2. Show overall financial summary:**
```bash
python main.py summary
```

**3. Show monthly report:**
```bash
python main.py monthly-report 2025-01
```

**4. Generate visualizations:**
```bash
python main.py plot
```
*(Charts will be saved inside the `reports/` directory: bar chart for income vs expense, pie chart for expenses by category, and line graph for savings over time).*

## Notes
- **Extensibility**: The keyword rules for auto-categorization can be extended within `categorizer.py`.
- **Parsing Flexibility**: The `TRANSACTION_PATTERN` located in `parser.py` is written to capture standard Date -> Description -> Amount -> Balance lines. Different bank formats might occasionally require pattern adjustments.



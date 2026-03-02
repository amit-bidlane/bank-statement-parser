import pdfplumber
import re
from datetime import datetime
from categorizer import categorize_transaction
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Sample Regex Pattern for transactions
# Looks for typical format: Date Description Amount [Amount] [Balance]
TRANSACTION_PATTERN = re.compile(
    r'^(?P<date>\d{2}[-/]\d{2}[-/]\d{4})\s+'       # Date: DD/MM/YYYY or DD-MM-YYYY
    r'(?P<desc>.+?)\s+'                             # Description: Any text until amount
    r'(?P<amount1>[\d,]+\.\d{2})\s*'                # First amount
    r'(?P<amount2>[\d,]+\.\d{2})?\s*'               # Second optional amount
    r'(?P<balance>[\d,]+\.\d{2})?$'                 # Balance
)

def parse_date(date_str: str):
    """Parses date string to datetime.date object."""
    try:
        if '-' in date_str:
            return datetime.strptime(date_str, '%d-%m-%Y').date()
        else:
            return datetime.strptime(date_str, '%d/%m/%Y').date()
    except ValueError:
        return None

def parse_pdf(file_path: str):
    """
    Parses a PDF bank statement and returns a list of dictionaries with extracted transaction data.
    """
    transactions = []
    
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue
                    
                lines = text.split('\n')
                for line in lines:
                    match = TRANSACTION_PATTERN.match(line.strip())
                    if match:
                        date_str = match.group('date')
                        desc = match.group('desc').strip()
                        amount1_str = match.group('amount1').replace(',', '')
                        amount2_str = match.group('amount2')
                        
                        date_obj = parse_date(date_str)
                        if not date_obj:
                            continue
                        
                        amount1 = float(amount1_str)
                        
                        # Simplified debit/credit logic based on typical single-column or keyword formats
                        if amount2_str:
                            # Typically means we explicitly have both debit and credit columns, 
                            # but only one of them will be purely filled on a per transaction line 
                            # if it's not a balance. We rely on keywords for robustness if heuristic fails.
                            amount2 = float(amount2_str.replace(',', ''))
                            if match.group('balance'):
                                # Standard 3 column format: Debit, Credit, Balance
                                if amount1 > 0:
                                    trans_type = 'debit'
                                    amount = amount1
                                else:
                                    trans_type = 'credit'
                                    amount = amount2
                            else:
                                trans_type = 'credit' if 'salary' in desc.lower() else 'debit'
                                amount = amount1
                        else:
                            # Only one amount column
                            if '-' in amount1_str or 'dr' in line.lower() or 'debited' in desc.lower():
                                trans_type = 'debit'
                            elif 'cr' in line.lower() or 'credited' in desc.lower():
                                trans_type = 'credit'
                            else:
                                trans_type = 'debit' # Default assumption
                            amount = amount1
                        
                        category = categorize_transaction(desc)
                        
                        transactions.append({
                            'date': date_obj,
                            'description': desc,
                            'amount': amount,
                            'type': trans_type,
                            'category': category
                        })
    except Exception as e:
        logging.error(f"Failed to parse PDF {file_path}: {e}")
        
    return transactions

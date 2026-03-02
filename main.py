
import argparse
from datetime import datetime
from database import init_db, get_session
from models import Transaction, Account
from parser import parse_pdf
from analytics import get_all_transactions, get_monthly_transactions, calculate_summary, category_expenses
from plots import generate_all_plots

def setup():
    """Initializes the database and underlying structure."""
    init_db()

def import_pdf(file_path):
    """Imports transactions from a PDF file."""
    setup()
    print(f"Importing {file_path}...")
    
    transactions_data = parse_pdf(file_path)
    if not transactions_data:
        print("No transactions found or failed to parse.")
        return
        
    session = get_session()
    
    # Create a default account if not exists
    account = session.query(Account).first()
    if not account:
        account = Account(bank_name="Default Bank", account_number="0000000000")
        session.add(account)
        session.commit()
        
    added_count = 0
    duplicate_count = 0
    
    for t_data in transactions_data:
        # Check for duplicates based on date, description, and amount
        existing = session.query(Transaction).filter_by(
            date=t_data['date'],
            description=t_data['description'],
            amount=t_data['amount'],
            account_id=account.id
        ).first()
        
        if existing:
            duplicate_count += 1
            continue
            
        transaction = Transaction(
            date=t_data['date'],
            description=t_data['description'],
            amount=t_data['amount'],
            type=t_data['type'],
            category=t_data['category'],
            account_id=account.id
        )
        session.add(transaction)
        added_count += 1
        
    session.commit()
    session.close()
    print(f"Import complete. Added {added_count} new transactions. Skipped {duplicate_count} duplicates.")


def show_summary():
    """Shows an overall summary of transactions."""
    setup()
    df = get_all_transactions()
    if df.empty:
        print("No transactions found in database.")
        return
        
    summary = calculate_summary(df)
    
    print("\n--- Overall Financial Summary ---")
    print(f"Total Income:   Rs.{summary['total_income']:.2f}")
    print(f"Total Expenses: Rs.{summary['total_expenses']:.2f}")
    print(f"Net Savings:    Rs.{summary['savings']:.2f}")
    print("-" * 33)


def monthly_report(month_str):
    """Shows a report for a specific month (YYYY-MM)."""
    setup()
    try:
        dt = datetime.strptime(month_str, "%Y-%m")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM.")
        return
        
    df = get_monthly_transactions(dt.year, dt.month)
    if df.empty:
        print(f"No transactions found for {month_str}.")
        return
        
    summary = calculate_summary(df)
    
    print(f"\n--- Monthly Report ({month_str}) ---")
    print(f"Total Income:   Rs.{summary['total_income']:.2f}")
    print(f"Total Expenses: Rs.{summary['total_expenses']:.2f}")
    print(f"Net Savings:    Rs.{summary['savings']:.2f}")
    print("\nExpenses by Category:")
    
    expenses = category_expenses(df)
    for category, amount in expenses.items():
        print(f"  - {category}: Rs.{amount:.2f}")
    print("-" * 33)


def generate_plots():
    """Generates visual plots from the transactions."""
    setup()
    df = get_all_transactions()
    if df.empty:
        print("No transactions found to plot.")
        return
        
    print("Generating plots...")
    generate_all_plots(df)
    print("Plots generated successfully in the 'reports' directory.")


def main():
    parser = argparse.ArgumentParser(description="Bank Statement Parser CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Import command
    import_parser = subparsers.add_parser("import", help="Import a bank statement PDF")
    import_parser.add_argument("file", help="Path to the PDF file")
    
    # Summary command
    subparsers.add_parser("summary", help="Show overall financial summary")
    
    # Monthly report command
    monthly_parser = subparsers.add_parser("monthly-report", help="Show report for a specific month")
    monthly_parser.add_argument("month", help="Month in YYYY-MM format")
    
    # Plot command
    subparsers.add_parser("plot", help="Generate visualizations")
    
    args = parser.parse_args()
    
    if args.command == "import":
        import_pdf(args.file)
    elif args.command == "summary":
        show_summary()
    elif args.command == "monthly-report":
        monthly_report(args.month)
    elif args.command == "plot":
        generate_plots()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

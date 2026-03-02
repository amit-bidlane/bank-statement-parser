import pandas as pd
from database import get_session
from models import Transaction
from sqlalchemy import extract

def get_monthly_transactions(year: int, month: int):
    """Fetches transactions for a given year and month and returns them as a pandas DataFrame."""
    session = get_session()
    transactions = session.query(Transaction).filter(
        extract('year', Transaction.date) == year,
        extract('month', Transaction.date) == month
    ).all()
    session.close()
    
    # Convert to pandas DataFrame for easy analysis
    data = [{
        'date': t.date,
        'description': t.description,
        'amount': t.amount,
        'type': t.type,
        'category': t.category
    } for t in transactions]
    
    if not data:
        return pd.DataFrame(columns=['date', 'description', 'amount', 'type', 'category'])
        
    return pd.DataFrame(data)

def get_all_transactions():
    """Fetches all transactions and returns them as a pandas DataFrame."""
    session = get_session()
    transactions = session.query(Transaction).all()
    session.close()
    
    data = [{
        'date': t.date,
        'description': t.description,
        'amount': t.amount,
        'type': t.type,
        'category': t.category
    } for t in transactions]
    
    # Return empty DataFrame with columns if no data
    if not data:
        return pd.DataFrame(columns=['date', 'description', 'amount', 'type', 'category'])
        
    return pd.DataFrame(data)

def calculate_summary(df: pd.DataFrame) -> dict:
    """Calculates total income, expenses, and savings from a DataFrame of transactions."""
    if df.empty:
        return {'total_income': 0, 'total_expenses': 0, 'savings': 0}
        
    income = df[df['type'] == 'credit']['amount'].sum()
    expenses = df[df['type'] == 'debit']['amount'].sum()
    savings = income - expenses
    
    return {
        'total_income': income,
        'total_expenses': expenses,
        'savings': savings
    }

def category_expenses(df: pd.DataFrame) -> pd.Series:
    """Groups expenses by category and returns the sums."""
    if df.empty:
        return pd.Series(dtype=float)
    expenses = df[df['type'] == 'debit']
    return expenses.groupby('category')['amount'].sum()

def monthly_trend_data(df: pd.DataFrame):
    """Aggregates transactions by month_year to show income, expense, and savings trends."""
    if df.empty:
        return pd.DataFrame()
        
    # Ensure date is datetime
    df['date'] = pd.to_datetime(df['date'])
    df['month_year'] = df['date'].dt.to_period('M')
    
    monthly_data = df.groupby(['month_year', 'type'])['amount'].sum().unstack(fill_value=0)
    
    # Ensure both debit and credit columns exist
    if 'credit' not in monthly_data.columns:
        monthly_data['credit'] = 0.0
    if 'debit' not in monthly_data.columns:
        monthly_data['debit'] = 0.0
        
    monthly_data['savings'] = monthly_data['credit'] - monthly_data['debit']
    return monthly_data

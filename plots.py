import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from analytics import category_expenses, monthly_trend_data

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_monthly_spending_bar_chart(df: pd.DataFrame, file_prefix: str = "monthly"):
    """Generates and saves a bar chart comparing income and expenses per month."""
    if df.empty:
        print("No data available for bar chart.")
        return
        
    trend_df = monthly_trend_data(df)
    if trend_df.empty:
        return
        
    plt.figure(figsize=(10, 6))
    
    # Convert index to strings for plotting
    months = trend_df.index.astype(str)
    
    x = range(len(months))
    width = 0.35
    
    plt.bar([i - width/2 for i in x], trend_df['credit'], width, label='Income (Credit)', color='green')
    plt.bar([i + width/2 for i in x], trend_df['debit'], width, label='Expenses (Debit)', color='red')
    
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.title('Monthly Income vs Expenses')
    plt.xticks(x, months, rotation=45)
    plt.legend()
    plt.tight_layout()
    
    filepath = os.path.join(REPORTS_DIR, f"{file_prefix}_bar_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"Saved bar chart to {filepath}")


def generate_category_pie_chart(df: pd.DataFrame, file_prefix: str = "expenses"):
    """Generates and saves a pie chart of expenses by category."""
    expenses = category_expenses(df)
    if expenses.empty or expenses.sum() == 0:
        print("No expense data available for pie chart.")
        return
        
    plt.figure(figsize=(8, 8))
    plt.pie(expenses, labels=expenses.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    plt.title('Expense by Category')
    plt.tight_layout()
    
    filepath = os.path.join(REPORTS_DIR, f"{file_prefix}_pie_chart.png")
    plt.savefig(filepath)
    plt.close()
    print(f"Saved pie chart to {filepath}")


def generate_savings_trend_line_graph(df: pd.DataFrame, file_prefix: str = "savings"):
    """Generates and saves a line graph reflecting savings over time."""
    if df.empty:
        print("No data available for savings trend.")
        return
        
    trend_df = monthly_trend_data(df)
    if trend_df.empty:
        return
        
    plt.figure(figsize=(10, 6))
    
    # Convert index to strings for plotting
    months = trend_df.index.astype(str)
    
    plt.plot(months, trend_df['savings'], marker='o', linestyle='-', color='blue', linewidth=2)
    
    plt.xlabel('Month')
    plt.ylabel('Savings Amount')
    plt.title('Savings Trend Over Time')
    plt.xticks(rotation=45)
    plt.axhline(0, color='black', linewidth=1, linestyle='--') # Add line for 0 savings
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    filepath = os.path.join(REPORTS_DIR, f"{file_prefix}_trend.png")
    plt.savefig(filepath)
    plt.close()
    print(f"Saved trend graph to {filepath}")

def generate_all_plots(df: pd.DataFrame, prefix: str = "all"):
    """Generates all the requested plots for the given dataframe."""
    generate_monthly_spending_bar_chart(df, prefix)
    generate_category_pie_chart(df, prefix)
    generate_savings_trend_line_graph(df, prefix)

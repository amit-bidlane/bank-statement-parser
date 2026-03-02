import re

def categorize_transaction(description: str) -> str:
    """
    Categorizes a transaction based on keyword rules.
    """
    desc_lower = description.lower()

    rules = {
        'Food': ['swiggy', 'zomato', 'restaurant', 'cafe', 'mcdonalds', 'kfc', 'starbucks', 'dominos'],
        'Shopping': ['amazon', 'flipkart', 'myntra', 'ajio', 'meesho', 'reliancedigital'],
        'Transport': ['uber', 'ola', 'fuel', 'petrol', 'irctc', 'makemytrip', 'redbus', 'metro'],
        'Bills': ['electricity', 'recharge', 'broadband', 'airtel', 'jio', 'vi', 'bescom', 'water'],
        'Salary': ['salary', 'credited by'],
        'Transfer': ['upi', 'imps', 'neft', 'rtgs']
    }

    for category, keywords in rules.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', desc_lower):
                return category

    return 'Others'

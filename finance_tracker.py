import json
import os
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    \"\"\"Loads transactions from the JSON file.\"\"\"
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    \"\"\"Saves transactions to the JSON file.\"\"\"
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")

def add_transaction(transactions):\
    \"\"\"Adds a new transaction.\"\"\"\
    print("\\n--- Add Transaction ---")

    while True:
        type_input = input("Type (income/expense): ").lower()
        if type_input in ["income", "expense"]:\
            break
        print("Invalid type. Please enter 'income' or 'expense'.")

    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    description = input("Description: ")
    category = input("Category (e.g., Food, Transport, Salary): ")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transaction = {
        "type": type_input,
        "amount": amount,
        "description": description,
        "category": category,
        "date": date
    }

    transactions.append(transaction)
    save_data(transactions)
    print("Transaction added successfully!")

def view_transactions(transactions):
    \"\"\"Lists all transactions.\"\"\"\
    print("\\n--- All Transactions ---")
    if not transactions:
        print("No transactions found.")
        return

    print(f"{\'Date\':<20} | {\'Type\':<10} | {\'Category\':<15} | {\'Amount\':<10} | {\'Description\'}")
    print("-" * 80)
    for t in transactions:
        print(f"{t['date']:<20} | {t['type']:<10} | {t.get('category', 'N/A'):<15} | {t['amount']:<10.2f} | {t['description']}")

def view_summary(transactions):
    \"\"\"Displays financial summary.\"\"\"\
    print("\\n--- Financial Summary ---")
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expense

    print(f"Total Income:   ${total_income:.2f}")
    print(f"Total Expense:  ${total_expense:.2f}")
    print(f"Net Balance:    ${balance:.2f}")

    print("\\n--- Summary by Category ---")
    categories = {}
    for t in transactions:
        category = t.get('category', 'Uncategorized')
        if category not in categories:
            categories[category] = {'income': 0, 'expense': 0}
        
        if t['type'] == 'income':
            categories[category]['income'] += t['amount']
        else:
            categories[category]['expense'] += t['amount']
    
    print(f"{\'Category\':<20} | {\'Income\':<10} | {\'Expense\':<10} | {\'Net\'}")
    print("-" * 55)
    for category, amounts in categories.items():
        cat_income = amounts['income']
        cat_expense = amounts['expense']
        cat_net = cat_income - cat_expense
        print(f"{category:<20} | {cat_income:<10.2f} | {cat_expense:<10.2f} | {cat_net:<10.2f}")


def main():
    transactions = load_data()

    while True:
        print("\\n=== Personal Finance Tracker ===")\
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. View Summary")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            add_transaction(transactions)
        elif choice == '2':
            view_transactions(transactions)
        elif choice == '3':
            view_summary(transactions)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

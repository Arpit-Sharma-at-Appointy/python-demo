import json
import os
import csv
from datetime import datetime
from collections import defaultdict

DATA_FILE = "data.json"

def load_data():
    """Loads transactions from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    """Saves transactions to the JSON file."""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data: {e}")

def add_transaction(transactions):
    """Adds a new transaction."""
    print("\n--- Add Transaction ---")
    
    while True:
        type_input = input("Type (income/expense): ").lower()
        if type_input in ["income", "expense"]:
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
    """Lists all transactions."""
    print("\n--- All Transactions ---")
    if not transactions:
        print("No transactions found.")
        return

    print(f"{'Date':<20} | {'Type':<10} | {'Amount':<10} | {'Category':<15} | {'Description'}")
    print("-" * 80)
    for t in transactions:
        print(f"{t['date']:<20} | {t['type']:<10} | {t['amount']:<10.2f} | {t.get('category', 'N/A'):<15} | {t['description']}")

def view_summary(transactions):
    """Displays financial summary."""
    print("\n--- Financial Summary ---")
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = total_income - total_expense

    print(f"Total Income:   ${total_income:.2f}")
    print(f"Total Expense:  ${total_expense:.2f}")
    print(f"Net Balance:    ${balance:.2f}")

    print("\n--- Expenses by Category ---")
    expenses_by_category = defaultdict(float)
    for t in transactions:
        if t['type'] == 'expense':
            expenses_by_category[t.get('category', 'Uncategorized')] += t['amount']

    if not expenses_by_category:
        print("No expenses to categorize.")
    else:
        for category, total in expenses_by_category.items():
            print(f"{category:<20}: ${total:.2f}")

def export_to_csv(transactions):
    """Exports transactions to a CSV file."""
    print("\n--- Export to CSV ---")
    if not transactions:
        print("No transactions to export.")
        return
    
    filename = input("Enter filename for CSV export (e.g., transactions.csv): ")
    if not filename.endswith('.csv'):
        filename += '.csv'
        
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['Date', 'Type', 'Amount', 'Category', 'Description'])
            # Write data
            for t in transactions:
                writer.writerow([t['date'], t['type'], t['amount'], t.get('category', 'N/A'), t['description']])
        print(f"Transactions successfully exported to {filename}")
    except (IOError, PermissionError) as e:
        print(f"Error exporting to CSV: {e}")


def main():
    transactions = load_data()

    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. View Summary")
        print("4. Export to CSV")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_transaction(transactions)
        elif choice == '2':
            view_transactions(transactions)
        elif choice == '3':
            view_summary(transactions)
        elif choice == '4':
            export_to_csv(transactions)
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

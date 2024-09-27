import pandas as pd
import matplotlib.pyplot as plt

# 1. Initialize an empty DataFrame to store transactions (income/expense)
transactions = pd.DataFrame(columns=['Date', 'Type', 'Category', 'Amount', 'Description'])


# 2. Function to add income
def add_income():
    amount = float(input("Enter the income amount: "))
    date = input("Enter the date (YYYY-MM-DD): ")
    description = input("Optional: Enter a description for this income (press Enter to skip): ")

    # Append income to the transactions DataFrame
    transactions.loc[len(transactions)] = [date, 'Income', 'N/A', amount, description]
    print(f"Income of {amount} added successfully!\n")


# 3. Function to add expense
def add_expense():
    amount = float(input("Enter the expense amount: "))
    date = input("Enter the date (YYYY-MM-DD): ")
    category = input("Enter the expense category (e.g., groceries, rent): ")
    description = input("Optional: Enter a description for this expense (press Enter to skip): ")

    # Append expense to the transactions DataFrame
    transactions.loc[len(transactions)] = [date, 'Expense', category, amount, description]
    print(f"Expense of {amount} for {category} added successfully!\n")


# 4. Function to generate reports (e.g., total income, total expense)
def generate_report():
    income = transactions[transactions['Type'] == 'Income']['Amount'].sum()
    expenses = transactions[transactions['Type'] == 'Expense']['Amount'].sum()
    savings = income - expenses
    print(f"Total Income: {income}")
    print(f"Total Expenses: {expenses}")
    print(f"Savings: {savings}")
    return income, expenses, savings


# 5. Function to visualize spending by category
def visualize_expenses():
    expenses_by_category = transactions[transactions['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
    if not expenses_by_category.empty:
        expenses_by_category.plot(kind='bar')
        plt.title('Expenses by Category')
        plt.ylabel('Amount')
        plt.show()
    else:
        print("No expenses to visualize.")


# 6. Save/Load data to CSV (optional)
def save_to_csv(filename):
    transactions.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def load_from_csv(filename):
    global transactions
    transactions = pd.read_csv(filename)
    print(f"Data loaded from {filename}")

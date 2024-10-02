import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

# connect to sqlite dbase (create if not exist)
conn = sqlite3.connect('finance.db')
c = conn.cursor()

# Create transactions table (if it doens't exist)
def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT,
                      type TEXT,
                      category TEXT,
                      amount REAL,
                      description TEXT)''')
    conn.commit()

# Function to add income
def add_income():
    amount = float(input("Enter the income amount: "))
    date = input("Enter the date (YYYY-MM-DD): ")
    description = input("Optional: Enter a description for this income (press Enter to skip): ")

    # Append income to the transactions DataFrame
    # transactions.loc[len(transactions)] = [date, 'Income', 'N/A', amount, description]
    c.execute("INSERT INTO transactions (date, type, category, amount, description) VALUES (?, 'Income', 'N/A', ?, ?)",
              (date, amount, description))
    conn.commit()
    print(f"Income of {amount} added successfully!\n")


# Function to add expense
def add_expense():
    amount = float(input("Enter the expense amount: "))
    date = input("Enter the date (YYYY-MM-DD): ")
    category = input("Enter the expense category (e.g., groceries, rent): ")
    description = input("Optional: Enter a description for this expense (press Enter to skip): ")

    # Append expense to the transactions DataFrame
    # transactions.loc[len(transactions)] = [date, 'Expense', category, amount, description]
    c.execute("INSERT INTO transactions (date, type, category, amount, description) VALUES (?, 'Expense', ?, ?, ?)",
              (date, category, amount, description))
    conn.commit()
    print(f"Expense of {amount} for {category} added successfully!\n")

create_table()


#  Function to generate reports (e.g., total income, total expense)
def generate_report():
    # income = transactions[transactions['Type'] == 'Income']['Amount'].sum()
    # expenses = transactions[transactions['Type'] == 'Expense']['Amount'].sum()

    # Fetch total income
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = c.fetchone()[0] or 0

    # Fetch total expenses
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expenses = c.fetchone()[0] or 0
    savings = income - expenses
    print(f"Total Income: {income}")
    print(f"Total Expenses: {expenses}")
    print(f"Savings: {savings}")
    return income, expenses, savings


# Function to visualize spending by category
def visualize_expenses():
    # Load the data into a Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM transactions WHERE type='Expense'", conn)
    if not df.empty:
        expenses_by_category = df.groupby('category')['amount'].sum()
        expenses_by_category.plot(kind='bar', title='Expenses by Category')
        plt.ylabel('Amount')
        plt.show()
    else:
        print("No expenses to visualize.")


# Function to set and track budget goals
def set_budget_goal():
    category = input("Enter the category for the budget (e.g., groceries, rent): ")
    budget = float(input(f"Set the budget limit for {category}: "))

    # Fetch total expenses in the specified category
    c.execute("SELECT SUM(amount) FROM transactions WHERE category=? AND type='Expense'", (category,))
    expenses_in_category = c.fetchone()[0] or 0

    if expenses_in_category <= budget:
        print(f"You're within the budget for {category}. Total spent: {expenses_in_category}. Budget: {budget}")
    else:
        print(f"Budget exceeded for {category}. Total spent: {expenses_in_category}. Budget: {budget}")


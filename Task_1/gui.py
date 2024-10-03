import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database (create if it doesn't exist)
conn = sqlite3.connect('finance.db')
c = conn.cursor()


# Create the transactions table if it doesn't exist
def create_table():
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT,
                      type TEXT,
                      category TEXT,
                      amount REAL,
                      description TEXT)''')
    conn.commit()

create_table()

root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("400x400")

def add_income():
    # A new window for adding income
    income_window = tk.Toplevel(root)
    income_window.title("Add Income")
    income_window.geometry("300x300")

    # Labels and input fields for date, amount, and description
    tk.Label(income_window, text="Date (YYYY-MM-DD):").pack(pady=5)
    date_entry = tk.Entry(income_window)
    date_entry.pack(pady=5)

    tk.Label(income_window, text="Amount:").pack(pady=5)
    amount_entry = tk.Entry(income_window)
    amount_entry.pack(pady=5)

    tk.Label(income_window, text="Description (optional):").pack(pady=5)
    description_entry = tk.Entry(income_window)
    description_entry.pack(pady=5)

    # Function to insert data into the database
    def submit_income():
        date = date_entry.get()
        amount = amount_entry.get()
        description = description_entry.get()

        # Check if amount is a valid number
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        # Insert into the database
        c.execute(
            "INSERT INTO transactions (date, type, category, amount, description) VALUES (?, 'Income', 'N/A', ?, ?)",
            (date, amount, description))
        conn.commit()
        messagebox.showinfo("Success", f"Income of {amount} added successfully!")
        income_window.destroy()  # Close the income window after submission

    # Submit button
    tk.Button(income_window, text="Submit", command=submit_income).pack(pady=10)

def add_expense():
    expense_window = tk.Toplevel(root)
    expense_window.title("Add Expense")
    expense_window.geometry("300x350")

    # Labels and input fields for date, amount, category, and description
    tk.Label(expense_window, text="Date (YYYY-MM-DD):").pack(pady=5)
    date_entry = tk.Entry(expense_window)
    date_entry.pack(pady=5)

    tk.Label(expense_window, text="Amount:").pack(pady=5)
    amount_entry = tk.Entry(expense_window)
    amount_entry.pack(pady=5)

    tk.Label(expense_window, text="Category (e.g., groceries, rent):").pack(pady=5)
    category_entry = tk.Entry(expense_window)
    category_entry.pack(pady=5)

    tk.Label(expense_window, text="Description (optional):").pack(pady=5)
    description_entry = tk.Entry(expense_window)
    description_entry.pack(pady=5)

    # Function to insert data into the database
    def submit_expense():
        date = date_entry.get()
        amount = amount_entry.get()
        category = category_entry.get()
        description = description_entry.get()

        # Check if amount is a valid number
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        # Insert into the database
        c.execute("INSERT INTO transactions (date, type, category, amount, description) VALUES (?, 'Expense', ?, ?, ?)",
                  (date, category, amount, description))
        conn.commit()
        messagebox.showinfo("Success", f"Expense of {amount} for {category} added successfully!")
        expense_window.destroy()  # Close the expense window after submission

    # Submit button
    tk.Button(expense_window, text="Submit", command=submit_expense).pack(pady=10)

def generate_report():
    # Fetch total income
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = c.fetchone()[0] or 0

    # Fetch total expenses
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expenses = c.fetchone()[0] or 0

    # Calculate savings
    savings = income - expenses

    # Display the report in a message box
    report = f"Total Income: {income}\nTotal Expenses: {expenses}\nSavings: {savings}"
    messagebox.showinfo("Financial Report", report)

def visualize_expenses():
    # Load the data from the database into a Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM transactions WHERE type='Expense'", conn)

    # Check if there are any expenses to visualize
    if not df.empty:
        # Group by category and sum the expenses
        expenses_by_category = df.groupby('category')['amount'].sum()

        # Plot the bar chart
        expenses_by_category.plot(kind='bar', title='Expenses by Category')
        plt.ylabel('Amount')
        plt.show()
    else:
        messagebox.showinfo("No Expenses", "There are no expenses to visualize.")
def set_budget_goal():
    # Create a new window for setting the budget
    budget_window = tk.Toplevel(root)
    budget_window.title("Set Budget Goal")
    budget_window.geometry("300x300")

    # Labels and input fields for category and budget limit
    tk.Label(budget_window, text="Category (e.g., groceries, rent):").pack(pady=5)
    category_entry = tk.Entry(budget_window)
    category_entry.pack(pady=5)

    tk.Label(budget_window, text="Budget Limit:").pack(pady=5)
    budget_entry = tk.Entry(budget_window)
    budget_entry.pack(pady=5)

    # Function to check the budget
    def submit_budget():
        category = category_entry.get()
        budget = budget_entry.get()

        # Check if budget is a valid number
        try:
            budget = float(budget)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid budget amount.")
            return

        # Fetch total expenses in the specified category
        c.execute("SELECT SUM(amount) FROM transactions WHERE category=? AND type='Expense'", (category,))
        expenses_in_category = c.fetchone()[0] or 0

        # Compare expenses with the budget
        if expenses_in_category <= budget:
            messagebox.showinfo("Budget Check",
                                f"You're within the budget for {category}. Total spent: {expenses_in_category}. Budget: {budget}")
        else:
            messagebox.showinfo("Budget Check",
                                f"Budget exceeded for {category}. Total spent: {expenses_in_category}. Budget: {budget}")

        budget_window.destroy()  # Close the budget window after checking

    # Submit button
    tk.Button(budget_window, text="Submit", command=submit_budget).pack(pady=10)

def export_to_csv():
    # Fetch all transactions from the database into a pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    # Ask the user to choose a file name and location to save the CSV
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                             title="Choose location to save CSV file")

    if file_path:
        # Export the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
        messagebox.showinfo("Success", f"Data exported successfully to {file_path}!")


def visualize_data_pie_chart():
    # Load the data into a Pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

    if not df.empty:
        # Group by type (Income/Expense) and sum the amounts
        expenses_vs_income = df.groupby('type')['amount'].sum()

        # Plot a pie chart
        expenses_vs_income.plot(kind='pie', autopct='%1.1f%%', startangle=90, title="Income vs Expenses")
        plt.ylabel('')  # Remove y-label for pie chart clarity
        plt.show()
    else:
        messagebox.showinfo("No Data", "There are no transactions to visualize.")


tk.Button(root, text="Add Income", command=add_income, width=20).pack(pady=10)
tk.Button(root, text="Add Expense", command=add_expense, width=20).pack(pady=10)
tk.Button(root, text="Generate Report", command=generate_report, width=20).pack(pady=10)
tk.Button(root, text="Visualize Expenses", command=visualize_expenses, width=20).pack(pady=10)
tk.Button(root, text="Set Budget Goal", command=set_budget_goal, width=20).pack(pady=10)
tk.Button(root, text="Export Data to CSV", command=export_to_csv, width=20).pack(pady=10)
tk.Button(root, text="Visualize Data (Pie Chart)", command=visualize_data_pie_chart, width=20).pack(pady=10)

root.mainloop()

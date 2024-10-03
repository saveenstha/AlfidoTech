import tkinter as tk
from tkinter import messagebox
import sqlite3

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
    messagebox.showinfo("Add Expense", "This will be the Add Expense functionality.")

def generate_report():
    messagebox.showinfo("Generate Report", "This will generate a report.")

def visualize_expenses():
    messagebox.showinfo("Visualize Expenses", "This will visualize expenses.")

def set_budget_goal():
    messagebox.showinfo("Set Budget Goal", "This will set a budget goal.")


tk.Button(root, text="Add Income", command=add_income, width=20).pack(pady=10)
tk.Button(root, text="Add Expense", command=add_expense, width=20).pack(pady=10)
tk.Button(root, text="Generate Report", command=generate_report, width=20).pack(pady=10)
tk.Button(root, text="Visualize Expenses", command=visualize_expenses, width=20).pack(pady=10)
tk.Button(root, text="Set Budget Goal", command=set_budget_goal, width=20).pack(pady=10)

root.mainloop()

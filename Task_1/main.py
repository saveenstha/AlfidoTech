import sqlite3
import  datetime

conn = sqlite3.connect("pft.db")
cur = conn.cursor()

def main():
    print("Welcome to the Personal Finance Tracker!")
    while True:
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Set Budget Goal")
        print("4. View Report")
        print("5. Export Data")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Logic for adding income
            pass
        elif choice == '2':
            # Logic for adding expense
            pass
        elif choice == '3':
            # Logic for setting a budget goal
            pass
        elif choice == '4':
            # Logic for viewing reports
            pass
        elif choice == '5':
            # Logic for exporting data
            pass
        elif choice == '6':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please try again.")

    if __name__ == "__main__":
        main()
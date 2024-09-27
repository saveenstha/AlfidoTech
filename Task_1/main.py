from task_1 import *

def main():
    while True:
        print("\nPersonal Finance Tracker Menu:")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Generate Report")
        print("4. Visualize Expenses")
        print("5. Set Budget Goal")
        print("6. Save Data to CSV")
        print("7. Load Data from CSV")
        print("8. Exit")

        choice = input("Select an option (1-8): ")

        if choice == '1':
            add_income()
        elif choice == '2':
            add_expense()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            visualize_expenses()
        elif choice == '5':
            set_budget_goal()
        elif choice == '6':
            filename = input("Enter the filename to save (e.g., 'data.csv'): ")
            save_to_csv(filename)
        elif choice == '7':
            filename = input("Enter the filename to load (e.g., 'data.csv'): ")
            load_from_csv(filename)
        elif choice == '8':
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please select a valid choice.")


if __name__ == '__main__':
    main()
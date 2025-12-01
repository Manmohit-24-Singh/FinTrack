# Import sys module for system operations (like exiting the program)
import sys
# Import database initialization function
from db import init_db
# Import all core operations functions
from operations import add_expense, monthly_report, view_all_expenses

def main():
    """
    Main application entry point.
    Initializes the database and runs the interactive menu loop.
    
    Menu Options:
        1. Add Expense - Record a new expense
        2. Monthly Report - View top 3 spending categories
        3. View All Expenses - Display complete expense history
        4. Exit - Quit the application
    """
    # Initialize database (creates expenses table if it doesn't exist)
    init_db()
    
    # Main application loop - runs until user chooses to exit
    while True:
        # Display menu header
        print("\n=== EXPENSE TRACKER ===")
        
        # Display menu options
        print("1. Add Expense")
        print("2. Monthly Report (Top 3)")
        print("3. View All Expenses")
        print("4. Exit")
        
        # Get user's menu choice and remove leading/trailing whitespace
        choice = input("\nSelect: ").strip()
        
        # Process user's choice using if-elif-else chain
        if choice == '1':
            # User selected option 1: Add a new expense
            add_expense()
        elif choice == '2':
            # User selected option 2: View top spending categories
            monthly_report()
        elif choice == '3':
            # User selected option 3: View all expenses in table format
            view_all_expenses()
        elif choice == '4':
            # User selected option 4: Exit the application
            print("Bye!")
            sys.exit(0)  # Exit program with status code 0 (success)
        else:
            # User entered an invalid option (not 1-4)
            print("Invalid choice.")

# Python idiom to check if script is being run directly
if __name__ == "__main__":
    # Run the main function when script is executed
    main()
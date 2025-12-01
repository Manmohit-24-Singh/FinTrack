"""
Interactive CLI: Menu-driven interface with real-time validation.
Key Pattern: Validates all inputs before database operations via validation.py.
"""
import os
from datetime import datetime
from db import list_categories, add_category, get_category_by_name
from expenses import add_expense, view_expenses, update_expense, delete_expense, get_expense_by_id
from reports import monthly_report
from validation import (
    validate_amount, validate_date, validate_category_id, 
    validate_category_name, validate_description, validate_expense_id,
    validate_year, validate_month
)


# UI helper functions
def clear_screen():
    """Clears terminal for better UX (works on both Unix and Windows)."""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(title):
    """Formats section headers for visual separation."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)



def print_categories():
    """Displays available categories for user reference during add/update."""
    categories = list_categories()
    if not categories:
        print("No categories available.")
        return
    
    print("\nAvailable Categories:")
    print("-" * 40)
    for cat_id, cat_name in categories:
        print(f"  {cat_id:2}. {cat_name}")
    print("-" * 40)


# Validation wrapper: Loops until valid input provided
def get_validated_input(prompt, validation_func, allow_empty=False):
    """
    Gets user input with real-time validation loop.
    Returns validated value or None if empty input allowed.
    """
    while True:
        user_input = input(prompt).strip()
        
        if not user_input and allow_empty:
            return None
        
        is_valid, error_msg, cleaned_value = validation_func(user_input)
        
        if is_valid:
            return cleaned_value
        else:
            print(f"❌ {error_msg}")


# Interactive CRUD functions - each follows same pattern: validate, execute, confirm
def add_expense_interactive():
    """Guides user through expense creation with category display and validation."""
    clear_screen()
    print_header("Add New Expense")
    
    print_categories()
    
    # Flexible category input: accepts both ID and name
    print("\nYou can enter either:")
    print("  - Category ID (e.g., 1)")
    print("  - Category Name (e.g., Food)")
    
    category_input = input("\nCategory: ").strip()
    
    # Try ID validation first, fallback to name validation
    is_valid, error_msg, category_id = validate_category_id(category_input)
    if not is_valid:
        is_valid, error_msg, category_id = validate_category_name(category_input)
        if not is_valid:
            print(f"❌ {error_msg}")
            input("\nPress Enter to continue...")
            return
    
    amount = get_validated_input("Amount: $", validate_amount)
    
    # Smart default: today's date if no input
    print(f"\nDate (YYYY-MM-DD) [Press Enter for today: {datetime.now().date()}]:")
    date_input = input().strip()
    if not date_input:
        date = str(datetime.now().date())
    else:
        is_valid, error_msg, date = validate_date(date_input)
        if not is_valid:
            print(f"❌ {error_msg}")
            input("\nPress Enter to continue...")
            return
    
    print("\nDescription (optional):")
    desc_input = input().strip()
    is_valid, error_msg, description = validate_description(desc_input)
    if not is_valid:
        print(f"❌ {error_msg}")
        input("\nPress Enter to continue...")
        return
    
    # Execute database operation with exception handling
    try:
        add_expense(amount, category_id, date, description)
        print(f"\n✅ Expense added successfully!")
        print(f"   Amount: ${amount:.2f}")
        print(f"   Date: {date}")
        print(f"   Description: {description if description else '(none)'}")
    except Exception as e:
        print(f"\n❌ Error adding expense: {e}")
    
    input("\nPress Enter to continue...")


def view_expenses_interactive():
    """Displays expenses with optional multi-criteria filtering (date, category, amount)."""
    clear_screen()
    print_header("View Expenses")
    
    print("\nFilter options (press Enter to skip):\n")
    
    # Build filters dynamically - each optional
    print("Filter by date range:")
    date_from_input = input("  From date (YYYY-MM-DD): ").strip()
    date_from = None
    if date_from_input:
        is_valid, error_msg, date_from = validate_date(date_from_input, allow_future=True)
        if not is_valid:
            print(f"❌ {error_msg}")
            input("\nPress Enter to continue...")
            return
    
    date_to_input = input("  To date (YYYY-MM-DD): ").strip()
    date_to = None
    if date_to_input:
        is_valid, error_msg, date_to = validate_date(date_to_input, allow_future=True)
        if not is_valid:
            print(f"❌ {error_msg}")
            input("\nPress Enter to continue...")
            return
    
    print_categories()
    category_input = input("\nFilter by category (ID or Name): ").strip()
    category_id = None
    if category_input:
        is_valid, error_msg, category_id = validate_category_id(category_input)
        if not is_valid:
            is_valid, error_msg, category_id = validate_category_name(category_input)
            if not is_valid:
                print(f"❌ {error_msg}")
                input("\nPress Enter to continue...")
                return
    
    print("\nFilter by amount range:")
    min_amount_input = input("  Minimum amount: $").strip()
    min_amount = None
    if min_amount_input:
        is_valid, error_msg, min_amount = validate_amount(min_amount_input)
        if not is_valid:
            print(f"❌ {error_msg}")
            input("\nPress Enter to continue...")
            return
    
    max_amount_input = input("  Maximum amount: $").strip()
    max_amount = None
    if max_amount_input:
        is_valid, error_msg, max_amount = validate_amount(max_amount_input)
        if not is_valid:
            print(f"❌ {error_msg}")
            input("\nPress Enter to continue...")
            return
    
    # Query with filters and display results
    try:
        expenses = view_expenses(date_from, date_to, category_id, min_amount, max_amount)
        
        clear_screen()
        print_header("Expense List")
        
        if not expenses:
            print("\nNo expenses found matching the criteria.")
        else:
            print(f"\n{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
            print("-" * 80)
            for row in expenses:
                print(f"{row[0]:<5} {str(row[3]):<12} {row[2]:<15} ${row[1]:<9.2f} {row[4]}")
            print("-" * 80)
            print(f"Total: {len(expenses)} expense(s)")
    
    except Exception as e:
        print(f"\n❌ Error retrieving expenses: {e}")
    
    input("\nPress Enter to continue...")


def update_expense_interactive():
    """Shows current values, allows selective field updates (Enter to keep current)."""
    clear_screen()
    print_header("Update Expense")
    
    expense_id = get_validated_input("\nExpense ID to update: ", validate_expense_id)
    
    # Fetch and display current values
    try:
        expense = get_expense_by_id(expense_id)
        if not expense:
            print(f"❌ Expense ID {expense_id} not found.")
            input("\nPress Enter to continue...")
            return
        
        exp_id, current_amount, cat_name, cat_id, current_date, current_desc = expense
        
        print(f"\nCurrent values:")
        print(f"  Amount: ${current_amount:.2f}")
        print(f"  Category: {cat_name}")
        print(f"  Date: {current_date}")
        print(f"  Description: {current_desc if current_desc else '(none)'}")
        
        print("\n" + "-" * 60)
        print("Enter new values (press Enter to keep current value):")
        print("-" * 60)
        
        # Selective updates: empty input keeps current value
        amount_input = input(f"\nNew Amount [${current_amount:.2f}]: $").strip()
        if amount_input:
            is_valid, error_msg, new_amount = validate_amount(amount_input)
            if not is_valid:
                print(f"❌ {error_msg}")
                input("\nPress Enter to continue...")
                return
        else:
            new_amount = float(current_amount)
        
        print_categories()
        category_input = input(f"\nNew Category [{cat_name}]: ").strip()
        if category_input:
            is_valid, error_msg, new_category_id = validate_category_id(category_input)
            if not is_valid:
                is_valid, error_msg, new_category_id = validate_category_name(category_input)
                if not is_valid:
                    print(f"❌ {error_msg}")
                    input("\nPress Enter to continue...")
                    return
        else:
            new_category_id = cat_id
        
        date_input = input(f"\nNew Date [{current_date}]: ").strip()
        if date_input:
            is_valid, error_msg, new_date = validate_date(date_input)
            if not is_valid:
                print(f"❌ {error_msg}")
                input("\nPress Enter to continue...")
                return
        else:
            new_date = str(current_date)
        
        desc_input = input(f"\nNew Description [{current_desc if current_desc else '(none)'}]: ").strip()
        if desc_input:
            is_valid, error_msg, new_description = validate_description(desc_input)
            if not is_valid:
                print(f"❌ {error_msg}")
                input("\nPress Enter to continue...")
                return
        else:
            new_description = current_desc if current_desc else ""
        
        update_expense(expense_id, new_amount, new_category_id, new_date, new_description)
        print(f"\n✅ Expense updated successfully!")
    
    except Exception as e:
        print(f"\n❌ Error updating expense: {e}")
    
    input("\nPress Enter to continue...")


def delete_expense_interactive():
    """Displays expense details and requires confirmation before deletion."""
    clear_screen()
    print_header("Delete Expense")
    
    expense_id = get_validated_input("\nExpense ID to delete: ", validate_expense_id)
    
    # Show full expense details before deletion
    try:
        expense = get_expense_by_id(expense_id)
        if not expense:
            print(f"❌ Expense ID {expense_id} not found.")
            input("\nPress Enter to continue...")
            return
        
        exp_id, amount, cat_name, cat_id, date, desc = expense
        
        print(f"\nExpense details:")
        print(f"  ID: {exp_id}")
        print(f"  Amount: ${amount:.2f}")
        print(f"  Category: {cat_name}")
        print(f"  Date: {date}")
        print(f"  Description: {desc if desc else '(none)'}")
        
        # Safety check: require explicit confirmation
        confirm = input("\n⚠️  Are you sure you want to delete this expense? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            delete_expense(expense_id)
            print(f"\n✅ Expense deleted successfully!")
        else:
            print("\n❌ Deletion cancelled.")
    
    except Exception as e:
        print(f"\n❌ Error deleting expense: {e}")
    
    input("\nPress Enter to continue...")


def monthly_report_interactive():
    """Generates monthly report with percentages for top 3 categories."""
    clear_screen()
    print_header("Monthly Report")
    
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # Smart defaults for current month/year
    year_input = input(f"\nYear [{current_year}]: ").strip()
    if year_input:
        is_valid, error_msg, year = validate_year(year_input)
        if not is_valid:
            print(f"❌ {error_msg}")
            input("\nPress Enter to continue...")
            return
    else:
        year = current_year
    
    month_input = input(f"Month (1-12) [{current_month}]: ").strip()
    if month_input:
        is_valid, error_msg, month = validate_month(month_input)
        if not is_valid:
            print(f"❌ {error_msg}")
            input("\nPress Enter to continue...")
            return
    else:
        month = current_month
    
    # Generate and display aggregated report
    try:
        report = monthly_report(year, month)
        
        clear_screen()
        print_header(f"Top 3 Expenses for {month}/{year}")
        
        if not report:
            print("\nNo expenses found for this period.")
        else:
            total = sum(row[1] for row in report)
            for i, row in enumerate(report, 1):
                percentage = (row[1] / total * 100) if total > 0 else 0
                print(f"{i}. {row[0]:<20} ${row[1]:>10.2f}  ({percentage:.1f}%)")
            print("-" * 60)
            print(f"{'Total:':<21} ${total:>10.2f}")
        
        print("=" * 60)
        print("✨ Automated Insight: Spending habits analyzed.")
    
    except Exception as e:
        print(f"\n❌ Error generating report: {e}")
    
    input("\nPress Enter to continue...")


def manage_categories_interactive():
    """Lists all categories and allows adding custom ones."""
    clear_screen()
    print_header("Manage Categories")
    
    print_categories()
    
    print("\nOptions:")
    print("  1. Add a new category")
    print("  2. Return to main menu")
    
    choice = input("\nChoice: ").strip()
    
    if choice == "1":
        category_name = input("\nNew category name: ").strip()
        if not category_name:
            print("❌ Category name cannot be empty.")
        else:
            try:
                success, result = add_category(category_name)
                if success:
                    print(f"✅ Category '{category_name}' added successfully! (ID: {result})")
                else:
                    print(f"❌ {result}")
            except Exception as e:
                print(f"❌ Error adding category: {e}")
    
    input("\nPress Enter to continue...")


# Main menu loop - dispatches to appropriate submenu
def main_menu():
    """Main menu loop: displays options and routes to corresponding functions."""
    while True:
        clear_screen()
        print_header("📊 Personal Expense Tracker")
        
        print("\nMain Menu:")
        print("  1. View Expenses")
        print("  2. Add Expense")
        print("  3. Update Expense")
        print("  4. Delete Expense")
        print("  5. Monthly Report")
        print("  6. Manage Categories")
        print("  7. Exit")
        
        choice = input("\nSelect an option (1-7): ").strip()
        
        # Route to appropriate function based on user choice
        if choice == "1":
            view_expenses_interactive()
        elif choice == "2":
            add_expense_interactive()
        elif choice == "3":
            update_expense_interactive()
        elif choice == "4":
            delete_expense_interactive()
        elif choice == "5":
            monthly_report_interactive()
        elif choice == "6":
            manage_categories_interactive()
        elif choice == "7":
            clear_screen()
            print("\n👋 Thank you for using Expense Tracker!\n")
            break
        else:
            print("\n❌ Invalid option. Please choose 1-7.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main_menu()

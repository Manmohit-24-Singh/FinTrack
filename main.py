"""
Entry point: Supports both interactive CLI and command-line modes.
Key Pattern: Mode selection based on arguments, all inputs validated before execution.
"""
import argparse
import sys
import random
from datetime import datetime, timedelta
from db import init_db, get_connection
from expenses import add_expense, view_expenses, update_expense, delete_expense
from reports import monthly_report
from validation import (
    validate_amount, validate_date, validate_category_id, 
    validate_expense_id, validate_year, validate_month
)

# Dual-mode architecture: Interactive menu vs. command-line
if len(sys.argv) == 1:
    # No arguments = launch interactive CLI
    from cli import main_menu
    main_menu()
    sys.exit(0)

# Arguments present = command-line mode with argparse
parser = argparse.ArgumentParser(description="Personal Expense Tracker (PostgreSQL)")
subparsers = parser.add_subparsers(dest="command")

# Command definitions
subparsers.add_parser("setup")  # Database initialization
subparsers.add_parser("seed")   # Generate demo data

# CRUD commands - arguments parsed as strings for validation
add_parser = subparsers.add_parser("add")
add_parser.add_argument("amount", type=str)
add_parser.add_argument("category_id", type=str)
add_parser.add_argument("date")
add_parser.add_argument("--desc", default="")

subparsers.add_parser("view")

update_parser = subparsers.add_parser("update")
update_parser.add_argument("id", type=str)
update_parser.add_argument("amount", type=str)
update_parser.add_argument("category_id", type=str)
update_parser.add_argument("date")
update_parser.add_argument("--desc", default="")

delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("id", type=str)

report_parser = subparsers.add_parser("report")
report_parser.add_argument("year", type=str)
report_parser.add_argument("month", type=str)

args = parser.parse_args()

# Command execution with validation
if args.command == "setup":
    init_db()

elif args.command == "seed":
    # Generates random expenses for current month
    today = datetime.today()
    print(f"🌱 Seeding data for {today.strftime('%B %Y')}...")
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id FROM categories")
    cat_ids = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    
    if not cat_ids:
        print("❌ No categories found. Run 'setup' first.")
    else:
        for _ in range(15):
            amt = round(random.uniform(10.0, 150.0), 2)
            cat = random.choice(cat_ids)
            day_offset = random.randint(0, 28)
            date_str = (today.replace(day=1) + timedelta(days=day_offset)).strftime("%Y-%m-%d")
            add_expense(amt, cat, date_str, "Demo Expense")
        print("✅ Added 15 random expenses.")

elif args.command == "add":
    # Validate before database operation
    is_valid, error_msg, amount = validate_amount(args.amount)
    if not is_valid:
        print(f"❌ Invalid amount: {error_msg}")
        sys.exit(1)
    
    is_valid, error_msg, category_id = validate_category_id(args.category_id)
    if not is_valid:
        print(f"❌ Invalid category ID: {error_msg}")
        sys.exit(1)
    
    is_valid, error_msg, date = validate_date(args.date)
    if not is_valid:
        print(f"❌ Invalid date: {error_msg}")
        sys.exit(1)
    
    try:
        add_expense(amount, category_id, date, args.desc)
        print("✅ Expense added successfully.")
    except Exception as e:
        print(f"❌ Error adding expense: {e}")
        sys.exit(1)

elif args.command == "view":
    try:
        expenses = view_expenses()
        print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
        print("-" * 60)
        for row in expenses:
            print(f"{row[0]:<5} {str(row[3]):<12} {row[2]:<15} ${row[1]:<9} {row[4]}")
    except Exception as e:
        print(f"❌ Error viewing expenses: {e}")
        sys.exit(1)

elif args.command == "update":
    # Multi-field validation
    is_valid, error_msg, expense_id = validate_expense_id(args.id)
    if not is_valid:
        print(f"❌ Invalid expense ID: {error_msg}")
        sys.exit(1)
    
    is_valid, error_msg, amount = validate_amount(args.amount)
    if not is_valid:
        print(f"❌ Invalid amount: {error_msg}")
        sys.exit(1)
    
    is_valid, error_msg, category_id = validate_category_id(args.category_id)
    if not is_valid:
        print(f"❌ Invalid category ID: {error_msg}")
        sys.exit(1)
    
    is_valid, error_msg, date = validate_date(args.date)
    if not is_valid:
        print(f"❌ Invalid date: {error_msg}")
        sys.exit(1)
    
    try:
        update_expense(expense_id, amount, category_id, date, args.desc)
        print("✅ Expense updated successfully.")
    except Exception as e:
        print(f"❌ Error updating expense: {e}")
        sys.exit(1)

elif args.command == "delete":
    is_valid, error_msg, expense_id = validate_expense_id(args.id)
    if not is_valid:
        print(f"❌ Invalid expense ID: {error_msg}")
        sys.exit(1)
    
    try:
        delete_expense(expense_id)
        print("✅ Expense deleted successfully.")
    except Exception as e:
        print(f"❌ Error deleting expense: {e}")
        sys.exit(1)

elif args.command == "report":
    is_valid, error_msg, year = validate_year(args.year)
    if not is_valid:
        print(f"❌ Invalid year: {error_msg}")
        sys.exit(1)
    
    is_valid, error_msg, month = validate_month(args.month)
    if not is_valid:
        print(f"❌ Invalid month: {error_msg}")
        sys.exit(1)
    
    try:
        report = monthly_report(year, month)
        print(f"\n📊 Top 3 Expenses for {month}/{year}")
        print("=" * 40)
        if not report:
            print("No expenses found for this period.")
        else:
            for i, row in enumerate(report, 1):
                print(f"{i}. {row[0]}: ${row[1]:.2f}")
        print("=" * 40)
        print("✨ Automated Insight: Spending habits analyzed.\n")
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        sys.exit(1)



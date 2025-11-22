import argparse
import random
from datetime import datetime, timedelta
from db import init_db, get_connection
from expenses import add_expense, view_expenses, update_expense, delete_expense
from reports import monthly_report

parser = argparse.ArgumentParser(description="Personal Expense Tracker (PostgreSQL)")
subparsers = parser.add_subparsers(dest="command")

# Setup DB
subparsers.add_parser("setup")

# Seed Data
subparsers.add_parser("seed")

# Add expense
add_parser = subparsers.add_parser("add")
add_parser.add_argument("amount", type=float)
add_parser.add_argument("category_id", type=int)
add_parser.add_argument("date")
add_parser.add_argument("--desc", default="")

# View expenses
subparsers.add_parser("view")

# Update expense
update_parser = subparsers.add_parser("update")
update_parser.add_argument("id", type=int)
update_parser.add_argument("amount", type=float)
update_parser.add_argument("category_id", type=int)
update_parser.add_argument("date")
update_parser.add_argument("--desc", default="")

# Delete expense
delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("id", type=int)

# Monthly report
report_parser = subparsers.add_parser("report")
report_parser.add_argument("year", type=int)
report_parser.add_argument("month", type=int)

args = parser.parse_args()

if args.command == "setup":
    init_db()

elif args.command == "seed":
    # Seed some random data for the current month
    today = datetime.today()
    print(f"🌱 Seeding data for {today.strftime('%B %Y')}...")
    
    # Get category IDs
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
    try:
        add_expense(args.amount, args.category_id, args.date, args.desc)
        print("✅ Expense added successfully.")
    except Exception as e:
        print(f"❌ Error adding expense: {e}")

elif args.command == "view":
    expenses = view_expenses()
    print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description'}")
    print("-" * 60)
    for row in expenses:
        # row: (id, amount, category, date, desc)
        print(f"{row[0]:<5} {str(row[3]):<12} {row[2]:<15} ${row[1]:<9} {row[4]}")

elif args.command == "update":
    try:
        update_expense(args.id, args.amount, args.category_id, args.date, args.desc)
        print("✅ Expense updated successfully.")
    except Exception as e:
        print(f"❌ Error updating expense: {e}")

elif args.command == "delete":
    try:
        delete_expense(args.id)
        print("✅ Expense deleted successfully.")
    except Exception as e:
        print(f"❌ Error deleting expense: {e}")

elif args.command == "report":
    report = monthly_report(args.year, args.month)
    print(f"\n📊 Top 3 Expenses for {args.month}/{args.year}")
    print("=" * 40)
    if not report:
        print("No expenses found for this period.")
    else:
        for i, row in enumerate(report, 1):
            print(f"{i}. {row[0]}: ${row[1]:.2f}")
    print("=" * 40)
    print("✨ Automated Insight: Spending habits analyzed.\n")

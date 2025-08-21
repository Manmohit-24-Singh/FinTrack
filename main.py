import argparse
from expenses import add_expense, view_expenses, update_expense, delete_expense
from reports import monthly_report

parser = argparse.ArgumentParser(description="Personal Expense Tracker (PostgreSQL)")
subparsers = parser.add_subparsers(dest="command")

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

if args.command == "add":
    add_expense(args.amount, args.category_id, args.date, args.desc)
    print("✅ Expense added.")
elif args.command == "view":
    for row in view_expenses():
        print(row)
elif args.command == "update":
    update_expense(args.id, args.amount, args.category_id, args.date, args.desc)
    print("✅ Expense updated.")
elif args.command == "delete":
    delete_expense(args.id)
    print("❌ Expense deleted.")
elif args.command == "report":
    report = monthly_report(args.year, args.month)
    for row in report:
        print(f"{row[0]}: {row[1]}")

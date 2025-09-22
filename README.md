# FinTrack - Personal Expense Tracker
A command-line expense tracking application built with Python and PostgreSQL that helps you manage your personal finances efficiently.

## Features
- **Add Expenses**: Record expenses with amount, category, date, and description
- **View Expenses**: Display all expenses in a clean, readable format
- **Update Expenses**: Modify existing expense records
- **Delete Expenses**: Remove unwanted expense entries
- **Monthly Reports**: Generate category-wise spending reports for any month
- **PostgreSQL Backend**: Reliable database storage with proper data integrity
- **CLI Interface**: Easy-to-use command-line interface

## Database Schema
### Tables
- **`expenses`**: Stores all expense records
  - `expense_id` (SERIAL PRIMARY KEY)
  - `amount` (DECIMAL)
  - `category_id` (INTEGER)
  - `expense_date` (DATE)
  - `description` (TEXT)
- **`categories`**: Pre-defined expense categories
  - `category_id` (SERIAL PRIMARY KEY)
  - `name` (VARCHAR)
### Default Categories
- **Category ID 1**: Food
- **Category ID 2**: Transport
- **Category ID 3**: Bills

## Prerequisites
- Python 3.8+
- PostgreSQL 14+
- pip package manager

## Installation
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```
### 2. Install Dependencies
```bash
pip install psycopg2-binary
```
### 3. Database Setup
**Create Database and User:**
```sql
CREATE DATABASE expense_tracker;
CREATE USER oop WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO oop;
```
**Create Tables** (run in PostgreSQL):
```sql
-- Connect to database
\c expense_tracker
-- Create categories table
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);
-- Create expenses table
CREATE TABLE expenses (
    expense_id SERIAL PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    expense_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Insert default categories
INSERT INTO categories (name) VALUES 
('Food'),
('Transport'),
('Bills');
```
### 4. Configure Database Connection
Edit `db.py` if your PostgreSQL configuration differs:
```python
def get_connection():
    return psycopg2.connect(
        host="localhost",      # Change if using remote server
        database="expense_tracker",
        user="oop",       
        password="password",
        port=5433             # Change if using default port 5432
    )
```

## Usage
### Command Syntax
```bash
python main.py <command> [arguments]
```
### Available Commands
#### Add an Expense
```bash
python main.py add <amount> <category_id> <date> [--desc "description"]
```
**Example:**
```bash
python main.py add 25.50 1 "2024-08-21" --desc "Lunch at cafe"
```
#### 👀 View All Expenses
```bash
python main.py view
```
**Output:**
```
(1, Decimal('25.50'), 'Food', datetime.date(2024, 8, 21), 'Lunch at cafe')
(2, Decimal('15.99'), 'Food', datetime.date(2024, 8, 20), 'Coffee')
```
#### Update an Expense
```bash
python main.py update <expense_id> <amount> <category_id> <date> [--desc "description"]
```
**Example:**
```bash
python main.py update 1 30.00 1 "2024-08-21" --desc "Dinner with friends"
```
#### Delete an Expense
```bash
python main.py delete <expense_id>
```
**Example:**
```bash
python main.py delete 1
```
#### Generate Monthly Report
```bash
python main.py report <year> <month>
```
**Example:**
```bash
python main.py report 2024 8
```
**Output:**
```
Food: 91.49
Bills: 120.00
Transport: 45.00
```

## Examples
### Complete Workflow Example
```bash
# Add some expenses
python main.py add 15.99 1 "2024-08-20" --desc "Coffee"
python main.py add 45.00 2 "2024-08-19" --desc "Bus fare"
python main.py add 120.00 3 "2024-08-18" --desc "Electricity bill"
python main.py add 75.50 1 "2024-08-17" --desc "Groceries"
# View all expenses
python main.py view
# Generate monthly report
python main.py report 2024 8
# Update an expense
python main.py update 2 50.00 2 "2024-08-19" --desc "Bus and subway"
# Delete an expense
python main.py delete 3
# View updated list
python main.py view
```

## Project Structure
```
expense_tracker/
├── main.py              # Main CLI application
├── expenses.py          # Expense CRUD operations
├── reports.py           # Reporting functions
├── db.py               # Database connection setup
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```
### File Descriptions
- **`main.py`**: Command-line interface using argparse
- **`expenses.py`**: Functions for add, view, update, delete operations
- **`reports.py`**: Monthly reporting functionality
- **`db.py`**: PostgreSQL database connection handler

## Troubleshooting
### Common Issues
1. **Connection Refused**
   ```bash
   # Check if PostgreSQL is running
   sudo service postgresql status
   
   # Verify port number in db.py
   ```
2. **Authentication Failed**
   ```bash
   # Verify username/password in db.py
   # Check user privileges in PostgreSQL
   ```
3. **Category Doesn't Exist**
   ```bash
   # Check available categories in database
   psql -d expense_tracker -c "SELECT * FROM categories;"
   ```
4. **Date Format Issues**
   ```bash
   # Use YYYY-MM-DD format only
   python main.py add 10.00 1 "2024-08-21" --desc "Test"
   ```
### Database Queries for Debugging
```sql
-- Check all expenses
SELECT * FROM expenses ORDER BY expense_date DESC;
-- Check categories
SELECT * FROM categories;
-- Check monthly summary
SELECT c.name, SUM(e.amount) as total
FROM expenses e
JOIN categories c ON e.category_id = c.category_id
WHERE EXTRACT(YEAR FROM e.expense_date) = 2024
AND EXTRACT(MONTH FROM e.expense_date) = 8
GROUP BY c.name
ORDER BY total DESC;
```
---

# FinTrack

A command-line expense tracking application built with Python and PostgreSQL, focused on reliable data storage and efficient management of personal finances via a minimalist CLI interface.

## 📋 Overview

Personal Expense Tracker is a lightweight, terminal-based application that helps you manage your daily expenses with simplicity and efficiency. Built with Python and PostgreSQL, it provides a fast and reliable way to track spending, categorize expenses, and generate monthly reports without the overhead of a graphical interface.

## ✨ Features

- **Expense Management**
  - Add new expenses with amount, category, date, and description
  - View all expenses in chronological order
  - Update existing expense records
  - Delete expenses

- **Category Organization**
  - Link expenses to predefined categories
  - Easy categorization for better expense tracking

- **Reporting**
  - Monthly expense reports
  - Category-wise spending summaries
  - Total spending by category

- **Data Persistence**
  - PostgreSQL database for reliable storage
  - Structured data with relationships
  - Fast queries and retrieval

## 🛠️ Tech Stack

- **Python 3.x** - Core application language
- **PostgreSQL** - Database management system
- **psycopg2** - PostgreSQL adapter for Python
- **argparse** - Command-line argument parsing

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python** (3.7 or higher)
- **PostgreSQL** (12 or higher)
- **pip** (Python package manager)

### Installation Commands

#### Ubuntu/Debian
```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Verify installations
python3 --version
psql --version
```

#### macOS
```bash
# Install Python
brew install python3

# Install PostgreSQL
brew install postgresql
brew services start postgresql

# Verify installations
python3 --version
psql --version
```

#### Windows
- Download and install [Python](https://www.python.org/downloads/)
- Download and install [PostgreSQL](https://www.postgresql.org/download/windows/)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Manmohit-24-Singh/expense-tracker.git
cd expense-tracker
```

### 2. Install Python Dependencies

```bash
pip install psycopg2-binary
```

### 3. Set Up PostgreSQL Database

#### Start PostgreSQL Service

```bash
# Linux
sudo service postgresql start

# macOS
brew services start postgresql

# Windows - PostgreSQL should auto-start as a service
```

#### Create Database and User

```bash
# Access PostgreSQL as postgres user
sudo -u postgres psql

# Or on Windows/macOS
psql -U postgres
```

In the PostgreSQL prompt, run:

```sql
-- Create database
CREATE DATABASE expense_tracker;

-- Create user
CREATE USER oop WITH PASSWORD 'ucalgary';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO oop;

-- Connect to the database
\c expense_tracker

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO oop;

-- Exit
\q
```

### 4. Create Database Schema

Connect to the database and create the necessary tables:

```bash
psql -U oop -d expense_tracker -h localhost -p 5433
```

Run the following SQL:

```sql
-- Categories table
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Expenses table
CREATE TABLE expenses (
    expense_id SERIAL PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    expense_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample categories
INSERT INTO categories (name, description) VALUES
    ('Food', 'Food and dining expenses'),
    ('Transport', 'Transportation costs'),
    ('Utilities', 'Utility bills'),
    ('Entertainment', 'Entertainment and leisure'),
    ('Healthcare', 'Medical and health expenses'),
    ('Shopping', 'Shopping and retail'),
    ('Education', 'Educational expenses'),
    ('Other', 'Miscellaneous expenses');
```

### 5. Configure Database Connection

Edit `db.py` to match your PostgreSQL configuration:

```python
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="expense_tracker",
        user="oop",       
        password="ucalgary",
        port=5433         # Change if using default port 5432
    )
```

## 🎯 Usage

The application uses command-line arguments for all operations. Here's how to use each feature:

### Add an Expense

```bash
python main.py add <amount> <category_id> <date> [--desc "description"]
```

**Example:**
```bash
# Add a $50 food expense
python main.py add 50.00 1 2024-01-15 --desc "Lunch at restaurant"

# Add transport expense without description
python main.py add 20.00 2 2024-01-15
```

### View All Expenses

```bash
python main.py view
```

**Output:**
```
(1, 50.00, 'Food', datetime.date(2024, 1, 15), 'Lunch at restaurant')
(2, 20.00, 'Transport', datetime.date(2024, 1, 15), '')
(3, 120.50, 'Utilities', datetime.date(2024, 1, 14), 'Electric bill')
```

### Update an Expense

```bash
python main.py update <expense_id> <amount> <category_id> <date> [--desc "description"]
```

**Example:**
```bash
# Update expense with ID 1
python main.py update 1 55.00 1 2024-01-15 --desc "Lunch and coffee"
```

### Delete an Expense

```bash
python main.py delete <expense_id>
```

**Example:**
```bash
# Delete expense with ID 3
python main.py delete 3
```

### Generate Monthly Report

```bash
python main.py report <year> <month>
```

**Example:**
```bash
# Get report for January 2024
python main.py report 2024 1
```

**Output:**
```
Food: 250.00
Transport: 150.00
Utilities: 120.50
Entertainment: 80.00
```

## 📂 Project Structure

```
expense-tracker/
├── db.py              # Database connection configuration
├── expenses.py        # Expense CRUD operations
├── reports.py         # Report generation functions
├── main.py            # Main application entry point
└── README.md          # Project documentation
```

### File Descriptions

#### `db.py`
- Manages PostgreSQL database connections
- Returns connection objects for database operations

#### `expenses.py`
- **add_expense()**: Insert new expense records
- **view_expenses()**: Retrieve all expenses with category names
- **update_expense()**: Modify existing expense records
- **delete_expense()**: Remove expense records

#### `reports.py`
- **monthly_report()**: Generate category-wise expense summary for a specific month

#### `main.py`
- Command-line interface using argparse
- Routes commands to appropriate functions
- Handles user input and displays results

## 🔍 Category Reference

Default category IDs (as created in setup):

| ID | Category      | Description                    |
|----|---------------|--------------------------------|
| 1  | Food          | Food and dining expenses       |
| 2  | Transport     | Transportation costs           |
| 3  | Utilities     | Utility bills                  |
| 4  | Entertainment | Entertainment and leisure      |
| 5  | Healthcare    | Medical and health expenses    |
| 6  | Shopping      | Shopping and retail            |
| 7  | Education     | Educational expenses           |
| 8  | Other         | Miscellaneous expenses         |

## 💡 Example Workflow

```bash
# 1. Add groceries expense
python main.py add 75.50 1 2024-01-15 --desc "Weekly groceries"
✅ Expense added.

# 2. Add gas expense
python main.py add 45.00 2 2024-01-15 --desc "Gas station"
✅ Expense added.

# 3. View all expenses
python main.py view
(1, 75.50, 'Food', datetime.date(2024, 1, 15), 'Weekly groceries')
(2, 45.00, 'Transport', datetime.date(2024, 1, 15), 'Gas station')

# 4. Update the groceries amount
python main.py update 1 80.00 1 2024-01-15 --desc "Weekly groceries + snacks"
✅ Expense updated.

# 5. Generate monthly report
python main.py report 2024 1
Food: 80.00
Transport: 45.00

# 6. Delete an expense
python main.py delete 2
❌ Expense deleted.
```

## 🔧 Database Schema

### Categories Table

```sql
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `category_id`: Auto-incrementing primary key
- `name`: Category name (unique)
- `description`: Optional category description
- `created_at`: Timestamp of creation

### Expenses Table

```sql
CREATE TABLE expenses (
    expense_id SERIAL PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    category_id INTEGER REFERENCES categories(category_id),
    expense_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Columns:**
- `expense_id`: Auto-incrementing primary key
- `amount`: Expense amount (decimal with 2 decimal places)
- `category_id`: Foreign key to categories table
- `expense_date`: Date of expense
- `description`: Optional expense description
- `created_at`: Timestamp of record creation

## 🐛 Troubleshooting

### Database Connection Error

**Error:**
```
psycopg2.OperationalError: could not connect to server
```

**Solution:**
1. Verify PostgreSQL is running:
   ```bash
   sudo service postgresql status
   ```
2. Check port number in `db.py` (default is 5432, yours is 5433)
3. Verify database credentials

### Module Not Found Error

**Error:**
```
ModuleNotFoundError: No module named 'psycopg2'
```

**Solution:**
```bash
pip install psycopg2-binary
```

### Permission Denied

**Error:**
```
psycopg2.errors.InsufficientPrivilege: permission denied
```

**Solution:**
```sql
-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO oop;
GRANT ALL ON SCHEMA public TO oop;
GRANT ALL ON ALL TABLES IN SCHEMA public TO oop;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO oop;
```

### Invalid Date Format

**Error:**
```
Invalid literal for int() with base 10
```

**Solution:**
Use date format: `YYYY-MM-DD` (e.g., `2024-01-15`)

## 🚀 Future Enhancements

- [ ] Budget tracking and alerts
- [ ] Export reports to CSV/PDF
- [ ] Recurring expense support
- [ ] Multiple currency support
- [ ] Data visualization (charts and graphs)
- [ ] Web interface
- [ ] Mobile app
- [ ] Category customization via CLI
- [ ] Search and filter expenses
- [ ] Annual reports
- [ ] Expense trends analysis
- [ ] Receipt attachment support
- [ ] Multi-user support
- [ ] Backup and restore functionality

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Guidelines
- Follow PEP 8 style guide for Python code
- Add comments for complex logic
- Test all database operations
- Update documentation for new features

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Manmohit Singh**
- GitHub: [@Manmohit-24-Singh](https://github.com/Manmohit-24-Singh)


## 📞 Support

For support, issues, or feature requests:
- Open an issue on GitHub
- Contact the maintainer through GitHub

---

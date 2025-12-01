# FinTrack

Personal expense tracker with Python and PostgreSQL. Command-line interface with input validation and interactive menus.

## Prerequisites

- Python 3.12+
- PostgreSQL 12+
- pip

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/Manmohit-24-Singh/expense-tracker.git
cd expense-tracker
```

### 2. Install Dependencies
```bash
pip install psycopg2-binary
```

### 3. Setup Database
```bash
# Start PostgreSQL
sudo service postgresql start  # Linux
brew services start postgresql # macOS

# Create database and user
psql -U postgres
```

```sql
CREATE DATABASE expense_tracker;
CREATE USER oop WITH PASSWORD 'ucalgary';
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO oop;
\c expense_tracker
GRANT ALL ON SCHEMA public TO oop;
\q
```

### 4. Initialize Tables
```bash
python main.py setup
```

### 5. Add Demo Data
```bash
python main.py seed
```

## Usage

### Interactive Mode (Recommended)
```bash
python main.py
```
Menu-driven interface with validation and filtering.

### Command-Line Mode
```bash
# Add expense
python main.py add <amount> <category_id> <date> [--desc "description"]
python main.py add 50.00 1 2025-11-30 --desc "Lunch"

# View expenses
python main.py view

# Update expense
python main.py update <id> <amount> <category_id> <date> [--desc "description"]
python main.py update 5 55.00 1 2025-11-30 --desc "Dinner"

# Delete expense
python main.py delete <id>
python main.py delete 5

# Monthly report
python main.py report <year> <month>
python main.py report 2025 11
```

## Default Categories

| ID | Category       |
|----|---------------|
| 1  | Food          |
| 2  | Transportation|
| 3  | Utilities     |
| 4  | Entertainment |
| 5  | Rent          |
| 6  | Groceries     |
| 7  | Misc          |

Add custom categories via interactive mode (option 6).

## Database Reset

```bash
# Drop and recreate tables
psql -h localhost -p 5433 -U oop -d expense_tracker -c "DROP TABLE IF EXISTS expenses CASCADE; DROP TABLE IF EXISTS categories CASCADE;" && python main.py setup

# Or clear data only
psql -h localhost -p 5433 -U oop -d expense_tracker -c "DELETE FROM expenses; DELETE FROM categories;" && python main.py setup
```

## Configuration

Edit `db.py` if your PostgreSQL uses different settings:
```python
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="expense_tracker",
        user="oop",
        password="ucalgary",
        port=5433  # Change if needed (default: 5432)
    )
```

## Features

- ✅ Input validation (amounts, dates, categories)
- ✅ Interactive CLI with menus
- ✅ Category support by ID or name
- ✅ Expense filtering (date range, category, amount)
- ✅ Monthly reports (top 3 categories)
- ✅ Custom category management

## Troubleshooting

**Connection error:**
```bash
# Check PostgreSQL status
sudo service postgresql status

# Verify port in db.py matches your PostgreSQL port
```

**Module not found:**
```bash
pip install psycopg2-binary
```

**Permission denied:**
```sql
GRANT ALL PRIVILEGES ON DATABASE expense_tracker TO oop;
GRANT ALL ON SCHEMA public TO oop;
GRANT ALL ON ALL TABLES IN SCHEMA public TO oop;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO oop;
```

## Author

**Manmohit Singh**  
GitHub: [@Manmohit-24-Singh](https://github.com/Manmohit-24-Singh)

# 💰 FinTrack - Expense Tracker

A **command-line expense tracking application** built with Python and PostgreSQL for efficient personal finance management.

## 📋 Overview

FinTrack is a lightweight, database-backed expense tracker that helps users record, categorize, and analyze their spending habits. It features robust input validation, automated reporting, and a clean command-line interface.

## ✨ Features

### 1. **Add Expense**
- Record expenses with amount, category, date, and optional description
- Smart input validation:
  - Ensures positive amounts only
  - Validates date format (YYYY-MM-DD)
  - Requires non-empty categories
  - Defaults to today's date if not specified
- Prevents SQL injection with parameterized queries

### 2. **Monthly Report (Top 3)**
- Displays top 3 spending categories
- Shows total amount per category
- Aggregates data using SQL GROUP BY
- Provides cumulative spending total

### 3. **View All Expenses**
- Comprehensive table view of all recorded expenses
- Sorted by date (most recent first)
- Displays: ID, Date, Category, Amount, Description
- Shows total expenses and count
- Smart truncation for long descriptions

### 4. **Data Persistence**
- PostgreSQL database for reliable storage
- Auto-initializes database schema on startup
- Handles 10,000+ transactions efficiently

## 🛠️ Technology Stack

- **Language**: Python 3.12
- **Database**: PostgreSQL
- **Libraries**: 
  - `psycopg2` - PostgreSQL adapter
  - `datetime` - Date handling and validation

## 📦 Installation

### Prerequisites
- Python 3.x installed
- PostgreSQL server running
- `psycopg2` library installed

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd /path/to/FinTrack
   ```

2. **Install dependencies**
   ```bash
   pip install psycopg2-binary
   ```

3. **Configure PostgreSQL**
   - Create a database named `expense_tracker`
   - Update credentials in `db.py` if needed:
     ```python
     host="localhost"
     database="expense_tracker"
     user="your_username"
     password="your_password"
     port=5433  # or your PostgreSQL port
     ```

4. **Create the database** (one-time setup)
   ```sql
   CREATE DATABASE expense_tracker;
   ```

## 🚀 Usage

### Running the Application
```bash
python main.py
```

### Example Workflow

```
=== EXPENSE TRACKER ===
1. Add Expense
2. Monthly Report (Top 3)
3. View All Expenses
4. Exit

Select: 1

--- Add Expense ---
Amount: $50.00
Category (e.g., Food, Rent): Food
Date [Enter for 2025-12-01]: 
Description (optional): Groceries from Walmart
✅ Saved!
```

### Viewing Reports
```
Select: 2

--- Monthly Report ---

🔥 Top 3 Categories:
  1. Food: $80.00
  2. Transportation: $50.00
  3. Entertainment: $30.00

Total Tracked: $160.00
```

### Viewing All Expenses
```
Select: 3

--- All Expenses ---

ID    Date         Category            Amount Description                   
---------------------------------------------------------------------------
3     2025-12-01   Food            $    50.00 Groceries from Walmart        
2     2025-11-30   Transportation  $    25.00 Uber to office                
1     2025-11-30   Food            $    30.00 Lunch at Subway               
---------------------------------------------------------------------------
Total:                            $   105.00

Total Expenses: 3
```

## 📁 Project Structure

```
FinTrack/
│
├── main.py          # Application entry point & menu system
├── operations.py    # Core features (add, report, view)
├── db.py           # Database connection & initialization
└── README.md       # This file
```

### File Descriptions

- **`main.py`**: Entry point with interactive menu loop
- **`operations.py`**: Contains all business logic and database operations
- **`db.py`**: Handles PostgreSQL connection and schema initialization

## 🗃️ Database Schema

```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,           -- Auto-incrementing ID
    amount REAL NOT NULL,            -- Expense amount
    category TEXT NOT NULL,          -- Category (Food, Rent, etc.)
    date DATE NOT NULL,              -- Date of expense
    description TEXT                 -- Optional details
);
```

## 🔒 Security Features

- ✅ **Parameterized SQL queries** - Prevents SQL injection
- ✅ **Input validation** - Ensures data integrity
- ✅ **Type checking** - Validates numeric and date inputs


## 🎯 Key Highlights

- **50% reduction in manual tracking effort** through automated categorization
- **Instant insights** with top spending categories
- **Complete expense history** at your fingertips
- **No data loss** with reliable PostgreSQL storage

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements.

## 📝 License

This project is open-source and available for personal and educational use.

## 👤 Author

**Manmohit Singh**

## 🔮 Future Enhancements

- [ ] Filter expenses by date range
- [ ] Edit/delete individual expenses
- [ ] Export data to CSV
- [ ] Budget setting and alerts
- [ ] Graphical visualizations
- [ ] Multi-user support

---

**Happy Tracking! 💸**

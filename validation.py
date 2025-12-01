"""
Input validation layer: Ensures data integrity before database operations.
Key Pattern: All validators return (is_valid, error_message, cleaned_value) tuple.
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation
from db import get_connection


# Amount validation: Uses Decimal for precise monetary calculations
def validate_amount(amount_str):
    """Validates positive amounts with max 2 decimal places. Prevents negative/zero values."""
    try:
        amount = Decimal(str(amount_str))
        
        if amount <= 0:
            return False, "Amount must be greater than zero.", None
        
        # Decimal precision check using tuple exponent
        if amount.as_tuple().exponent < -2:
            return False, "Amount can have at most 2 decimal places.", None
        
        if amount > 1000000:
            return False, "Amount seems unreasonably high. Maximum is $1,000,000.", None
        
        return True, "", float(amount)
    
    except (InvalidOperation, ValueError, TypeError):
        return False, "Invalid amount. Please enter a valid number.", None


# Date validation: Uses strptime for format checking
def validate_date(date_str, allow_future=False):
    """Validates YYYY-MM-DD format, prevents future dates for expenses."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Business rule: expenses can't be in the future
        if not allow_future and date_obj.date() > datetime.now().date():
            return False, "Expense date cannot be in the future.", None
        
        if date_obj.year < 1900:
            return False, "Date seems unreasonably old.", None
        
        return True, "", date_str
    
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD (e.g., 2025-11-30).", None


# Category ID validation: Verifies existence with database query
def validate_category_id(category_id):
    """Validates category ID exists in database."""
    try:
        cat_id = int(category_id)
        
        if cat_id <= 0:
            return False, "Category ID must be a positive number.", None
        
        # Database existence check
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT category_id FROM categories WHERE category_id = %s", (cat_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result is None:
            return False, f"Category ID {cat_id} does not exist.", None
        
        return True, "", cat_id
    
    except (ValueError, TypeError):
        return False, "Category ID must be a valid integer.", None
    except Exception as e:
        return False, f"Database error: {str(e)}", None


# Category name validation: Case-insensitive lookup, returns ID
def validate_category_name(category_name):
    """Validates category by name (case-insensitive), returns category ID."""
    if not category_name or not category_name.strip():
        return False, "Category name cannot be empty.", None
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT category_id FROM categories WHERE LOWER(name) = LOWER(%s)", 
            (category_name.strip(),)
        )
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result is None:
            return False, f"Category '{category_name}' does not exist.", None
        
        return True, "", result[0]
    
    except Exception as e:
        return False, f"Database error: {str(e)}", None


# Description validation: Simple length check
def validate_description(description):
    """Validates description length (max 500 characters)."""
    if description is None:
        description = ""
    
    desc_str = str(description).strip()
    
    if len(desc_str) > 500:
        return False, "Description is too long. Maximum 500 characters.", None
    
    return True, "", desc_str


# Expense ID validation: Verifies existence for update/delete
def validate_expense_id(expense_id):
    """Validates expense ID exists in database."""
    try:
        exp_id = int(expense_id)
        
        if exp_id <= 0:
            return False, "Expense ID must be a positive number.", None
        
        # Database existence check
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT expense_id FROM expenses WHERE expense_id = %s", (exp_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        if result is None:
            return False, f"Expense ID {exp_id} does not exist.", None
        
        return True, "", exp_id
    
    except (ValueError, TypeError):
        return False, "Expense ID must be a valid integer.", None
    except Exception as e:
        return False, f"Database error: {str(e)}", None


# Year/Month validation for reports
def validate_year(year_str):
    """Validates year range (1900 to current year + 1)."""
    try:
        year = int(year_str)
        current_year = datetime.now().year
        
        if year < 1900 or year > current_year + 1:
            return False, f"Year must be between 1900 and {current_year + 1}.", None
        
        return True, "", year
    
    except (ValueError, TypeError):
        return False, "Invalid year. Please enter a valid number.", None


def validate_month(month_str):
    """Validates month range (1-12)."""
    try:
        month = int(month_str)
        
        if month < 1 or month > 12:
            return False, "Month must be between 1 and 12.", None
        
        return True, "", month
    
    except (ValueError, TypeError):
        return False, "Invalid month. Please enter a number between 1 and 12.", None


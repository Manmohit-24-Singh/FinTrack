"""
Expense CRUD operations with dynamic filtering support.
Key Pattern: Parameterized queries prevent SQL injection.
"""
from db import get_connection


# CREATE - Insert new expense record
def add_expense(amount, category_id, expense_date, description):
    """Adds expense with parameterized query for security."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO expenses (amount, category_id, expense_date, description)
               VALUES (%s, %s, %s, %s)"""
    cursor.execute(query, (amount, category_id, expense_date, description))
    conn.commit()
    cursor.close()
    conn.close()


# READ - Retrieve expenses with optional multi-criteria filtering
def view_expenses(date_from=None, date_to=None, category_id=None, min_amount=None, max_amount=None):
    """
    Flexible query builder: Dynamically constructs WHERE clause based on provided filters.
    Uses LEFT JOIN to include category names in results.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Base query with JOIN to get category names
    query = """
        SELECT e.expense_id, e.amount, c.name AS category, e.expense_date, e.description
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.category_id
        WHERE 1=1
    """
    params = []
    
    # Dynamic filter building - only add conditions if parameters provided
    if date_from:
        query += " AND e.expense_date >= %s"
        params.append(date_from)
    if date_to:
        query += " AND e.expense_date <= %s"
        params.append(date_to)
    if category_id:
        query += " AND e.category_id = %s"
        params.append(category_id)
    if min_amount:
        query += " AND e.amount >= %s"
        params.append(min_amount)
    if max_amount:
        query += " AND e.amount <= %s"
        params.append(max_amount)
    
    query += " ORDER BY e.expense_date DESC"
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


# UPDATE - Modify existing expense
def update_expense(expense_id, amount, category_id, expense_date, description):
    """Updates all fields of an expense record."""
    conn = get_connection()
    cursor = conn.cursor()
    query = """UPDATE expenses 
               SET amount=%s, category_id=%s, expense_date=%s, description=%s
               WHERE expense_id=%s"""
    cursor.execute(query, (amount, category_id, expense_date, description, expense_id))
    conn.commit()
    cursor.close()
    conn.close()


# DELETE - Remove expense record
def delete_expense(expense_id):
    """Deletes expense by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE expense_id=%s", (expense_id,))
    conn.commit()
    cursor.close()
    conn.close()


# Helper function for updates - retrieves current expense details
def get_expense_by_id(expense_id):
    """
    Fetches single expense with JOIN for displaying current values during updates.
    Returns tuple: (id, amount, category_name, category_id, date, description)
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.expense_id, e.amount, c.name AS category, e.category_id, e.expense_date, e.description
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.category_id
        WHERE e.expense_id = %s
    """, (expense_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

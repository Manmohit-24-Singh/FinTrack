from db import get_connection

def add_expense(amount, category_id, expense_date, description):
    conn = get_connection()
    cursor = conn.cursor()
    query = """INSERT INTO expenses (amount, category_id, expense_date, description)
               VALUES (%s, %s, %s, %s)"""
    cursor.execute(query, (amount, category_id, expense_date, description))
    conn.commit()
    cursor.close()
    conn.close()

def view_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.expense_id, e.amount, c.name AS category, e.expense_date, e.description
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.category_id
        ORDER BY e.expense_date DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def update_expense(expense_id, amount, category_id, expense_date, description):
    conn = get_connection()
    cursor = conn.cursor()
    query = """UPDATE expenses 
               SET amount=%s, category_id=%s, expense_date=%s, description=%s
               WHERE expense_id=%s"""
    cursor.execute(query, (amount, category_id, expense_date, description, expense_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE expense_id=%s", (expense_id,))
    conn.commit()
    cursor.close()
    conn.close()

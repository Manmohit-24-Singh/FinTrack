from db import get_connection

def monthly_report(year, month):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT c.name AS category, SUM(e.amount) AS total
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.category_id
        WHERE EXTRACT(YEAR FROM e.expense_date)=%s AND EXTRACT(MONTH FROM e.expense_date)=%s
        GROUP BY c.name
        ORDER BY total DESC
    """
    cursor.execute(query, (year, month))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

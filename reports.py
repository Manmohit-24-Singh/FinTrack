"""
Reporting module: Generates spending summaries using SQL aggregation.
Key Pattern: GROUP BY with SUM for category-wise totals.
"""
from db import get_connection


def monthly_report(year, month):
    """
    Generates top 3 expense categories for a given month.
    Uses SQL aggregation (GROUP BY + SUM) for efficient calculation.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate date range: first day of month to first day of next month
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_date = f"{year+1}-01-01"  # Wrap to next year
    else:
        end_date = f"{year}-{month+1:02d}-01"
    
    # Aggregation query: SUM grouped by category, ordered by total spending
    # Uses >= and < for precise month boundaries (excludes next month's first day)
    query = """
        SELECT c.name AS category, SUM(e.amount) AS total
        FROM expenses e
        LEFT JOIN categories c ON e.category_id = c.category_id
        WHERE e.expense_date >= %s AND e.expense_date < %s
        GROUP BY c.name
        ORDER BY total DESC
    """
    cursor.execute(query, (start_date, end_date))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Return top 3 categories (Python slicing instead of SQL LIMIT)
    return results[:3]

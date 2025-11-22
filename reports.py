from db import get_connection

def monthly_report(year, month):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Calculate start and end dates for the month
    # Note: This simple logic assumes valid months. 
    # For a robust app, use calendar.monthrange, but we keep it simple.
    start_date = f"{year}-{month:02d}-01"
    if month == 12:
        end_date = f"{year+1}-01-01"
    else:
        end_date = f"{year}-{month+1:02d}-01"

    # Query using basic SQL commands from the allowed list
    # We use BETWEEN or >= AND < logic. 
    # The user list has BETWEEN, <, >=. 
    # "BETWEEN '2002-01-01' AND '2003-01-01'" is inclusive.
    # To be precise with months, >= start AND < next_month_start is safer, 
    # but BETWEEN is requested. Let's use >= AND < as it uses allowed symbols.
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
    
    # Return only top 3 (simulating LIMIT 3)
    return results[:3]

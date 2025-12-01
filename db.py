"""
Database layer: Handles PostgreSQL connections and schema initialization.
Key Pattern: Centralized connection management for all database operations.
"""
import psycopg2


# Connection factory - returns new connection for each operation
def get_connection():
    """Establishes PostgreSQL connection with configured credentials."""
    return psycopg2.connect(
        host="localhost",
        database="expense_tracker",
        user="oop",
        password="ucalgary",
        port=5433
    )


# Schema initialization - creates tables and seeds default categories
def init_db():
    """
    Database setup: Creates schema and seeds default categories.
    Uses CREATE TABLE IF NOT EXISTS for idempotency.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Categories table: Stores expense categories with unique names
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    
    # Expenses table: Foreign key relationship to categories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id SERIAL PRIMARY KEY,
            amount DECIMAL(10, 2) NOT NULL,
            category_id INTEGER REFERENCES categories(category_id),
            expense_date DATE NOT NULL,
            description TEXT
        );
    """)
    
    # Seed default categories if they don't exist
    default_categories = ["Food", "Transportation", "Utilities", "Entertainment", "Rent", "Groceries", "Misc"]
    for category in default_categories:
        cursor.execute("SELECT category_id FROM categories WHERE name = %s", (category,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category,))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database initialized and tables created.")


# Category lookup functions - support both ID and name-based queries
def get_category_by_name(name):
    """Case-insensitive category lookup by name. Returns (id, name) tuple."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, name FROM categories WHERE LOWER(name) = LOWER(%s)", (name,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def get_category_by_id(category_id):
    """Retrieves category details by ID. Returns (id, name) tuple."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, name FROM categories WHERE category_id = %s", (category_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def list_categories():
    """Returns all categories sorted alphabetically for user selection."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, name FROM categories ORDER BY name")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def add_category(name):
    """
    Adds custom category with duplicate prevention.
    Returns (success_bool, result) where result is category_id or error message.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Prevent duplicates with case-insensitive check
    cur.execute("SELECT category_id FROM categories WHERE LOWER(name) = LOWER(%s)", (name,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return False, "Category already exists."
    
    # RETURNING clause gets the auto-generated ID
    cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING category_id", (name,))
    category_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return True, category_id


def expense_exists(expense_id):
    """Validates expense ID existence for update/delete operations."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT expense_id FROM expenses WHERE expense_id = %s", (expense_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="expense_tracker",
        user="oop",       
        password="ucalgary",
        port=5433         
    )

def init_db():
    """Creates the necessary tables if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Categories Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    """)
    
    # Create Expenses Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id SERIAL PRIMARY KEY,
            amount DECIMAL(10, 2) NOT NULL,
            category_id INTEGER REFERENCES categories(category_id),
            expense_date DATE NOT NULL,
            description TEXT
        );
    """)
    
    # Seed Default Categories
    default_categories = ["Food", "Transportation", "Utilities", "Entertainment", "Rent", "Groceries", "Misc"]
    for category in default_categories:
        # Check if category exists using basic SQL
        cursor.execute("SELECT category_id FROM categories WHERE name = %s", (category,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category,))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database initialized and tables created.")

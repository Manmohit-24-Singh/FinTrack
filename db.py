# Import PostgreSQL adapter for Python to enable database connectivity
import psycopg2

def get_connection():
    """
    Establishes a connection to the PostgreSQL database.
    
    Returns:
        connection: A psycopg2 connection object that can be used to interact with the database
    
    Note:
        Connection parameters are hardcoded for local development
        In production, use environment variables for security
    """
    # Create and return a database connection with the following parameters:
    return psycopg2.connect(
        host="localhost",        # Database server location (local machine)
        database="expense_tracker",  # Name of the database to connect to
        user="oop",              # PostgreSQL username for authentication
        password="ucalgary",     # Password for the user
        port=5433                # PostgreSQL port number
    )

def init_db():
    """
    Initializes the database by creating the expenses table if it doesn't already exist.
    This function is called on application startup to ensure the database schema is ready.
    
    Table Schema:
        - id: Auto-incrementing primary key
        - amount: Expense amount (must not be empty)
        - category: Expense category like Food, Rent, etc. (required)
        - date: Date of the expense (required)
        - description: Optional text description of the expense
    """
    # Establish connection to the PostgreSQL database
    conn = get_connection()
    
    # Create a cursor object to execute SQL commands
    cur = conn.cursor()
    
    # Execute CREATE TABLE command (only creates if table doesn't exist)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,        -- Auto-incrementing unique identifier for each expense
            amount REAL NOT NULL,         -- Expense amount (decimal number, required)
            category TEXT NOT NULL,       -- Category name (required field)
            date DATE NOT NULL,           -- Date when expense occurred (required)
            description TEXT              -- Optional details about the expense
        );
    """)
    
    # Commit the transaction to save changes to the database
    conn.commit()
    
    # Close the database connection to free up resources
    conn.close()
    
    # Print confirmation message to user
    print("✅ Database ready.")
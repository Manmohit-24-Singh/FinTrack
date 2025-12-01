# Import datetime for date handling and validation
from datetime import datetime
# Import database connection function from db module
from db import get_connection

# --- INPUT VALIDATION ---
# These functions ensure user input is valid before saving to database

def get_valid_float(prompt):
    """
    Prompts user for a positive decimal number and validates the input.
    Loops until valid input is provided.
    
    Args:
        prompt: String to display when asking for input
    
    Returns:
        float: A valid positive number entered by the user
    """
    # Infinite loop until valid input is received
    while True:
        try:
            # Attempt to convert user input to float
            value = float(input(prompt))
            
            # Check if the number is positive (expenses can't be negative or zero)
            if value <= 0:
                print("❌ Amount must be positive.")
                continue  # Ask again
            
            # Valid input received, return the value
            return value
        except ValueError:
            # User entered non-numeric input (e.g., "abc")
            print("❌ Invalid input. Please enter a number (e.g., 12.50).")

def get_valid_date(prompt):
    """
    Prompts user for a date in YYYY-MM-DD format.
    If user presses Enter without typing, defaults to today's date.
    
    Args:
        prompt: String to display when asking for date input
    
    Returns:
        str: Valid date string in YYYY-MM-DD format
    """
    # Loop until valid date is entered
    while True:
        # Get user input and remove leading/trailing whitespace
        date_str = input(prompt).strip()
        
        # If user pressed Enter without typing, use today's date
        if not date_str:
            return datetime.now().strftime("%Y-%m-%d")
        
        try:
            # Attempt to parse the date to validate format
            datetime.strptime(date_str, "%Y-%m-%d")
            # If parsing succeeds, return the valid date string
            return date_str
        except ValueError:
            # Date format is incorrect, show error and ask again
            print("❌ Invalid format. Use YYYY-MM-DD.")

# --- CORE FEATURES ---
# Main application functionality for managing expenses

def add_expense():
    """
    Interactive function to capture expense details from user and save to database.
    Validates all inputs before saving to ensure data integrity.
    
    Workflow:
        1. Prompt for amount (validated as positive number)
        2. Prompt for category (required, cannot be empty)
        3. Prompt for date (defaults to today if not provided)
        4. Prompt for description (optional)
        5. Save to database using parameterized query (prevents SQL injection)
    """
    print("\n--- Add Expense ---")
    
    # Get and validate amount (must be positive number)
    amount = get_valid_float("Amount: $")
    
    # Get category and ensure it's not empty
    category = input("Category (e.g., Food, Rent): ").strip()
    while not category:
        print("Category cannot be empty.")
        category = input("Category: ").strip()
    
    # Get date with today's date as default option
    date = get_valid_date(f"Date [Enter for {datetime.now().date()}]: ")
    
    # Get optional description (can be empty)
    desc = input("Description (optional): ")

    # Establish database connection
    conn = get_connection()
    
    # Create cursor for executing SQL commands
    cur = conn.cursor()
    
    # Execute parameterized INSERT query to prevent SQL injection attacks
    # %s placeholders are safely replaced with actual values
    cur.execute(
        "INSERT INTO expenses (amount, category, date, description) VALUES (%s, %s, %s, %s)",
        (amount, category, date, desc)  # Tuple of values to insert
    )
    
    # Commit transaction to save changes permanently
    conn.commit()
    
    # Close database connection
    conn.close()
    
    # Confirm successful save to user
    print("✅ Saved!")

def monthly_report():
    """
    Generates a report showing the top 3 spending categories.
    Uses SQL aggregation to sum expenses by category and sort by total amount.
    
    Displays:
        - Top 3 categories by total spending
        - Amount spent in each category
        - Total amount across all top 3 categories
    """
    print("\n--- Monthly Report ---")
    
    # Establish database connection
    conn = get_connection()
    
    # Create cursor for executing queries
    cur = conn.cursor()
    
    # SQL query to aggregate expenses by category
    query = """
        SELECT category, SUM(amount) as total   -- Sum all amounts for each category
        FROM expenses                           -- From the expenses table
        GROUP BY category                       -- Group rows by category name
        ORDER BY total DESC                     -- Sort by total (highest first)
        LIMIT 3                                 -- Only show top 3 results
    """
    
    # Execute the query
    cur.execute(query)
    
    # Fetch all results as a list of tuples [(category1, total1), (category2, total2), ...]
    results = cur.fetchall()
    
    # Close database connection
    conn.close()

    # Check if any expenses exist in database
    if not results:
        print("No expenses found.")
        return  # Exit function early

    # Display header
    print(f"\n🔥 Top 3 Categories:")
    
    # Initialize variable to track total spending across top 3 categories
    total_spent = 0
    
    # Iterate through results with rank numbers (starting from 1)
    for rank, (cat, total) in enumerate(results, 1):
        # Display each category with its rank and total amount
        print(f"  {rank}. {cat}: ${total:.2f}")  # .2f formats to 2 decimal places
        
        # Add to running total
        total_spent += total
    
    # Display the combined total of top 3 categories
    print(f"\nTotal Tracked: ${total_spent:.2f}")

def view_all_expenses():
    """
    Retrieves and displays all expenses from the database in a formatted table.
    Shows complete expense history sorted by date (most recent first).
    
    Displays:
        - Expense ID, date, category, amount, and description
        - Total amount spent across all expenses
        - Count of total expenses
    """
    print("\n--- All Expenses ---")
    
    # Establish database connection
    conn = get_connection()
    
    # Create cursor for query execution
    cur = conn.cursor()
    
    # SQL query to retrieve all expense records
    query = """
        SELECT id, date, category, amount, description   -- Select all relevant columns
        FROM expenses                                    -- From expenses table
        ORDER BY date DESC, id DESC                      -- Sort by date (newest first), then by ID
    """
    
    # Execute the SELECT query
    cur.execute(query)
    
    # Fetch all rows as list of tuples
    results = cur.fetchall()
    
    # Close database connection
    conn.close()

    # Check if any expenses exist
    if not results:
        print("No expenses found.")
        return  # Exit function if no data

    # Print formatted table header with column alignment
    # <5 = left-aligned with width 5, >10 = right-aligned with width 10
    print(f"\n{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':>10} {'Description':<30}")
    
    # Print separator line (75 dashes)
    print("-" * 75)
    
    # Initialize total expense accumulator
    total_spent = 0
    
    # Iterate through each expense record
    for expense_id, date, category, amount, description in results:
        # Truncate long descriptions to fit in table (27 chars + "..." = 30 chars)
        desc_display = (description[:27] + '...') if description and len(description) > 30 else (description or '')
        
        # Print expense row with proper alignment and formatting
        print(f"{expense_id:<5} {str(date):<12} {category:<15} ${amount:>9.2f} {desc_display:<30}")
        
        # Add amount to running total
        total_spent += amount
    
    # Print bottom separator line
    print("-" * 75)
    
    # Display total amount spent (aligned with Amount column)
    print(f"{'Total:':<33} ${total_spent:>9.2f}")
    
    # Display count of expenses
    print(f"\nTotal Expenses: {len(results)}")
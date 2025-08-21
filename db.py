import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="expense_tracker",
        user="oop",       
        password="ucalgary",
        port=5433         
    )

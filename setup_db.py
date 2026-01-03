import pymysql
from database import create_tables, init_db

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server (without specifying database)
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='9948318650'
        )
        
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS demo_fast")
        print("Database 'demo_fast' created or already exists")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

if __name__ == "__main__":
    print("Setting up database...")
    
    # Create database
    if create_database():
        print("Database setup successful")
        
        # Create tables and initialize data
        try:
            create_tables()
            init_db()
            print("Tables created and sample data inserted successfully")
        except Exception as e:
            print(f"Error setting up tables: {e}")
    else:
        print("Failed to create database")
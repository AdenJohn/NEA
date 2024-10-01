import psycopg2
from psycopg2 import sql
from psycopg2 import errors

def create_tables(): 
    try: 
        conn = psycopg2.connect(
            host = "localhost", 
            database = "NEA", 
            user = "postgres", 
            password="1510",
            port = "5432",)

        cursor = conn.cursor()

        #creating the users table
        create_user_table = """CREATE TABLE IF NOT EXISTS Users(
            user_id SERIAL PRIMARY KEY,
            employee_code VARCHAR(50) UNIQUE NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL, 
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            password_salt VARCHAR(255) NOT NULL
            );"""
            
        cursor.execute(create_user_table)
        
        #creating the products table
        create_inventory_table = """CREATE TABLE IF NOT EXISTS Inventory(
            product_id SERIAL PRIMARY KEY, 
            SKU VARCHAR(50) UNIQUE NOT NULL, 
            name VARCHAR(255) NOT NULL, 
            price DECIMAL(10, 2) NOT NULL, 
            quantity INTEGER NOT NULL 
        );"""

        cursor.execute(create_inventory_table)

        create_clients_table = """CREATE TABLE IF NOT EXISTS Clients(
            client_id SERIAL PRIMARY KEY, 
            client_name VARCHAR(250) NOT NULL,
            client_phone INT UNIQUE NOT NULL,
            client_email VARCHAR(150) UNIQUE NOT NULL,
            street_address VARCHAR(100) NOT NULL, 
            city VARCHAR(100) NOT NULL,
            region VARCHAR(100) NOT NULL, 
            postal_code VARCHAR(100) NOT NULL, 
            country VARCHAR(100) NOT NULL, 
            full_address TEXT
        );"""

        cursor.execute(create_clients_table)

        conn.commit()
        cursor.close()
        conn.close()
        print("Tables created successfully")
        
    except psycopg2.Error as error:
        print(f"Found this error while trying to connect: {error}") 
        
if __name__ == "__main__": 
    create_tables()
        


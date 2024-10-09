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
            client_email VARCHAR(150) UNIQUE NOT NULL,
            client_phone INT UNIQUE NOT NULL,
            street_address VARCHAR(100), 
            city VARCHAR(100) NOT NULL,
            region VARCHAR(100), 
            postal_code VARCHAR(100), 
            country VARCHAR(100) NOT NULL, 
            full_address TEXT
        );"""

        cursor.execute(create_clients_table)

        create_orders_table = """CREATE TABLE IF NOT EXISTS Orders(
            order_id SERIAL PRIMARY KEY, 
            client_id INT REFERENCES Clients(client_id),
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            total_price DECIMAL(10,2), 
            order_status VARCHAR(50) DEFAULT 'PENDING',
            payment_status VARCHAR(50) DEFAULT 'Unpaid', 
            delivery_address TEXT, 
            estimated_deliverydate DATE, 
            delivery_date DATE);"""
        
        cursor.execute(create_orders_table)

        create_orderitems_table = """CREATE TABLE IF NOT EXISTS OrderItems(
            order_item_id SERIAL PRIMARY KEY,
            order_id INT REFERENCES Orders(order_id) ON DELETE CASCADE, 
            product_id INT REFERENCES Inventory(product_id),
            product_quantity INT NOT NULL, 
            item_total_price DECIMAL(10,2) NOT NULL);"""
        
        cursor.execute(create_orderitems_table)

        conn.commit()
        cursor.close()
        conn.close()
        print("Tables created successfully")
        
    except psycopg2.Error as error:
        print(f"Found this error while trying to connect: {error}") 
        
if __name__ == "__main__": 
    create_tables()
        

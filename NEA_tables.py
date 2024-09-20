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
            port = "5432",
        )
        cursor = conn.cursor()

        #creating the users table
        create_user_table = """CREATE TABLE IF NOT EXISTS Users(
            user_id SERIAL PRIMARY KEY,
            employee_code VARCHAR(50) UNIQUE NOT NULL,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL, 
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
            );"""
            
        cursor.execute(create_user_table)
        conn.commit()
        cursor.close()
        conn.close()
        print("Tables created successfully")
        
    except psycopg2.Error as error:
        print(f"Found this error while trying to connect: {error}") 
        
if __name__ == "__main__": 
    create_tables()
        
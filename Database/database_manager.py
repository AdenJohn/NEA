import psycopg2
from .database_connection import get_connection

class DatabaseManager: 
    def __init__(self): 
        self.conn = psycopg2.connect("NEA", "localhost", "postgres", "1510", 5432)

    def close_connection(self): 

        if self.conn: 
            self.conn.close()
            self.conn = None

    def execute_query(self, query, paramaters=None): 

        if not self.conn: 
            raise Exception("Database connection not established")
        
        try: 
            with self.conn.cursor() as cursor: 
                cursor.execute(query, paramaters)
                self.conn.commit()

        except psycopg2.Error as error:
            self.conn.rollback()
            print(f"Error while executing query {error}")


 

            


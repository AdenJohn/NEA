import psycopg2


def get_connection(dbname, host, user, password, port):

    try: 
        connection = psycopg2.connect(
            dbname = dbname, 
            host = host, 
            user = user, 
            password = password,
            port = port)
        print("connection successful")
        
    except Exception as error: 
        print(f"Error {error}")

from Database.database_manager import DatabaseManager
from Models.Clients import Clients

class ClientManager: 
    def __init__(self, db_manager: DatabaseManager): 
        self.db_manager = db_manager

    def add_client(self, client_name, client_email, client_phone, address_line, city, country): 
        full_address = f"{address_line}, {city}, {country}"
        query = """INSERT INTO Client(client_name, client_email, client_phone, address_line, city, country, full_address) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        paramaters = (client_name, client_email, client_phone, address_line, city, country, full_address)

        self.db_manager.execute_query(query, paramaters)

    def update_client(self, client_id, new_client_name=None, new_client_email=None, new_client_phone=None, new_address_line=None, new_city=None, new_country=None):

        query = """UPDATE Client SET
            client_name = COALESCE(%s, client_name),
            client_email = COALESCE(%s, client_email),
            client_phone = COALESCE(%s, client_phone), 
            address_line = COALESCE(%s, address_line),
            city = COALESCE(%s, city),
            country = COALESCE(%s, country), 
            full_address = COALESCE(%s, full_address) WHERE client_id = %s"""

        new_full_address = f"{new_address_line}, {new_city}, {new_country}"
        paramaters  = (new_client_name, new_client_email, new_client_phone, new_address_line, new_city, new_country, new_full_address, client_id)
        self.db_manager.execute_query(query, paramaters)

    def delete_client(self, client_id): 
        query = """DELETE FROM Client WHERE client_id = %s"""
        self.db_manager.execute_query(query, (client_id,))

    def get_all_clients(self): 
        query = """SELECT client_id, client_name, client_email, client_phone, address_line, city, country, full_address FROM Client"""

        all_clients = self.db_manager.execute_query(query)
        clients = []
        if all_clients:
            for row in all_clients: 
                client = Clients(client_id=row[0], 
                                 client_name=row[1],
                                 client_email=row[2],
                                 client_phone=row[3],
                                 address_line=row[4],
                                 city=row[5],
                                 country=row[6],
                                 full_address=[7])
                
                clients.append(client)

            return clients
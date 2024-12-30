from Database.database_manager import DatabaseManager
from Models.Users import Users
from KeyAlgorithms.Hashing import HashFunctions

class UserManager: 
    def __init__(self, db_manager: DatabaseManager, hashing: HashFunctions):
        self.dbmanager = db_manager
        self.hashing = hashing

    def register_user(self, employee_code, first_name, last_name, email, register_password): 
        
        register_query = """INSERT INTO Users(employee_code, first_name, last_name, email, password_hash, password_salt)VALUES(%s, %s, %s, %s, %s, %s)"""
        password_salt = self.hashing.generate_salt()
        password_hash = self.hashing.hash_password(register_password, password_salt)

        register_paramaters = (employee_code, first_name, last_name, email, password_hash, password_salt.hex())

        try: 
            self.dbmanager.execute_query(register_query, register_paramaters)
            return True
        except Exception as error: 
            return False


    def login_user(self, employee_code, login_password):

        login_query = """SELECT password_hash, password_salt from Users WHERE employee_code = %s"""
        result = self.dbmanager.execute_query(login_query, (employee_code,))
        row = result[0]

        password_hash, password_salt = row[0], row[1]

        return self.hashing.verify_password(password_hash, password_salt, login_password)

        
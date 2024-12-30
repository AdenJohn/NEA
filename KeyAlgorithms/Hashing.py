import os

class HashFunctions: 

    def generate_salt(self): 

        return os.urandom(16)
    
    def hash_password(self, password, salt): 

        password_bytes = password.encode('utf-8')
        hashed_bytes = bytearray()

        for i in range(len(password_bytes)): 
            hashed_bytes.append(password_bytes[i] ^ salt[i % len(salt)])

        return hashed_bytes.hex()
    
    def verify_password(self, stored_password, salt, login_password): 

        login_hash = self.hash_password(login_password, salt)
        return login_hash == stored_password
    


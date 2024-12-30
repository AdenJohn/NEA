class Users: 
    def __init__(self, user_id=None, employee_code=None, first_name="", last_name="", password_hash="", password_salt=""): 

        self.user_id = user_id
        self.employee_code = employee_code
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash
        self.password_salt = password_salt

    def get_name(self): 
        return f"{self.first_name} {self.last_name}"
    

        
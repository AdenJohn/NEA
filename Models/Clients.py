class Clients: 
    def __init__(self, client_id = None, client_name="", client_email="", client_phone="", address_line="", city="", country="", full_address=""): 

        self.client_id = client_id
        self.client_name = client_name
        self.client_email = client_email
        self.client_phone = client_phone
        self.address_line = address_line
        self.city = city
        self.country = country
        full_address = f"{self.address_line}, {self.city}, {self.country}"
        self.full_address = full_address



    

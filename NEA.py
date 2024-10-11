import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import psycopg2
from datetime import datetime
from psycopg2 import sql
from tkinter import messagebox
import NEA_tables


#class for database management and psycopg2/SQL related things, it has connection to the local server and execution of commands(queries)
class DatabaseManager: 
    def __init__(self, host="localhost", database="NEA", user="postgres", password="1510", port="5432"): 
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = self.connect_to_database()

    def connect_to_database(self): 
        try: 
            conn = psycopg2.connect(
                host= self.host, 
                database= self.database, 
                user= self.user,
                password= self.password,
                port= self.port)
            return conn
        except psycopg2.Error as error:
            print("Connection Error", f"Encountered: {error}")
            return None
        
    def execute_command(self, query, paramaters=()): 
        try: 
            cursor = self.conn.cursor()
            cursor.execute(query, paramaters)
            self.conn.commit()
            return cursor
        except psycopg2.Error as error: 
            self.conn.rollback()
            print("Error", f"Query execution error: {error}")
            raise error

class UserManager: 
    def __init__(self, database_manager, password_hasher):
        self.database_manager = database_manager
        self.password_hasher = password_hasher

    def register_user(self, employee_code, first_name, last_name, email, password): 
        salt = self.password_hasher.generating_salt()
        hashed_password = self.password_hasher.hash(password, salt)

        register_query = """INSERT INTO Users(employee_code, first_name, last_name, email, password_hash, password_salt) VALUES(%s, %s, %s, %s, %s, %s)"""
        paramaters = (employee_code, first_name, last_name, email, hashed_password, salt.hex())

        try: 
            self.database_manager.execute_command(register_query, paramaters)
        except psycopg2.Error as error:
            messagebox.showerror("Error", f"Registration error: {error}")
            print(f"Registration error: {error}")

    def authenticate_user(self, employee_code, password): 
        login_query = """SELECT first_name, last_name, password_hash, password_salt FROM Users WHERE employee_code = %s"""
        
        try: 
            cursor = self.database_manager.execute_command(login_query, (employee_code,))
            user = cursor.fetchone()
            if user: 
                first_name, last_name, registered_password, stored_salt = user
                stored_salt = bytes.fromhex(stored_salt)
            if self.password_hasher.verify_password(password, stored_salt, registered_password): 
                return first_name, last_name
            return None
        except Exception as error:
            print(f"Login Error, {error}")
            return None
        
class PasswordHasher: 
    def __init__(self, salt_length=16): 
        self.salt_length = salt_length

    def generating_salt(self): 
        return os.urandom(self.salt_length)
    
    def hash(self, password, salt): 
        
        password_bytes = password.encode('utf-8')
        hashed_bytes = bytearray()

        for i in range(len(password_bytes)): 
            hashed_bytes.append(password_bytes[i] ^ salt[i % len(salt)])
        
        return ''.join(format(byte, '02x') for byte in hashed_bytes)

    def verify_password(self, login_password, stored_salt, registered_password): 
        new_hash = self.hash(login_password, stored_salt)
        return new_hash == registered_password

class InventoryManager: 
    def __init__(self, database_manager): 
        self.database_manager = database_manager

    def add_product(self, sku, name, price, quantity): 
        add_product_query = """INSERT INTO Inventory(SKU, name, price, quantity) VALUES(%s, %s, %s, %s)"""
        parameters = (sku, name, price, quantity)

        try: 
            self.database_manager.execute_command(add_product_query, parameters)
        except psycopg2.errors.UniqueViolation:
            print("Product with SKU already exists")
        except Exception as error: 
            print(f"Error adding product: {error}")

    def get_inventory(self): 
        get_inventory_query = """SELECT product_id, SKU, name, price, quantity FROM Inventory"""

        try:
            cursor = self.database_manager.execute_command(get_inventory_query)
            return cursor.fetchall()
        except Exception as error: 
            messagebox.showerror("Error", f"Error retrieving inventory: {error}")
            return []
        
    def update_product(self, sku, name, price, quantity, original_sku): 
        update_product_query = """UPDATE Inventory SET SKU = %s, name = %s, price = %s, quantity =%s WHERE SKU = %s"""

        try: 
            price = float(price)
            quantity = int(quantity)
        except ValueError: 
            raise ValueError("Invalid format for price or quantity")
        
        parameters = (str(sku), str(name), float(price), int(quantity), str(original_sku))

        try: 
            self.database_manager.execute_command(update_product_query, parameters)
            messagebox.showinfo("Update Product", f"Product Updated Successfully")
        except Exception as error: 
            messagebox.showerror("Error", f"Error while updating products: {error}")

class ClientManager: 
    def __init__(self, database_manager): 
        self.database_manager = database_manager

    def add_client(self, name, email, phone, street, city, region, postcode, country):
        full_address = f"{street}, {city}, {region}, {postcode}, {country}"

        client_add_query = """INSERT INTO Clients(client_name, client_email, client_phone, street_address, city, region, postal_code, country, full_address)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        paramaters = (name, email, phone, street, city, region, postcode, country, full_address)

        try: 
            self.database_manager.execute_command(client_add_query, paramaters)
            messagebox.showinfo("Success", "Added Client to database")
        except Exception as error: 
            messagebox.showerror("Error", f"Encountered this error {error}")

    def get_clients(self): 
        get_client_query = """SELECT client_id, client_name, client_email, client_phone, street_address, city, region, postal_code, country, full_address FROM Clients"""

        try: 
            cursor = self.database_manager.execute_command(get_client_query)
            return cursor.fetchall()
        except Exception as error: 
            messagebox.showerror("Error", f"Error retrieving inventory: {error}")
            return []

    def update_clients(self, name, email, phone, street, city, region, postcode, country, full_address, original_email): 
        update_client_query = """UPDATE Clients SET client_name = %s, client_email = %s, client_phone = %s, street_address = %s, city = %s, region =%s, postal_code=%s, country=%s, full_address = %s WHERE client_email = %s"""

        paramaters = (name, email, phone, street, city, region, postcode, country, full_address, original_email)

        try: 
            self.database_manager.execute_command(update_client_query, paramaters)
            messagebox.showinfo("Update Client", f"Client Successfully Updated")
        except Exception as error: 
            messagebox.showerror("Error", f"Encountered this error {error}")

class OrdersManager: 
    def __init__(self, database_manager): 
        self.database_manager = database_manager

    def add_order(self, client_id, total_price, delivery_address, estimated_deliverydate, payment_status, order_status):

        add_order_query = """INSERT INTO Orders(client_id, total_price, delivery_address, estimated_deliverydate, payment_status, order_status)VALUES(%s,%s,%s,%s,%s,%s) RETURNING order_id"""
        paramaters = (client_id, total_price, delivery_address, estimated_deliverydate, payment_status, order_status)

        try: 
            cursor = self.database_manager.execute_command(add_order_query, paramaters)
            order_id = cursor.fetchone()[0]
            messagebox.showinfo("SUCCESS", f"Order {order_id} has been successfully added")
            return order_id
        except Exception as error: 
            messagebox.showerror("", f"Error: {error}")
            return None
        
    def add_order_item(self, order_id, product_id, product_quantity, item_total_price): 
        add_item_query = """INSERT INTO OrderItems(order_id, product_id, product_quantity, item_total_price) VALUES(%s,%s,%s,%s);"""
        paramaters = (order_id, product_id, product_quantity, item_total_price)

        self.database_manager.execute_command(add_item_query, paramaters)

    def order_with_items(self, client_id, delivery_address, estimated_deliverydate, payment_status, order_status, items): 
        
        total_price = sum(item[2] for item in items)

        order_id = self.add_order(client_id, total_price, delivery_address, estimated_deliverydate, payment_status, order_status)

        for product_id, product_quantity, item_total_price in items: 
            self.add_order_item(order_id, product_id, product_quantity, item_total_price)

        return order_id

    def show_all_orders(self): 
        show_orders_query = """SELECT order_id, client_id, order_date, total_price, estimated_deliverydate, order_status FROM Orders ORDER BY order_id;"""

        try: 
            cursor = self.database_manager.execute_command(show_orders_query)
            return cursor.fetchall()
        except Exception as error: 
            messagebox.showerror("Error", f"Error {error}")
            return[]
        
    def get_all_products(self): 

        get_products_query = """SELECT product_id, name, price FROM Inventory ORDER BY product_id ASC;"""

        cursor = self.database_manager.execute_command(get_products_query)
        return cursor.fetchall()

    def edit_order(self, order_id, new_estimated_deliverydate=None, new_payment_status=None, new_order_status=None): 

        edit_order_query = """UPDATE Orders SET
            estimated_deliverydate = COALESCE(%s, estimated_deliverydate),
            payment_status = COALESCE(%s, payment_status),
            order_status = COALESCE(%s, order_status)
        WHERE order_id= %s"""

        paramaters = (new_estimated_deliverydate, new_payment_status, new_order_status, order_id)

        try: 
            self.database_manager.execute_command(edit_order_query, paramaters)
            messagebox.showinfo("Updated Order")
        except Exception as error: 
            messagebox.showerror("Error", f"Error: {error}")

    def view_order(self, order_id):

        view_order_query = """SELECT o.order_id, o.client_id, o.order_date, o.total_price,
        o.order_status, o.payment_status, o.estimated_deliverydate, o.delivery_date, 
        c.client_name, c.client_email, c.client_phone, c.full_address
        FROM Orders o, Clients c
        WHERE o.client_id = c.client_id AND o.order_id = %s;"""

        cursor = self.database_manager.execute_command(view_order_query, (order_id,))
        return cursor.fetchone()
    
    def delete_order(self, order_id): 
        
        delete_order_query = """DELETE FROM Orders WHERE order_id = %s"""
        self.database_manager.execute_command(delete_order_query, (order_id,))

    def get_all_clients(self): 

        get_all_clients_query = """SELECT client_id, client_name FROM Clients ORDER BY client_id ASC;"""

        try: 
            cursor = self.database_manager.execute_command(get_all_clients_query)
            return cursor.fetchall()
        except Exception as error: 
            messagebox.showerror("Error", f"Error: {error}")
            return []

    def get_client_address(self, client_id):
        get_client_address_query = """SELECT full_address FROM Clients WHERE client_id = %s"""
        cursor = self.database_manager.execute_command(get_client_address_query, (client_id,))
        address = cursor.fetchone()
        return address[0] if address else ""

    def update_inventory_quantity(self, product_id, quantity_sold):
        update_query = """UPDATE Inventory SET quantity = quantity - %s WHERE product_id = %s"""
        self.database_manager.execute_command(update_query, (quantity_sold, product_id))

class Application(ttk.Window): 
    def __init__(self): 
        super().__init__(title="Fashion Match (Sales Order Processing System)")
        self.geometry("900x400")

        self.database_manager = DatabaseManager()
        self.password_hasher = PasswordHasher()
        self.user_manager = UserManager(self.database_manager, self.password_hasher)
        self.inventory_manager = InventoryManager(self.database_manager)
        self.client_manager = ClientManager(self.database_manager)
        self.orders_manager = OrdersManager(self.database_manager)

        if not self.database_manager: 
            messagebox.showerror("Error", "Connection Unsuccessful")
            self.destroy()
        else: 
            self.widgets()

    def widgets(self): 
        for widget in self.winfo_children(): 
            widget.destroy()

        self.label_onboarding_welcome = ttk.Label(self, text="Welcome to Fashion Match, your very own Sales Order Processing System")
        self.label_onboarding_welcome.pack(pady=50)

        self.button_onboarding_register = ttk.Button(self, text="Register", command=self.show_registration_page)
        self.button_onboarding_register.pack(pady=10)

        self.button_onboarding_login = ttk.Button(self, text="Login", command=self.show_login_page)
        self.button_onboarding_login.pack(pady=10)

    def show_registration_page(self): 
        for widget in self.winfo_children(): 
            widget.destroy()

        self.title("Register")
        self.geometry("900x400")

        frame = ttk.Frame(self)
        frame.pack(pady=10)

        self.label_register_empcode = ttk.Label(frame, text="Employee Code")
        self.label_register_empcode.grid(row=0, column=0, pady=10, padx=5, sticky="e")

        self.entry_register_empcode = ttk.Entry(frame)
        self.entry_register_empcode.grid(row=0, column=1, pady=10, padx=5)

        self.label_register_firstname = ttk.Label(frame, text="First Name")
        self.label_register_firstname.grid(row=1, column=0, pady=10, padx=5, sticky="e")

        self.entry_register_firstname = ttk.Entry(frame)
        self.entry_register_firstname.grid(row=1, column=1, pady=10, padx=5)

        self.label_register_lastname = ttk.Label(frame, text="Last Name")
        self.label_register_lastname.grid(row=2, column=0, pady=10, padx=5, sticky="e")

        self.entry_register_lastname = ttk.Entry(frame)
        self.entry_register_lastname.grid(row=2, column=1, pady=10, padx=5)

        self.label_register_email = ttk.Label(frame, text="Email")
        self.label_register_email.grid(row=3, column=0, padx=5, pady=10, sticky="e")

        self.entry_register_email = ttk.Entry(frame)
        self.entry_register_email.grid(row=3, column=1, pady=10, padx=5)

        self.label_register_password = ttk.Label(frame, text="Password")
        self.label_register_password.grid(row=4, column=0, padx=5, pady=10, sticky="e")

        self.entry_register_password = ttk.Entry(frame)
        self.entry_register_password.grid(row=4, column=1, padx=5, pady=10)

        self.button_register_back = ttk.Button(frame, text="Back", command=self.widgets)
        self.button_register_back.grid(row=5, column=0, padx=5, pady=10, sticky="e")

        self.button_register_register = ttk.Button(frame, text="Register", command=self.register_user)
        self.button_register_register.grid(row=5, column=1, padx=5, pady=10, sticky="w")

    def register_user(self): 
        employee_code = self.entry_register_empcode.get().strip()
        first_name = self.entry_register_firstname.get().strip()
        last_name = self.entry_register_lastname.get().strip()
        email = self.entry_register_email.get().strip()
        password = self.entry_register_password.get().strip()


        if not employee_code or not first_name or not last_name or not email or not password: 
            messagebox.showerror("Error", "All Fields are Required")
            return
        
        self.user_manager.register_user(employee_code, first_name, last_name, email, password)
        messagebox.showinfo("Success", "You have been successfully registered")
        self.clear_entrybox()
        self.widgets()

    def clear_entrybox(self):
        self.entry_register_empcode.delete(0, ttk.END) 
        self.entry_register_firstname.delete(0, ttk.END) 
        self.entry_register_lastname.delete(0, ttk.END) 
        self.entry_register_email.delete(0, ttk.END) 
        self.entry_register_password.delete(0, ttk.END) 

    def show_login_page(self): 
        for widget in self.winfo_children(): 
            widget.destroy()

        self.title("Login")
        self.geometry("900x400")

        frame = ttk.Frame(self)
        frame.pack(pady=10)

        self.label_login_empcode = ttk.Label(frame, text="Employee Code")
        self.label_login_empcode.grid(row=0, column=0, pady=10, padx=5, sticky="e")

        self.entry_login_empcode = ttk.Entry(frame)
        self.entry_login_empcode.grid(row=0, column=1, padx=5, pady=10)

        self.label_login_password = ttk.Label(frame, text="Password")
        self.label_login_password.grid(row=1, column=0, padx=5, pady=10, sticky="e")

        self.entry_login_password = ttk.Entry(frame)
        self.entry_login_password.grid(row=1, column=1, pady=10, padx=5)

        self.button_login_back = ttk.Button(frame, text="Back", command=self.widgets)
        self.button_login_back.grid(row=2, column=0, pady=10, padx=5, sticky="e")

        self.button_login_login = ttk.Button(frame, text="Login", command=self.login_user)
        self.button_login_login.grid(row=2, column=1, padx=5, pady=10, sticky="w")

    def login_user(self): 
        employee_code = self.entry_login_empcode.get().strip()
        password = self.entry_login_password.get().strip()

        if not employee_code or not password: 
            messagebox.showerror("Error", "All Fields are Required")
            return
        
        user_data = self.user_manager.authenticate_user(employee_code, password)

        if user_data:
            first_name, last_name = user_data
            messagebox.showinfo("Success", "Login Successful")
            self.show_main_window(first_name, last_name)
        else: 
            messagebox.showerror("Error", "Invalid Credentials, please try again!")

    def show_main_window(self, first_name, last_name): 
        for widget in self.winfo_children(): 
            widget.destroy()

        self.title("Home Page")
        self.geometry("900x400")

        self.navigation_page = ttk.Frame(self)
        self.navigation_page.pack(side=TOP, fill=X)

        self.content_page = ttk.Frame(self)
        self.content_page.pack(fill=BOTH, expand=True)
        
        self.button_main_logout = ttk.Button(self.navigation_page, text="Logout", bootstyle="DANGER", command=self.widgets)
        self.button_main_logout.pack(side=LEFT, pady=10, padx=5)

        self.button_main_home = ttk.Button(self.navigation_page, text="Home", command=lambda: self.show_main_window(first_name, last_name))
        self.button_main_home.pack(side=LEFT, padx=5, pady=10)

        self.label_main_welcome = ttk.Label(self.content_page, text=f"Welcome {first_name} {last_name}")
        self.label_main_welcome.pack(pady=10, padx=5)

        self.button_main_inventory = ttk.Button(self.content_page, text="Inventory", command=self.show_inventory)
        self.button_main_inventory.pack(pady=10, padx=5)

        self.button_main_clients = ttk.Button(self.content_page, text="Clients", bootstyle="SUCCESS", command=self.show_clients)
        self.button_main_clients.pack(padx=5, pady=10)

        self.button_main_orders = ttk.Button(self.content_page, text="Orders", bootstyle="DANGER",command=self.show_order_window)
        self.button_main_orders.pack(padx=5, pady=10)

    def show_inventory(self):
        for widget in self.content_page.winfo_children(): 
            widget.destroy()

        self.title("Inventory")
        self.geometry("900x600")

        self.inventory_search_var = ttk.StringVar()
        inventory_search_frame = ttk.Frame(self.content_page)
        inventory_search_frame.pack(padx=10, pady=10, fill=X)

        self.label_inventory_search = ttk.Label(inventory_search_frame, text="Search Product (SKU or Name):")
        self.label_inventory_search.pack(side=LEFT, padx=(150,5),pady=(80,0))

        self.entry_inventory_search = ttk.Entry(inventory_search_frame, textvariable=self.inventory_search_var, width=30)
        self.entry_inventory_search.pack(side=LEFT, pady=(80,0),padx=5)

        self.button_inventory_search = ttk.Button(inventory_search_frame, text="Search", command=self.search_inventory)
        self.button_inventory_search.pack(side=LEFT, padx=5, pady=(80,0))

        self.button_inventory_clear = ttk.Button(inventory_search_frame, text="Clear", command=self.clear_search)
        self.button_inventory_clear.pack(side=LEFT, padx=5, pady=(80,0))

        columns = ("Product ID", "SKU", "Name", "Price/SQM", "Quantity")
        self.tree_inventory_list = ttk.Treeview(self.content_page, columns=columns, show="headings")
    
        self.tree_inventory_list.heading("Product ID", text="Product ID", anchor="center")
        self.tree_inventory_list.heading("SKU", text="SKU", anchor="center")
        self.tree_inventory_list.heading("Name", text="Name", anchor="center")
        self.tree_inventory_list.heading("Price/SQM", text="Price/SQM", anchor="center")
        self.tree_inventory_list.heading("Quantity", text="Quantity", anchor="center")
        
        self.tree_inventory_list.column("Product ID", width=100, anchor="center", stretch=False)
        self.tree_inventory_list.column("SKU", width=100, anchor="center", stretch=False)
        self.tree_inventory_list.column("Name", width=150, anchor="center", stretch=False)
        self.tree_inventory_list.column("Price/SQM", width=100, anchor="center", stretch=False)
        self.tree_inventory_list.column("Quantity", width=250, anchor="center", stretch=False)
        
        scrollbar = ttk.Scrollbar(self.content_page, orient="vertical", command=self.tree_inventory_list.yview)
        self.tree_inventory_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree_inventory_list.pack(expand=True, padx=10, pady=(10,0))

        inventory_data = self.inventory_manager.get_inventory()

        for product in inventory_data: 
            self.tree_inventory_list.insert('', 'end', values=product)

        self.load_inventory_data()

        self.button_inventory_add = ttk.Button(self.content_page, text="Add Product", bootstyle="SUCCESS", command=self.show_productadd)
        self.button_inventory_add.pack(pady=(10,5))

        self.button_inventory_edit = ttk.Button(self.content_page, text="Edit Product", bootstyle="WARNING", command=self.show_edit_window)
        self.button_inventory_edit.pack(pady=(5,50))

    def load_inventory_data(self, data=None): 

        for item in self.tree_inventory_list.get_children(): 
            self.tree_inventory_list.delete(item)

        inventory_data = data if data else self.inventory_manager.get_inventory()

        for product in inventory_data: 
            self.tree_inventory_list.insert('', 'end', values=product)

    def search_inventory(self): 
        search_item = self.inventory_search_var.get().lower()

        inventory_data = self.inventory_manager.get_inventory()

        filtered_data = [
            product for product in inventory_data
            if search_item in str(product[1]).lower() or
               search_item in str(product[2]).lower()
        ]

        self.load_inventory_data(filtered_data)

    def clear_search(self): 
        self.inventory_search_var.set("")
        self.load_inventory_data()

    def show_productadd(self): 
        for widget in self.content_page.winfo_children(): 
            widget.destroy()

        self.title("Add Product")
        self.geometry("900x400")

        self.label_productadd_sku = ttk.Label(self.content_page, text="SKU")
        self.label_productadd_sku.grid(row=0, column=0, padx=5, pady=10, sticky = "e")

        self.entry_productadd_sku = ttk.Entry(self.content_page)
        self.entry_productadd_sku.grid(row=0, column=1, padx=5, pady=10)

        self.label_productadd_name = ttk.Label(self.content_page, text="Product Name")
        self.label_productadd_name.grid(row=1, column=0, pady=10, padx=5, sticky="e")

        self.entry_productadd_name = ttk.Entry(self.content_page)
        self.entry_productadd_name.grid(row=1, column=1, padx=5, pady=10)

        self.label_productadd_price = ttk.Label(self.content_page, text="Price Per Sheet")
        self.label_productadd_price.grid(row=2, column=0, pady=10, padx=5, stick="e")

        self.entry_productadd_price = ttk.Entry(self.content_page)
        self.entry_productadd_price.grid(row=2, column=1, pady=10, padx=5)

        self.label_productadd_quantity = ttk.Label(self.content_page, text="Quantity")
        self.label_productadd_quantity.grid(row=3, column=0, pady=10, padx=5, sticky="e")

        self.entry_productadd_quantity = ttk.Entry(self.content_page)
        self.entry_productadd_quantity.grid(row=3, column=1, padx=5, pady=10)

        self.button_productadd_back = ttk.Button(self.content_page, text="Back", command=self.show_inventory)

        self.button_productadd_add = ttk.Button(self.content_page, text="Add Product", command=self.add_product)
        self.button_productadd_add.grid(row=4, column=1, padx=5, pady=10, sticky="w")

    def add_product(self): 
        sku = self.entry_productadd_sku.get().strip()
        name = self.entry_productadd_name.get().strip()
        price = self.entry_productadd_price.get().strip()
        quantity = self.entry_productadd_quantity.get().strip()


        if not sku or not name or not price or not quantity: 
            messagebox.showerror("Error", "All fields are required")
            return
        
        self.inventory_manager.add_product(sku, name, price, quantity)
        messagebox.showinfo("Success", "Product added successfully")
        self.show_inventory()

    def show_edit_window(self):

        selected_product = self.tree_inventory_list.selection()
        if not selected_product: 
            messagebox.showerror("Error", "Please select a product to edit")
            return
        
        original_sku = self.tree_inventory_list.item(selected_product)['values'][1]
        product_values = self.tree_inventory_list.item(selected_product)['values']

        if not product_values: 
            messagebox.showerror("Error", "Couldn't retrieve product information")
            return
        
        edit_window = ttk.Toplevel(self)
        edit_window.title("Edit Product")
        edit_window.geometry("500x400")
        edit_window.resizable(False, False)

        frame = ttk.Frame(edit_window)
        frame.pack(fill='x', pady=10, expand=True)

        for row in range(6): 
            frame.rowconfigure(row, weight=1)
            
        for column in range(5): 
            frame.columnconfigure(column, weight=1)
    
        self.label_edit_sku = ttk.Label(frame, text="New SKU")
        self.label_edit_sku.grid(row=0, column=1, padx=10, pady=10)
        
        self.entry_edit_sku = ttk.Entry(frame)
        self.entry_edit_sku.grid(row=0, column=2, sticky="w", pady=10)
        self.entry_edit_sku.insert(0, product_values[1])
        
        self.label_edit_name = ttk.Label(frame, text="New name")
        self.label_edit_name.grid(row=1, column=1, padx=10, pady=10)
        
        self.entry_edit_name = ttk.Entry(frame)
        self.entry_edit_name.grid(row=1, column=2, sticky="w", pady=10)
        self.entry_edit_name.insert(0, product_values[2])
        
        self.label_edit_price = ttk.Label(frame, text="New Price")
        self.label_edit_price.grid(row=2, column=1, padx=10, pady=10)
        
        self.entry_edit_price = ttk.Entry(frame)
        self.entry_edit_price.grid(row=2, column=2, sticky="w", pady=10)
        self.entry_edit_price.insert(0, product_values[3])
        
        self.label_edit_quantity = ttk.Label(frame, text="New Quantity")
        self.label_edit_quantity.grid(row=3, column=1, padx=10, pady=10)
        
        self.entry_edit_quantity = ttk.Entry(frame)
        self.entry_edit_quantity.grid(row=3, column=2, sticky="w", pady=10)
        self.entry_edit_quantity.insert(0, product_values[4])

        self.button_edit_back = ttk.Button(frame, text="Back", bootstyle="DANGER", command=edit_window.destroy)
        self.button_edit_back.grid(row=4, column=0, pady=10, padx=5, sticky="e")

        self.button_edit_update = ttk.Button(frame, text="Update Product", bootstyle="SUCCESS", command=lambda: self.update_product(self.entry_edit_sku.get().strip(), self.entry_edit_name.get().strip(), self.entry_edit_price.get().strip(), self.entry_edit_quantity.get().strip(), original_sku, edit_window))
        self.button_edit_update.grid(row=4, column=1, pady=10, padx=5, sticky="w")

    def update_product(self, sku, name, price, quantity, original_sku, edit_window):
        try: 
            self.inventory_manager.update_product(sku, name, price, quantity, original_sku)

            self.show_updated_inventory()
            edit_window.destroy()

        except Exception as error: 
            messagebox.showerror("Error", f"Encountered this error {error}")

    def show_updated_inventory(self): 
        for item in self.tree_inventory_list.get_children(): 
            self.tree_inventory_list.delete(item)

        updated_inventory = self.inventory_manager.get_inventory()

        for product in updated_inventory: 
            self.tree_inventory_list.insert('', 'end', values=product)

    def show_clients(self): 
        for widget in self.content_page.winfo_children(): 
            widget.destroy()

        self.title("Inventory")
        self.geometry("1200x600")

        self.client_search_var = ttk.StringVar()
        clients_search_frame = ttk.Frame(self.content_page)
        clients_search_frame.pack(padx=10, pady=10, fill=X)

        self.label_clients_search = ttk.Label(clients_search_frame, text="Search Client (Name, Email, or Phone): ")
        self.label_clients_search.pack(side=LEFT, padx=(150,5), pady=(80,0))

        self.entry_clients_search = ttk.Entry(clients_search_frame, textvariable=self.client_search_var, width=30)
        self.entry_clients_search.pack(side=LEFT, pady=(80,0),padx=5)

        self.button_clients_search = ttk.Button(clients_search_frame, text="Search", bootstyle="SUCCESS", command=self.search_clients)
        self.button_clients_search.pack(side=LEFT, padx=5, pady=(80,0))

        self.button_clients_clear = ttk.Button(clients_search_frame, text="Clear", bootstyle="DANGER", command=self.clear_client_search)
        self.button_clients_clear.pack(side=LEFT, padx=5, pady=(80,0))

        columns = ("Client ID", "Client Name", "Email", "Phone", "Full Address")
        self.tree_clients_list = ttk.Treeview(self.content_page, columns=columns, show="headings")

        self.tree_clients_list.heading("Client ID", text="Client ID", anchor="center")
        self.tree_clients_list.heading("Client Name", text="Client Name", anchor="center")
        self.tree_clients_list.heading("Email", text="Email", anchor="center")
        self.tree_clients_list.heading("Phone", text="Phone", anchor="center")
        self.tree_clients_list.heading("Full Address", text="Full Address", anchor="center")

        self.tree_clients_list.column("Client ID", width=75, anchor="center", stretch=False)
        self.tree_clients_list.column("Client Name", width=125, anchor="center", stretch=False)
        self.tree_clients_list.column("Email", width=200, anchor="center", stretch=False)
        self.tree_clients_list.column("Phone", width=120, anchor="center", stretch=False)
        self.tree_clients_list.column("Full Address", width=500, anchor="center", stretch=False)

        client_scrollbar = ttk.Scrollbar(self.content_page, orient="vertical", command=self.tree_clients_list.yview)
        self.tree_clients_list.configure(yscrollcommand=client_scrollbar.set)
        client_scrollbar.pack(side="right", fill="y")
        self.tree_clients_list.pack(expand=True, padx=10, pady=(10,0))

        client_data = self.client_manager.get_clients()
        filtered_data = self.filter_client_data(client_data)

        for client in filtered_data:
            self.tree_clients_list.insert('', 'end', values=client)

        self.load_client_data()

        self.button_clients_add = ttk.Button(self.content_page, text="Add Client", bootstyle="SUCCESS", command=self.show_clientadd)
        self.button_clients_add.pack(pady=(10,5))

        self.button_clients_edit = ttk.Button(self.content_page, text="Edit Client", bootstyle="WARNING", command=self.show_editclient_window)
        self.button_clients_edit.pack(pady=(5,50))

    def load_client_data(self, data=None): 
        for item in self.tree_clients_list.get_children(): 
            self.tree_clients_list.delete(item)

        client_data = data if data else self.client_manager.get_clients()

        for client in client_data:
            filtered_values = (client[0], client[1], client[2], client[3], client[9])
            self.tree_clients_list.insert('', 'end', values=filtered_values)
            
    def filter_client_data(self, client_data): 
        filtered_data = []
        
        for client in client_data:
            client_id = client[0]
            client_name = client[1]
            email = client[2]
            phone = client[3]
            full_address = client[9]
            filtered_data.append((client_id, client_name, email, phone, full_address))
        
        return filtered_data
        
    def search_clients(self): 
        search_client = self.client_search_var.get().lower()

        client_data = self.client_manager.get_clients()

        filtered_data = [
            client for client in client_data
            if search_client in str(client_data[0]).lower() or
               search_client in str(client_data[1]).lower() or
               search_client in str(client_data[2]).lower() or
               search_client in str(client_data[3]).lower() or
               search_client in str(client_data[4]).lower()]
        
        self.load_client_data(filtered_data)
    
    def clear_client_search(self):
        self.client_search_var.set("")
        self.load_client_data() 

    def show_clientadd(self): 
        for widget in self.content_page.winfo_children(): 
            widget.destroy()

        self.title("Add Client")
        self.geometry("900x550")

        self.label_clientadd_name = ttk.Label(self.content_page, text="Client Name")
        self.label_clientadd_name.grid(row=0,column=0, padx=5, pady=(20,10), sticky="e")

        self.label_clientadd_email = ttk.Label(self.content_page, text="Email")
        self.label_clientadd_email.grid(row=1,column=0, padx=5, pady=10, sticky="e")

        self.label_clientadd_phone = ttk.Label(self.content_page, text="Phone No.")
        self.label_clientadd_phone.grid(row=2,column=0, padx=5, pady=10, sticky="e")

        self.label_clientadd_street = ttk.Label(self.content_page, text="Street")
        self.label_clientadd_street.grid(row=3,column=0, padx=5, pady=10, sticky="e")

        self.label_clientadd_city = ttk.Label(self.content_page, text="City")
        self.label_clientadd_city.grid(row=4,column=0, padx=5, pady=10, sticky="e")

        self.label_clientadd_region = ttk.Label(self.content_page, text="Region")
        self.label_clientadd_region.grid(row=5,column=0, padx=5, pady=10, sticky="e")

        self.label_clientadd_postcode = ttk.Label(self.content_page, text="Postal Code")
        self.label_clientadd_postcode.grid(row=6,column=0, padx=5, pady=10, sticky="e")

        self.label_clientadd_country = ttk.Label(self.content_page, text="Country")
        self.label_clientadd_country.grid(row=7,column=0, padx=5, pady=10, sticky="e")

        self.entry_clientadd_name = ttk.Entry(self.content_page)
        self.entry_clientadd_name.grid(row=0, column=1, padx=5, pady=(20,10))

        self.entry_clientadd_email = ttk.Entry(self.content_page)
        self.entry_clientadd_email.grid(row=1, column=1, padx=5, pady=10)

        self.entry_clientadd_phone = ttk.Entry(self.content_page)
        self.entry_clientadd_phone.grid(row=2, column=1, padx=5, pady=10)

        self.entry_clientadd_street = ttk.Entry(self.content_page)
        self.entry_clientadd_street.grid(row=3, column=1, padx=5, pady=10)

        self.entry_clientadd_city = ttk.Entry(self.content_page)
        self.entry_clientadd_city.grid(row=4, column=1, padx=5, pady=10)

        self.entry_clientadd_region = ttk.Entry(self.content_page)
        self.entry_clientadd_region.grid(row=5, column=1, padx=5, pady=10)

        self.entry_clientadd_postcode = ttk.Entry(self.content_page)
        self.entry_clientadd_postcode.grid(row=6, column=1, padx=5, pady=10)

        self.entry_clientadd_country = ttk.Entry(self.content_page)
        self.entry_clientadd_country.grid(row=7, column=1, padx=5, pady=10)

        self.button_clientadd_back = ttk.Button(self.content_page, text="Back", bootstyle="DANGER", command=self.show_clients)
        self.button_clientadd_back.grid(row=8, column=0, padx=10, pady=10, sticky="e")

        self.button_clientadd_save = ttk.Button(self.content_page, text="Add Client", bootstyle="SUCCESS", command=self.add_client)
        self.button_clientadd_save.grid(row=8, column=1, padx=10, pady=10, sticky="w")

    def add_client(self): 
        name = self.entry_clientadd_name.get()
        email = self.entry_clientadd_email.get()
        phone = self.entry_clientadd_phone.get()
        street = self.entry_clientadd_street.get()
        city = self.entry_clientadd_city.get()
        region = self.entry_clientadd_region.get()
        postcode = self.entry_clientadd_postcode.get()
        country = self.entry_clientadd_country.get()

        if not name or not email or not phone or not city or not country: 
            messagebox.showerror("Error", "All fields are requried")
            return
        
        self.client_manager.add_client(name, email, phone, street, city, region, postcode, country)
        self.show_clients()
        
    def show_editclient_window(self):
        
        selected_client = self.tree_clients_list.selection()
        if not selected_client: 
            messagebox.showerror("Error", "Please select a client to edit")
            return
        
        original_email = self.tree_clients_list.item(selected_client)['values'][2]
        selected_client_id = self.tree_clients_list.item(selected_client)['values'][0]
        
        
        all_clients = self.client_manager.get_clients()
        client_values = None
        
        for client in all_clients:
            if client[0] == selected_client_id: 
                client_values = client
                break
            
        
        if not client_values: 
            messagebox.showerror("Error", "Couldn't retrieve client information")
            return
        
        edit_window = ttk.Toplevel(self)
        edit_window.title("Update Client")
        edit_window.geometry("550x600")
        edit_window.resizable(False, False)
        
        frame = ttk.Frame(edit_window)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_clientedit_name = ttk.Label(frame, text="New Client Name")
        self.label_clientedit_name.grid(row=0,column=0, padx=5, pady=(20,10), sticky="e")

        self.label_clientedit_email = ttk.Label(frame, text="New Email")
        self.label_clientedit_email.grid(row=1,column=0, padx=5, pady=10, sticky="e")

        self.label_clientedit_phone = ttk.Label(frame, text="New Phone No.")
        self.label_clientedit_phone.grid(row=2,column=0, padx=5, pady=10, sticky="e")

        self.label_clientedit_street = ttk.Label(frame, text="New Street")
        self.label_clientedit_street.grid(row=3,column=0, padx=5, pady=10, sticky="e")

        self.label_clientedit_city = ttk.Label(frame, text="New City")
        self.label_clientedit_city.grid(row=4,column=0, padx=5, pady=10, sticky="e")

        self.label_clientedit_region = ttk.Label(frame, text="New Region")
        self.label_clientedit_region.grid(row=5,column=0, padx=5, pady=10, sticky="e")

        self.label_clientedit_postcode = ttk.Label(frame, text="New Postal Code")
        self.label_clientedit_postcode.grid(row=6,column=0, padx=5, pady=10, sticky="e")

        self.label_clientedit_country = ttk.Label(frame, text="New Country")
        self.label_clientedit_country.grid(row=7,column=0, padx=5, pady=10, sticky="e")

        self.entry_clientedit_name = ttk.Entry(frame)
        self.entry_clientedit_name.grid(row=0, column=1, padx=5, pady=(20,10))
        self.entry_clientedit_name.insert(0, client_values[1])

        self.entry_clientedit_email = ttk.Entry(frame)
        self.entry_clientedit_email.grid(row=1, column=1, padx=5, pady=10)
        self.entry_clientedit_email.insert(0, client_values[2])

        self.entry_clientedit_phone = ttk.Entry(frame)
        self.entry_clientedit_phone.grid(row=2, column=1, padx=5, pady=10)
        self.entry_clientedit_phone.insert(0, client_values[3])

        self.entry_clientedit_street = ttk.Entry(frame)
        self.entry_clientedit_street.grid(row=3, column=1, padx=5, pady=10)
        self.entry_clientedit_street.insert(0, client_values[4])

        self.entry_clientedit_city = ttk.Entry(frame)
        self.entry_clientedit_city.grid(row=4, column=1, padx=5, pady=10)
        self.entry_clientedit_city.insert(0, client_values[5])

        self.entry_clientedit_region = ttk.Entry(frame)
        self.entry_clientedit_region.grid(row=5, column=1, padx=5, pady=10)
        self.entry_clientedit_region.insert(0, client_values[6])

        self.entry_clientedit_postcode = ttk.Entry(frame)
        self.entry_clientedit_postcode.grid(row=6, column=1, padx=5, pady=10)
        self.entry_clientedit_postcode.insert(0, client_values[7])

        self.entry_clientedit_country = ttk.Entry(frame)
        self.entry_clientedit_country.grid(row=7, column=1, padx=5, pady=10)
        self.entry_clientedit_country.insert(0, client_values[8])
        
        self.button_clientedit_back = ttk.Button(frame, text="Back", bootstyle="DANGER", command=edit_window.destroy)
        self.button_clientedit_back.grid(row=8, column=0, padx=10, pady=10, sticky="e")

        self.button_clientedit_save = ttk.Button(
            frame,
            text="Save Changes",
            bootstyle="SUCCESS",
            command=lambda: self.update_client(
                self.entry_clientedit_name.get().strip(),
                self.entry_clientedit_email.get().strip(),
                self.entry_clientedit_phone.get().strip(),
                self.entry_clientedit_street.get().strip(),
                self.entry_clientedit_city.get().strip(),
                self.entry_clientedit_region.get().strip(),
                self.entry_clientedit_postcode.get().strip(),
                self.entry_clientedit_country.get().strip(), original_email, edit_window))
        
        self.button_clientedit_save.grid(row=8, column=1, padx=10, pady=10, sticky="w")
        
    def update_client(self, name, email, phone, street, city, region, postcode, country, original_email, edit_window): 
        try: 
            full_address = f"{street}, {city}, {region}, {postcode}, {country}"
            self.client_manager.update_clients(name, email, phone, street, city, region, postcode, country, full_address, original_email)
            edit_window.destroy()
            self.show_updated_clients()

        except Exception as error: 
            messagebox.showerror("Error", f"Encountered this error: {error}")
            
    def show_updated_clients(self): 
        for item in self.tree_clients_list.get_children(): 
            self.tree_clients_list.delete(item)
            
        updated_clients = self.client_manager.get_clients()
        updated_clients_filtered = self.filter_client_data(updated_clients)

        for client in updated_clients_filtered: 
            self.tree_clients_list.insert('','end',values=client)

    def show_order_window(self): 
        for widget in self.content_page.winfo_children(): 
            widget.destroy()

        self.title("Orders")
        self.geometry("1200x600")

        self.order_search_var = ttk.StringVar()
        orders_search_frame = ttk.Frame(self.content_page)
        orders_search_frame.pack(padx=10, pady=10, fill=X)

        self.label_orders_search = ttk.Label(orders_search_frame, text="Search Orders: ")
        self.label_orders_search.pack(side=LEFT, padx=(400,5), pady=(80,0))

        self.entry_orders_search = ttk.Entry(orders_search_frame)
        self.entry_orders_search.pack(side=LEFT, pady=(80,0),padx=5)

        self.button_clients_search = ttk.Button(orders_search_frame, text="Search", bootstyle="SUCCESS", command=self.search_orders)
        self.button_clients_search.pack(side=LEFT, padx=5, pady=(80,0))

        self.button_clients_clear = ttk.Button(orders_search_frame, text="Clear", bootstyle="DANGER", command=self.clear_orders_search)
        self.button_clients_clear.pack(side=LEFT, padx=5, pady=(80,0))

        columns = ("Order ID", "Client ID", "Order Date", "Total Price", "Estimated Delivery Date", "Order Status")
        self.tree_orders_list = ttk.Treeview(self.content_page, columns=columns, show="headings")

        self.tree_orders_list.heading("Order ID", text="Order ID", anchor="center")
        self.tree_orders_list.heading("Client ID", text="Client ID", anchor="center")
        self.tree_orders_list.heading("Order Date", text="Order Date", anchor="center")
        self.tree_orders_list.heading("Total Price", text="Total Price", anchor="center")
        self.tree_orders_list.heading("Estimated Delivery Date", text="Estimated Delivery Date", anchor="center")
        self.tree_orders_list.heading("Order Status", text="Order Status", anchor="center")

        self.tree_orders_list.column("Order ID", width=100, anchor="center", stretch=False)
        self.tree_orders_list.column("Client ID", width=100, anchor="center", stretch=False)
        self.tree_orders_list.column("Order Date", width=200, anchor="center", stretch=False)
        self.tree_orders_list.column("Total Price", width=200, anchor="center", stretch=False)
        self.tree_orders_list.column("Estimated Delivery Date", width=200, anchor="center", stretch=False)
        self.tree_orders_list.column("Order Status", width=200, anchor="center", stretch=False)

        order_scrollbar = ttk.Scrollbar(self.content_page, orient="vertical", command=self.tree_orders_list.yview)
        self.tree_orders_list.configure(yscrollcommand=order_scrollbar.set)
        order_scrollbar.pack(side="right", fill="y")
        self.tree_orders_list.pack(expand=True, padx=10, pady=(10,0))

        order_data = self.orders_manager.show_all_orders()
        self.load_order_data(order_data)

        self.button_orders_add = ttk.Button(self.content_page, text="Add Order", bootstyle="SUCCESS", command=self.show_orderadd)
        self.button_orders_add.pack(pady=(10, 5))

        self.button_orders_edit = ttk.Button(self.content_page, text="Edit Order", bootstyle="WARNING", command=None)
        self.button_orders_edit.pack(pady=(5, 5))

        self.button_orders_delete = ttk.Button(self.content_page, text="Delete Order", bootstyle="DANGER", command=None)
        self.button_orders_delete.pack(pady=(5,50))

    def load_order_data(self, order_data): 
        for item in self.tree_orders_list.get_children(): 
            self.tree_orders_list.delete(item)

        for order in order_data:

            self.tree_orders_list.insert('','end', values=order)

    def search_orders(self):
        search_text = self.order_search_var.get().lower()
        order_data = self.orders_manager.show_all_orders()

        filtered_orders = [
            order for order in order_data
            if any(search_text in str(value).lower() for value in order)]
        
        self.load_order_data(filtered_orders)

    def clear_orders_search(self): 
        
        self.order_search_var.set("")
        order_data = self.orders_manager.show_all_orders()
        self.load_order_data(order_data)
            
    def show_orderadd(self): 
        
        for widget in self.content_page.winfo_children(): 
            widget.destroy()

        self.title("Add Order")
        self.geometry("900x500")

        frame = ttk.Frame(self.content_page)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label_orderadd_client = ttk.Label(frame, text="Select Client: ")
        self.label_orderadd_client.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        client_data = self.orders_manager.get_all_clients()
        self.client_map = {f"{client[1]} (ID: {client[0]})": client[0] for client in client_data}

        client_options= list(self.client_map.keys())
        self.combo_orderadd_id = ttk.Combobox(frame, values=client_options, state="readonly")
        self.combo_orderadd_id.grid(row=0, column=1, padx=10, pady=10)
        self.combo_orderadd_id.bind("<<ComboboxSelected>>", self.update_address_field)

        self.label_orderadd_date = ttk.Label(frame, text="Order Date: ")
        self.label_orderadd_date.grid(row=1, column=0, padx=10, pady=10, sticky ="e")

        self.date_orderadd_date = ttk.DateEntry(frame, bootstyle="DANGER", dateformat="%d-%m-%Y", startdate=datetime.today())
        self.date_orderadd_date.grid(row=1, column=1, padx=10, pady=10)

        self.label_orderadd_estimateddelivery = ttk.Label(frame, text="Estimated Delivery Date: ")
        self.label_orderadd_estimateddelivery.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.date_orderadd_estimateddelivery = ttk.DateEntry(frame, bootstyle="SUCCESS", dateformat="%d-%m-%Y", startdate=datetime.today())
        self.date_orderadd_estimateddelivery.grid(row=2, column=1, pady=10, padx=10)

        self.label_orderadd_orderstatus = ttk.Label(frame, text="Order Status: ")
        self.label_orderadd_orderstatus.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        self.combo_orderadd_orderstatus = ttk.Combobox(frame, values=["PENDING", "PROCESSING", "SHIPPED", "DELIVERED"])
        self.combo_orderadd_orderstatus.set("PENDING")
        self.combo_orderadd_orderstatus.grid(row=3, column=1, padx=10, pady=10)

        self.label_orderadd_paymentstatus = ttk.Label(frame, text="Payment Status")
        self.label_orderadd_paymentstatus.grid(row=4, column=0, padx=10, pady=10, sticky="e")

        self.combo_orderadd_paymentstatus = ttk.Combobox(frame, values=["UNPAID", "PAID"], state="readonly")
        self.combo_orderadd_paymentstatus.set("UNPAID")
        self.combo_orderadd_paymentstatus.grid(row=4, column=1, pady=10, padx=10)

        self.label_orderadd_address = ttk.Label(frame, text="Delivery Address: ")
        self.label_orderadd_address.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.label_orderadd_address_value = ttk.Label(frame, text="", bootstyle="info")
        self.label_orderadd_address_value.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.button_orderadd_products = ttk.Button(frame, text="Add Products", command=None)
        self.button_orderadd_products.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        self.button_orderadd_save = ttk.Button(frame, text="Save Order", bootstyle="SUCCESS", command=self.save_order)
        self.button_orderadd_save.grid(row=7, column=1, pady=20, padx=10, sticky="w")

        self.button_orderadd_back = ttk.Button(frame, text="Back", bootstyle="DANGER", command=self.show_order_window)
        self.button_orderadd_back.grid(row=7, column=0, pady=20, padx=10, sticky="e")

    def update_address_field(self, event):

        selected_client = self.combo_orderadd_id.get()
        if not selected_client: 
            return
        
        client_id = self.client_map[selected_client]
        address = self.orders_manager.get_client_address(client_id)
        self.label_orderadd_address_value.config(text=address)

    def save_order(self):
        try:
            selected_client_display = self.combo_orderadd_id.get()
            client_id = self.client_map[selected_client_display]
            order_status = self.combo_orderadd_orderstatus.get()
            payment_status = self.combo_orderadd_paymentstatus.get()
            delivery_address = self.label_orderadd_address_value.cget("text")
            estimated_deliverydate = self.date_orderadd_estimateddelivery.get_date().strftime('%Y-%m-%d')

            total_price = 0
            self.current_order_id = self.orders_manager.add_order(client_id, total_price, delivery_address, estimated_deliverydate, payment_status, order_status)

            self.orders_manager.add_order(client_id, total_price, delivery_address, estimated_deliverydate, payment_status, order_status)
            self.show_order_window()

        except Exception as error: 
            messagebox.showerror("Error", f"Error {error}")

    def product_selection_window(self):

        self.select_productwindow = ttk.Toplevel(self)
        self.select_productwindow.title("Add products to order")
        self.select_productwindow.geometry("900x600")

        frame = ttk.Frame(self.select_productwindow)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        columns = ("Product ID", "Product Name", "Price", "Available Quantity", "Select Quantity")
        self.select_products_list = ttk.Treeview(frame, columns=columns, show="headings")

        self.select_products_list.heading("Product ID", text="Product ID", anchor="center")
        self.select_products_list.heading("Product Name", text="Product Name", anchor="center")
        self.select_products_list.heading("Price", text="Price", anchor="center")
        self.select_products_list.heading("Available Quantity", text="Available Quantity", anchor="center")
        self.select_products_list.heading("Selected Quantity", text="Selected Quantity", anchor="center")

        self.select_products_list.column("Product ID", width=100, text="Product ID", anchor="center", stretch=False)
        self.select_products_list.column("Product Name", width=200, text="Product Name",anchor="center",stretch=False)
        self.select_products_list.column("Price", width=150, text="Product ID",anchor="center",stretch=False)
        self.select_products_list.column("Available Quantity", width=150, text="Product ID",anchor="center",stretch=False)
        self.select_products_list.column("Selected Quantity", width=100, text="Product ID",anchor="center",stretch=False)

        selected_product_scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.select_products_list.yview)
        self.select_products_list.configure(yscrollcommand=selected_product_scrollbar.set)
        selected_product_scrollbar.pack(side="right", fill="y")
        self.select_products_list.pack(pady=(10,0),padx=10 expand=True)

        product_data = self.orders_manager.get_all_products()
        self.quantity_entries = {}

        for product in product_data: 
            product_id = product[0]

            self.select_products_list.insert('','end', iid=str(product_id), values=(product_id, product[1], product[2], product[3], "0"))
            
            quantity_entry = ttk.Entry(self.select_products_list)
            self.select_products_list.set(str(product_id), "Select Quantity", "0")
            quantity_entry.insert(0,"0")

            self.quantity_entries[product_id] = quantity_entry

            self.select_products_list.bind("<ButtonRelease-1>", self.position_quantity_entry)

            self.button_select_confirm = ttk.Button(frame, text="Add Selected Products", bootstyle="SUCCESS", command=self.confirm_product_selection)
            self.button_select_confirm.pack(pady=10)

    def position_quantity_entry(self, event): 

        selected_item = self.select_products_list.selection()
        if selected_item: 
            item_id = selected_item[0]
            column = self.select_products_list.identify_column(event.x)

            if column == "#5": 
                quantity_entry = self.quantity_entries[int(item_id)]
                quantity_entry.place_forget()
                quantity_entry.place(x=event.x_root - self.select_products_list.winfo_rootx() - 50, 
                        y=event.y_root - self.select_products_list.winfo_rooty() + 5, 
                        width=150)


    def confirm_product_selection(self): 

        selected_items = []
        insufficient_stock = []

        for item in self.select_products_list.get_children(): 
            values = self.select_products_list.item(item, "values")
            product_id = int(values[0])
            product_name = str(values[1])
            price = float(values[2])
            available_quantity = int(values[3])
            selected_quantity = int(self.quantity_entries[product_id].get())

            if selected_quantity > 0: 
                if selected_quantity > available_quantity: 
                    insufficient_stock.append(f"{product_name} (Available: {available_quantity}, Selected: {selected_quantity})")
                else: 
                    item_total_price = price * selected_quantity
                    selected_items.append((product_id, selected_quantity, item_total_price))


        if insufficient_stock: 
            messagebox.showwarning("Insufficient Stock", f"Not enough stock for: {', '.join(insufficient_stock)}")
            return
        
        if hasattr(self, "current_order_id") and self.current_order_id: 
            for product_id, quantity, item_total in selected_items: 
                self.orders_manager.add_order_item(self.current_order_id, product_id, quantity, item_total)
                self.orders_manager.update_inventory_quantity(product_id, quantity)

            messagebox.showinfo("Success", f"Products successfully added to Order #{self.current_order_id}")
            self.select_productwindow.destroy()








if __name__ == "__main__":
    NEA_tables.create_tables()

    app = Application()
    app.mainloop()




















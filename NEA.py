#Importing all the necessary libraries

import os #for the hashing algorithm construction
import ttkbootstrap as ttk #this and tkinter are for UI related things
import tkinter as tk
from tkinter import messagebox #a way to show error messages as popups, will be useful during exception handling
from ttkbootstrap.constants import * 
import psycopg2
from datetime import datetime #for setting order dates later
from psycopg2 import sql #for all sql related activities, like queries



#Establishing connection to database and also for queries
class DatabaseManager: 
    def __init__(self, host="localhost", database="NEA", user="postgres", password="1510", port="5432"): 
        self.host = host 
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.conn = self.connect_to_database()
        
        if self.conn: 
            self.create_tables('C:/Users/clust/Desktop/NEA_folder/NEA_coding/DDL_Script_NEA.sql')
        
    def connect_to_database(self): #performs the actual connection
        
        try: 
            conn = psycopg2.connect(
                host=self.host, 
                dbname = self.database, 
                user = self.user,
                password = self.password,
                port = self.port)
            print("Database Connection Successful")
            return conn
        except Exception as error: #exception handling through except statements
            print(f"Error connecting to database: {error}") #making it easier to debug by printing
            return None

    def create_tables(self, ddl_script_path): 
        
        if not os.path.exists(ddl_script_path): 
            print(f"DDL file path: {ddl_script_path} not found")
            return
        
        try: 
            with open(ddl_script_path, "r") as file: 
                ddl_script = file.read()
                
            cursor = self.conn.cursor()
            cursor.execute(ddl_script)
            self.conn.commit()
            print("Tables created successfully")
        except psycopg2.Error as error: 
            print(f"Error executing DDL Script: {error}")
        except Exception as error1: 
            print(f"Error reading DDL Script: {error1}")
      
#use this to execute any command like inserting values into tables or updating values etc
    def execute_query(self, query, paramaters=()): #this is to reduce the number of times I write out the execution of a query and instead I can just use this
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, paramaters)
            self.conn.commit()
            return cursor
        except psycopg2.Error as error:
            self.conn.rollback() #undo all statements so it goes back to the original unchanged and doesn't cause problems later
            print(f"Error executing query: {error}")
            return error
        
    def close_connection(self): #to close the connection at at the end
        
        if self.conn: 
            self.conn.close()
            print("Database connection closed")
            
            
class UserManager: #a class to add users through registration and check their credentials while logging in
    def __init__(self, database_manager): 
        self.database_manager = database_manager #since I will be executing queries I will need this
        
    def generate_salt(self): 
        #used to generate the salt so I can XOR it with the password after
        return os.urandom(16)
    
    def hash_password(self, password, salt): #hashing algorithm
        
        password_bytes = password.encode('utf-8')
        hashed_bytes = bytearray() #creates an array that can store binary
        
        for i in range(len(password_bytes)): 
            hashed_bytes.append(password_bytes[i] ^ salt[i % len(salt)]) #xor's it with the salt
            
        return ''.join(format(byte, '02x') for byte in hashed_bytes) #converts all of it to hexadecimal
        
    def register_user(self, employee_code, first_name, last_name, email, password): 
        #the user's password will need to be hashed first
        
        salt = self.generate_salt()
        hashed_password = self.hash_password(password, salt)
        
        query_register = """INSERT INTO Users(
            employee_code, first_name, last_name, email, password_hash, password_salt)
            VALUES(%s,%s,%s,%s,%s,%s)"""
            
        paramaters = (employee_code, first_name, last_name, email, hashed_password, salt.hex())
        
        try: 
            self.database_manager.execute_query(query_register, paramaters)
            messagebox.showinfo("Registration Successful",f"User {first_name} {last_name} has been registered")
        except Exception as error: 
            messagebox.showerror("Error", f"Error while registration: {error}")
        
    def authenticate_user(self, employee_code, password): #checks if their login credentials are correct when they login
        
        query_authentication = """SELECT first_name, last_name, password_hash, password_salt 
                                  FROM Users WHERE employee_code = %s"""
        
        try: 
            cursor = self.database_manager.execute_query(query_authentication, (employee_code,))
            user_data = cursor.fetchone()
            if user_data: 
                first_name, last_name, stored_password, stored_salt = user_data
                bytes_salt = bytes.fromhex(stored_salt)
                
                if self.verify_password(password, bytes_salt, stored_password): 
                    print(f"User {first_name} {last_name} authenticated successfully")
                    return first_name, last_name
            return None
        except Exception as error:
            messagebox.showerror("Error", f"Encountered error: {error}")
            return None
        
    def verify_password(self, login_password, salt, stored_password): #hashes their login password to see if its the same as the registration one
        login_hash = self.hash_password(login_password, salt)
        
        return login_hash == stored_password
    
#A class for adding, editing and retrieving clients
class ClientManager: 
    def __init__(self, database_manager): 
        self.database_manager = database_manager

    def add_client(self, client_name, client_email, client_phone,
                   address_line, city, country, full_address): 
        
        full_address = f"{address_line}, {city}, {country}"

        query_add_client = """INSERT INTO Clients(client_name, client_email, client_phone,
        address_line, city, country, full_address)
        VALUES(%s,%s,%s,%s,%s,%s,%s)""" 

        paramaters = (client_name, client_email, client_phone,
                      address_line, city, country, full_address)
        
        try: 
            self.database_manager.execute_query(query_add_client, paramaters)
            messagebox.showinfo("SUCCESS",f"Client {client_name} added successfully")
        except Exception as error: 
            messagebox.showerror("ERROR",f"Error adding client: {error}")

    def edit_clients(self, client_id, client_name=None, client_email=None, client_phone=None,
                     address_line=None, city=None, country=None):
        
        query_edit_client = """
            UPDATE Clients
            SET client_name = COALESCE(%s, client_name),
                client_email = COALESCE(%s, client_email),
                client_phone = COALESCE(%s, client_phone),
                address_line = COALESCE(%s, address_line), 
                city = COALESCE(%s, city),
                country = COALESCE(%s, country)
                full_address = COALESCE(%s, full_address)
            WHERE client_id = %s"""
        
        full_address = f"{address_line}, {city}, {country}" if address_line and city and country else None

        paramaters = (client_name, client_email, client_phone,
                      address_line, city, country, full_address, client_id)
        
        try: 
            self.database_manager.execute_query(query_edit_client, paramaters)
            messagebox.showinfo("SUCCESS", f"Client {client_id} has been updated successfully")
        except Exception as error: 
            messagebox.showerror("ERROR",f"Error updating client: {error}")

    def get_clients(self): 
        
        query_get_clients = """SELECT * FROM Clients"""
        try: 
            cursor = self.database_manager.execute_query(query_get_clients)
            return cursor.fetchall()
        except Exception as error: 
            messagebox.showerror("ERROR",f"Error retrieving clients: {error}")
            return []

#class for addding, editing and retreiving proucts to and from the inventory
class InventoryManager: 
    def __init__(self, database_manager): 
        self.database_manager = database_manager

    #adds the product
    def add_product(self, sku, product_name, product_price, stock_quantity):
        query_add_product = """INSERT INTO Inventory(sku, product_name, product_price, stock_quantity)
                                VALUES(%s,%s,%s,%s)"""
        
        paramaters = (sku, product_name, product_price, stock_quantity)

        try: 
            self.database_manager.execute_query(query_add_product, paramaters)
            messagebox.showinfo("Add Product", f"{product_name}, sku: {sku} added successfully")
        except Exception as error: 
            messagebox.showerror("Error", f"Error adding product {error}")

    def edit_product(self, product_id, sku=None, product_name=None, product_price=None, stock_quantity=None): 
        query_edit_product = """UPDATE Inventory
            SET sku = COALESCE(%s, sku),
                product_name = COALESCE(%s, product_name), 
                product_price = COALESCE(%s, product_price), 
                stock_quantity = COALESCE(%s, stock_quantity)
            WHERE product_id = %s"""
            
        paramaters = (sku, product_name, product_price, stock_quantity, product_id)
        
        try: 
            self.database_manager.execute_query(query_edit_product, paramaters)
            messagebox.showinfo("Success", f"Product {product_id}, sku: {sku} has been updated successfully")
        except Exception as error: 
            messagebox.showerror("Error", f"Error while updating product: {error}")
            
    def get_inventory(self): 
        query_get_inventory = """SELECT * FROM Inventory"""
        
        try: 
            cursor = self.database_manager.execute_query(query_get_inventory)
            return cursor.fetchall()
        except Exception as error: 
            messagebox.showerror("Error", f"Error retrieving inventory: {error}")
            return []
        
    def delete_product(self, product_id): 
        query_delete_product = """DELETE FROM Inventory WHERE product_id = %s"""
        
        try: 
            self.database_manager.execute_query(query_delete_product, (product_id,))
        except Exception as error: 
            messagebox.showerror("Error", "Erorr while deleting product")

#this class is for managing orders, you can add delete, edit and retrieve orders
class OrderManager: 
    def __init__(self, database_manager): 
        self.database_manager = database_manager
        
    def add_order(self, client_id, total_price, estimated_delivery_date,
                  payment_status="UNPAID", order_status="PENDING", delivery_date=None):
        
        query_add_order = """INSERT INTO Orders(
            client_id, total_price, order_status, payment_status, estimated_delivery_date, delivery_date)
            VALUES(%s,%s,%s,%s,%s,%s)"""
            
        paramaters = (client_id, total_price, order_status, payment_status,
                      estimated_delivery_date, delivery_date)
        
        try: 
            cursor = self.database_manager.execute_query(query_add_order, paramaters)
            order_id = cursor.fetchone()[0]
            messagebox.showinfo("Add Order", f"Order {order_id} added successfully")
        except Exception as error: 
            messagebox.showerror("Error", f"Error while adding order: {error}")
            return None
        
    def add_order_item(self, order_id, product_id, product_quantity, total_price): 
        query_add_order_item = """INSERT INTO OrderItems(
            order_id, product_id, product_quantity, total_price) VALUES(%s,%s,%s,%s)"""
            
        paramaters = (order_id, product_id, product_quantity, total_price)
        
        try: 
            self.database_manager.execute_query(query_add_order_item, paramaters)
            messagebox.showinfo("Order Item", f"Product with id: {product_id} added to order: {order_id}")
        except Exception as error: 
            messagebox.showerror("Error", f"Error adding item to order: {error}")

    def edit_order(self, order_id, new_client_id=None, new_total_price=None,
                   new_estimated_delivery_date=None, new_payment_stauts=None, new_order_status=None,
                   new_delivery_date=None):
    
        query_edit_order = """UPDATE Orders
            SET client_id = COALESCE(%s, client_id) 
                total_price = COALESCE(%s, total_price)
                estimated_delivery_date = COALESCE(%s, estimated_delivery_date),
                payment_status = COALESCE(%s, payment_status),
                order_status = COALESCE(%s, order_status),
                delivery_date = (%s, delivery_date)
            WHERE order_id = %s"""
            
        paramaters= (new_client_id, new_total_price, new_estimated_delivery_date,
                   new_payment_stauts, new_order_status, new_delivery_date, order_id)
        
        try: 
            self.database_manager.execute_query(query_edit_order, paramaters)
            messagebox.showinfo("Update Order", f"Updated Order {order_id} successfully")
        except Exception as error:
            messagebox.showerror("Error", f"Error editing order: {error}")
    
    def edit_order_item(self, order_id, product_id,  new_product_quantity=None, new_total_price=None):
        query_edit_order_item = """UPDATE OrderItems
            SET product_quantity = COALESCE(%s, product_quantity), 
                total_price = COALESCE(%s, total_price)
            WHERE order_id = %s AND product_id = %s"""
            
        paramaters = (new_product_quantity, new_total_price, order_id, product_id)
    
        try: 
            self.database_manager.execute_query(query_edit_order_item, paramaters)
            messagebox.showinfo("Edit Order Item", f"Product with id: {product_id} updated successfully")
        except Exception as error: 
            messagebox.showerror("Error", f"Error while updating order item: {error}")
             
    
    def delete_order_items(self, order_id): 
        
        query_delete_order_items = """DELETE FROM OrderItems WHERE order_id = %s"""
        
        try: 
            self.database_manager.execute_query(query_delete_order_items, (order_id,))
            messagebox.showinfo("Delete Order Item", f"Item has been deleted for order: {order_id}")
        except Exception as error: 
            messagebox.showerror("Error", f"Error while deleting order items: {error}")
            
    def delete_order(self, order_id): 
        self.delete_order_items(order_id)
        
        query_delete_order = """DELETE FROM Orders WHERE order_id = %s"""
        
        try: 
            self.database_manager.execute_query(query_delete_order, (order_id,))
            messagebox.showinfo("Delete Order", f"Deleted order with id: {order_id}")
        except Exception as error: 
            messagebox.showerror("Error", f"Error while deleting order: {error}")
            

#blueprint for all the pages that will be used in the program
class BasePage(ttk.Frame):
    def __init__(self, parent, controller, database_manager): 
        super().__init__(parent)
        self.controller = controller
        self.database_manager = database_manager 
        
    def show(self): 
        self.pack(fill="both", expand=True)
    
    def hide(self): 
        self.pack_forget()
        
class Application(ttk.Window): 
    def __init__(self): 
        super().__init__(title="Fashion Match (Sales Order Processing System)")
        self.geometry("900x600")
        
        self.database_manager = DatabaseManager()
        if not self.database_manager.conn: 
            messagebox.showerror("Error", "Connection Unsuccessful")
            self.destroy()
            return
        
        self.user_manager = UserManager(self.database_manager)
        
        self.current_user = None
        
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.create_navigation_frame()
        
        self.content_frame = ttk.Frame(self.container)
        self.content_frame.pack(fill="both", expand=True)
        
        self.show_main_page()
        
    def create_navigation_frame(self): 
        self.navigation_frame = ttk.Frame(self.container)
        self.navigation_frame.pack(side="top", fill="x")
        
        self.button_logout = None
        self.button_home = None
        
    def update_navigation_buttons(self, logged_in): 
        for widget in self.navigation_frame.winfo_children(): 
            widget.destroy()
            
        if logged_in: 
            self.button_logout = ttk.Button(self.navigation_frame, text="Logout", bootstyle="DANGER",
                                            command=self.logout)
            self.button_logout.pack(side="left", pady=10, padx=5)
            
            self.home_button = ttk.Button(self.navigation_frame, text="Home", bootstyle="SUCCESS",
                                          command=self.show_home_page)
        else: 
            pass
        
    def show_main_page(self):
        self.update_navigation_buttons(logged_in=False) 
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()
        
            
        main_page = MainPage(parent=self.content_frame, controller=self, database_manager=self.database_manager)
        main_page.show()
        
    def show_login_page(self):
        self.update_navigation_buttons(logged_in=False)
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()
        
        login_page = LoginPage(parent=self.content_frame, controller=self, database_manager=self.database_manager)
        login_page.show()

    def show_register_page(self):
        self.update_navigation_buttons(logged_in=False)
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()
        
        register_page = RegisterPage(parent=self.content_frame, controller=self, database_manager=self.database_manager)
        register_page.show()       
        
    def show_home_page(self, first_name, last_name):
        self.update_navigation_buttons(logged_in=True)
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()
        

        
        home_page = HomePage(parent=self.content_frame, controller=self, database_manager=self.database_manager,
                             first_name = first_name, last_name = last_name)
        
        home_page.show()
        
    def show_inventory_page(self): 
        self.update_navigation_buttons(logged_in=True)
        
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()
            
        inventory_page = InventoryPage(parent=self.content_frame, controller=self, database_manager=self.database_manager)
        inventory_page.show()
        
    def logout(self): 
        self.current_user = None
        self.show_main_page()
        
class MainPage(BasePage): 
    def __init__(self, parent, controller, database_manager): 
        super().__init__(parent, controller, database_manager)
        self.create_widgets()
        
    def create_widgets(self): 
        
        for widget in self.winfo_children(): 
            widget.destroy()
            
        self.welcome_label = ttk.Label(self, text="Welcome to Fashion Match",font=("Veranada", 22))
        self.welcome_label.pack(pady=(50,5))
        
        self.welcome_label2 = ttk.Label(self, text="Your very own sales order processing system!!", bootstyle="PRIMARY",font=("Helvetica", 11))
        self.welcome_label2.pack(pady=(5,50))
        
        self.register_button = ttk.Button(self, text="Register", bootstyle="SUCCESS", command=self.controller.show_register_page)
        self.register_button.pack(pady=10)
        
        self.login_button = ttk.Button(self, text="Login", command=self.controller.show_login_page)
        self.login_button.pack(pady=10)
        

class LoginPage(BasePage): 
    def __init__(self, parent, controller, database_manager): 
        super().__init__(parent, controller, database_manager)
        self.user_manager = controller.user_manager
        self.create_widgets()
        
    def create_widgets(self): 
        for widget in self.winfo_children(): 
            widget.destroy()
            
        frame = ttk.Frame(self)
        frame.pack(pady=50)
        
        self.label_employee_code = ttk.Label(frame, text="Employee Code")
        self.label_employee_code.grid(row=0, column=0, pady=10, padx=5, sticky="e")
        
        self.entry_employee_code = ttk.Entry(frame)
        self.entry_employee_code.grid(row=0, column=1, padx=5, pady=10)
        
        self.label_password = ttk.Label(frame, text="Password")
        self.label_password.grid(row=1, column=0, pady=10, padx=5, sticky="e")
        
        self.entry_password = ttk.Entry(frame, show="*")
        self.entry_password.grid(row=1, column=1, pady=10, padx=5)
        
        self.button_back = ttk.Button(frame, text="Back", bootstyle="WARNING", command=self.controller.show_main_page)
        self.button_back.grid(row=2, column=0, pady=10, padx=5, sticky="e")
        
        self.button_login = ttk.Button(frame, text="Login", bootstyle="SUCCESS", command=self.login_user)
        self.button_login.grid(row=2, column=1, pady=10, padx=5, sticky="w")
        
    def login_user(self): 
        employee_code = self.entry_employee_code.get().strip()
        password = self.entry_password.get().strip()
        
        if not employee_code or not password: 
            messagebox.showerror("Error", "All fields are required")
            return
        
        user_data = self.user_manager.authenticate_user(employee_code, password)
        
        if user_data: 
            first_name, last_name = user_data
            messagebox.showinfo("Success", f"Welcome {first_name} {last_name}")
            self.controller.current_user = (first_name, last_name)
            self.controller.show_home_page(first_name, last_name)
        else: 
            messagebox.showerror("Error", "Invalid Credentials, please try again or register")

class RegisterPage(BasePage): 
    def __init__(self, parent, controller, database_manager): 
        super().__init__(parent, controller, database_manager)
        self.user_manager = controller.user_manager
        self.create_widgets()
        
    def create_widgets(self): 
        for widget in self.winfo_children(): 
            widget.destroy()
            
        frame = ttk.Frame(self)
        frame.pack(pady=10)
        
        self.label_employee_code = ttk.Label(frame, text="Employee Code")
        self.label_employee_code.grid(row=0, column=0, pady=10, padx=5, sticky="e")
        
        self.entry_employee_code = ttk.Entry(frame)
        self.entry_employee_code.grid(row=0, column=1, pady=10, padx=5)
        
        self.label_first_name = ttk.Label(frame, text="First Name")
        self.label_first_name.grid(row=1, column=0, pady=10, padx=5, sticky="e")
        
        self.entry_first_name = ttk.Entry(frame)
        self.entry_first_name.grid(row=1, column=1, pady=10, padx=5)
        
        self.label_last_name = ttk.Label(frame, text="Last Name")
        self.label_last_name.grid(row=2, column=0, pady=10, padx=5, sticky="e")
        
        self.entry_last_name = ttk.Entry(frame)
        self.entry_last_name.grid(row=2, column=1, pady=10, padx=5)
        
        self.label_email = ttk.Label(frame, text="Email")
        self.label_email.grid(row=3, column=0, pady=10, padx=5, sticky="e")
        
        self.entry_email = ttk.Entry(frame)
        self.entry_email.grid(row=3, column=1, pady=10, padx=5)

        self.label_password = ttk.Label(frame, text="Password")
        self.label_password.grid(row=4, column=0, pady=10, padx=5, sticky="e")
        
        self.entry_password = ttk.Entry(frame)
        self.entry_password.grid(row=4, column=1, pady=10, padx=5)
        
        self.button_back = ttk.Button(frame, text="Back", bootstyle="WARNING", command=self.controller.show_main_page)
        self.button_back.grid(row=5, column=0, pady=10, padx=5, sticky="e")
        
        self.button_register = ttk.Button(frame, text="Register", bootstyle="SUCCESS", command=self.register_user)
        self.button_register.grid(row=5, column=1, pady=10, padx=5, sticky="w")
        
    def register_user(self): 
        employee_code = self.entry_employee_code.get().strip()
        first_name = self.entry_first_name.get().strip()
        last_name = self.entry_last_name.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        
        if not employee_code or not first_name or not last_name or not email or not password: 
            messagebox.showerror("Error", "All fields are required")
            return
            
        self.user_manager.register_user(employee_code, first_name, last_name, email, password)
        self.controller.show_main_page()
        
class HomePage(BasePage): 
    def __init__(self, parent, controller, database_manager, first_name, last_name): 
        super().__init__(parent, controller, database_manager)
        self.first_name = first_name
        self.last_name= last_name
        
        self.client_manager = ClientManager(self.database_manager)
        self.inventory_manager = InventoryManager(self.database_manager)
        self.order_manager = OrderManager(self.database_manager)
        self.create_widgets()
        
    def create_widgets(self): 
        for widget in self.winfo_children(): 
            widget.destroy()
            
        self.label_welcome = ttk.Label(self, text=f"Welcome {self.first_name} {self.last_name}", font=("Helvetica", 18))
        self.label_welcome.pack(pady=50)
        
        self.button_inventory = ttk.Button(self, text="Inventory", command=self.controller.show_inventory_page)
        self.button_inventory.pack(pady=(20, 5))
        
        self.button_clients = ttk.Button(self, text="Clients", bootstyle="DANGER", command=None)
        self.button_clients.pack(pady=(0, 5))
        
        self.button_orders = ttk.Button(self, text="Orders", bootstyle="WARNING", command=None)
        self.button_orders.pack(pady=(0,20))
    
    
class InventoryPage(BasePage): 
    def __init__(self, parent, controller, database_manager): 
        super().__init__(parent, controller, database_manager)
        self.inventory_manager = InventoryManager(self.database_manager)
        self.create_widgets()
        
    def create_widgets(self): 
        
        search_frame = ttk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", padx=(0,10))
        search_entry.bind('<KeyRelease>', self.update_treeview)
        
        add_button = ttk.Button(search_frame, text="Add Product", command=self.add_product)
        add_button.pack(side="left", padx=5)
        
        edit_button = ttk.Button(search_frame, text="Edit Product", command=self.edit_product)
        edit_button.pack(side="left", padx=5)
        
        delete_button = ttk.Button(search_frame, text="Delete", command=self.delete_product)
        delete_button.pack(side="left", padx=5)
        
        columns = ("Product ID", "SKU", "Product Name", "Price Per Unit", "Stock Quantity")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        for col in columns: 
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            self.tree.column(col, width=150, anchor="center")
            
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.inventory_data = self.inventory_manager.get_inventory()
        self.filtered_data = self.inventory_data.copy()
        self.populate_treeview(self.filtered_data)
        
        
    def populate_treeview(self, data): 
        for item in self.tree.get_children(): 
            self.tree.delete(item)
            
        for row in data: 
            self.tree.insert('', 'end', values=row)
            
    def sort_treeview(self, col, reverse): 
        col_index = {"Product ID": 0, "SKU": 1, "Product Name": 2, "Price Per Unit": 3, "Stock Quantity" : 4}[col]
        
        try: 
            self.filtered_data.sort(key=lambda x: float(x[col_index]), reverse=reverse)
        except ValueError: 
            self.filtered_data.sort(key=lambda x: x[col_index], reverse=reverse)
        
        self.populate_treeview(self.filtered_data)
        
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))
        
    def update_treeview(self, event=None): 
        
        search_term = self.search_var.get().lower()
        
        self.filtered_data = [
            row for row in self.inventory_data
            if search_term in str(row).lower()
        ]
        
        self.populate_treeview(self.filtered_data)
        
    def add_product(self): 
        
        AddProductWindow(self, self.inventory_manager, self.refresh_inventory_data)
        
    def edit_product(self): 
        selected_item = self.tree.selection()
        if not selected_item: 
            messagebox.showwarning("Warning", f"Please select an item to continue")
            return
        
        item_values = self.tree.item(selected_item)['values']
        
        EditProductWindow(self, self.inventory_manager, item_values, self.refresh_inventory_data)
    
    def delete_product(self): 
        
        selected_item = self.tree.selection()
        if not selected_item: 
            messagebox.showwarning("Warning", "Please select a product to delete")
            return

        item_values = self.tree.item(selected_item)['values']
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete product {item_values[2]}?")
        if confirm:

            self.inventory_manager.delete_product(item_values[0])  
            self.refresh_inventory_data()
            messagebox.showinfo("Success", "Product deleted successfully.")
            
        
    def refresh_inventory_data(self):

        self.inventory_data = self.inventory_manager.get_inventory()
        self.update_treeview()
    
class AddProductWindow(tk.Toplevel):
    def __init__(self, parent, inventory_manager, refresh_callback):
        super().__init__(parent)
        self.title("Add Product")
        self.inventory_manager = inventory_manager
        self.refresh_callback = refresh_callback
        self.create_widgets()
        self.transient(parent)  
        self.grab_set()         
        self.focus_set()
        self.wait_window(self)

    def create_widgets(self):
        
        self.label_sku = ttk.Label(self, text="SKU:")
        self.label_sku.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_sku = ttk.Entry(self)
        self.entry_sku.grid(row=0, column=1, padx=5, pady=5)

        self.label_name = ttk.Label(self, text="Product Name:")
        self.label_name.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        self.label_price = ttk.Label(self, text="Price:")
        self.label_price.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_price = ttk.Entry(self)
        self.entry_price.grid(row=2, column=1, padx=5, pady=5)

        self.label_quantity = ttk.Label(self, text="Stock Quantity:")
        self.label_quantity.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_quantity = ttk.Entry(self)
        self.entry_quantity.grid(row=3, column=1, padx=5, pady=5)

        
        save_button = ttk.Button(self, text="Save", command=self.save_product)
        save_button.grid(row=4, column=0, padx=5, pady=10)

        cancel_button = ttk.Button(self, text="Cancel", command=self.destroy)
        cancel_button.grid(row=4, column=1, padx=5, pady=10)

    def save_product(self):
        
        sku = self.entry_sku.get().strip()
        name = self.entry_name.get().strip()
        price = self.entry_price.get().strip()
        quantity = self.entry_quantity.get().strip()


        if not sku or not name or not price or not quantity:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            price = float(price)
            quantity = int(quantity)

            self.inventory_manager.add_product(sku, name, price, quantity)
            self.refresh_callback()
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid price or quantity.")

        
class EditProductWindow(tk.Toplevel):
    def __init__(self, parent, inventory_manager, item_values, refresh_callback):
        super().__init__(parent)
        self.title("Edit Product")
        self.inventory_manager = inventory_manager
        self.item_values = item_values
        self.refresh_callback = refresh_callback
        self.create_widgets()
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        self.wait_window(self)

    def create_widgets(self):
        
        self.label_sku = ttk.Label(self, text="SKU:")
        self.label_sku.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_sku = ttk.Entry(self)
        self.entry_sku.grid(row=0, column=1, padx=5, pady=5)
        self.entry_sku.insert(0, self.item_values[1])

        self.label_name = ttk.Label(self, text="Product Name:")
        self.label_name.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_name = ttk.Entry(self)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)
        self.entry_name.insert(0, self.item_values[2])

        self.label_price = ttk.Label(self, text="Price:")
        self.label_price.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_price = ttk.Entry(self)
        self.entry_price.grid(row=2, column=1, padx=5, pady=5)
        self.entry_price.insert(0, self.item_values[3])

        self.label_quantity = ttk.Label(self, text="Stock Quantity:")
        self.label_quantity.grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_quantity = ttk.Entry(self)
        self.entry_quantity.grid(row=3, column=1, padx=5, pady=5)
        self.entry_quantity.insert(0, self.item_values[4])

        
        save_button = ttk.Button(self, text="Save", command=self.save_changes)
        save_button.grid(row=4, column=0, padx=5, pady=10)

        cancel_button = ttk.Button(self, text="Cancel", command=self.destroy)
        cancel_button.grid(row=4, column=1, padx=5, pady=10)

    def save_changes(self):
        
        product_id = self.item_values[0]
        sku = self.entry_sku.get().strip()
        name = self.entry_name.get().strip()
        price = self.entry_price.get().strip()
        quantity = self.entry_quantity.get().strip()

       
        if not sku or not name or not price or not quantity:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            price = float(price)
            quantity = int(quantity)
           
            self.inventory_manager.edit_product(product_id, sku, name, price, quantity)
            self.refresh_callback()
            self.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid price or quantity.")

            
if __name__ == "__main__": 
    app = Application()
    app.mainloop()
            
          
    
            
    
    

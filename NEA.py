import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import psycopg2
from psycopg2 import sql
from tkinter import messagebox
import NEA_tables

def database_connection(): 
    try: 
        conn = psycopg2.connect(
            host ="localhost",
            database = "NEA",
            user = "postgres",
            password = "1510",
            port = "5432",
        )
        return conn
        
    except psycopg2.Error as error: 
        print(f"Found this error while trying to connect: {error}")
        return None
        
class Application(ttk.Window):
    def __init__(self): 
        super().__init__(title = "Sales Order Processing System")
        self.geometry("900x400")
        
        self.conn = database_connection()
        
        if not self.conn: 
            messagebox.showerror("Error", "Connection Unsuccessful")
            self.destroy()
            
        else: 
            self.widgets()
            
    def widgets(self): 
        
        for widget in self.winfo_children(): 
            widget.destroy()
            
        self.label_homepage_welcome = ttk.Label(self, text="Welcome To Fashion Match!")
        self.label_homepage_welcome.pack(pady=50)
        
        self.button_homepage_register = ttk.Button(self, text="Register", command=self.show_registration_page)
        self.button_homepage_register.pack(pady=10)
        
        self.button_homepage_login = ttk.Button(self, text="Login", command=self.user_login)
        self.button_homepage_login.pack(pady=10)
        
    def show_registration_page(self): 
        
        for widget in self.winfo_children(): 
            widget.destroy()
            
        self.geometry("900x400")
        self.title("Register")
            
        frame = ttk.Frame(self)
        frame.pack(pady=10)
        
        self.label_register_empcode = ttk.Label(frame, text="Employee Code", width=15)
        self.label_register_empcode.grid(row=0, column=0, padx=10, pady=10, sticky="E")
        
        self.entry_register_empcode = ttk.Entry(frame)
        self.entry_register_empcode.grid(row=0, column=1, pady=10)
        
        self.label_register_firstname = ttk.Label(frame, text="First Name")
        self.label_register_firstname.grid(row=1, column=0, padx=10, pady=10, sticky="E")
        
        self.entry_register_firstname = ttk.Entry(frame)
        self.entry_register_firstname.grid(row=1, column=1, pady=10)
        
        self.label_register_lastname = ttk.Label(frame, text="Last Name")
        self.label_register_lastname.grid(row=2, column=0, padx=10, pady=10, sticky="E")
        
        self.entry_register_lastname = ttk.Entry(frame)
        self.entry_register_lastname.grid(row=2, column=1, pady=10)
        
        self.label_register_email = ttk.Label(frame, text="Email")
        self.label_register_email.grid(row=3, column=0, padx=10, pady=10, sticky="E")
        
        self.entry_register_email = ttk.Entry(frame)
        self.entry_register_email.grid(row=3, column=1, pady=10)
        
        self.label_register_password = ttk.Label(frame, text="Password")
        self.label_register_password.grid(row=4, column=0, padx=10, pady=10, sticky="E")
        
        self.entry_register_password = ttk.Entry(frame)
        self.entry_register_password.grid(row=4, column=1, pady=10)
        
        self.button_register_register = ttk.Button(frame, text="Register", command=self.register_user)
        self.button_register_register.grid(row=5, column=1, padx=10, pady=10)
        
        self.button_register_homepage = ttk.Button(frame, text="Back", command=self.widgets)
        self.button_register_homepage.grid(row=5, column=0, sticky="E")
        
    def register_user(self): 
        
        employee_code = self.entry_register_empcode.get().strip()
        first_name = self.entry_register_firstname.get().strip()
        last_name = self.entry_register_lastname.get().strip()
        email = self.entry_register_email.get().strip()
        password = self.entry_register_password.get().strip()
        
        if not employee_code or not first_name or not last_name or not email: 
            messagebox.showerror("Error", "You must fill all boxes!")
            return
            
        self.insert_user(employee_code, first_name, last_name, email, password)
    
    def insert_user(self, employee_code, first_name, last_name, email, password):
        try: 
            cursor = self.conn.cursor()
            inserter = sql.SQL("""INSERT INTO Users(employee_code, first_name, last_name, email, password) VALUES (%s, %s, %s, %s, %s)""")
            cursor.execute(inserter, (employee_code, first_name, last_name, email, password))
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("Success", "You have been successfully registered!")
            self.clear_entrybox()
            
            self.widgets()
            
        except psycopg2.Error as error: 
            print(f"Found this error while trying to insert {error}")
            
    def clear_entrybox(self): 
        self.entry_register_empcode.delete(0, ttk.END)
        self.entry_register_firstname.delete(0, ttk.END)
        self.entry_register_lastname.delete(0, ttk.END)
        self.entry_register_email.delete(0, ttk.END)
        self.entry_register_password.delete(0, ttk.END)
        
    def user_login(self): 
        
        for widget in self.winfo_children(): 
            widget.destroy()
            
        frame = ttk.Frame()
        frame.pack(pady=10)
        
        self.label_login_empcode = ttk.Label(frame, text="Employee Code")
        self.label_login_empcode.grid(row=0, column=0, padx=10, pady=10, sticky="E")
        
        self.entry_login_empcode = ttk.Entry(frame)
        self.entry_login_empcode.grid(row=0, column=1, pady=10)

        self.label_login_email = ttk.Label(frame, text="Email")
        self.label_login_email.grid(row=1, column=0, padx=10, pady=10, sticky="E")
        
        self.entry_login_email = ttk.Entry(frame)
        self.entry_login_email.grid(row=1, column=1, pady=10)
        
        self.label_login_password = ttk.Label(frame, text="Password")
        self.label_login_password.grid(row=2, column=0, padx=10, pady=10, sticky="E")
        
        self.entry_login_password = ttk.Entry(frame)
        self.entry_login_password.grid(row=2, column=1, pady=10)
        
        self.button_login_login = ttk.Button(frame, text="Login", command=self.auth_userlogin)
        self.button_login_login.grid(row=3, column=1, padx=10, pady=10)
        
        self.button_login_homepage = ttk.Button(frame, text="Back", command=self.widgets)
        self.button_login_homepage.grid(row=3, column=0, sticky="E")

    def auth_userlogin(self): 
        
        employee_code = self.entry_login_empcode.get().strip()
        email = self.entry_login_email.get().strip()
        password = self.entry_login_password.get().strip()
        
        if not employee_code or not email or not password: 
            messagebox.showerror("Error", "You must fill in all boxes!")
            return
        
        try: 
            cursor = self.conn.cursor()
            authenticator = sql.SQL("""
                                    SELECT * FROM Users
                                    WHERE employee_code = %s AND email = %s AND password = %s
                                    """)
            cursor.execute(authenticator, (employee_code, email, password))
            user = cursor.fetchone()
            cursor.close()
            
            if user: 
                messagebox.showinfo("Success", "You have successfully logged in")
                
                self.show_main_window(user)
                
            else: 
                messagebox.showerror("Invalid Credentials", "Try again or Register")
            
        except Exception as error: 
            messagebox.showerror("Database Error:", error)
            
            
    def show_main_window(self, user): 
        
        for widget in self.winfo_children(): 
            widget.destroy()
            
        self.user = user
        
        self.geometry("900x400")
        self.title("Home Page")
        
        self.navigation_frame = ttk.Frame(self)
        self.navigation_frame.pack(side=TOP, fill=X)
        
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill=BOTH, expand=True)
        
        self.button_main_logout = ttk.Button(self.navigation_frame, text="Logout", command=self.widgets)
        self.button_main_logout.pack(side=LEFT, padx=5, pady=5)
        
        self.button_main_home = ttk.Button(self.navigation_frame, text="Home", command=self.show_home)
        self.button_main_home.pack(side=LEFT, padx=5, pady=5)
        
        self.label_main_welcome = ttk.Label(self.content_frame, text=f"Welcome {self.user[2]} {self.user[3]}")
        self.label_main_welcome.pack(pady=10)
        
        self.button_main_inventory = ttk.Button(self.navigation_frame, text="Inventory", command=self.display_inventory)
        self.button_main_inventory.pack(side=LEFT, padx= 5, pady=5)
        
        self.show_home()
        
    def show_home(self): 
        
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()
            
        self.title("Home Page")
        
        self.label_home_welcome = ttk.Label(self.content_frame, text=f"Welcome {self.user[2]} {self.user[3]}")
        self.label_home_welcome.pack(pady=10)

        
    def display_inventory(self):

        for widget in self.content_frame.winfo_children(): 
            widget.destroy()

        self.title("Inventory")

        self.button_inventory_add = ttk.Button(self.content_frame, text="Add Product", command=self.add_products)
        self.button_inventory_add.pack(side=TOP, padx=5, pady=5)
        
        #put edit product button here
        self.button_edit_product = ttk.Button(self.content_frame, text="Edit Product", command=self.edit_product)
        self.button_edit_product.pack(side=TOP, padx=5, pady=5)

        columns = ('SKU', 'Name', "Price/SQM", "Quantity")
        self.tree_inventory_list = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        
        
        self.tree_inventory_list.heading("SKU", text="SKU", anchor="center")
        self.tree_inventory_list.heading("Name", text="Name", anchor="center")
        self.tree_inventory_list.heading("Price/SQM", text="Price/SQM", anchor="center")
        self.tree_inventory_list.heading("Quantity", text="Quantity", anchor="center")
        
        self.tree_inventory_list.column("SKU", width="100", anchor="center", stretch=False)
        self.tree_inventory_list.column("Name", width=150, anchor="center", stretch=False)
        self.tree_inventory_list.column("Price/SQM", width=100, anchor="center", stretch=False)
        self.tree_inventory_list.column("Quantity", width=250, anchor="center", stretch=False)
        
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree_inventory_list.yview)
        self.tree_inventory_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.tree_inventory_list.pack(expand=True, padx=10, pady=10)

        try: 
            cursor = self.conn.cursor()
            displayer = """SELECT SKU, name, price_per_sqm, quantity FROM Inventory"""

            cursor.execute(displayer)
            inventory=cursor.fetchall()
            cursor.close()

            for product in inventory: 
                self.tree_inventory_list.insert('', 'end', value=product)

        except Exception as error: 
            messagebox.showerror("Error", f"Encountered this: {error}")

    def add_products(self): 
        
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()

        self.title("Add Product to Inventory")

        frame = self.content_frame

        self.label_productadd_sku = ttk.Label(frame, text="SKU")
        self.label_productadd_sku.grid(row=0, column=0, padx=5, pady=10)

        self.entry_productadd_sku = ttk.Entry(frame)
        self.entry_productadd_sku.grid(row=0, column=1, padx=5, pady=10)

        self.label_productadd_name = ttk.Label(frame, text="Name")
        self.label_productadd_name.grid(row=1, column=0, padx=5, pady=10)

        self.entry_productadd_name = ttk.Entry(frame)
        self.entry_productadd_name.grid(row=1, column=1, padx=5, pady=10)

        self.label_productadd_price = ttk.Label(frame, text="Price Per SQM")
        self.label_productadd_price.grid(row=2, column=0, padx=5, pady=10)

        self.entry_productadd_price = ttk.Entry(frame)
        self.entry_productadd_price.grid(row=2, column=1, padx=5, pady=10)

        self.label_productadd_quantity = ttk.Label(frame, text="Quantity")
        self.label_productadd_quantity.grid(row=3, column=0, padx=5, pady=10)

        self.entry_productadd_quantity = ttk.Entry(frame)
        self.entry_productadd_quantity.grid(row=3, column=1, padx=5, pady=10)

        self.button_productadd_save = ttk.Button(frame, text="Save", command=self.save_product, bootstyle=SUCCESS)
        self.button_productadd_save.grid(row=4, column=0, columnspan=2)


    def save_product(self): 

        sku = self.entry_productadd_sku.get().strip()
        name = self.entry_productadd_name.get().strip()
        price_per_sqm = self.entry_productadd_price.get().strip()
        quantity = self.entry_productadd_quantity.get().strip()

        if not sku or not name or not price_per_sqm: 
            messagebox.showerror("ERROR", "All Fields Are Required")

        try: 
            cursor = self.conn.cursor()

            save_product = sql.SQL("""
                                   INSERT INTO Inventory(SKU, name, price_per_sqm, quantity) VALUES (%s, %s, %s, %s)
                                   """)

            cursor.execute(save_product, (str(sku),  name, price_per_sqm, quantity))
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("SUCCESS", "Added new product to product list")
            self.display_inventory()
        except psycopg2.errors.UniqueViolation: 
            self.conn.rollback()
            messagebox.showerror("ERROR", "Product with this SKU already exists")
            
        except Exception as error: 
            messagebox.showerror("ERROR", f"Encountered this error: {error}")
            
    def edit_product(self): 
        #maybe make it so that you can see the old name as well as the new name when you type it in
        
        selected_product = self.tree_inventory_list.selection()
        if not selected_product: 
            messagebox.showerror("Error", "Please select an item")
            return
        
        product_values = self.tree_inventory_list.item(selected_product)['values']
        
        if not product_values: 
            messagebox.showerror("Error", "Selecte product has no data")
            return

        editing_window = ttk.Toplevel(self)
        editing_window.title("Edit Product")
        editing_window.geometry("500x500")
        editing_window.resizable(False, False)
        
        frame = ttk.Frame(editing_window)
        frame.pack(pady=10, fill='x', expand=True)
        
        for row in range(6): 
            frame.rowconfigure(row, weight=1)
            
        for column in range(5): 
            frame.columnconfigure(column, weight=1)
    
        self.label_edit_sku = ttk.Label(frame, text="New SKU")
        self.label_edit_sku.grid(row=0, column=1, padx=10, pady=10)
        
        self.entry_edit_sku = ttk.Entry(frame)
        self.entry_edit_sku.grid(row=0, column=2, sticky="w", pady=10)
        self.entry_edit_sku.insert(0, product_values[0])
        
        self.label_edit_name = ttk.Label(frame, text="New name")
        self.label_edit_name.grid(row=1, column=1, padx=10, pady=10)
        
        self.entry_edit_name = ttk.Entry(frame)
        self.entry_edit_name.grid(row=1, column=2, sticky="w", pady=10)
        self.entry_edit_name.insert(0, product_values[1])
        
        self.label_edit_price = ttk.Label(frame, text="New price per SQM")
        self.label_edit_price.grid(row=2, column=1, padx=10, pady=10)
        
        self.entry_edit_price = ttk.Entry(frame)
        self.entry_edit_price.grid(row=2, column=2, sticky="w", pady=10)
        self.entry_edit_price.insert(0, product_values[2])
        
        self.label_edit_quantity = ttk.Label(frame, text="New Quantity")
        self.label_edit_quantity.grid(row=3, column=1, padx=10, pady=10)
        
        self.entry_edit_quantity = ttk.Entry(frame)
        self.entry_edit_quantity.grid(row=3, column=2, sticky="w", pady=10)
        self.entry_edit_quantity.insert(0, product_values[3])
        
        self.button_edit_save = ttk.Button(frame, text="Save Changes", bootstyle=SUCCESS, command=lambda: self.save_edit_changes(self.entry_edit_sku.get().strip(), self.entry_edit_name.get().strip(), self.entry_edit_price.get().strip(), self.entry_edit_quantity.get().strip(), editing_window))
        self.button_edit_save.grid(row=4, column=1, columnspan=2, pady=10)
        
    def save_edit_changes(self, sku, name, price_per_sqm, quantity, frame): 

        if not sku or not name or not price_per_sqm or not quantity:
            messagebox.showerror("Error", "All fields are required")
            return
        
        try: 
            price_per_sqm = float(price_per_sqm)
        except ValueError: 
            messagebox.showerror("Error", "Price must be an integer or decimal number")
            return

        try: 
            cursor = self.conn.cursor()
                
            selected_item = self.tree_inventory_list.selection()
            original_sku = self.tree_inventory_list.item(selected_item)['values'][0]
                
            if sku != original_sku: 
                cursor.execute("SELECT SKU FROM Inventory WHERE SKU = %s", (str(sku),))
                if cursor.fetchone(): 
                    messagebox.showerror("Error", "Another product with this SKU already exists")
                    return
        
            updating_inventory = sql.SQL("""UPDATE Inventory SET SKU = %s, name = %s, price_per_sqm = %s, quantity = %s WHERE SKU = %s""")
            cursor.execute(updating_inventory, (str(sku), name, price_per_sqm, quantity, str(original_sku)))
            self.conn.commit()
            messagebox.showinfo("Success", "Product has been updated")
            self.display_inventory()
            frame.destroy()
        
        except psycopg2.errors.UniqueViolation: 
            self.conn.rollback()
            messagebox.showerror("Error", "Product with this SKU already exists")
        except Exception as error: 
            self.conn.rollback()
            messagebox.showerror("Error", f"Encountered this error: {error}")
            print(f"Encountered this error: {error}")

if __name__ == "__main__":
    NEA_tables.create_tables()
    app = Application()
    app.mainloop()
    
    
    #things that are next in line
        #hashing
        #search bar for inventory
        #clients
        #orders
        #deliveries
        #reports

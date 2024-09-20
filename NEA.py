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
        
        self.button_main_products = ttk.Button(self.navigation_frame, text="Products", command=self.show_products)
        self.button_main_products.pack(side=LEFT, padx= 5, pady=5)
        
        self.button_main_inventory = ttk.Button(self.navigation_frame, text="Inventory", command=None)
        self.button_main_inventory.pack(side=LEFT, padx= 5, pady=5)
        
        self.show_home()
        
    def show_home(self): 
        
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()
            
        self.title("Home Page")
        
        self.label_home_welcome = ttk.Label(self.content_frame, text=f"Welcome {self.user[2]} {self.user[3]}")
        self.label_home_welcome.pack(pady=10)
        
    def show_products(self): #shows all products and has a thing at the 
        
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()
            
            
        self.title("Products")
        
        self.button_products_add = ttk.Button(self.content_frame, text="Add Product", command=self.add_products)
        self.button_products_add.pack(side=TOP, padx=5, pady=5)
        
        self.display_products()
        
        
    def display_products(self):
        columns = ('SKU', 'Name', "Price/SQM", "Description")
        self.tree_products_list = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        
        
        self.tree_products_list.heading("SKU", text="SKU", anchor="center")
        self.tree_products_list.heading("Name", text="Name", anchor="center")
        self.tree_products_list.heading("Price/SQM", text="Price/SQM", anchor="center")
        self.tree_products_list.heading("Description", text="Description", anchor="center")
        
        self.tree_products_list.column("SKU", width="100", anchor="center", stretch=False)
        self.tree_products_list.column("Name", width=150, anchor="center", stretch=False)
        self.tree_products_list.column("Price/SQM", width=100, anchor="center", stretch=False)
        self.tree_products_list.column("Description", width=250, anchor="center", stretch=False)
        
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree_products_list)
        self.tree_products_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        self.tree_products_list.pack(expand=True, padx=10, pady=10)

        try: 
            cursor = self.conn.cursor()
            displayer = """SELECT SKU, name, price_per_sqm, description FROM Products"""

            cursor.execute(displayer)
            products=cursor.fetchall()
            cursor.close()

            for product in products: 
                self.tree_products_list.insert('', 'end', value=product)

        except Exception as error: 
            messagebox.showerror("Error", f"Encountered this: {error}")

    def add_products(self): 
        
        for widget in self.content_frame.winfo_children(): 
            widget.destroy()

        self.title("Add Products")

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

        self.label_productadd_description = ttk.Label(frame, text="Description")
        self.label_productadd_description.grid(row=3, column=0, padx=5, pady=10)

        self.entry_productadd_description = ttk.Entry(frame)
        self.entry_productadd_description.grid(row=3, column=1, padx=5, pady=10)

        self.button_productadd_save = ttk.Button(frame, text="Save", command=self.save_product, bootstyle=SUCCESS)
        self.button_productadd_save.grid(row=4, column=0, columnspan=2)


    def save_product(self): 

        sku = self.entry_productadd_sku.get().strip()
        name = self.entry_productadd_name.get().strip()
        price_per_sqm = self.entry_productadd_price.get().strip()
        description = self.entry_productadd_description.get().strip()

        if not sku or not name or not price_per_sqm: 
            messagebox.showerror("ERROR", "All Fields Are Required")

        try: 
            cursor = self.conn.cursor()

            save_product = sql.SQL("""
                                   INSERT INTO Products(SKU, name, price_per_sqm, description) VALUES (%s, %s, %s, %s)
                                   """)

            cursor.execute(save_product, (sku,  name, price_per_sqm, description))
            self.conn.commit()
            cursor.close()
            messagebox.showinfo("SUCCESS", "Added new product to product list")
            self.show_products()
        except psycopg2.errors.UniqueViolation: 
            self.conn.rollback()
            messagebox.showerror("ERROR", "Product with this SKU already exists")
            
        except Exception as error: 
            messagebox.showerror("ERROR", f"Encountered this error: {error}")

if __name__ == "__main__":
    NEA_tables.create_tables()
     
    app = Application()
    app.mainloop()

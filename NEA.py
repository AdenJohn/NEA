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
        self.geometry("500x500")
        
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
            
        frame = ttk.Frame()
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
        
        self.button_register_homepage = ttk.Button(frame, text="Home", command=self.widgets)
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
        
        self.label_login_empcode = ttk.Label(frame, text="Employee Code", width=15)
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
        
        self.button_login_homepage = ttk.Button(frame, text="Home", command=self.widgets)
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
            
        frame = ttk.Frame()
        frame.pack(pady=10)
        
        self.label_main_welcome = ttk.Label(frame, text=f"Welcome, {user[2]} {user[3]}")
        self.label_main_welcome.grid(row=1, column=0, pady=10)
        
        
        self.button_main_logout = ttk.Button(frame, text="Logout", command=self.widgets)
        self.button_main_logout.grid(row=0, column=0, padx=10, pady=10)

        
if __name__ == "__main__":
    NEA_tables.create_tables()
     
    app = Application()
    app.mainloop()
    
    
    
        
        
        
          
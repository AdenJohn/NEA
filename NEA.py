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
            print(f"User {first_name} {last_name} has been registered")
        except Exception as error: 
            messagebox.showerror("Error", f"Error while registration: {error}")
        
    def authenticate_user(self, employee_code, password): #checks if their login credentials are correct when they login
        
        query_authentication = """SELECT first_name, last_name, password_hash, password_salt 
                                  FROM Users WHERE employee_code = %s"""
        
        try: 
            cursor = self.database_manager.execute_query(query_authentication, (employee_code))
            user_data = cursor.fetchone()
            if user_data: 
                first_name, last_name, stored_password, stored_salt = user_data
                bytes_salt = bytes.fromhex(stored_salt)
                
                if self.verify_password(password, stored_salt, stored_password): 
                    print(f"User {first_name} {last_name} authenticated successfully")
                    return first_name, last_name
            return None
        except Exception as error:
            messagebox.showerror("Error", f"Encountered error: {error}")
            return None
        
    def verify_password(self, login_password, salt, stored_password): #hashes their login password to see if its the same as the registration one
        login_hash = self.hash_password(login_password, salt)
        
        return login_hash == stored_password
    
        
    
        
            
        
        
        
    
        
    
        
    
            
            
            
        
        





-- DDL Script for the NEA, this is used to create tables. I will be importing and using this in my main application

-- Users Table
CREATE TABLE IF NOT EXISTS Users(
    user_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL, 
    password_hash VARCHAR(255) NOT NULL, 
    password_salt VARCHAR(255) NOT NULL);

-- Clients Table
CREATE TABLE IF NOT EXISTS Clients(
    client_id SERIAL PRIMARY KEY, 
    client_name VARCHAR(255) NOT NULL, 
    client_email VARCHAR(150) UNIQUE NOT NULL, 
    client_phone VARCHAR(20) UNIQUE NOT NULL, 
    address_line VARCHAR(255) NOT NULL, 
    city VARCHAR(100) NOT NULL, 
    postcode VARCHAR(20), 
    country VARCHAR(100) NOT NULL, 
    full_address TEXT);

-- Inventory Table
CREATE TABLE IF NOT EXISTS Inventory(
    product_id SERIAL PRIMARY KEY, 
    SKU VARCHAR(10) UNIQUE NOT NULL, 
    product_name VARCHAR(255) NOT NULL, 
    product_price DECIMAL(10,2) NOT NULL, 
    stock_quantity INT NOT NULL); 

-- Orders Table
CREATE TABLE IF NOT EXISTS Orders(
    order_id SERIAL PRIMARY KEY, 
    client_id INT REFERENCES Clients(client_id) ON DELETE CASCADE, 
    order_date DATE DEFAULT CURRENT_DATE, 
    total_price DECIMAL(10,2),
    order_status VARCHAR(20) DEFAULT 'PENDING',
    payment_status VARCHAR(20) DEFAULT 'UNPAID',
    estimated_deliverydate DATE, 
    delivery_date DATE);

-- Order Items Table
CREATE TABLE IF NOT EXISTS OrderItems(
    order_item_id SERIAL PRIMARY KEY, 
    order_id INT REFERENCES Orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES Inventory(product_id), 
    product_quantity INT NOT NULL, 
    total_price DECIMAL(10,2) NOT NUll);

--DDL Script

CREATE TABLE IF NOT EXISTS Users(
	user_id SERIAL PRIMARY KEY, 
	employee_code VARCHAR(50), 
	first_name VARCHAR(100) NOT NULL, 
	last_name VARCHAR(100) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	password_salt VARCHAR(255) NOT NULL); 

CREATE TABLE IF NOT EXISTS Inventory(
	product_id SERIAL PRIMARY KEY, 
	sku VARCHAR(50) UNIQUE NOT NULL, 
	product_name VARCHAR(255) UNIQUE NOT NULL,
	price DECIMAL(10, 2) NOT NULL, 
	stock_quantity INT NOT NULL DEFAULT 0);

CREATE TABLE IF NOT EXISTS Client(
	client_id SERIAL PRIMARY KEY, 
	client_name VARCHAR(255) NOT NULL, 
	client_email VARCHAR(255), 
	client_phone VARCHAR(50), 
	address_line VARCHAR(250), 
	city VARCHAR(100), 
	country VARCHAR(100), 
	full_address TEXT);

CREATE TABLE IF NOT EXISTS Orders(
	order_id SERIAL PRIMARY KEY,
	client_id INT NOT NULL, 
	order_date DATE NOT NULL, 
	total_price DECIMAL(10,2) NOT NULL, 
	order_status VARCHAR(50) NOT NULL, 
	payment_status VARCHAR(50) NOT NULL, 
	estimated_delivery_date DATE, 
	delivery_date DATE, 
	processed_by INT,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(), 
	updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
	CONSTRAINT fk_orders_client FOREIGN KEY (client_id) REFERENCES client (client_id) ON DELETE CASCADE, 
	CONSTRAINT fk_orders_user FOREIGN KEY (processed_by) REFERENCES users (user_id) ON DELETE SET NULL); 

CREATE TABLE IF NOT EXISTS OrderItems(
	order_item_id SERIAL PRIMARY KEY, 
	order_id INT NOT NULL, 
	product_id INT NOT NULL, 
	product_quantity INT NOT NULL, 
	total_price DECIMAL(10,2) NOT NULL, 
	CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE, 
	CONSTRAINT fk_order_items_inventory FOREIGN KEY (product_id) REFERENCES inventory (product_id) ON DELETE RESTRICT
); 

CREATE TABLE IF NOT EXISTS Invoices(
	invoice_id SERIAL PRIMARY KEY, 
	order_id INT NOT NULL, client_id INT NOT NULL, 
	tax DECIMAL(10,2) NOT NULL, 
	total_price DECIMAL(10,2) NOT NULL, 
	payment_method VARCHAR(50), 
	CONSTRAINT fk_invoices_orders FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE, 
	CONSTRAINT fk_invoices_client FOREIGN KEY (client_id) REFERENCES client (client_id) ON DELETE RESTRICT, 

CREATE TABLE IF NOT EXISTS ProductReturns(
	return_id SERIAL PRIMARY KEY, 
	order_id INT NOT NULL, 
	order_item_id INT NOT NULL, 
	return_reason TEXT, 
	return_status VARCHAR(50), 
	refund_amount DECIMAL(10,2), 
	CONSTRAINT fk_returns_orders FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE, 
	CONSTRAINT fk_returns_order_items FOREIGN KEY (order_item_id) REFERENCES order_items (order_item_id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS Reports(
	report_id SERIAL PRIMARY KEY, 
	report_type VARCHAR(50), 
	generated_date DATE NOT NULL DEFAULT CURRENT_DATE, 
	parameters JSON, report_output TEXT, generated_by INT, 
	client_id INT, 
	CONSTRAINT fk_reports_user FOREIGN KEY (generated_by) REFERENCES users (user_id) ON DELETE SET NULL, 
	CONSTRAINT fk_reports_client FOREIGN KEY (client_id) REFERENCES client (client_id) ON DELETE SET NULL);

CREATE TABLE IF NOT EXISTS AuditLog(
	audit_id SERIAL PRIMARY KEY, 
	table_name VARCHAR(50) NOT NULL, 
	record_id INT NOT NULL, 
	operation VARCHAR(10) NOT NULL, 
	changed_by INT NOT NULL, 
	changed_at TIMESTAMP NOT NULL DEFAULT NOW(), 
	old_data JSONB, 
	new_data JSONB, 
	CONSTRAINT fk_audit_log_user FOREIGN KEY (changed_by) REFERENCES users (user_id) ON DELETE CASCADE);

from Database.database_manager import DatabaseManager
from Models.Orders import Orders
from Models.OrderItem import OrderItem

class OrderManager: 
    def __init__(self, db_manager: DatabaseManager): 
        self.db_manager = db_manager

    def create_order(self, client_id, order_date, total_price, order_status, payment_status, estimated_delivery_date=None, delivery_date=None, processed_by=None): 
        query = """INSERT INTO Orders(client_id, order_date, total_price, order_status, payment_status, estimated_delivery_date, delivery_date, processed_by) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING order_id"""
        paramaters = (client_id, order_date, total_price, order_status, payment_status, estimated_delivery_date, delivery_date, processed_by)
        create_order = self.db_manager.execute_query(query, paramaters)
        if create_order: 
            order_id = create_order[0][0]
            return order_id
        else: 
            return None

    def add_order_item(self, order_id, product_id, product_quantity, total_price): 
        query = """INSERT INTO OrderItems(order_id, product_id, product_quantity, total_price) VALUES(%s,%s,%s,%s)"""
        paramaters = (order_id, product_id, product_quantity, total_price)
        self.db_manager.execute_query(query, paramaters)

    def update_order(self, order_id, new_total_price=None, new_order_status=None, new_payment_status=None, new_estimated_delivery_date=None, new_delivery_date=None): 
        query = """UPDATE Orders SET 
            total_price = COALESCE(%s, total_price),
            order_status = COALESCE(%s, order_status),
            payment_status = COALESCE(%s, payment_status),
            estimated_delivery_date = COALESCE(%s, estimated_delivery_date),
            delivery_date = COALESCE(%s, delivery_date),
            updated_at = NOW() WHERE order_id = %s"""

        paramaters = (new_total_price, new_order_status, new_payment_status, new_estimated_delivery_date, new_delivery_date)
        self.database_manager.execute_query(query, paramaters)

    def delete_order(self, order_id): 
        query = """DELETE FROM Orders WHERE order_id = %s"""
        self.database_manager.execute_query(query, (order_id,))

    def update_order_item(self, order_item_id, new_product_quantity=None, new_total_price=None): 
        query = """UPDATE OrderItems SET
            product_quantity = COALESCE(%s, product_quantity), 
            total_price = COALESCE(%s, total_price) WHERE order_item_id = %s""" 

        paramaters = (new_product_quantity, new_total_price, order_item_id)
        self.db_manager.execute_query(query, paramaters)

    def get_all_orders(self): 
        query = """SELECT order_id, client_id, order_date, total_price, order_status, payment_status, estimated_delivery_date, delivery_date, processed_by, created_at, updated_at FROM Orders ORDER BY created_at DESC"""

        order_rows = self.db_manager.execute_query(query)
        orders = []

        if order_rows: 
            for row in order_rows: 
                order = Orders(
                    order_id=row[0], 
                    client_id=row[1],
                    order_date=row[2],
                    total_price=row[3],
                    order_status=row[4],
                    payment_status=row[5],
                    estimated_delivery_date=row[6],
                    delivery_date=row[7],
                    processed_by=row[8],
                    created_at=row[9],
                    updated_at=row[10])
                orders.append(order)
            return orders


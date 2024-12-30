from Database.database_manager import DatabaseManager
from Models.Inventory import Inventory

class InventoryManager: 
    def __init__(self, dbmanager: DatabaseManager): 
        self.dbmanager = dbmanager

    def add_product(self, sku, product_name, price, stock_quantity):

        
        adding_query = """INSERT INTO Inventory(sku, product_name, price, stock_quantity)VALUES(%s, %s, %s)"""
        adding_paramaters = (sku, product_name, price, stock_quantity)

        try: 
            self.dbmanager.execute_query(adding_query, adding_paramaters)

        except Exception as error: 
            print(f"Error occured while adding product {error}")

    def get_products(self):
        get_query = """SELECT product_id, sku, product_name, stock_quantity FROM Inventory"""

        try: 
            rows = self.dbmanager.execute_query(get_query)
            products = []

            if rows: 
                for row in rows: 
                    product = Inventory(
                        product_id = row[0], 
                        sku = row[1], 
                        product_name = row[2], 
                        price = row[3],
                        stock_quantity = row[4])
                    
                    products.append(product)
                return products
        except Exception as error: 
            print(f"Error while fetching products: {error}")

    def edit_product(self, product_id, new_sku=None, new_product_name=None, new_price=None, new_stock_quantity=None):

        edit_query = """"UPDATE Inventory SET sku = COALESCE(%s, sku), product_name = COALESCE(%s, product_name), price = COALESCE(%s, price), stock_quantity= COALESCE(%s, stock_quantity) WHERE product_id = %s"""
        edit_paramaters = (new_sku, new_product_name, new_price, new_stock_quantity, product_id)

        try: 
            self.dbmanager.execute_query(edit_query, edit_paramaters)
            print("Product edited successfully")
        except Exception as error: 
            print(f"Error occured while editing product with id: {product_id}") 

    def remove_product(self, product_id):

        remove_query = """DELETE FROM Inventory WHERE product_id = %s"""

        try: 
            self.dbmanager.execute_query(remove_query, (product_id,))
            print("Product removed successfully")

        except Exception as error: 
            print(f"Error while removing product: {error}") 

        
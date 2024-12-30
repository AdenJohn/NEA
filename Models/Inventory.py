class Inventory: 
    def __init__(self, product_id=None, sku="", price=None, stock_quantity=None): 

        self.product_id = product_id
        self.sku = sku 
        self.price = price
        self.stock_quantity = stock_quantity

    def in_stock(self, quantity=1): 
        return self.stock_quantity >= quantity
    

class OrderItem: 
    def __init__(self, order_item_id=None, order_id=None, product_id=None, product_quantity=1, total_price=0.0): 

        self.order_item_id = order_item_id
        self.order_id = order_id
        self.product_id = product_id
        self.product_quantity = product_quantity
        self.total_price = total_price

    def calculate_total(self, product_price): 

        self.total_price = self.product_quantity * product_price
        return self.total_price

class Orders: 
    def __init__(self, order_id=None, order_date=None, total_price=None, order_status="", payment_status="", estimated_delivery_date=None, delivery_date=None, processed_by=None, created_at=None, updated_at=None):
       
       self.order_id = order_id
       self.order_date = order_date
       self.total_price = total_price
       self.order_status = order_status
       self.payment_status = payment_status
       self.estimated_delivery = estimated_delivery_date
       self.delivery_date = delivery_date
       self.processed_by = processed_by
       self.created_at = created_at
       self.updated_at = updated_at

    def is_delivered(self): 
        return self.order_status == "Delivered"
    


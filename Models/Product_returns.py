class ProductReturns: 
    def __init__(self, return_id=None, order_id=None, order_item_id=None, return_reason="", return_status="Requested", refund_amount=0.0): 

        self.return_id = return_id
        self.order_id = order_id
        self.order_item_id = order_item_id
        self.return_reason = return_reason
        self.return_status = return_status
        self.refund_amount = refund_amount

    def approve_return(self, refund_amount): 
        
        self.return_status = "Approved"
        self.refund_amount = refund_amount

        
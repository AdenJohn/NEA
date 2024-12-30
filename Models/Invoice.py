class Invoice: 
    def __init__(self, invoice_id=None, order_id=None, client_id=None, tax=0, total_price=0.0, payment_method=""): 

        self.invoice_id = invoice_id
        self.order_id = order_id
        self.client_id = client_id 
        self.tax = tax
        self.total_price = total_price
        self.payment_method = payment_method

    def total_with_tax(self, total_without_tax):

        self.total_price = self.tax * total_without_tax
        return self.total_price
    

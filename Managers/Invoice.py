from Database.database_manager import DatabaseManager

class InvoiceManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def create_invoice(self, order_id, client_id, tax, total_price, payment_method):
        query = """
        INSERT INTO Invoices(order_id, client_id, tax, total_price, payment_method)
        VALUES(%s, %s, %s, %s, %s) RETURNING invoice_id
        """
        parameters = (order_id, client_id, tax, total_price, payment_method)
        result = self.db_manager.execute_query(query, parameters)
        if result:
            return result[0][0]
        return None

    def get_invoice_history(self):
        query = """
        SELECT invoice_id, order_id, client_id, tax, total_price, payment_method 
        FROM Invoices 
        ORDER BY invoice_id DESC
        """
        rows = self.db_manager.execute_query(query)
        invoices = []
        if rows:
            for row in rows:
                invoice = {
                    "invoice_id": row[0],
                    "order_id": row[1],
                    "client_id": row[2],
                    "tax": row[3],
                    "total_price": row[4],
                    "payment_method": row[5]
                }
                invoices.append(invoice)
        return invoices

    def delete_invoice(self, invoice_id):
        query = "DELETE FROM Invoices WHERE invoice_id = %s"
        self.db_manager.execute_query(query, (invoice_id,))
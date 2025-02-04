from Database.database_manager import DatabaseManager

class ProductReturnsManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def log_return(self, order_id, order_item_id, return_reason, return_status, refund_amount):
        query = """
        INSERT INTO ProductReturns(order_id, order_item_id, return_reason, return_status, refund_amount)
        VALUES(%s, %s, %s, %s, %s)
        """
        parameters = (order_id, order_item_id, return_reason, return_status, refund_amount)
        self.db_manager.execute_query(query, parameters)

    def update_return_status(self, return_id, new_status):
        query = """
        UPDATE ProductReturns
        SET return_status = %s
        WHERE return_id = %s
        """
        parameters = (new_status, return_id)
        self.db_manager.execute_query(query, parameters)

    def delete_return(self, return_id):
        query = "DELETE FROM ProductReturns WHERE return_id = %s"
        self.db_manager.execute_query(query, (return_id,))

    def get_all_returns(self):
        query = """
        SELECT return_id, order_id, order_item_id, return_reason, return_status, refund_amount 
        FROM ProductReturns 
        ORDER BY return_id DESC
        """
        rows = self.db_manager.execute_query(query)
        returns = []
        if rows:
            for row in rows:
                ret = {
                    "return_id": row[0],
                    "order_id": row[1],
                    "order_item_id": row[2],
                    "return_reason": row[3],
                    "return_status": row[4],
                    "refund_amount": row[5]
                }
                returns.append(ret)
        return returns



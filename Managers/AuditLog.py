from Database.database_manager import DatabaseManager
import json

class AuditLogManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def log_change(self, table_name, record_id, operation, changed_by, old_data, new_data):
        query = """
        INSERT INTO AuditLog(table_name, record_id, operation, changed_by, changed_at, old_data, new_data)
        VALUES(%s, %s, %s, %s, NOW(), %s, %s)
        """
        parameters = (
            table_name,
            record_id,
            operation,
            changed_by,
            json.dumps(old_data),
            json.dumps(new_data)
        )
        self.db_manager.execute_query(query, parameters)

    def get_audit_logs(self):
        query = """
        SELECT audit_id, table_name, record_id, operation, changed_by, changed_at, old_data, new_data 
        FROM AuditLog 
        ORDER BY changed_at DESC
        """
        rows = self.db_manager.execute_query(query)
        logs = []
        if rows:
            for row in rows:
                log = {
                    "audit_id": row[0],
                    "table_name": row[1],
                    "record_id": row[2],
                    "operation": row[3],
                    "changed_by": row[4],
                    "changed_at": row[5],
                    "old_data": row[6],
                    "new_data": row[7]
                }
                logs.append(log)
        return logs
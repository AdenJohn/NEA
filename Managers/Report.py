from Database.database_manager import DatabaseManager
import json

class ReportManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def generate_profit_report(self):
        query = """
        SELECT client_id, SUM(total_price) AS total_profit 
        FROM Orders 
        GROUP BY client_id
        """
        rows = self.db_manager.execute_query(query)
        report = []
        if rows:
            for row in rows:
                report.append({
                    "client_id": row[0],
                    "total_profit": row[1]
                })
        return report

    def generate_total_revenue_report(self):
        query = "SELECT SUM(total_price) FROM Orders"
        rows = self.db_manager.execute_query(query)
        if rows:
            return rows[0][0]
        return 0

    def generate_custom_report(self, parameters: dict):
        """
        Example: Search for reports whose parameters (stored as JSON) match a given pattern.
        """
        param_json = json.dumps(parameters)
        query = """
        SELECT report_id, report_type, generated_date, parameters, report_output, generated_by, client_id 
        FROM Reports 
        WHERE parameters::text LIKE %s
        """
        rows = self.db_manager.execute_query(query, (f"%{param_json}%",))
        reports = []
        if rows:
            for row in rows:
                report = {
                    "report_id": row[0],
                    "report_type": row[1],
                    "generated_date": row[2],
                    "parameters": row[3],
                    "report_output": row[4],
                    "generated_by": row[5],
                    "client_id": row[6]
                }
                reports.append(report)
        return reports

    def delete_report(self, report_id):
        query = "DELETE FROM Reports WHERE report_id = %s"
        self.db_manager.execute_query(query, (report_id,))




class Reports: 
    def __init__(self, report_id=None, report_type="", generated_date=None, paramaters=None, report_output=None, generated_by=None, client_id=None): 

        self.report_id = report_id
        self.report_type = report_type
        self.generated_date = generated_date
        self.paramaters = paramaters
        self.report_ouput = report_output
        self.generated_by = generated_by
        self.client_id = client_id


    def show_paramaters(self): 

        return str(self.paramaters)
    
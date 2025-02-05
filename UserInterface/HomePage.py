import ttkbootstrap as ttk
from ttkbootstrap.constants import * 
from BasePage import BasePage

class HomePage(BasePage): 
    def __init__(self, parent, controller, *args, **kwargs): 
        super().__init__(parent, controller, *args, **kwargs)

        self.show_navigation_buttons()
        
        self.title_label = ttk.Label(self.main_frame, text="Welcome to the Dashboard", font=("Arial", 20))
        self.title_label.pack(pady=(20, 10))

        self.dashboard_frame = ttk.Frame(self.main_frame)
        self.dashboard_frame.pack(pady=10)

        self.inventory_button = ttk.Button(self.dashboard_frame, text="Inventory", command=lambda: self.navigate_to("Inventory"))
        self.inventory_button.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        self.clients_button = ttk.Button(self.dashboard_frame, text="Clients", command=lambda: self.navigate_to("Clients"))
        self.clients_button.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.orders_button = ttk.Button(self.dashboard_frame, text="Orders", command=lambda: self.navigate_to("Orders"))
        self.orders_button.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        self.invoices_button = ttk.Button(self.dashboard_frame, text="Invoices", command=lambda: self.navigate_to("Invoices"))
        self.invoices_button.grid(row=3,column=1, padx=5, pady=10, sticky="ew")

        self.reports_button = ttk.Button(self.dashboard_frame, text="Reports", command=lambda: self.navigate_to("Reports"))
        self.reports_button.grid(row=4, column=1, padx=5, pady=10, sticky="ew")

        self.auditlog_button = ttk.Button(self.dashboard_frame, text="AuditLog", command=lambda: self.navigate_to("AuditLog"))
        self.auditlog_button.grid(row=5, column=1, padx=5, pady=10, sticky="ew")

    
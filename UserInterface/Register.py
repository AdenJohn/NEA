import ttkbootstrap as ttk 
from ttkbootstrap.constants import * 
from ttkbootstrap.dialogs import Messagebox
from BasePage import BasePage
from Managers.User import UserManager

class RegisterPage(BasePage): 
    def __init__(self, parent, controller, *args, **kwargs): 
        super().__init__(parent, controller, *args, **kwargs)

        self.hide_navigation_buttons()

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        self.title_label = ttk.Label(self.main_frame, text="Register New User", font=("Aerial", 15))
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        self.empcode_label = ttk.Label(self.main_frame, text="Employee Code: ")
        self.empcode_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.empcode_entry = ttk.Entry(self.main_frame)
        self.empcode_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.fname_label =ttk.Label(self.main_frame, text="First Name: ")
        self.fname_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.fname_entry = ttk.Label(self.main_frame)
        self.fname_entry.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        self.lname_label =ttk.Label(self.main_frame, text="Last Name: ")
        self.lname_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.lname_entry = ttk.Label(self.main_frame)
        self.lname_entry.grid(row=3, column=1, padx=5, pady=10, sticky="w")

        self.email_label = ttk.Label(self.main_frame, text="Email: ")
        self.email_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.email_entry = ttk.Entry(self.main_frame)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.password_label = ttk.Label(self.main_frame, text="Password: ")
        self.password_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(self.main_frame)
        self.password_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        self.back_button = ttk.Button(self.main_frame, text="Back", command=lambda: self.navigate_to("LandingPage"))
        self.back_button.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.register_button = ttk.Button(self.main_frame, text="Register", command=lambda: self.register())
        self.register_button.grid(row=6, column=1, padx=10, pady=10, sticky="w")

    def register(self):
        employee_code = self.empcode_entry.get().strip()
        first_name = self.fname_entry.get().strip()
        last_name = self.lname_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if UserManager.register_user(employee_code, first_name, last_name, email, password): 
            Messagebox.show_info(f"Registered User: {first_name} {last_name}, {employee_code} successfully.")

        else: 
            Messagebox.show_error("Error while registering")
        


import ttkbootstrap as ttk 
from ttkbootstrap.constants import * 
from BasePage import BasePage
from Managers.User import UserManager

class LoginPage(BasePage): 
    def __init__(self, parent, controller, *args, **kwargs): 
        super().__init__(parent, controller, *args, **kwargs)

        self.hide_navigation_buttons()

        self.title_label = ttk.Label(self.main_frame, text="User Login", font=("Aerial", 15))
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky="new")

        self.empcode_label = ttk.Label(self.main_frame, text="Employee Code: ")
        self.empcode_label.grid(row=1, column=0, padx=5, pady=10, sticky="e")

        self.empcode_entry = ttk.Entry(self.main_frame)
        self.empcode_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        self.password_label = ttk.Label(self.main_frame, text="Password: ")
        self.password_label.grid(row=2, column=0, padx=5, pady=10, sticky="e")

        self.password_entry = ttk.Entry(self.main_frame)
        self.password_entry.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        self.login_button = ttk.Button(self.main_frame, text="Login", command=lambda: self.login())
        self.login_button.grid(row=3, column=(0,1), padx=5, pady=10, sticky="ew")

    def login(self): 
        employee_code = self.empcode_entry.get().strip()
        password = self.password_entry.get().strip()

        if UserManager.login_user(employee_code, password): 
            Messagebox.show_info(f"Success", "Login Successful")
            self.navigate_to("HomePage")
        else: 
            Messagebox.show_error("Invalid Credentials", "User could not be logged in")




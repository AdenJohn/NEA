import ttkbootstrap as ttk
from ttkbootstrap.constants import * 
from BasePage import BasePage

class LandingPage(BasePage): 
    def __init__(self, parent, controller, *args, **kwargs): 
        super().__init__(parent, controller, *args, **kwargs)

        self.hide_navigation_buttons()

        self.main_frame.columnconfigure(0, weight=1)

        welcome_label = ttk.Label(self.main_frame, text="Welcome to Fashion Match!", font=("Aerial", 16))
        welcome_label.grid(row=0, column=0, pady=(20,10), sticky="n")

        prompt_label = ttk.Label(self.main_frame, text="Please Login or Register to continue", font=("Aerial", 12))
        prompt_label.grid(row=1, column=0, sticky='n', pady=5)

        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, pady=10)

        login_button = ttk.Button(button_frame, text="Login", bootstyle="SUCCESS", command=lambda: self.navigate_to("LoginPage"))
        login_button.pack(side=TOP, padx=10)

        register_button = ttk.Button(button_frame, text="Register", bootstyle="WARNING", command=lambda: self.navigate_to("RegisterPage"))
        register_button.pack(side=TOP, padx=10)

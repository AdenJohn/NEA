import ttkbootstrap as ttk
from ttkbootstrap.constants import * 
from ttkbootstrap.dialogs import Messagebox

class BasePage(ttk.Frame): 
    def __init__(self, parent, controller, *args, **kwargs):
        super().__init__(self, parent, *args, **kwargs)
        
        self.controller = controller

        self.navigation_frame = ttk.Frame(self, bootstyle="primary")
        self.navigation_frame.pack(side=TOP, fill=X)

        
        self.header_label = ttk.Label(self.navigation_frame, text="Fashion Match (SOP)", bootstyle="inverse-primary", font=("Arial", 16))
        self.header_label.pack(side=TOP, padx=5, pady=5)

        self.home_button = ttk.Button(self.navigation_frame, text="Home", bootstyle="SUCCESS", command=lambda: self.controller.clear_stack())
        self.back_button = ttk.Button(self.navigation_frame, text="Back", bootstyle="WARNING", command=self.controller.go_back())
        self.logout_button = ttk.Button(self.navigation_frame, text="Logout", bootstyle="DANGER", command=lambda: self.navigate_to("LandingPage"))

        self.main_frame = ttk.Frame(self, bootstyle="INFO")
        self.main_frame.pack(side=TOP, fill=X, expand=YES, padx=10, pady=10)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

        self.hide_navigation_buttons()

    def show_navigation_buttons(self): 

        self.home_button.pack(side=LEFT, padx=5)
        self.back_button.pack(side=LEFT, padx=5)

        self.logout_button.pack(side=RIGHT, padx=5)

    def hide_navigation_buttons(self): 

        self.home_button.pack_forget()
        self.back_button.pack_foget()
        self.logout_button.pack_forget()

    def navigate_to(self, page_name): 
        self.controller.show_page(page_name)



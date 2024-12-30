import ttkbootstrap as ttk
from ttkbootstrap.constants import * 
from ttkbootstrap.dialogs import Messagebox
from BasePage import BasePage
from KeyAlgorithms.Stack import Stack

from LandingPage import LandingPage
from Register import RegisterPage

class Application(ttk.Window): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)

        self.title("Fashion Match, Sales Order Processing System")
        self.geometry("650x500")

        conatiner = ttk.Frame(self)
        conatiner.pack(expand=True, fill=BOTH)

        self.frames = {}

        self.stack = Stack()

        for PageClass in (LandingPage, RegisterPage): 
            page_name = PageClass.__name__
            frame = PageClass(parent=conatiner, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("LandingPage")

    def show_page(self, page_name: str): 
        frame = self.frames[page_name]
        frame.tkraise()

    def go_back(self): 
        if self.stack.size() > 1: 
            self.stack.pop()
            previous_page = self.stack.peek()
            if previous_page: 
                self.show_page(previous_page)
        else: 
            Messagebox.show_error("Already at first page, can't go back further")

    


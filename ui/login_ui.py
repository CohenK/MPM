import tkinter as tk
from tkinter import ttk
from os.path import exists
from classes import Profile
from utils import helper
import PIL.Image
import PIL.ImageTk
from ui.display_ui import Display
from ui.login_logic import Logic

primary_lighter = '#226666'
primary_lighter = "#407F7F"
primary_light = '#669999'
primary_darker = '#0D4D4D'
primary_dark = '#003333'
secondary_lighter = '#2E4172'
secondary_light = '#7887AB'
secondary_lighter = '#4F628E'
secondary_darker = '#162955'
secondary_dark = '#061539'
thirtiary_color = '#AA6C39'
thirtiary_light = '#D49A6A'
thirtiary_dark = '#804515'

class Login():
    def __init__(self, root:tk.Tk, call_display):
        self.root = root
        self.root.config(menu=None)
        self.call_display = call_display

        self.main_login_frame = tk.Frame(self.root, bg=primary_lighter)
        self.main_login_frame.grid(row=0,column=0, sticky="NSEW")
        self.main_login_frame.grid_columnconfigure(0, weight=1)
        self.main_login_frame.grid_rowconfigure(0, weight=1)
        
        self.title_frame = tk.Frame(self.main_login_frame, bg=primary_lighter)
        self.title = tk.Label(self.title_frame, text = "MPM", font=('Times  90'), background=primary_lighter, foreground="black")
        self.miniTitle = tk.Label(self.title_frame, text = "My Password Manager", font=('Times  23'), background=primary_lighter, foreground="black")
        
        self.title_frame.grid(row=0, column=0)
        self.title_frame.grid_rowconfigure(0,weight=1)
        self.title_frame.grid_rowconfigure(1,weight=2)
        self.title_frame.grid_rowconfigure(2,weight=2)
        self.title.grid(row=0, column=0)


        def login_on_click(event):
            if self.login_pass.get() == '(Password)':
                self.login_pass.delete(0, tk.END)
                self.login_pass.configure(show = "*")

        def login_unfocus(event):
            if len(self.login_pass.get()) == 0 or self.login_pass.get() == "(Password)":
                self.login_pass.configure(show = "")
                self.login_pass.insert(0, "(Password)")
                self.show_login_password.configure(text="Show Password")

        def new_on_click(event):
            if self.new_pass.get() == '(Password)':
                self.new_pass.delete(0, tk.END)
                self.new_pass.configure(show = "*")

        def new_unfocus(event):
            if len(self.new_pass.get()) == 0 or self.new_pass.get() == "(Password)":
                self.new_pass.configure(show = "")
                self.new_pass.insert(0, "(Password)")
                self.show_new_password.configure(text="Show Password")

        def determine_focus(event):
            try:
                x,y = self.root.winfo_pointerxy()
                currentWidget = self.root.winfo_containing(x,y)
                if currentWidget not in (self.login_user, self.login_pass, self.new_user, self.new_pass):
                    self.main_login_frame.focus_set()
            except Exception as error:
                return
        
        def select_all(event):
            event.widget.select_range(0,tk.END)
            event.widget.icursor(tk.END)

        #login UI
        self.login_frame = tk.Frame(self.title_frame, bg=secondary_light, pady=30)        
        self.login_frame.grid(row=1, column=0, pady=25, sticky="NSEW")
        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(1, weight=2)
        self.login_frame.grid_rowconfigure(2, weight=2)
        self.login_frame.grid_rowconfigure(3, weight=3)
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_title = tk.Label(self.login_frame, text="Existing User", font=('Calibri 16 bold'), bg=secondary_light)
        self.login_user = tk.Entry(self.login_frame, font=('Calibri 16'), justify=tk.CENTER, bd=5)
        self.login_pass = tk.Entry(self.login_frame, font=('Calibri 16'), justify=tk.CENTER, bd=5)
        helper.entry_QOF(self.login_user, self.login, "(Username)")
        helper.entry_QOF(self.login_pass, self.login, "(Password)")

        self.login_buttons_frame = tk.Frame(self.login_frame, bg=secondary_light)
        self.login_buttons_frame.grid_rowconfigure(0,weight=1)
        self.login_buttons_frame.grid_rowconfigure(1,weight=1)
        self.login_buttons_frame.grid_columnconfigure(0,weight=1)
        self.login_button = tk.Button(self.login_buttons_frame, text="Login", bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', font=('Calibri 14 bold'), padx = 55, pady=10, command=self.login)
        self.show_login_password = tk.Button(self.login_buttons_frame, text="Show Password", bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', font=('Calibri 12'), pady=5, command=lambda: self.show_password(self.show_login_password, self.login_pass))
        self.login_pass.bind("<FocusIn>", login_on_click)
        self.login_pass.bind("<FocusOut>", login_unfocus)
        self.login_title.grid(row=0,column=0)
        self.login_user.grid(row=1, column=0, pady=5, ipady=5)
        self.login_pass.grid(row=2, column=0, pady=5, ipady=5)
        self.login_buttons_frame.grid(row=3, column=0, pady=10)
        self.login_button.grid(row=0, column=0, sticky="NSEW", pady=5)
        self.show_login_password.grid(row=1, column=0, sticky="NSEW", pady=5)

        #register UI
        self.new_frame = tk.Frame(self.title_frame, bg=secondary_light, pady=30)
        self.new_frame.grid(row=2, column=0, pady=25, sticky="NSEW")
        self.new_frame.grid_rowconfigure(0, weight=1)
        self.new_frame.grid_rowconfigure(1, weight=2)
        self.new_frame.grid_rowconfigure(2, weight=2)
        self.new_frame.grid_rowconfigure(3, weight=3)
        self.new_frame.grid_columnconfigure(0, weight=1)
        self.new_title = tk.Label(self.new_frame, text="New User", font=('Calibri 16 bold'), bg=secondary_light)       
        self.new_user = tk.Entry(self.new_frame, font=('Calibri 16'), justify=tk.CENTER, bd=5)
        self.new_pass = tk.Entry(self.new_frame, font=('Calibri 16'), justify=tk.CENTER, bd=5)
        helper.entry_QOF(self.new_user, self.new_account, "(Username)")
        helper.entry_QOF(self.new_pass, self.new_account, "(Password)")

        self.new_buttons_frame = tk.Frame(self.new_frame, bg=secondary_light)
        self.new_buttons_frame.grid_rowconfigure(0,weight=1)
        self.new_buttons_frame.grid_rowconfigure(1,weight=1)
        self.new_buttons_frame.grid_columnconfigure(0,weight=1)
        self.new_account_button = tk.Button(self.new_buttons_frame, text="Create", bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', font=('Calibri 14 bold'), padx = 53, pady=10, command=self.new_account)
        self.show_new_password = tk.Button(self.new_buttons_frame, text="Show Password", bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', font=('Calibri 12'), pady=5, command=lambda: self.show_password(self.show_new_password ,self.new_pass))
        self.new_pass.bind("<FocusIn>", new_on_click)
        self.new_pass.bind("<FocusOut>", new_unfocus)
        self.new_pass.bind_class("Entry","<Control-a>", select_all)
        self.new_title.grid(row=0,column=0)
        self.new_user.grid(row=1, column=0, pady=5, ipady=5)
        self.new_pass.grid(row=2, column=0, pady=5, ipady=5)
        self.new_buttons_frame.grid(row=3, column=0, pady=10)
        self.new_account_button.grid(row=0, column=0, sticky="NSEW", pady=5)
        self.show_new_password.grid(row=1, column=0, sticky="NSEW", pady=5)
        
        self.root.bind("<Button-1>", determine_focus)

        self.logic = Logic(self.root, self.main_login_frame, self.call_display,
                            self.login_user, self.login_pass, self.login_button, self.show_login_password,
                            self.new_user, self.new_pass, self.new_account_button, self.show_new_password)
    
    def login(self):
        self.logic.login()

    def new_account(self):
        self.logic.new_account()

    def show_password(self,button, entry):
        self.logic.show_password(button,entry)

    def hide_password(self,button, entry):
        self.logic.hide_password(button,entry)

    def run(self):
        self.logic.run()
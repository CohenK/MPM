from src.utils import helper
import tkinter as tk
from os.path import exists
from src.classes import Profile
from src.ui.custom_widget_classes import Error_Window

class Logic():
    def __init__(self, root, main_login_frame, call_display, login_user, login_pass, login_button, show_login_password,
                 new_user, new_pass, new_account_button, show_new_password):
        self.root = root
        self.main_login_frame = main_login_frame
        self.call_display = call_display
        self.login_user = login_user
        self.login_pass = login_pass
        self.login_button = login_button
        self.show_login_password = show_login_password
        self.new_user = new_user
        self.new_pass = new_pass
        self.new_account_button = new_account_button
        self.show_new_password = show_new_password
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

    def login(self):
        user = self.login_user.get().strip()
        password = self.login_pass.get().strip()
        self.login_user.delete(0,tk.END)
        self.login_user.insert(0, "(Username)")
        self.login_pass.delete(0, tk.END)
        self.login_pass.insert(0, "(Password)")
        self.login_pass.config(show="")
        if (len(user) == 0 or len(password) == 0 or user == "(Username)"):
            message = "Please enter your credentials."
            Error_Window(message)
            return
        else:
            filepath = helper.resource_path(str("../profiles/" + user + ".enc"))
            
            if not exists(filepath):
                message = "This user does not exists."
                Error_Window(message)
                return

            user_profile = helper.read_decrypt_file(filepath, password)
            self.main_login_frame.destroy()
            self.call_display(user_profile)

    def new_account(self):
        user = self.new_user.get().strip()
        password = self.new_pass.get().strip()
        self.new_user.delete(0,tk.END)
        self.new_user.insert(0, "(Username)")
        self.new_pass.delete(0, tk.END)
        self.new_pass.insert(0, "(Password)")
        self.new_pass.config(show="")
        if (len(user) == 0 or len(password) == 0 or user == "(Username)"):
            message= "Invalid user information."
            Error_Window(message)
            return
        else:
            filepath = helper.resource_path(str("../profiles/" + user + ".enc"))
            if exists(filepath):
                message = "This user already exists."
                Error_Window(message)
                return

            profiles = dict()
            profiles[user] = Profile(user, password)
            helper.write_encrypt_file(filepath, profiles[user], password)

    def show_password(self,button, entry):
        if entry.get() == "(Password)":
            return
        entry.config(show="")
        button.configure(command = lambda: self.hide_password(button, entry), text = 'Hide Password')

    def hide_password(self,button, entry):
        entry.config(show="*")
        button.configure(command = lambda: self.show_password(button, entry), text = 'Show Password')

    def run(self):
        self.root.mainloop()
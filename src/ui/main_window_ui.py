import tkinter as tk
import PIL.Image, PIL.ImageTk
from src.utils import helper
from src.ui.login_ui import Login
from src.ui.display_ui import Display
import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Main_Window():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x800")
        programIconPath = resource_path(helper.resource_path("assets/Icons/logo.png"))
        programIcon = PIL.Image.open(programIconPath)
        rProgramIcon = PIL.ImageTk.PhotoImage(programIcon)
        self.root.tk.call('wm', 'iconphoto', self.root._w, rProgramIcon)
        self.root.title("MY PASSWORD MANAGER")
        self.root.minsize(1200,800)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        '''Making app centered'''
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        helper.window_centering(self.root, 1200, 800, self.root.winfo_screenwidth(), self.root.winfo_screenheight())

    def show_login(self):
        self.login = Login(self.root, self.show_display)
        self.login.run()

    def show_display(self, profile):
        if profile:
            del self.login
            self.display = Display(self.root, profile, self.show_login)
            self.display.run()
        else:
            self.show_login()
    
    def run(self):
        self.show_login()
        self.root.mainloop()
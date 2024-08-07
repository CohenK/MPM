import tkinter as tk
import PIL.Image, PIL.ImageTk
from utils import helper
from ui import *
from classes import profile

class Main_Window():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1200x800")
        programIconPath = helper.resource_path("assets/Icons/logo.png")
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
        del self.login
        self.display = Display(self.root, profile, self.show_login)
        self.display.run()
    
    def run(self):
        self.show_login()
        self.root.mainloop()
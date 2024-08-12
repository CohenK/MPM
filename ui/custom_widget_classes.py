import tkinter as tk
from tkinter import ttk
from utils import helper
import pyperclip

primary_color = '#226666'
primary_lighter = "#407F7F"
primary_light = '#669999'
primary_darker = '#0D4D4D'
primary_dark = '#003333'

secondary_color = '#2E4172'
secondary_light = '#7887AB'
secondary_lighter = '#4F628E'
secondary_darker = '#162955'
secondary_dark = '#061539'

thirtiary_color = '#AA6C39'
thirtiary_light = '#D49A6A'
thirtiary_dark = '#804515'

class Custom_Treeview(ttk.Treeview):
    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.bind("<Button-2>", self.on_right_click)
        self.bind("<Button-3>", self.on_right_click)
    
    def on_right_click(self, event):
        region_clicked = self.identify_region(event.x, event.y)
        if region_clicked != 'cell':
            return
        row = self.identify_row(event.y)
        self.selection_set(row)
        selected_values = self.item(row)
        password = selected_values.get("values")[2]
        pyperclip.copy(password)
        popup = Popup(self, notification="copied "+password)
        popup.geometry("500x100")
        popup.update_idletasks()

class Popup(tk.Toplevel):
    def __init__(self,parent:tk.Tk,notification, **kw):
        super().__init__(parent, **kw)
        self.overrideredirect(True)
        self.config(background=primary_light)
        self.minsize(500,75)
        self.maxsize(500,75)
        helper.window_centering(self,500,75,self.winfo_screenwidth(),self.winfo_screenheight())
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        tk.Label(self, text=notification, font=['Calibri','12','bold'], bg=primary_light, fg=secondary_dark).grid(row=0, column=0)
        self.after(1000,self.destroy)

class Autocomplete_Combobox(ttk.Combobox):
    def set_list(self, completion_list):
        self.completion_list = sorted(completion_list) 
        self.hits = []
        self.hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.on_keyrelease)
        self.bind('<FocusOut>', self.focus_out)
        self['values'] = self.completion_list

    def on_keyrelease(self, event):
        if event.keysym in ("BackSpace", "Left", "Right", "Up", "Down", "Shift_L", "Control_L", "Tab_L"):
            return
        
        text = self.get()
        self.position = len(text)

        # update list of matching strings
        if text == '':
            self.hits = []
            self['values'] = self.completion_list
        else:
            self.hits = [item for item in self.completion_list if item.startswith(text)]

        # reset the combobox values
        self['values'] = self.hits

        if len(self.hits) > 0:
            # Autocomplete the entry widget with the first hit
            self.hit_index = 0
            self.position = len(text)  # Position of the cursor
            self.set(self.hits[0])
            self.select_range(self.position, tk.END)

    def set(self, value):
        # override the Combobox set method to change its text
        self.delete(0, tk.END)
        self.insert(0, value)
        self.icursor(self.position)

    def focus_out(self, event):
        self.select_clear()
        self.icursor(tk.END)
import tkinter as tk
from tkinter import ttk
from src.utils import helper
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
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        message_label = tk.Label(self, text=notification, font=['Calibri','12','bold'], bg=primary_light, fg=secondary_dark, wraplength=500)
        message_label.grid(row=0, column=0)
        self.update_idletasks()
        # Set the window size based on the label size, with some padding
        label_width = message_label.winfo_width()
        label_height = message_label.winfo_height()
        self.geometry(f"{label_width + 20}x{label_height + 20}")

        helper.window_centering(self,self.winfo_width(),self.winfo_height(),self.winfo_screenwidth(),self.winfo_screenheight())
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

class Error_Window(tk.Toplevel):
    def __init__(self, error_message, **kw):
        super().__init__(**kw)
        self.config(bg=primary_color)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.max_width = self.winfo_screenwidth()
        self.max_height = self.winfo_screenheight()
        self.title("MPM Error Detected")
        self.minsize(500,100)
        self.protocol("WM_DELETE_WINDOW", self.kill_error_window)
        message_label = tk.Label(self, text=error_message, font=("Calibri 16 bold"), bg=primary_color, wraplength=500)
        self.okButton = tk.Button(self, bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', text = "OK", padx=15 ,command =self.kill_error_window)
        message_label.grid(row=0, column=0)
        self.okButton.grid(row=1, column=0, sticky="N")
        self.focus_set()
        self.bind("<Return>", self.kill_error_window)  

        self.update_idletasks()
        # Set the window size based on the label size, with some padding
        label_width = message_label.winfo_width()
        label_height = message_label.winfo_height()
        self.geometry(f"{label_width + 20}x{label_height + 20}")
        helper.window_centering(self,self.winfo_width(),self.winfo_height(),self.winfo_screenwidth(),self.winfo_screenheight())

        self.grab_set()
        self.transient(self.master)
        self.master.wait_window(self)
        
    def kill_error_window(self, event=None):
        self.grab_release()
        self.destroy()

class Confirmation_Window(tk.Toplevel):
    def __init__(self,parent,message):
        super().__init__(master=parent)
        self.result = tk.BooleanVar()
        self.title("MPM Confirmation")
        self.geometry("750x100")
        self.config(bg=primary_color)
        self.minsize(750,100)
        self.maxsize(750,100)
        self.grab_set()
        helper.window_centering(self, 750, 100, self.winfo_screenwidth(), self.winfo_screenheight())
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.focus_set()

        label = tk.Label(self, text=message, bg=primary_color)
        label.config(font=('Calibri',14,'bold'))
        confirm_button= tk.Button(self, bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', text = "Confirm", padx=15 ,command=self.confirm)
        cancel_button= tk.Button(self, bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', text = "Cancel", padx=15 ,command=self.cancel)
        confirm_button.config(font=('Calibri',10,'bold'))
        cancel_button.config(font=('Calibri',10,'bold'))
        label.grid(row=0, column=0, columnspan=2, pady=10)
        confirm_button.grid(row=1, column=0, sticky='E',padx=10, pady=5)
        cancel_button.grid(row=1, column=1, sticky='W',padx=10, pady=5)

        self.grab_set()
        self.transient(self.master)
        self.master.wait_window(self)

    def confirm(self):
        self.grab_release()
        self.result.set(True)
        self.destroy()

    def cancel(self):
        self.grab_release()
        self.result.set(False)
        self.destroy() 
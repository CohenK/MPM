from classes import Profile
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
    
    
        # region_clicked = self.identify_region(event.x, event.y)
        # if region_clicked == "nothing":
        #     self.parent.parent.focus()

    # def on_double_click(self, event):
    #     region_clicked = self.identify_region(event.x, event.y)
    #     if region_clicked not in ("tree","cell"):
    #         return
    #     column = self.identify_column(event.x)
    #     column_index = int(column[1:])
    #     selected_iid = self.focus()
    #     selected_values = self.item(selected_iid)

    #     if column != '#0':
    #         selected_text = selected_values.get("values")[column_index-1]

    #     x,y,w,h = self.bbox(selected_iid,column)
    #     cell_edit = tk.Entry(self)
    #     cell_edit.column = column_index-1
    #     cell_edit.item = selected_iid
    #     cell_edit.place(x=x,y=y,w=w,h=h)
    #     cell_edit.insert(0,selected_text)
    #     cell_edit.select_range(0,tk.END)
    #     cell_edit.focus()

    #     cell_edit.bind("<FocusOut>", self.on_focus_out)
    #     cell_edit.bind("<Return>", self.on_enter)

    # def on_focus_out(self, event):
    #     event.widget.destroy()
    
    # def on_enter(self, event):
    #     new_text = event.widget.get()
    #     selected_iid = event.widget.item
    #     column = event.widget.column
    #     current_values = self.item(selected_iid).get("values")
    #     prev_site, prev_username, prev_password = current_values
    #     current_values[column] = new_text
    #     site, username, password = current_values
    #     if site == prev_site and username == prev_username and password != prev_password:
    #             self.profile.updatePassword(site,username,password)
    #             self.item(selected_iid, values = current_values)
    #     else:
    #         if self.profile.addSite(site,username,password):
    #             self.profile.deleteUser(prev_site, prev_username)
    #             self.item(selected_iid, values = current_values)
    #         else:
    #             self.item(selected_iid, values = [prev_site,prev_username,prev_password])
    #             helper.error_window("Record already exists.", 750, 100)
    #     event.widget.destroy()

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
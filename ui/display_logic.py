import tkinter as tk
from tkinter import filedialog
from typing import OrderedDict
from utils import helper
from utils.google_drive_util import GoogleDriveClient
import pyperclip
from classes import Profile
import os

class Logic:
    def __init__(self, root:tk.Tk, display_frame, menu_bar, tree,search_entry,search_button,back_button,
                current_site, current_user, current_pass, clear_button,edit_button,delete_button,add_button,
                lower_chars,upper_chars,num_chars,special_chars,generate_button,new_password,
                callback, profile: Profile, accounts, sorted_dict, prev, screen_width, screen_height):
    
        self.root = root
        self.display_frame = display_frame
        self.menu_bar = menu_bar
        self.tree = tree
        self.search_entry = search_entry
        self.search_button = search_button
        self.back_button = back_button
        self.current_site = current_site
        self.current_user = current_user
        self.current_pass = current_pass
        self.clear_button = clear_button
        self.edit_button = edit_button
        self.delete_button = delete_button
        self.add_button = add_button
        self.lower_chars = lower_chars
        self.upper_chars = upper_chars
        self.num_chars = num_chars
        self.special_chars = special_chars
        self.generate_button = generate_button
        self.new_password = new_password
        self.callback = callback
        self.profile = profile
        self.accounts = accounts
        self.sorted_dict = sorted_dict
        self.prev = prev
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.primary_color = '#226666'
        self.primary_lighter = "#407F7F"
        self.primary_light = '#669999'
        self.primary_darker = '#0D4D4D'
        self.primary_dark = '#003333'

        self.secondary_color = '#2E4172'
        self.secondary_light = '#7887AB'
        self.secondary_lighter = '#4F628E'
        self.secondary_darker = '#162955'
        self.secondary_dark = '#061539'

        self.thirtiary_color = '#AA6C39'
        self.thirtiary_light = '#D49A6A'
        self.thirtiary_dark = '#804515'
        self.sort_dicts(self.accounts, self.sorted_dict)
        self.insert_records(self.sorted_dict)
        self.drive = GoogleDriveClient()
        
    def insert_records(self, data):
        count=0
        for site in data:
            for credentials in data[site]:
                self.tree.insert(parent='', index='end', iid=count, text='Parent', values=(site, credentials, data[site][credentials]))
                count += 1
    
    def sort_dicts(self, data, result):
        sorted_list = sorted(data.items())
        for item in sorted_list:
            temp = dict(item[1])
            inner_sort = sorted(temp.items())
            result[str(item[0])] = OrderedDict(inner_sort)
    
    def display_current_records(self):
        temp = OrderedDict()
        accounts = self.profile.get_accounts()
        self.sort_dicts(accounts, temp)
        self.destroy_all_records()
        self.insert_records(temp)
    
    def add_record(self):
            site = self.current_site.get().strip()
            user = self.current_user.get().strip()
            password = self.current_pass.get().strip()
            self.current_site.delete(0, tk.END)
            self.current_user.delete(0, tk.END)
            self.current_pass.delete(0, tk.END)

            if site == '' or user == '' or password == '':
                helper.error_window("One or more fields is empty.", self.screen_width, self.screen_height)
                return 
            if self.profile.add_site(site, user, password):
                self.display_current_records()
                self.prev = None
            else:
                helper.error_window("Record already exists.", self.screen_width, self.screen_height)

    def on_tree_left_click(self,event):
        row = self.tree.identify_row(event.y)
        if not row:
            self.clear_current_selected()
            self.tree.selection_remove(self.tree.selection())
            self.prev = None
            self.display_frame.focus()
        else:
            self.tree.focus(row)
            record = self.tree.item(self.tree.focus())
            self.prev = record
            site=record['values'][0]
            username=record['values'][1]
            password=record['values'][2]
            self.clear_current_selected()
            self.current_site.insert(0, site)
            self.current_user.insert(0, username)
            self.current_pass.insert(0, password)
            
    def clear_current_selected(self):
        self.current_site.delete(0, tk.END)
        self.current_user.delete(0, tk.END)
        self.current_pass.delete(0, tk.END)
    
    def edit_account(self):
        if not self.prev:
            helper.error_window("No record was selected.", self.screen_width, self.screen_height)
            return
        prev_site=self.prev['values'][0]
        prev_username=self.prev['values'][1]
        prev_password=self.prev['values'][2]
        site=self.current_site.get().strip()
        username=self.current_user.get().strip()
        password=self.current_pass.get().strip()


        if len(site) == 0 or len(username) == 0 or len(password)==0:
            self.clear_current_selected()
            self.current_site.insert(0,prev_site)
            self.current_user.insert(0,prev_username)
            self.current_pass.insert(0,prev_password)
            helper.error_window("Some fields are missing.", self.screen_width, self.screen_height)
            return
        self.clear_current_selected()

        dialog = helper.Confirmation_Window(self.root, 'Are you sure you want to make this change?')
        self.root.wait_window(dialog)
        if dialog.result.get():
            if site == prev_site and username == prev_username and password != prev_password:
                self.profile.update_password(site,username,password)
            else:
                if self.profile.add_site(site, username, password):
                    self.profile.delete_user(prev_site, prev_username)
                    self.prev = None
                else:
                    self.current_site.insert(0,prev_site)
                    self.current_user.insert(0,prev_username)
                    self.current_pass.insert(0,prev_password)
                    helper.error_window("Record already exists.", self.screen_width, self.screen_height)
            self.display_current_records()
    
    def destroy_all_records(self):
        for row in self.tree.get_children():
                self.tree.delete(row)
    
    def insert_records(self, data):
        count=0
        for site in data:
            for credentials in data[site]:
                self.tree.insert(parent='', index='end', iid=count, text='Parent', values=(site, credentials, data[site][credentials]))
                count += 1
    
    def query(self):
        username = self.search_entry.get()
        temp = OrderedDict()
        results = self.profile.search_user(username)
        message = ""
        if username == "(username)":
            message = "Nothing entered"
            helper.error_window(message, self.screen_width, self.screen_height)
            return

        if len(results) == 0:
            if len(username)==0:
                message = "Nothing entered"
            else:
                message = "No such username is in this database"
            helper.error_window(message, self.screen_width, self.screen_height)    
            return
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "(username)")
        self.destroy_all_records()
        self.sort_dicts(results, temp)
        self.insert_records(temp)
        self.root.focus()

    def delete_record(self):
        site=self.current_site.get().strip()
        username=self.current_user.get().strip()
        password = self.current_pass.get().strip()
        self.current_site.delete(0,tk.END)
        self.current_user.delete(0,tk.END)
        self.current_pass.delete(0,tk.END)

        if not site or not username or not password:
            helper.error_window("Incomplete record information.", self.screen_width, self.screen_height)
            return
        dialog = helper.Confirmation_Window(self.root, 'Are you sure you want to make this change?')
        self.root.wait_window(dialog)
        if dialog.result.get():
            if self.profile.delete_user(site, username):
                self.prev = None
                self.display_current_records()
            else:
                helper.error_window("No such record exists.", self.screen_width, self.screen_height)

    def copy_account_password(self):
        record = self.tree.item(self.tree.focus())
        if len(self.tree.selection()) == 0:
            return
        password = record['values'][2]
        pyperclip.copy(password)
    
    def user_logout(self):
        self.root.config(menu=None)
        self.menu_bar.destroy()
        self.save_profile()
        self.display_frame.destroy()
        print("logging out")
        self.callback()

    def save_profile(self):
        filepath = helper.resource_path(str("profiles/" + self.profile.get_user() + ".enc"))
        password = self.profile.get_password()
        helper.write_encrypt_file(filepath, self.profile ,password)
    
    def exit_app(self):
        print("exiting")
        self.save_profile()
        self.root.destroy()

    def change_password(self):
        new_password_window = tk.Toplevel(padx=5, pady=7)
        new_password_window.config(bg=self.primary_color)
        new_password_window.geometry("550x150")
        new_password_window.minsize(550, 150)
        new_password_window.maxsize(550, 150)
        helper.window_centering(new_password_window, 550, 150, new_password_window.winfo_screenwidth(), new_password_window.winfo_screenheight())
        new_password_window.focus_set()
        new_password_window.rowconfigure(0, weight=1)
        new_password_window.columnconfigure(0, weight=1)
        new_password_window.columnconfigure(1, weight=1)

        def change_password_window():
            dialog = helper.Confirmation_Window(self.root, 'Are you sure you want to make this change?')
            self.root.wait_window(dialog)
            if dialog.result.get():
                password = new_pass_entry.get().strip()
                if password != '(New Password)':
                    self.profile.set_password(password)
                    filepath = helper.resource_path(str("profiles/" + self.profile.get_user() + ".enc"))
                    helper.write_encrypt_file(filepath, self.profile, password)
                    new_password_window.destroy() 
                else:
                    helper.error_window("Password cannot be empty.")
        
        new_pass_entry = tk.Entry(new_password_window, font=('Calibri 16'), justify=tk.LEFT, bd=2)
        helper.entry_QOF(new_pass_entry, change_password_window, "(New Password)")
        new_pass_entry.grid(row=0, column=0, sticky='NEWS',padx=5,pady=30)
            
        edit_button = tk.Button(new_password_window, bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black', text='Edit', command=change_password_window, width=7)
        edit_button.grid(row=0, column=1, sticky='NEWS',padx=5,pady=30)

        def focusRoot(event):
            x,y = new_password_window.winfo_pointerxy()
            currentWidget = new_password_window.winfo_containing(x,y)
            if not currentWidget == new_pass_entry:
                new_password_window.focus_set()
    
        new_password_window.bind("<Button-1>", focusRoot)
        new_password_window.mainloop()

    def change_username(self):
        new_user_window = tk.Toplevel(padx=5, pady=7)
        new_user_window.config(bg=self.primary_color)
        new_user_window.geometry("550x150")
        new_user_window.minsize(550, 150)
        new_user_window.maxsize(550, 150)
        helper.window_centering(new_user_window, 550, 150, new_user_window.winfo_screenwidth(), new_user_window.winfo_screenheight())
        new_user_window.focus_set()
        new_user_window.rowconfigure(0, weight=1)
        new_user_window.columnconfigure(0, weight=1)
        new_user_window.columnconfigure(1, weight=1)

        def change_username_window():
            dialog = helper.Confirmation_Window(self.root, 'Are you sure you want to make this change?')
            self.root.wait_window(dialog)
            if dialog.result.get():
                user = new_pass_entry.get().strip()
                if user != '(New Username)':
                    old = helper.resource_path("profiles/"+ self.profile.get_user() + ".enc")
                    new = helper.resource_path("profiles/"+ user + ".enc")
                    self.profile.set_user(user)
                    os.rename(old, new)
                    helper.write_encrypt_file(new, self.profile, self.profile.get_password())
                    new_user_window.destroy() 
                else:
                    helper.error_window("Username cannot be empty.")
        
        new_pass_entry = tk.Entry(new_user_window, font=('Calibri 16'), justify=tk.LEFT, bd=2)
        helper.entry_QOF(new_pass_entry, change_username_window, "(New Username)")
        new_pass_entry.grid(row=0, column=0, sticky='NEWS',padx=5,pady=30)
            
        edit_button = tk.Button(new_user_window, bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black', text='Edit', command=change_username_window, width=7)
        edit_button.grid(row=0, column=1, sticky='NEWS',padx=5,pady=30)

        def focusRoot(event):
            x,y = new_user_window.winfo_pointerxy()
            currentWidget = new_user_window.winfo_containing(x,y)
            if not currentWidget == new_pass_entry:
                new_user_window.focus_set()
    
        new_user_window.bind("<Button-1>", focusRoot)
        new_user_window.mainloop()

    def local_backup(self):
        profile_dir = helper.resource_path('profiles/')
        filepath = filedialog.asksaveasfilename(title="MPM Backup", initialdir=profile_dir, defaultextension=".enc")
        helper.write_encrypt_file(filepath,self.profile,self.profile.get_password())

    def drive_backup(self):
        filepath = helper.resource_path("profiles/"+self.profile.get_user()+".enc")
        file_id = self.drive.upload_file(root=self.root,file_path=filepath)
        return file_id
    
    def drive_reset(self):
        self.drive.reset_token(self.root)

    def determine_focus(self):
        try:
            x,y = self.root.winfo_pointerxy()
            currentWidget = self.root.winfo_containing(x,y)
            if currentWidget not in (self.search_entry,self.current_site,self.current_user,self.current_pass,self.lower_chars,self.upper_chars,self.num_chars,self.special_chars, self.new_password, self.menu_bar):
                self.display_frame.focus_set()
        except Exception as error:
            print("determine_focus: ")
            print(error)

    def edit_help(self):
        help = tk.Toplevel()
        help.overrideredirect(True)
        help.config(background=self.primary_light)
        help.minsize(750,500)
        help.maxsize(750,500)
        helper.window_centering(help,500,75,help.winfo_screenwidth(),help.winfo_screenheight())
        help.grid_rowconfigure(0, weight=1)
        help.grid_rowconfigure(1,weight=1)
        help.grid_columnconfigure(0, weight=1)
        message = ("To edit your main account go to Settings > Edit Password or Settings > Edit Username, \n " +
                   "To edit each individual username and/or site, please select them from the list and this will \n" + 
                   "auto populate the commands section where you can make edits and/or deletion by clicking the respective buttons. \n" + 
                   "You can also type in a brand new site, username and password and use the \"add\" button to add a brand new record.")
        tk.Label(help, text=message, bg=self.primary_light, fg=self.secondary_dark).grid(row=0, column=0)
        tk.Button(help, text="OK", font=['Calibri','12'], bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black',command=lambda event: help.destroy()).grid(row=1, column=0)
    
    def password_help(self):
        help = tk.Toplevel()
        help.overrideredirect(True)
        help.config(background=self.primary_light)
        help.minsize(750,500)
        help.maxsize(750,500)
        helper.window_centering(help,500,75,help.winfo_screenwidth(),help.winfo_screenheight())
        help.grid_rowconfigure(0, weight=1)
        help.grid_rowconfigure(1,weight=1)
        help.grid_columnconfigure(0, weight=1)
        message = ("Included in this application is a password generation feature located at the bottom, \n " +
                   "passwords generated from this tool are cryptographically secure and automatically added \n" + 
                   "to your clipboard, so you can just paste this into the password field in the above section \n" +
                   "to use them. There are three optional fields in the password generation tool section labeled: \n" + 
                   "lower, upper, number, and special. These corresponds to the number of these respective characters \n" + 
                   "that you would like to include in the password that you generate. \n \n" + 
                   "For example if at the time of the generate button being clicked there is a: \n" +
                   " 1, 2, 3 and 4 in the respective fields, the generated password will have: \n" + 
                   "1 lower case, 2 upper case, 3 numbers and 4 special characters. \n" +
                   "If no input is present the generator will randomly generate a password that \n" + 
                   "is 8-15 characters long and include at least 1 of each type of character.")
        tk.Label(help, text=message, bg=self.primary_light, fg=self.secondary_dark).grid(row=0, column=0)
        tk.Button(help, text="OK", font=['Calibri','12'], bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black',command=lambda event: help.destroy()).grid(row=1, column=0)
    
    def other_help(self):
        help = tk.Toplevel()
        help.overrideredirect(True)
        help.config(background=self.primary_light)
        help.minsize(750,500)
        help.maxsize(750,500)
        helper.window_centering(help,500,75,help.winfo_screenwidth(),help.winfo_screenheight())
        help.grid_rowconfigure(0, weight=1)
        help.grid_rowconfigure(1,weight=1)
        help.grid_columnconfigure(0, weight=1)
        message = ("If there are any other questions that have not been answered in the other help sections \n" + 
                   "please visit https://github.com/CohenK/PassMan for a more detailed explanation guide on how \n" + 
                   "to use this application or email the developer at kangcohen@gmail.com, thank you for using MPM.")
        tk.Label(help, text=message, bg=self.primary_light, fg=self.secondary_dark).grid(row=0, column=0)
        tk.Button(help, text="OK", font=['Calibri','12'], bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black',command=lambda event: help.destroy()).grid(row=1, column=0)

    def run(self):
        self.root.mainloop()
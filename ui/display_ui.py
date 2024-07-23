import tkinter as tk
from tkinter import ttk
from typing import OrderedDict
from utils import helper
import pyperclip
import PIL.Image
import PIL.ImageTk
from classes import Profile

class Display:
    def __init__(self, user_profile: Profile, callback):
        self.main_color = '#69A090'

        self.callback = callback
        self.profile = user_profile
        self.accounts = self.profile.getAccounts()
        self.sorted_dict = OrderedDict()


        self.root = tk.Tk()
        self.root.minsize(750, 400)
        self.root.title("MY PASSWORD MANAGER")
        self.program_icon_path = helper.resource_path("assets/Icons/lock_and_key.png")
        self.program_icon = PIL.Image.open(self.program_icon_path)
        self.program_icon_image = PIL.ImageTk.PhotoImage(self.program_icon)
        self.root.tk.call('wm', 'iconphoto', self.root._w, self.program_icon_image)
        # row and column weights
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.root.rowconfigure(0, weight=14)
        self.root.rowconfigure(1, weight=1, minsize=60)
        self.root.columnconfigure(0, weight=1)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure('Treeview.Heading', background='#8c94a3')
        self.style.configure('Treeview', rowheight = 30, background="#292c30", foreground = "white", activeforeground="white", fieldbackground = "#292c30")
        self.style.map("Treeview", background=[('selected', '#5a5e66')])

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        helper.window_centering(self.root, 750, 400, self.root.winfo_screenwidth(), self.root.winfo_screenheight())



        self.top=tk.Frame(self.root)
        self.top.grid(row=0, column=0, sticky='NSEW')

        self.scroll = tk.Scrollbar(self.top, orient=tk.VERTICAL, highlightcolor='black', activebackground='black', bg='grey', troughcolor='#8c94a3')
        self.tree = ttk.Treeview(self.top, yscrollcommand=self.scroll.set, selectmode="browse")    
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)    
        self.scroll.config(command=self.tree.yview)

        self.bottom = tk.Frame(self.root, padx=10, pady=10, bg='#69A090')
        self.bottom.grid(row=1, column=0, sticky='NSEW')
        self.bottom.grid_rowconfigure(0, weight=1)
        self.bottom.grid_columnconfigure(0, weight=1)
        self.bottom.grid_columnconfigure(1, weight=1)
        self.bottom.grid_columnconfigure(2, weight=1)
        self.bottom.grid_columnconfigure(3, weight=1)
        self.bottom.grid_columnconfigure(4, weight=1)
        self.bottom.grid_columnconfigure(5, weight=1)
        self.bottom.grid_columnconfigure(6, weight=1)

        self.tree['columns'] = ("Site", "User", "Password")
        self.tree.column("#0", width = 0, stretch=tk.NO)
        self.tree.column("Site", anchor=tk.W, width= 200, minwidth=200)
        self.tree.column("User", anchor=tk.W, width= 200, minwidth=200)
        self.tree.column("Password", anchor=tk.W, width= 200, minwidth=200)
        self.tree.heading('#0', text="", anchor=tk.W)
        self.tree.heading('Site', text="Site", anchor=tk.W)
        self.tree.heading('User', text="User", anchor=tk.W)
        self.tree.heading('Password', text="Password", anchor=tk.W)

        self.search = tk.Button(self.bottom, bg="#16cca8", fg='black', activeforeground='black', text='SEARCH', width=12, command=self.search)
        self.backButton = tk.Button(self.bottom, bg="#16cca8", fg='black', activeforeground='black', text='BACK', width=12, command=self.return_from_search)
        self.addButton = tk.Button(self.bottom, bg="#16cca8", fg='black', activeforeground='black', text='ADD', command=self.add_tool, width=12)
        self.editButton = tk.Button(self.bottom, bg="#16cca8", fg='black', activeforeground='black', text='EDIT', command=self.edit_tool, width=12)
        self.deleteButton = tk.Button(self.bottom, bg="#16cca8", fg='black', activeforeground='black', text='DELETE', command=self.delete_account, width=12)
        self.copyButton = tk.Button(self.bottom, bg="#16cca8", fg='black', activeforeground='black', text='COPY PASSWORD', command=self.copy_account_password, width=12)
        self.logoutButton = tk.Button(self.bottom, bg="#16cca8", fg='black', activeforeground='black', text='LOGOUT', command=self.user_loguot, width=12)
        
        self.search.grid(row=0, column=0, sticky='NSEW')
        self.backButton.grid(row=0, column=1, sticky='NSEW')
        self.addButton.grid(row=0, column=2, sticky='NSEW')
        self.editButton.grid(row=0, column=3, sticky='NSEW')
        self.deleteButton.grid(row=0, column=4, sticky='NSEW')
        self.copyButton.grid(row=0, column=5, sticky='NSEW')
        self.logoutButton.grid(row=0, column=6, sticky='NSEW')


    # to do implement
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
    
    def search(self):
        global searchWindow
        searchWindow = tk.Toplevel(padx=5, pady=7, bg=self.main_color)
        searchWindow.geometry("350x125")
        # searchIconPath = helper.resource_path("Icons\\search.png")
        # searchIcon = PIL.Image.open(searchIconPath)
        # rSearchIcon = PIL.ImageTk.PhotoImage(searchIcon)
        #searchWindow.tk.call('wm', 'iconphoto', searchWindow._w)
        searchWindow.title("MPM Search Box")
        searchWindow.minsize(350, 125)
        searchWindow.maxsize(350, 125)
        helper.window_centering(searchWindow, 350, 125, searchWindow.winfo_screenwidth(), searchWindow.winfo_screenheight())
        searchWindow.focus_set()
        searchWindow.grid_rowconfigure(0, weight=2)
        searchWindow.grid_rowconfigure(1, weight=1)
        searchWindow.grid_rowconfigure(2, weight=2)
        searchWindow.grid_columnconfigure(0, weight=3, minsize=100)
        searchWindow.grid_columnconfigure(1, weight=2)

        global searchEntry
        searchEntry = tk.Entry(searchWindow, font=('Calibri 16'), justify=tk.LEFT, bd=2)
        helper.entry_QOF(searchEntry, self.query, "(Username to be searched)")
        searchEntry.grid(row=1, column=0, sticky='NSEW')
        helper.unfocus_entry(searchWindow, searchEntry)

        searchButton = tk.Button(searchWindow, bg="#16cca8", fg='black', activeforeground='black', text='Search', command=self.query, width=7)
        searchButton.grid(row=1, column=1, sticky='NSEW')
    
    def return_from_search(self):
        temp = OrderedDict()
        accounts = self.profile.getAccounts()
        self.sort_dicts(accounts, temp)
        self.destroy_all_records()
        self.insert_records(temp)
    
    def add_tool(self):
        addWindow = tk.Toplevel(bg=self.main_color)
        addWindow.geometry("650x400")
        # addIconPath = helper.resource_path("Icons\\add.png")
        # addIcon = PIL.Image.open(addIconPath)
        # rAddIcon = PIL.ImageTk.PhotoImage(addIcon)
        #addWindow.tk.call('wm', 'iconphoto', addWindow._w)
        addWindow.minsize(650, 400)
        helper.window_centering(addWindow, 650, 400, addWindow.winfo_screenwidth(), addWindow.winfo_screenheight())

        addWindow.focus_set()
        addWindow.grid_rowconfigure(0, weight=1)
        addWindow.grid_rowconfigure(1, weight=1)
        addWindow.grid_columnconfigure(0, weight=1)

        def addRecord():
            addAdd.focus_set()
            site = newSite.get().strip()
            user = newUser.get().strip()
            password = newPass.get().strip()
            newSite.delete(0, tk.END)
            newSite.insert(0, "(NEW SITE)")
            newUser.delete(0, tk.END)
            newUser.insert(0, "(NEW USER)")
            newPass.delete(0, tk.END)
            newPass.insert(0, "(NEW PASSWORD)")

            if site == '' or site == '(NEW SITE)' or user == '' or user == '(NEW USER)' or password == '' or password == '(NEW PASSWORD)':
                helper.error_window("One or more fields is empty.", self.screen_width, self.screen_height)
                return 
            if self.profile.addSite(site, user, password):
                temp = OrderedDict()
                self.destroy_all_records()
                self.sort_dicts(self.profile.getAccounts(), temp)
                self.insert_records(temp)
            else:
                helper.error_window("Record already exists.", self.screen_width, self.screen_height)

        addHolder = tk.Frame(addWindow, padx=10, pady=5, relief=tk.SUNKEN, bg='#69A090')
        newSite = tk.Entry(addHolder, font=('Calibri 16'), justify=tk.LEFT, bd=2)
        helper.entry_QOF(newSite, addRecord, "(NEW SITE)")
        newUser = tk.Entry(addHolder, font=('Calibri 16'), justify=tk.LEFT, bd=2)
        helper.entry_QOF(newUser, addRecord, "(NEW USER)")
        newPass = tk.Entry(addHolder, font=('Calibri 16'), justify=tk.LEFT, bd=2)
        helper.entry_QOF(newPass, addRecord, "(NEW PASSWORD)")
        addAdd = tk.Button(addHolder, text="ADD RECORD", bg="#16cca8", fg='black', activeforeground='black', command=addRecord)
        addHolder.grid(row=0, column=0, sticky='NSEW')
        addHolder.grid_rowconfigure(0, weight=2)
        addHolder.grid_rowconfigure(1, weight=1)
        addHolder.grid_rowconfigure(2, weight=1)
        addHolder.grid_rowconfigure(3, weight=2)
        addHolder.grid_columnconfigure(0, weight=1)
        addHolder.grid_columnconfigure(1, weight=1)
        addHolder.grid_columnconfigure(2, weight=1)
        newSite.grid(row=1, column=0, sticky='NSEW')
        newUser.grid(row=1, column=1, sticky='NSEW')
        newPass.grid(row=1, column=2, sticky='NSEW')
        addAdd.grid(row=2, column=0, columnspan=3, sticky='NSEW')

        helper.generate_layout(addWindow, newPass, self.screen_width, self.screen_height)
    

    def edit_tool(self):
        if len(self.tree.selection()) == 0:
            return
        #global editWindow
        editWindow = tk.Toplevel(padx=5, pady=7, bg=self.main_color)
        editWindow.geometry("550x150")
        editWindow.title("MPM Edit Window")
        editWindow.minsize(550, 150)
        editWindow.maxsize(550, 150)
        helper.window_centering(editWindow, 550, 150, editWindow.winfo_screenwidth(), editWindow.winfo_screenheight())
        editWindow.focus_set()
        editWindow.grid_rowconfigure(0, weight=2)
        editWindow.grid_rowconfigure(1, weight=1)
        editWindow.grid_rowconfigure(2, weight=2)
        editWindow.grid_columnconfigure(0, weight=2, minsize=100)
        editWindow.grid_columnconfigure(1, weight=2, minsize=100)
        editWindow.grid_columnconfigure(2, weight=1)

        def edit_account():
            record = self.tree.item(self.tree.focus())
            site=record['values'][0]
            username=record['values'][1]
            password=record['values'][2]

            userInput = ""
            passInput = ""
            if editUserEntry.get() == "(Username to be editted)":
                pass
            else:
                userInput = editUserEntry.get()
            if editPassEntry.get() == "(Password to be editted)":
                pass
            else:
                passInput = editPassEntry.get()

            if len(userInput) == 0 and len(passInput) == 0:
                return
            if not len(passInput) == 0 and len(userInput) == 0:
                self.profile.updatePassword(site, username, passInput)
            elif len(passInput) == 0 and not len(userInput) == 0:
                if self.profile.addSite(site, userInput, password):
                    self.profile.deleteUser(site, username)
                else:
                    helper.error_window("Record already exists.", self.screen_width, self.screen_height)
            elif not len(passInput) == 0 and not len(userInput) == 0:
                if self.profile.addSite(site, userInput, passInput):
                    self.profile.deleteUser(site, username)
                else:
                    helper.error_window("Record already exists.", self.screen_width, self.screen_height)
            
            temp = OrderedDict()
            self.destroy_all_records()
            self.sort_dicts(self.profile.getAccounts(), temp)
            self.insert_records(temp)
            editWindow.destroy()

        #global editUserEntry
        editUserEntry = tk.Entry(editWindow, font=('Calibri 16'), justify=tk.LEFT, bd=2)
        helper.entry_QOF(editUserEntry, edit_account, "(Username to be editted)")
        editUserEntry.grid(row=1, column=0, sticky='NSEW')
        
        #global editPassEntry
        editPassEntry = tk.Entry(editWindow, font=('Calibri 16'), justify=tk.LEFT, bd=2)
        helper.entry_QOF(editPassEntry, edit_account, "(Password to be editted)")
        editPassEntry.grid(row=1, column=1, sticky='NSEW')
        
        
        # def edit_target():
        #     self.edit_account(editUserEntry, editPassEntry)
            
        editButton = tk.Button(editWindow, bg="#16cca8", fg='black', activeforeground='black', text='Edit', command=edit_account, width=7)
        editButton.grid(row=1, column=2, sticky='NSEW')
        def focusRoot(event):
            x,y = editWindow.winfo_pointerxy()
            currentWidget = editWindow.winfo_containing(x,y)
            if not currentWidget == editUserEntry and not currentWidget == editPassEntry:
                editWindow.focus_set()
    
        editWindow.bind("<Button-1>", focusRoot)
        editWindow.mainloop()
    
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
        username = searchEntry.get()
        searchEntry.delete(0, tk.END)
        searchEntry.insert(0, "(Username to be searched)")
        temp = OrderedDict()
        results = self.profile.searchUser(username)
        message = ""
        if username == "(Username to be searched)":
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

        self.destroy_all_records()
        self.sort_dicts(results, temp)
        self.insert_records(temp)
        searchWindow.destroy()

    def delete_account(self):
        record = self.tree.item(self.tree.focus())
        if len(self.tree.selection()) == 0:
            return
        site=record['values'][0]
        username=record['values'][1]
        if self.profile.deleteUser(site, username):
            self.tree.delete(self.tree.selection()[0])
        else:
            helper.error_window("No such record exists.", self.screen_width, self.screen_height)

    
    def copy_account_password(self):
        record = self.tree.item(self.tree.focus())
        if len(self.tree.selection()) == 0:
            return
        password = record['values'][2]
        pyperclip.copy(password)
    
    def user_loguot(self):
        self.exit_app()
        self.callback() 
    
    def exit_app(self):
        filepath = helper.resource_path(str("Profile/" + self.profile.getUser() + ".enc"))
        password = self.profile.getPassword()
        # helper.read_decrypt_file(filepath, password)
        helper.write_encrypt_file(filepath, self.profile ,password)
        self.root.destroy()

    def run(self):
        self.sort_dicts(self.accounts, self.sorted_dict)
        self.insert_records(self.sorted_dict)
        self.root.mainloop()
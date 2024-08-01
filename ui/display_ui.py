import tkinter as tk
from tkinter import ttk
from typing import OrderedDict
from utils import helper
import PIL.Image
import PIL.ImageTk
from classes import Profile
from ui.display_logic import Logic
import ui.custom_widget_classes as cw
  
class Display:
    def __init__(self, root, user_profile: Profile, callback):
        #general properties and member variables 
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

        self.callback = callback
        self.profile = user_profile
        self.accounts = self.profile.getAccounts()
        self.sorted_dict = OrderedDict()
        self.prev = None

        #setting up root and its properties
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        #menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        self.menu_bar.config(font=('Calibri 12'))

        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Save", command=self.save_profile)
        self.settings_menu.add_command(label="Change Password", command=self.change_password)
        self.settings_menu.add_command(label="Change Username", command=self.change_username)
        self.settings_menu.add_separator()
        self.settings_menu.add_command(label="Logout", command=self.user_logout)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label='Help', menu=self.help_menu)
        self.help_menu.add_command(label="Editing an Account", command=self.save_profile)
        self.help_menu.add_command(label="Password Generator", command=self.change_password)
        self.help_menu.add_command(label="Copying a Password", command=self.change_username)
        # self.help_menu.add_command(label="About", command=self.show_about)

        #setting up the styles for treeview
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure('Treeview.Heading', background=self.secondary_lighter, padding=(0,5))
        self.style.configure('Treeview', rowheight=30, background=self.secondary_light, foreground = self.secondary_dark, activeforeground=self.secondary_dark, fieldbackground = self.secondary_light)
        self.style.map("Treeview", background=[('selected', self.secondary_color)])

        #make display frame
        self.display_frame = tk.Frame(self.root, bg=self.primary_color)
        self.display_frame.grid(row=0, column=0, sticky='NSEW')
        self.display_frame.rowconfigure(0, weight=10)
        self.display_frame.rowconfigure(1, weight=1, minsize=60)
        self.display_frame.rowconfigure(2, weight=3, minsize=60)
        self.display_frame.rowconfigure(3, weight=1, minsize=60)
        self.display_frame.columnconfigure(0, weight=1)

        #setting up the treeview and scrollbar
        self.content=tk.Frame(self.display_frame, highlightbackground=self.primary_darker, highlightthickness=2)
        self.content.grid(row=0, column=0, sticky='NSEW' ,padx=10, pady=10)
        self.content.parent = self.display_frame

        self.scroll = tk.Scrollbar(self.content, orient=tk.VERTICAL, highlightcolor='black', activebackground='black', bg='grey', troughcolor='#8c94a3')
        self.tree = cw.Custom_Treeview(self.content, yscrollcommand=self.scroll.set, selectmode="browse")    
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)    
        self.scroll.config(command=self.tree.yview)
        
        self.tree['columns'] = ("Site", "User", "Password")
        self.tree.column("#0", width = 0, stretch=tk.NO)
        self.tree.column("Site", anchor=tk.W, width= 200, minwidth=200)
        self.tree.column("User", anchor=tk.W, width= 200, minwidth=200)
        self.tree.column("Password", anchor=tk.W, width= 200, minwidth=200)
        self.tree.heading('#0', text="", anchor=tk.W)
        self.tree.heading('Site', text="Site", anchor=tk.W)
        self.tree.heading('User', text="User", anchor=tk.W)
        self.tree.heading('Password', text="Password", anchor=tk.W)
        self.tree.tag_configure('oddrow', background=self.primary_darker)
        self.tree.tag_configure('evenrow', background=self.primary_lighter)
        self.tree.bind("<Button-1>", self.on_tree_left_click)

        #setting up search section
        self.look_up = tk.LabelFrame(self.display_frame, text="Search", padx=10, pady=10, bd=3, bg=self.primary_color)
        self.look_up.configure(font=("Calibri", 14, "bold"),foreground=self.thirtiary_light)
        self.look_up.grid(row=1, column=0, sticky='NSEW', padx=10, pady=5)
        self.look_up.grid_rowconfigure(0, weight=1)
        self.look_up.grid_columnconfigure(0, weight=3)
        self.look_up.grid_columnconfigure(1, weight=1)
        self.look_up.grid_columnconfigure(2, weight=1)

        self.search_entry = tk.Entry(self.look_up, font=('Calibri 16'), justify=tk.LEFT,bd=2)
        self.search_button = tk.Button(self.look_up, bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black', text='SEARCH', width=12, command=self.query)
        self.back_button = tk.Button(self.look_up, bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black', text='BACK', width=12, command=self.display_current_records)
        
        self.search_entry.grid(row=0,column=0,sticky='NSEW', padx=5)
        helper.entry_QOF(self.search_entry, self.query, '(username)')

        self.search_button.grid(row=0, column=1, sticky='NSEW', padx=5)
        self.back_button.grid(row=0, column=2, sticky='NSEW', padx=5)

        #setting up command section
        self.commands = tk.LabelFrame(self.display_frame, text="Commands", padx=10, pady=10, bd=3, bg=self.primary_color)
        self.commands.configure(font=("Calibri", 14, "bold"),foreground=self.thirtiary_light)
        self.commands.grid(row=2, column=0, sticky='NSEW', padx=10, pady=5)
        self.commands.grid_rowconfigure(0, weight=1)
        self.commands.grid_rowconfigure(1, weight=1)
        self.commands.grid_columnconfigure(0, weight=3)
        self.commands.grid_columnconfigure(1, weight=3)
        self.commands.grid_columnconfigure(2, weight=3)
        self.commands.grid_columnconfigure(3, weight=1)

        self.current_site = tk.Entry(self.commands, font=('Calibri 16'), justify=tk.LEFT,bd=2)
        self.current_user = tk.Entry(self.commands, font=('Calibri 16'), justify=tk.LEFT,bd=2)
        self.current_pass = tk.Entry(self.commands, font=('Calibri 16'), justify=tk.LEFT,bd=2)
        self.clear_button = tk.Button(self.commands, bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black', text='CLEAR', command=self.clear_current_selected, width=12, height=1)
        
        self.edit_button = tk.Button(self.commands, bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black', text='EDIT', command=self.edit_account, width=12, height=1)
        self.delete_button = tk.Button(self.commands, bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black', text='DELETE', command=self.delete_record, width=12, height=1)
        self.add_button = tk.Button(self.commands, bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black', text='ADD', command=self.add_record, width=12, height=1)
    
        
        self.current_site.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)
        self.current_user.grid(row=0, column=1, sticky='NSEW', padx=5, pady=5)
        self.current_pass.grid(row=0, column=2, sticky='NSEW', padx=5, pady=5)
        self.clear_button.grid(row=0, column=3, sticky='NSEW', padx=5, pady=5)
        self.edit_button.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
        self.delete_button.grid(row=1, column=1, sticky='NSEW', padx=5, pady=5)
        self.add_button.grid(row=1, column=2, sticky='NSEW', padx=5, pady=5)

        #setting up password generator section
        self.password_generator = tk.LabelFrame(self.display_frame, text="Password Generator", padx=10, pady=10, bd=3, bg=self.primary_color)
        self.password_generator.configure(font=("Calibri", 14, "bold"),foreground=self.thirtiary_light)
        self.password_generator.grid(row=3, column=0, sticky='NSEW', padx=10, pady=5)
        self.password_generator.grid_rowconfigure(0, weight=1)
        self.password_generator.grid_columnconfigure(0, weight=5)
        self.password_generator.grid_columnconfigure(1, weight=5)
        self.password_generator.grid_columnconfigure(2, weight=5)
        self.password_generator.grid_columnconfigure(3, weight=5)
        self.password_generator.grid_columnconfigure(4, weight=1)
        self.password_generator.grid_columnconfigure(5, weight=5)
        
        self.lower_chars = tk.Entry(self.password_generator, font=('Calibri','16'), justify=tk.LEFT,bd=2)
        self.upper_chars = tk.Entry(self.password_generator, font=('Calibri','16'), justify=tk.LEFT,bd=2)
        self.num_chars = tk.Entry(self.password_generator, font=('Calibri','16'), justify=tk.LEFT,bd=2)
        self.special_chars = tk.Entry(self.password_generator, font=('Calibri','16'), justify=tk.LEFT,bd=2)
        self.generate_button = tk.Button(self.password_generator, bg=self.thirtiary_light, fg='black', activebackground=self.thirtiary_color, activeforeground='black', text='GENERATE', width=12, command=self.password_generation)
        self.new_password = tk.Entry(self.password_generator, font=('Calibri','16'), justify=tk.LEFT,bd=2)

        self.lower_chars.grid(row=0, column=0, sticky='NSEW', padx=5, pady=5)
        self.upper_chars.grid(row=0, column=1, sticky='NSEW', padx=5, pady=5)
        self.num_chars.grid(row=0, column=2, sticky='NSEW', padx=5, pady=5)
        self.special_chars.grid(row=0, column=3, sticky='NSEW', padx=5, pady=5)
        self.generate_button.grid(row=0, column=4, sticky='NSEW', padx=5, pady=5)
        self.new_password.grid(row=0, column=5, sticky='NSEW', padx=5, pady=5)

        self.lower_chars.insert(0,'lower')
        self.upper_chars.insert(0,'upper')
        self.num_chars.insert(0,'number')
        self.special_chars.insert(0,'special')
        self.lower_chars.bind("<FocusIn>",lambda event: on_focus(self.lower_chars))
        self.upper_chars.bind("<FocusIn>",lambda event: on_focus(self.upper_chars))
        self.num_chars.bind("<FocusIn>",lambda event: on_focus(self.num_chars))
        self.special_chars.bind("<FocusIn>",lambda event: on_focus(self.special_chars))
        self.lower_chars.bind("<FocusOut>",lambda event: focus_out(self.lower_chars, 'lower'))
        self.upper_chars.bind("<FocusOut>",lambda event: focus_out(self.upper_chars, 'upper'))
        self.num_chars.bind("<FocusOut>",lambda event: focus_out(self.num_chars, 'number'))
        self.special_chars.bind("<FocusOut>",lambda event: focus_out(self.special_chars,'special'))

        self.display_frame.bind_all("<Button-1>", self.determine_focus)

        def on_focus(entry):
            entry.delete(0,tk.END)
        def focus_out(entry, message):
            text = entry.get().strip()
            if text == '':
                entry.insert(0,message)
        
        self.logic = Logic(self.root, self.display_frame,self.menu_bar, self.tree,self.search_entry,self.search_button,self.back_button,
                           self.current_site, self.current_user, self.current_pass, self.clear_button,self.edit_button,self.delete_button,self.add_button,
                           self.lower_chars,self.upper_chars,self.num_chars,self.special_chars,self.generate_button,self.new_password,
                           self.callback, self.profile, self.accounts, self.sorted_dict, self.prev, self.screen_width, self.screen_height)

    def insert_records(self, data):
        self.logic.insert_records(data)
    
    def determine_focus(self, event):
        self.logic.determine_focus()
    
    def sort_dicts(self, data, result):
        self.logic.sort_dicts(data,result)
    
    def display_current_records(self):
        self.logic.display_current_records()
    
    def password_generation(self):
        helper.generate_pass(self.lower_chars, self.upper_chars, self.num_chars, self.special_chars, self.new_password, 500, 300)
        self.display_frame.focus()
    
    def add_record(self):
            self.logic.add_record()
    
    def on_tree_left_click(self,event):
        self.logic.on_tree_left_click(event)
    
    def clear_current_selected(self):
        self.logic.clear_current_selected()
    
    def edit_account(self):
        self.logic.edit_account()
    
    def destroy_all_records(self):
        self.logic.destroy_all_records()
    
    def insert_records(self, data):
        self.logic.insert_records(data)
    
    def query(self):
        self.logic.query()

    def delete_record(self):
        self.logic.delete_record()

    def copy_account_password(self):
        self.logic.copy_account_password()
    
    def user_logout(self):
        self.logic.user_logout()
    
    def change_password(self):
        self.logic.change_password()
    
    def change_username(self):
        self.logic.change_username()
    
    def save_profile(self):
        self.logic.save_profile()
    
    def exit_app(self):
        self.logic.exit_app()

    def run(self):
        self.logic.run()
from tkinter import *
from tkinter import ttk
from typing import OrderedDict
from utils import helper
import pyperclip
import pickle
import PIL.Image
import PIL.ImageTk


def create(current, callback):

    mainColor = '#69A090'

    #functions
    def sortNDict(data, result):
        sortedList = sorted(data.items())
        for item in sortedList:
            temp = dict(item[1])
            innerSort = sorted(temp.items())
            result[str(item[0])] = OrderedDict(innerSort)
    
    def deleteRecord():
        record = tree.item(tree.focus())
        if len(tree.selection()) == 0:
            return
        site=record['values'][0]
        username=record['values'][1]
        if current.deleteUser(site, username):
            tree.delete(tree.selection()[0])
        else:
            helper.errorWindow("No such record exists.", screen_width, screen_height)

    def copyPassword():
        record = tree.item(tree.focus())
        if len(tree.selection()) == 0:
            return
        password = record['values'][2]
        pyperclip.copy(password)

    def destroyAllRecords():
        for row in tree.get_children():
                tree.delete(row)

    def insertRecords(data):
        count=0
        for site in data:
            for credentials in data[site]:
                tree.insert(parent='', index='end', iid=count, text='Parent', values=(site, credentials, data[site][credentials]))
                count += 1

    def query():
        username = searchEntry.get()
        searchEntry.delete(0, END)
        searchEntry.insert(0, "(Username to be searched)")
        temp = OrderedDict()
        results = current.searchUser(username)
        message = ""
        if username == "(Username to be searched)":
            message = "Nothing entered"
            helper.errorWindow(message, screen_width, screen_height)
            return

        if len(results) == 0:
            if len(username)==0:
                message = "Nothing entered"
            else:
                message = "No such username is in this database"
            helper.errorWindow(message, screen_width, screen_height)    
            return

        destroyAllRecords()
        sortNDict(results, temp)
        insertRecords(temp)
        searchWindow.destroy()

    def revert():
        temp = OrderedDict()
        accounts = current.getAccounts()
        sortNDict(accounts, temp)
        destroyAllRecords()
        insertRecords(temp)

    def searchTool():
        global searchWindow
        searchWindow = Toplevel(padx=5, pady=7, bg=mainColor)
        searchWindow.geometry("350x125")
        # searchIconPath = helper.resourcePath("Icons\\search.png")
        # searchIcon = PIL.Image.open(searchIconPath)
        # rSearchIcon = PIL.ImageTk.PhotoImage(searchIcon)
        #searchWindow.tk.call('wm', 'iconphoto', searchWindow._w)
        searchWindow.title("MPM Search Box")
        searchWindow.minsize(350, 125)
        searchWindow.maxsize(350, 125)
        helper.windowCentering(searchWindow, 350, 125, searchWindow.winfo_screenwidth(), searchWindow.winfo_screenheight())
        searchWindow.focus_set()
        searchWindow.grid_rowconfigure(0, weight=2)
        searchWindow.grid_rowconfigure(1, weight=1)
        searchWindow.grid_rowconfigure(2, weight=2)
        searchWindow.grid_columnconfigure(0, weight=3, minsize=100)
        searchWindow.grid_columnconfigure(1, weight=2)

        global searchEntry
        searchEntry = Entry(searchWindow, font=('Calibri 16'), justify=LEFT, bd=2)
        helper.entryQOF(searchEntry, query, "(Username to be searched)")
        searchEntry.grid(row=1, column=0, sticky='NSEW')
        helper.unfocusEntry(searchWindow, searchEntry)

        searchButton = Button(searchWindow, bg="#16cca8", fg='black', activeforeground='black', text='Search', command=query, width=7)
        searchButton.grid(row=1, column=1, sticky='NSEW')

    def addTool():
        addWindow = Toplevel(bg=mainColor)
        addWindow.geometry("650x400")
        # addIconPath = helper.resourcePath("Icons\\add.png")
        # addIcon = PIL.Image.open(addIconPath)
        # rAddIcon = PIL.ImageTk.PhotoImage(addIcon)
        #addWindow.tk.call('wm', 'iconphoto', addWindow._w)
        addWindow.minsize(650, 400)
        helper.windowCentering(addWindow, 650, 400, addWindow.winfo_screenwidth(), addWindow.winfo_screenheight())

        addWindow.focus_set()
        addWindow.grid_rowconfigure(0, weight=1)
        addWindow.grid_rowconfigure(1, weight=1)
        addWindow.grid_columnconfigure(0, weight=1)

        def addRecord():
            addAdd.focus_set()
            site = newSite.get().strip()
            user = newUser.get().strip()
            password = newPass.get().strip()
            newSite.delete(0, END)
            newSite.insert(0, "(NEW SITE)")
            newUser.delete(0, END)
            newUser.insert(0, "(NEW USER)")
            newPass.delete(0, END)
            newPass.insert(0, "(NEW PASSWORD)")

            if site == '' or site == '(NEW SITE)' or user == '' or user == '(NEW USER)' or password == '' or password == '(NEW PASSWORD)':
                helper.errorWindow("One or more fields is empty.", screen_width, screen_height)
                return 
            if current.addSite(site, user, password):
                temp = OrderedDict()
                destroyAllRecords()
                sortNDict(current.getAccounts(), temp)
                insertRecords(temp)
            else:
                helper.errorWindow("Record already exists.", screen_width, screen_height)

        addHolder = Frame(addWindow, padx=10, pady=5, relief=SUNKEN, bg='#69A090')
        newSite = Entry(addHolder, font=('Calibri 16'), justify=LEFT, bd=2)
        helper.entryQOF(newSite, addRecord, "(NEW SITE)")
        newUser = Entry(addHolder, font=('Calibri 16'), justify=LEFT, bd=2)
        helper.entryQOF(newUser, addRecord, "(NEW USER)")
        newPass = Entry(addHolder, font=('Calibri 16'), justify=LEFT, bd=2)
        helper.entryQOF(newPass, addRecord, "(NEW PASSWORD)")
        addAdd = Button(addHolder, text="ADD RECORD", bg="#16cca8", fg='black', activeforeground='black', command=addRecord)
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

        helper.generateLayout(addWindow, newPass, screen_width, screen_height)

    def exitApp():
        filepath = helper.resourcePath(str("Profile/" + current.getUser() + ".txt"))
        helper.decrypt(filepath)
        f = open(filepath, "wb")
        f.truncate(0)
        pickle.dump(current, f)
        f.close()
        helper.encrypt(filepath)
        root.destroy()

    def logout():
        exitApp()
        callback() 


    def edit():
        record = tree.item(tree.focus())
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
            current.updatePassword(site, username, passInput)
        elif len(passInput) == 0 and not len(userInput) == 0:
            if current.addSite(site, userInput, password):
                current.deleteUser(site, username)
            else:
                helper.errorWindow("Record already exists.", screen_width, screen_height)
        elif not len(passInput) == 0 and not len(userInput) == 0:
            if current.addSite(site, userInput, passInput):
                current.deleteUser(site, username)
            else:
                helper.errorWindow("Record already exists.", screen_width, screen_height)
        
        temp = OrderedDict()
        destroyAllRecords()
        sortNDict(current.getAccounts(), temp)
        insertRecords(temp)
        editWindow.destroy()


    def editTool():
        if len(tree.selection()) == 0:
            return
        global editWindow
        editWindow = Toplevel(padx=5, pady=7, bg=mainColor)
        editWindow.geometry("550x150")
        # editIconPath = helper.resourcePath("Icons\\edit.png")
        # editIcon = PIL.Image.open(editIconPath)
        # rEditIcon = PIL.ImageTk.PhotoImage(editIcon)
        #editWindow.tk.call('wm', 'iconphoto', editWindow._w)
        editWindow.title("MPM Edit Window")
        editWindow.minsize(550, 150)
        editWindow.maxsize(550, 150)
        helper.windowCentering(editWindow, 550, 150, editWindow.winfo_screenwidth(), editWindow.winfo_screenheight())
        editWindow.focus_set()
        editWindow.grid_rowconfigure(0, weight=2)
        editWindow.grid_rowconfigure(1, weight=1)
        editWindow.grid_rowconfigure(2, weight=2)
        editWindow.grid_columnconfigure(0, weight=2, minsize=100)
        editWindow.grid_columnconfigure(1, weight=2, minsize=100)
        editWindow.grid_columnconfigure(2, weight=1)

        global editUserEntry
        editUserEntry = Entry(editWindow, font=('Calibri 16'), justify=LEFT, bd=2)
        helper.entryQOF(editUserEntry, edit, "(Username to be editted)")
        editUserEntry.grid(row=1, column=0, sticky='NSEW')
        
        global editPassEntry
        editPassEntry = Entry(editWindow, font=('Calibri 16'), justify=LEFT, bd=2)
        helper.entryQOF(editPassEntry, edit, "(Password to be editted)")
        editPassEntry.grid(row=1, column=1, sticky='NSEW')
        
        editButton = Button(editWindow, bg="#16cca8", fg='black', activeforeground='black', text='Edit', command=edit, width=7)
        editButton.grid(row=1, column=2, sticky='NSEW')
        def focusRoot(event):
            x,y = editWindow.winfo_pointerxy()
            currentWidget = editWindow.winfo_containing(x,y)
            if not currentWidget == editUserEntry and not currentWidget == editPassEntry:
                editWindow.focus_set()
    
        editWindow.bind("<Button-1>", focusRoot)
        editWindow.mainloop()
    #end of functions
    
    
    root = Tk()
    root.minsize(750, 400)
    root.title("MY PASSWORD MANAGER")
    programIconPath = helper.resourcePath("assets/Icons/lock_and_key.png")
    programIcon = PIL.Image.open(programIconPath)
    rProgramIcon = PIL.ImageTk.PhotoImage(programIcon)
    root.tk.call('wm', 'iconphoto', root._w, rProgramIcon)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure('Treeview.Heading', background='#8c94a3')
    style.configure('Treeview', rowheight = 30, background="#292c30", foreground = "white", activeforeground="white", fieldbackground = "#292c30")
    style.map("Treeview", background=[('selected', '#5a5e66')])

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    helper.windowCentering(root, 750, 400, root.winfo_screenwidth(), root.winfo_screenheight())
    root.protocol("WM_DELETE_WINDOW", exitApp)
    root.rowconfigure(0, weight=14)
    root.rowconfigure(1, weight=1, minsize=60)
    root.columnconfigure(0, weight=1)

    top=Frame(root)
    top.grid(row=0, column=0, sticky='NSEW')

    scroll = Scrollbar(top, orient=VERTICAL, highlightcolor='black', activebackground='black', bg='grey', troughcolor='#8c94a3')
    tree = ttk.Treeview(top, yscrollcommand=scroll.set, selectmode="browse")    
    
    tree.pack(side=LEFT, fill=BOTH, expand=1)
    scroll.pack(side=RIGHT, fill=Y)    
    scroll.config(command=tree.yview)

    bottom = Frame(root, padx=10, pady=10, bg='#69A090')
    bottom.grid(row=1, column=0, sticky='NSEW')
    bottom.grid_rowconfigure(0, weight=1)
    bottom.grid_columnconfigure(0, weight=1)
    bottom.grid_columnconfigure(1, weight=1)
    bottom.grid_columnconfigure(2, weight=1)
    bottom.grid_columnconfigure(3, weight=1)
    bottom.grid_columnconfigure(4, weight=1)
    bottom.grid_columnconfigure(5, weight=1)
    bottom.grid_columnconfigure(6, weight=1)

    tree['columns'] = ("Site", "User", "Password")
    tree.column("#0", width = 0, stretch=NO)
    tree.column("Site", anchor=W, width= 200, minwidth=200)
    tree.column("User", anchor=W, width= 200, minwidth=200)
    tree.column("Password", anchor=W, width= 200, minwidth=200)
    tree.heading('#0', text="", anchor=W)
    tree.heading('Site', text="Site", anchor=W)
    tree.heading('User', text="User", anchor=W)
    tree.heading('Password', text="Password", anchor=W)

    search = Button(bottom, bg="#16cca8", fg='black', activeforeground='black', text='SEARCH', width=12, command=searchTool)
    backButton = Button(bottom, bg="#16cca8", fg='black', activeforeground='black', text='BACK', width=12, command=revert)
    addButton = Button(bottom, bg="#16cca8", fg='black', activeforeground='black', text='ADD', command=addTool, width=12)
    editButton = Button(bottom, bg="#16cca8", fg='black', activeforeground='black', text='EDIT', command=editTool, width=12)
    deleteButton = Button(bottom, bg="#16cca8", fg='black', activeforeground='black', text='DELETE', command=deleteRecord, width=12)
    copyButton = Button(bottom, bg="#16cca8", fg='black', activeforeground='black', text='COPY PASSWORD', command=copyPassword, width=12)
    logoutButton = Button(bottom, bg="#16cca8", fg='black', activeforeground='black', text='LOGOUT', command=logout, width=12)
    
    search.grid(row=0, column=0, sticky='NSEW')
    backButton.grid(row=0, column=1, sticky='NSEW')
    addButton.grid(row=0, column=2, sticky='NSEW')
    editButton.grid(row=0, column=3, sticky='NSEW')
    deleteButton.grid(row=0, column=4, sticky='NSEW')
    copyButton.grid(row=0, column=5, sticky='NSEW')
    logoutButton.grid(row=0, column=6, sticky='NSEW')
    
    accounts = current.getAccounts()
    sortedDict = OrderedDict()
    sortNDict(accounts, sortedDict)
    insertRecords(sortedDict)

    root.mainloop()
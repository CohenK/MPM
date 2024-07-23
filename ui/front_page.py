import sys
#sys.path.append('/home/cohenk/PassMan/classes/')
from tkinter import *
from os.path import exists, dirname
from classes import Profile
from ui import content_ui
from utils import helper
import pickle
import PIL.Image
import PIL.ImageTk
from ui.display_ui import Display

def mainCreate():

    
    mainColor = '#69A090'
    secondaryColor = '#A3D09D'
    

    root = Tk()
    root.geometry("1200x800")
    programIconPath = helper.resource_path("assets/Icons/lock_and_key.png")
    programIcon = PIL.Image.open(programIconPath)
    rProgramIcon = PIL.ImageTk.PhotoImage(programIcon)
    root.tk.call('wm', 'iconphoto', root._w, rProgramIcon)
    root.configure(background=mainColor)
    root.title("MY PASSWORD MANAGER")
    root.minsize(500,700)

    '''Making app centered'''
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    helper.window_centering(root, 1000, 800, root.winfo_screenwidth(), root.winfo_screenheight())

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=2)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)

    titleFrame = Frame(root, bg=mainColor, padx=20, pady=10)
    title = Label(titleFrame, text = "MPM", font=('Times  90'), background=mainColor, foreground="black")
    miniTitle = Label(titleFrame, text = "My Password Manager", font=('Times  23'), background=mainColor, foreground="black")
    loginFrame = Frame(root, bg=secondaryColor, padx=25, pady=10)
    newFrame = Frame(root, bg=secondaryColor, padx=20, pady=10)

    global loginUser
    global loginPass
    global newUser
    global newPass

    def login():
        user = loginUser.get().strip()
        password = loginPass.get().strip()
        loginUser.delete(0,END)
        loginUser.insert(0, "(Username)")
        loginPass.delete(0, END)
        loginPass.insert(0, "(Password)")
        if (len(user) == 0 or len(password) == 0):
            message = "Please enter your credentials."
            helper.error_window(message, screen_width, screen_height)
            
            return
        else:
            filepath = helper.resource_path(str("Profile/" + user + ".enc"))
            
            if not exists(filepath):
                message = "This user does not exists."
                helper.error_window(message, screen_width, screen_height)
                return
            
            global userProfile
            userProfile = helper.read_decrypt_file(filepath, password)

            helper.write_encrypt_file(filepath, userProfile, password)
            if not userProfile:
                userProfile = None
                message = "Incorrect credentials, please try again."
                helper.error_window(message, screen_width, screen_height)
                
                return
            root.destroy()
            display = Display(userProfile, mainCreate)
            display.run()

    def newAccount():
        user = newUser.get().strip()
        password = newPass.get().strip()
        newUser.delete(0,END)
        newUser.insert(0, "(Username)")
        newPass.delete(0, END)
        newPass.insert(0, "(Password)")
        if (len(user) == 0 or len(password) == 0):
            message= "Please enter your credentials."
            helper.error_window(message, screen_width, screen_height)
            
            return
        else:
            global newAccountUser
            newAccountUser = user
            global newAccountPass
            newAccountPass = password
            filepath = helper.resource_path(str("Profile/" + newAccountUser + ".enc"))
            if exists(filepath + ".enc"):
                message = "This user already exists."
                helper.error_window(message, screen_width, screen_height)
                return

            profiles = dict()
            profiles[newAccountUser] = Profile(newAccountUser, newAccountPass)
            helper.write_encrypt_file(filepath, profiles[newAccountUser], password)

    def showPassword(button, entry):
        if entry.get() == "(Password)":
            return
        entry.config(show="")
        button.configure(command = lambda: hidePassword(button, entry), text = 'Hide Password')


    def hidePassword(button, entry):
        entry.config(show="*")
        button.configure(command = lambda: showPassword(button, entry), text = 'Show Password')

    
    def loginOnClick(event):
        if loginPass.get() == '(Password)':
            loginPass.delete(0, END)
            loginPass.configure(show = "*")

    def loginUnfocus(event):
        if len(loginPass.get()) == 0 or loginPass.get() == "(Password)":
            loginPass.configure(show = "")
            loginPass.insert(0, "(Password)")
            loginShowPassword.configure(text="Show Password")

    def newOnClick(event):
        if newPass.get() == '(Password)':
            newPass.delete(0, END)
            newPass.configure(show = "*")

    def newUnfocus(event):
        if len(newPass.get()) == 0 or newPass.get() == "(Password)":
            newPass.configure(show = "")
            newPass.insert(0, "(Password)")
            newShowPassword.configure(text="Show Password")

    #login UI
    loginTitle = Label(loginFrame, text="Existing User", font=('Calibri 16 bold'), bg=secondaryColor)
    loginButton = Button(loginFrame, text="Login", font=('Calibri 16 bold'), padx = 55, background="#9DBDD0", activebackground="white", command=login)
    loginUser = Entry(loginFrame, font=('Calibri 16'), justify=CENTER, bd=5)
    loginPass = Entry(loginFrame, font=('Calibri 16'), justify=CENTER, bd=5)
    helper.entry_QOF(loginUser, login, "(Username)")
    helper.entry_QOF(loginPass, login, "(Password)")
    loginShowPassword = Button(loginFrame, text="Show Password", background="#9DBDD0", padx = 40, activebackground="white", command=lambda: showPassword(loginShowPassword, loginPass))
    loginPass.bind("<Button-1>", loginOnClick)
    loginPass.bind("<FocusOut>", loginUnfocus)
    #register UI
    newTitle = Label(newFrame, text="New User", font=('Calibri 16 bold'), bg=secondaryColor)
    newAccountButton = Button(newFrame, text="Create Account", font=('Calibri 16 bold'), padx = 12, background="#9DBDD0", activebackground="white", command=newAccount)
    newUser = Entry(newFrame, font=('Calibri 16'), justify=CENTER, bd=5)
    newPass = Entry(newFrame, font=('Calibri 16'), justify=CENTER, bd=5)
    helper.entry_QOF(newUser, newAccount, "(Username)")
    helper.entry_QOF(newPass, newAccount, "(Password)")
    newShowPassword = Button(newFrame, text="Show Password", background="#9DBDD0", padx = 40, activebackground="white", command=lambda: showPassword(newShowPassword ,newPass))
    newPass.bind("<Button-1>", newOnClick)
    newPass.bind("<FocusOut>", newUnfocus)

    loginFrame.grid_rowconfigure(0, weight=1)
    loginFrame.grid_rowconfigure(1, weight=2)
    loginFrame.grid_rowconfigure(2, weight=2)
    loginFrame.grid_rowconfigure(3, weight=3)
    loginFrame.grid_rowconfigure(4, weight=2)
    loginFrame.grid_rowconfigure(5, weight=1)
    newFrame.grid_rowconfigure(0, weight=1)
    newFrame.grid_rowconfigure(1, weight=2)
    newFrame.grid_rowconfigure(2, weight=2)
    newFrame.grid_rowconfigure(3, weight=3)
    newFrame.grid_rowconfigure(4, weight=2)
    newFrame.grid_rowconfigure(5, weight=1)

    #widget placement
    titleFrame.grid(row=0, column=0, pady=(80,0))
    title.grid(row=0, column=0)
    miniTitle.grid(row=1, column=0)
    loginFrame.grid(row=2, column=0, pady=25)
    newFrame.grid(row=3, column=0, pady=25)

    loginTitle.grid(row=0,column=0)
    loginUser.grid(row=1, column=0, pady=5)
    loginPass.grid(row=2, column=0, pady=5)
    loginButton.grid(row=3, column=0, pady=5)
    loginShowPassword.grid(row=4, column=0)

    newTitle.grid(row=0,column=0)
    newUser.grid(row=1, column=0, padx=5)
    newPass.grid(row=2, column=0, pady=5)
    newAccountButton.grid(row=3, column=0, pady=5)
    newShowPassword.grid(row=4, column=0)


    def focusRoot(event):
        x,y = root.winfo_pointerxy()
        currentWidget = root.winfo_containing(x,y)
        if not currentWidget == loginUser and not currentWidget == loginPass and not currentWidget == newUser and not currentWidget == newPass:
            root.focus_set()
    
    root.bind("<Button-1>", focusRoot)
    root.mainloop()
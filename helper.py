from tkinter import *
import sys
from os import path, getcwd
import random
import string
from cryptography.fernet import Fernet
import PIL.Image
import PIL.ImageTk

def entryQOF(input, executedFunction, message):
    input.insert(0, message)
    def clearEntry(event):
        if input.get() == message:
            input.delete(0, END)
    def unfocusedEntry(event):
        if input.get() == "":
            input.insert(0, message)
    def entryEnter(event):
        executedFunction()
    input.bind("<FocusOut>", unfocusedEntry)
    input.bind("<FocusIn>", clearEntry)
    input.bind("<Return>", entryEnter)


def errorWindow(errorMessage, sw, sh):
    errorWindow = Toplevel()
    errorIconPath = resourcePath("Icons\\error.png")
    errorIcon = PIL.Image.open(errorIconPath)
    rErrorIcon = PIL.ImageTk.PhotoImage(errorIcon)
    errorWindow.tk.call('wm', 'iconphoto', errorWindow._w, rErrorIcon)

    errorWindow.title("MPM Error Detected")
    errorWindow.minsize(750,75)
    errorWindow.maxsize(750,75)
    '''making errorwindow centered'''
    windowCentering(errorWindow, 750, 75, errorWindow.winfo_screenwidth(), errorWindow.winfo_screenheight())
    
    def killErrorWindow():
        errorWindow.destroy()

    errorMessage = Label(errorWindow, text=errorMessage, font=("Calibri 16"))
    okButton = Button(errorWindow, text = "OK", padx=15 ,command =killErrorWindow, bg="#16cca8")
    def enterKey(event):
        killErrorWindow()
    errorWindow.bind("<Return>", enterKey)


    errorMessage.grid(row=0, column=0)
    okButton.grid(row=1, column=0)
    errorWindow.grid_columnconfigure(0, weight=1)
    errorWindow.focus_set()

    
def generatePassword(lower, upper, numbers, special):
    lowerChars =''
    upperChars =''
    numberChars =''
    specialChars =''
    result = ''
    specialList = '!#$%&*+/?@^_~'
    if lower == 0 and upper == 0 and numbers == 0 and special == 0:
        lower=random.randint(4, 6)
        upper=random.randint(4, 6)
        numbers=random.randint(3, 4)
        special=random.randint(2, 4)

    for b in range(lower):
        lowerChars += random.choice(string.ascii_lowercase)
    for b in range(upper):
        upperChars += random.choice(string.ascii_uppercase)
    for b in range(numbers):
        numberChars += str(random.randint(0,9))
    for b in range(special):
        specialChars += random.choice(specialList)
  
    result+= (lowerChars + upperChars + numberChars + specialChars)
    rresult = ''.join(random.sample(result, len(result)))
    return rresult

def generatePass(numLower, numUpper, numNumber, numSpecial, newPass, screen_width, screen_height):
    lower = 0
    upper = 0
    num = 0
    special = 0
    if numLower.get() == '':
        pass
    else:
        if numLower.get().strip().isdigit():
            lower = int(numLower.get())
            numLower.delete(0, END)
            numLower.insert(0, '0')
        else:
            errorWindow("One or more inputs are not positive integers.", screen_width, screen_height)
            numLower.delete(0, END)
            numLower.insert(0, '0')
            return
    if numUpper.get() == '':
        pass
    else:
        if numUpper.get().strip().isdigit():
            upper = int(numUpper.get())
            numUpper.delete(0, END)
            numUpper.insert(0, '0')
        else:
            errorWindow("One or more inputs are not positive integers.", screen_width, screen_height)
            numUpper.delete(0, END)
            numUpper.insert(0, '0')
            return
    if numNumber.get() == '':
        pass
    else:
        if numNumber.get().strip().isdigit():
            num = int(numNumber.get())
            numNumber.delete(0, END)
            numNumber.insert(0, '0')
        else:
            errorWindow("One or more inputs are not positive integers.", screen_width, screen_height)
            numNumber.delete(0, END)
            numNumber.insert(0, '0')
            return
    if numSpecial.get() == '':
        pass
    else:
        if numSpecial.get().strip().isdigit():
            special = int(numSpecial.get())
            numSpecial.delete(0, END)
            numSpecial.insert(0, '0')
        else:
            errorWindow("One or more inputs are not positive integers.", screen_width, screen_height)
            numSpecial.delete(0, END)
            numSpecial.insert(0, '0')
            return
    generatedPassword = generatePassword(lower, upper, num, special)
    newPass.delete(0, END)
    newPass.insert(0, generatedPassword)

def generateLayout(window, newPass, screen_width, screen_height):
    passHolder = Frame(window, padx=10, pady=5, relief=SUNKEN, bg='#69A090')
    description = Label(passHolder, text="Below is a password generator that you may use to create new passwords.\n The inputs are the number of the different characters that you want in your password. \n If no input are given a random password will be generated containing the following: \n 4-6 lower case letters, 4-6 upper case letters, 3-4 numbers and 2-4 special characters.\n Special characters include the following: !#$%&*+-/?@^_~", font=('Calibri 10') , bg='#69A090')
    lower = Label(passHolder, text= "Lower Case", font=('Calibri 10') , bg='#69A090')
    upper = Label(passHolder, text= "Upper Case", font=('Calibri 10') , bg='#69A090')
    number = Label(passHolder, text= "Numbers", font=('Calibri 10') , bg='#69A090')
    special = Label(passHolder, text= "Special Characters", font=('Calibri 10') , bg='#69A090')
    numLower = Entry(passHolder, font=('Calibri 16'), justify=LEFT, bd=2)
    entryQOF(numLower, generatePass, "0")
    numUpper = Entry(passHolder, font=('Calibri 16'), justify=LEFT, bd=2)
    entryQOF(numUpper, generatePass, "0")
    numNumber = Entry(passHolder, font=('Calibri 16'), justify=LEFT, bd=2)
    entryQOF(numNumber, generatePass, "0")
    numSpecial = Entry(passHolder, font=('Calibri 16'), justify=LEFT, bd=2)
    entryQOF(numSpecial, generatePass, "0")
    generate = Button(passHolder, text='GENERATE PASSWORD', bg="#16cca8", fg='black', activeforeground='black', command=lambda: generatePass(numLower, numUpper, numNumber, numSpecial, newPass, screen_width, screen_height))
    passHolder.grid(row=1, column=0, sticky='NSEW')
    passHolder.grid_rowconfigure(0, weight=2)
    passHolder.grid_rowconfigure(1, weight=1)
    passHolder.grid_rowconfigure(2, weight=1)
    passHolder.grid_rowconfigure(3, weight=1)
    passHolder.grid_columnconfigure(0, weight=1)
    passHolder.grid_columnconfigure(1, weight=1)
    passHolder.grid_columnconfigure(2, weight=1)
    passHolder.grid_columnconfigure(3, weight=1)
    description.grid(row=0, column=0, columnspan=4, sticky='NSEW')
    lower.grid(row=1, column=0, sticky='NSEW')
    upper.grid(row=1, column=1, sticky='NSEW')
    number.grid(row=1, column=2, sticky='NSEW')
    special.grid(row=1, column=3, sticky='NSEW')
    numLower.grid(row=2, column=0, sticky='NSEW')
    numUpper.grid(row=2, column=1, sticky='NSEW')
    numNumber.grid(row=2, column=2, sticky='NSEW')
    numSpecial.grid(row=2, column=3, sticky='NSEW')
    generate.grid(row=3, column=0, columnspan=4, sticky='NSEW')


def windowCentering(window, ww, wh, sw, sh):
    window_x=(sw/2)-(ww/2)
    window_y=(sh/2)-(wh/2)
    window.geometry(f'{ww}x{wh}+{int(window_x)}+{int(window_y)}')

def unfocusEntry(window, entry):

    def clickOutside(event):
        x,y = window.winfo_pointerxy()
        currentWidget = window.winfo_containing(x,y)
        if not currentWidget == entry:
            window.focus_set()
    
    window.bind("<Button-1>", clickOutside)



key = '4YWpaEueGQrKpchPX3tAkT9llZHaF38l1nk1UwU-_Ew='
fernetObject = Fernet(key)

def encrypt(filepath):
    with open(filepath, 'rb') as originalFile:
        original = originalFile.read()

    encryptedFile = fernetObject.encrypt(original)

    with open(filepath, 'wb') as eFile:
        eFile.write(encryptedFile)

def decrypt(filepath):
    with open(filepath, 'rb') as eFile:
        encrypted = eFile.read()

    decrypted = fernetObject.decrypt(encrypted)

    with open(filepath, 'wb') as dFile:
        dFile.write(decrypted)

def resourcePath(file_name):
    if getattr(sys, 'frozen', False):
        application_path = path.dirname(sys.executable)
    else:
        try:
            app_full_path = path.realpath(__file__)
            application_path = path.dirname(app_full_path)
        except NameError:
            application_path = getcwd()
    full_path = path.join(application_path, file_name)
    return full_path

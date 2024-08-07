from tkinter import *
import sys
from os import path, getcwd
import string
import PIL.Image
import PIL.ImageTk
import pickle
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import secrets
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

def entry_QOF(input, executed_function, message):
    input.insert(0, message)
    def clear_entry(event):
        if input.get() == message:
            input.delete(0, END)
    def unfocused_entry(event):
        if input.get() == "":
            input.insert(0, message)
    def entry_enter(event):
        executed_function()
    input.bind("<FocusOut>", unfocused_entry)
    input.bind("<FocusIn>", clear_entry)
    input.bind("<Return>", entry_enter)

def error_window(error_message, sw = 500, sh = 100):
    error_window = Toplevel()
    error_icon_path = resource_path("assets/Icons/error.png")
    error_icon = PIL.Image.open(error_icon_path)
    r_error_icon = PIL.ImageTk.PhotoImage(error_icon)
    error_window.tk.call('wm', 'iconphoto', error_window._w, r_error_icon)
    error_window.config(bg=primary_color)
    error_window.grid_rowconfigure(0,weight=1)
    error_window.grid_rowconfigure(1,weight=1)
    error_window.grid_columnconfigure(0,weight=1)
    max_width = error_window.winfo_screenwidth()
    max_height = error_window.winfo_screenheight()

    error_window.title("MPM Error Detected")
    error_window.minsize(750,250)
    error_window.maxsize(750,250)
    window_centering(error_window, 750, 250, max_width, max_height)
    
    def kill_error_window():
        error_window.destroy()

    error_message = Label(error_window, text=error_message, font=("Calibri 16 bold"), bg=primary_color, wraplength=500)
    okButton = Button(error_window, bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', text = "OK", padx=15 ,command =kill_error_window)
    def enterKey(event):
        kill_error_window()
    error_window.bind("<Return>", enterKey)
    error_message.grid(row=0, column=0)
    okButton.grid(row=1, column=0, sticky="N")
    error_window.focus_set()

class Confirmation_Window(Toplevel):
    def __init__(self,parent,message):
        super().__init__(parent)
        self.result = BooleanVar()
        self.title("MPM Confirmation")
        self.geometry("750x100")
        self.config(bg=primary_color)
        self.minsize(750,100)
        self.maxsize(750,100)
        self.grab_set()
        window_centering(self, 750, 100, self.winfo_screenwidth(), self.winfo_screenheight())
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.focus_set()

        label = Label(self, text=message, bg=primary_color)
        label.config(font=('Calibri',14,'bold'))
        confirm_button= Button(self, bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', text = "Confirm", padx=15 ,command=self.confirm)
        cancel_button= Button(self, bg=thirtiary_light, fg='black', activebackground=thirtiary_color, activeforeground='black', text = "Cancel", padx=15 ,command=self.cancel)
        confirm_button.config(font=('Calibri',10,'bold'))
        cancel_button.config(font=('Calibri',10,'bold'))
        label.grid(row=0, column=0, columnspan=2, pady=10)
        confirm_button.grid(row=1, column=0, sticky='E',padx=10, pady=5)
        cancel_button.grid(row=1, column=1, sticky='W',padx=10, pady=5)

    def confirm(self):
        self.result.set(True)
        self.destroy()

    def cancel(self):
        self.result.set(False)
        self.destroy() 
    
def generate_password(lower, upper, numbers, special):
    lower_chars = string.ascii_uppercase
    upper_chars = string.ascii_lowercase
    number_chars = string.digits
    special_chars = string.punctuation
    password_chars = []

    if lower != 0 or upper != 0 or numbers != 0 or special != 0:
        password_chars = (  [secrets.choice(lower_chars) for n in range(lower)] + 
                            [secrets.choice(upper_chars) for n in range(upper)] + 
                            [secrets.choice(number_chars) for n in range(numbers)] + 
                            [secrets.choice(special_chars) for n in range(special)])
    else:
        fill = secrets.SystemRandom().randint(8,15)
        all_chars = lower_chars + upper_chars + number_chars + special_chars
        password_chars = ([secrets.choice(lower_chars) for n in range(1)] + 
                        [secrets.choice(upper_chars) for n in range(1)] + 
                        [secrets.choice(number_chars) for n in range(1)] + 
                        [secrets.choice(special_chars) for n in range(1)] +
                        [ secrets.choice(all_chars) for n in range(fill-4)])

    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)

def generate_pass(numLower, numUpper, numNumber, numSpecial, newPass, screen_width, screen_height):
    lower = 0
    upper = 0
    num = 0
    special = 0
    def reset_entry(entry, message):
        entry.delete(0,END)
        entry.insert(0,message)

    if numLower.get() == 'lower':
        pass
    else:
        if numLower.get().strip().isdigit():
            lower = int(numLower.get())
            reset_entry(numLower,'lower')
        else:
            error_window("One or more inputs are not positive integers.", screen_width, screen_height)
            reset_entry(numLower,'lower')
            return
    if numUpper.get() == 'upper':
        pass
    else:
        if numUpper.get().strip().isdigit():
            upper = int(numUpper.get())
            reset_entry(numUpper,'upper')
        else:
            error_window("One or more inputs are not positive integers.", screen_width, screen_height)
            reset_entry(numUpper,'upper')
            return
    if numNumber.get() == 'number':
        pass
    else:
        if numNumber.get().strip().isdigit():
            num = int(numNumber.get())
            reset_entry(numNumber,'number')
        else:
            error_window("One or more inputs are not positive integers.", screen_width, screen_height)
            reset_entry(numNumber,'number')
            return
    if numSpecial.get() == 'special':
        pass
    else:
        if numSpecial.get().strip().isdigit():
            special = int(numSpecial.get())
            reset_entry(numSpecial,'special')
        else:
            error_window("One or more inputs are not positive integers.", screen_width, screen_height)
            reset_entry(numSpecial,'special')
            return
    generatedPassword = generate_password(lower, upper, num, special)
    newPass.delete(0, END)
    newPass.insert(0, generatedPassword)
    pyperclip.copy(generatedPassword)

def generate_layout(window, newPass, screen_width, screen_height):
    passHolder = Frame(window, padx=10, pady=5, relief=SUNKEN, bg='#69A090')
    description = Label(passHolder, text="Below is a password generator that you may use to create new passwords.\n The inputs are the number of the different characters that you want in your password. \n If no input are given a random password will be generated containing the following: \n 4-6 lower case letters, 4-6 upper case letters, 3-4 numbers and 2-4 special characters.\n Special characters include the following: !#$%&*+-/?@^_~", font=('Calibri 10') , bg='#69A090')
    lower = Label(passHolder, text= "Lower Case", font=('Calibri 10') , bg='#69A090')
    upper = Label(passHolder, text= "Upper Case", font=('Calibri 10') , bg='#69A090')
    number = Label(passHolder, text= "Numbers", font=('Calibri 10') , bg='#69A090')
    special = Label(passHolder, text= "Special Characters", font=('Calibri 10') , bg='#69A090')
    numLower = Entry(passHolder, font=('Calibri 16'), justify=LEFT, bd=2)
    entry_QOF(numLower, generate_pass, "0")
    numUpper = Entry(passHolder, font=('Calibri 16'), justify=LEFT, bd=2)
    entry_QOF(numUpper, generate_pass, "0")
    numNumber = Entry(passHolder, font=('Calibri 16'), justify=LEFT, bd=2)
    entry_QOF(numNumber, generate_pass, "0")
    numSpecial = Entry(passHolder, font=('Calibri 16'), justify=LEFT, bd=2)
    entry_QOF(numSpecial, generate_pass, "0")
    generate = Button(passHolder, text='GENERATE PASSWORD', bg="#16cca8", fg='black', activeforeground='black', command=lambda: generate_pass(numLower, numUpper, numNumber, numSpecial, newPass, screen_width, screen_height))
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

def window_centering(window, ww, wh, sw, sh):
    window_x=(sw/2)-(ww/2)
    window_y=(sh/2)-(wh/2)
    window.geometry(f'{ww}x{wh}+{int(window_x)}+{int(window_y)}')

def unfocus_entry(window, entry):

    def clickOutside(event):
        x,y = window.winfo_pointerxy()
        currentWidget = window.winfo_containing(x,y)
        if not currentWidget == entry:
            window.focus_set()
    
    window.bind("<Button-1>", clickOutside)

# key = '4YWpaEueGQrKpchPX3tAkT9llZHaF38l1nk1UwU-_Ew='
# fernetObject = Fernet(key)
# def encrypt(filepath):
#     with open(filepath, 'rb') as originalFile:
#         original = originalFile.read()
#     encryptedFile = fernetObject.encrypt(original)
#     with open(filepath, 'wb') as eFile:
#         eFile.write(encryptedFile)
# def decrypt(filepath):
#     with open(filepath, 'rb') as eFile:
#         encrypted = eFile.read()
#     decrypted = fernetObject.decrypt(encrypted)
#     with open(filepath, 'wb') as dFile:
#         dFile.write(decrypted)

def resource_path(file_name):
    if getattr(sys, 'frozen', False):
        application_path = path.dirname(sys.executable)
    else:
        try:
            app_full_path = path.realpath(__file__)
            application_path = path.dirname(path.dirname(app_full_path))
        except NameError:
            application_path = getcwd()

    full_path = path.join(application_path, file_name)
    return full_path

def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())

def write_encrypt_file(file_path: str, data, password: str):
    
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)

    with open(file_path, 'rb') as f:
        data = f.read()

    salt = os.urandom(16)
    key = generate_key(password, salt)
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(file_path, 'wb') as f:
        f.write(salt + iv + encrypted_data)

def read_decrypt_file(file_path: str, password: str):
    message = ""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        salt, iv, encrypted_data = data[:16], data[16:32], data[32:]
        key = generate_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()

        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        deserialized_data = []

        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        deserialized_data = pickle.loads(decrypted_data)
        
        return deserialized_data

    except ValueError as e:
        message = "ValueError. Error"
    except (pickle.UnpicklingError, EOFError) as e:
        message = "Deserialization failed. Error"
    except Exception as e:
        message = "Unknown error. Error"
    
    error_window(message)
from tkinter import *
import sys
from os import path, getcwd
import string
import pickle
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import secrets
import pyperclip
from src.ui.custom_widget_classes import Error_Window

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
            Error_Window("One or more inputs are not positive integers.")
            reset_entry(numLower,'lower')
            return
    if numUpper.get() == 'upper':
        pass
    else:
        if numUpper.get().strip().isdigit():
            upper = int(numUpper.get())
            reset_entry(numUpper,'upper')
        else:
            Error_Window("One or more inputs are not positive integers.")
            reset_entry(numUpper,'upper')
            return
    if numNumber.get() == 'number':
        pass
    else:
        if numNumber.get().strip().isdigit():
            num = int(numNumber.get())
            reset_entry(numNumber,'number')
        else:
            Error_Window("One or more inputs are not positive integers.")
            reset_entry(numNumber,'number')
            return
    if numSpecial.get() == 'special':
        pass
    else:
        if numSpecial.get().strip().isdigit():
            special = int(numSpecial.get())
            reset_entry(numSpecial,'special')
        else:
            Error_Window("One or more inputs are not positive integers.")
            reset_entry(numSpecial,'special')
            return
    generatedPassword = generate_password(lower, upper, num, special)
    newPass.delete(0, END)
    newPass.insert(0, generatedPassword)
    pyperclip.copy(generatedPassword)

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
    
    Error_Window(message)
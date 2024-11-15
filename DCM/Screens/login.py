########################################################################################################################
#
#                                        Login class for showing login screen
#
########################################################################################################################
import tkinter as tk
from tkinter import messagebox
from Screens.home import show_home_screen
from Utils.login import UserManager

def show_login_screen(root):
    root.geometry("400x300")
    root.title("Pacemaker DCM Login")

    # User login fields and buttons
    username_label = tk.Label(root, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    password_label = tk.Label(root, text="Password:")
    password_label.pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    user_manager = UserManager()  

    def authenticate_and_open_home(root, username, password):
        if user_manager.authenticate_user(username, password):
            show_home_screen(root, username)
        else:
            messagebox.showerror("Error", "usernamer or password incorrect")      

    login_button = tk.Button(root, text="Login", 
                             command=lambda: authenticate_and_open_home(root, username_entry.get(), password_entry.get()))
    login_button.pack(pady=20)

    register_button = tk.Button(root, text="Register New User", command=lambda: user_manager.register_new_user(root))
    register_button.pack(pady=10)

    about_button = tk.Button(root, text="About", command=show_about_section)
    about_button.pack(pady=10)

def show_about_section():
    about_window = tk.Toplevel()
    about_window.title("About")
    about_window.geometry("300x200")
    APP_INFO = {
        "Model Number": "1234",
        "Software Revision": "v1.0",
        "DCM Serial Number": "SN-123456789",
        "Institution Name": "McMaster"
    }
    for key, value in APP_INFO.items():
        info_label = tk.Label(about_window, text=f"{key}: {value}")
        info_label.pack(anchor="w", padx=10, pady=5)
    tk.Button(about_window, text="Close", command=about_window.destroy).pack(pady=10)



########################################################################################################################
#
#                               Login class for backend registering and loging in users
#
########################################################################################################################

import json
import tkinter as tk
from tkinter import messagebox

def get_users():
    try:
        with open('Data/users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Filepath Error")
        return 0

class UserManager:
    MAX_USERS = 10

    def __init__(self):
        self.users = get_users()

    def authenticate_user(self, username, password):
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

    def add_user(self, new_user):
        for user in self.users:
            if user['username'] == new_user['username']:
                messagebox.showinfo("Fail", f"Fail user \"{new_user['username']}\" already registered!")
                return None
        
        self.users.append(new_user)

        with open('Data/users.json', 'w') as f:
            json.dump(self.users, f, indent=4)

        messagebox.showinfo("Success", f"{new_user['role']} registered successfully!")

    def register_new_user(self, root):
        with open('Data/users.json', 'r') as f:
            self.users = json.load(f)

        if len(self.users) >= self.MAX_USERS:
            messagebox.showerror("Error", "Max user limit reached")
            return

        def save_new_user():
            new_user = {
                "username": username_entry.get(),
                "password": password_entry.get(),
                "role": role_var.get()
            }
            self.add_user(new_user)
            registration_window.destroy()

        registration_window = tk.Toplevel(root)
        registration_window.title("Register New User")

        tk.Label(registration_window, text="Username:").grid(row=0, column=0)
        username_entry = tk.Entry(registration_window)
        username_entry.grid(row=0, column=1)

        tk.Label(registration_window, text="Password:").grid(row=1, column=0)
        password_entry = tk.Entry(registration_window, show='*')
        password_entry.grid(row=1, column=1)

        # Add role selection
        tk.Label(registration_window, text="Role:").grid(row=2, column=0)
        role_var = tk.StringVar(value="Patient")
        tk.Radiobutton(registration_window, text="Patient", variable=role_var, value="Patient").grid(row=2, column=1)
        tk.Radiobutton(registration_window, text="Practitioner", variable=role_var, value="Practitioner").grid(row=2, column=2)

        register_button = tk.Button(registration_window, text="Register", command=save_new_user)
        register_button.grid(row=3, column=1)
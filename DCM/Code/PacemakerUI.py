import tkinter as tk
from tkinter import messagebox

import json
import os
import sys

sys.path.append(os.path.abspath('../'))

from DCM.Languages.Lang import translations

# File to store user data
USER_DATA_FILE = "data/users.json"
PACEMAKER_PARAMS_FILE = "data/pacemaker_params.json"

egram_data = {
    "user": "JohnDoe",
    "session_id": "S12345",
    "mode": "DDD",
    "pacemakerID": "123ABC",
    "data_points": [
        {"time": 0.0, "atrial_signal": 1.2, "ventricular_signal": 2.4, "event": "Atrial Pace", "heart_rate": 60},
        {"time": 0.5, "atrial_signal": 1.3, "ventricular_signal": 2.3, "event": "Ventricular Pace", "heart_rate": 62},
        {"time": 1.0, "atrial_signal": 1.1, "ventricular_signal": 2.5, "event": "Atrial Sense", "heart_rate": 63},
        # More data points...
    ]
}

default_params = {
    "Lower Rate Limit": "60 BPM",
    "Upper Rate Limit": "120 BPM",
    "Atrial Amplitude": "70 %",
    "Atrial Pulse Width": "10 ms",
    "Ventricle Amplitude": "70 %",
    "Ventricle Pulse Width": "10 ms",
    "VRP": "250ms",
    "ARP": "250ms"
}

# Ensure the 'data/' folder exists
if not os.path.exists('data'):
    os.makedirs('data')

# Load user data from file if it exists
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save user data to file
def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Dictionary to hold user data
users = load_users()

# Set current language (default to English)
current_lang = 'EN'

# Function for existing user login
def existing_user_login():
    login_window = tk.Toplevel(root)
    login_window.title(translations[current_lang]["existing_user"])
    login_window.geometry("300x200")

    username_label = tk.Label(login_window, text=translations[current_lang]["username"])
    username_label.pack(pady=5)
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)

    password_label = tk.Label(login_window, text=translations[current_lang]["password"])
    password_label.pack(pady=5)
    password_entry = tk.Entry(login_window, show="*", width=30)
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username in users and users[username] == password:
            messagebox.showinfo("Login", translations[current_lang]["login_success"])
            login_window.destroy()  # Close the login window
            user_home(username)  # Show the new screen with 4 buttons
        else:
            messagebox.showerror("Login", translations[current_lang]["login_failed"])

    login_button = tk.Button(login_window, text=translations[current_lang]["login"], command=login)
    login_button.pack(pady=10)

# Function for new user registration
def new_user_registration():
    if len(users) >= 10:
        messagebox.showerror("Registration Error", "max users reached")
        return  # Stop the registration process if the limit is reached

    register_window = tk.Toplevel(root)
    register_window.title(translations[current_lang]["new_user"])
    register_window.geometry("300x200")

    username_label = tk.Label(register_window, text=translations[current_lang]["username"])
    username_label.pack(pady=5)
    username_entry = tk.Entry(register_window, width=30)
    username_entry.pack(pady=5)

    password_label = tk.Label(register_window, text=translations[current_lang]["password"])
    password_label.pack(pady=5)
    password_entry = tk.Entry(register_window, show="*", width=30)
    password_entry.pack(pady=5)

    def register():
        username = username_entry.get()
        password = password_entry.get()
        if username in users:
            messagebox.showerror("Registration Error", "User already exists")
        else:
            users[username] = password  # Add the new user
            save_users(users)  # Save the users to a file
            messagebox.showinfo("Registration", translations[current_lang]["register_success"])
            register_window.destroy()  # Close the registration window

    register_button = tk.Button(register_window, text=translations[current_lang]["register"], command=register)
    register_button.pack(pady=10)

def user_home(username):
    root.title("Pacemaker DCM")
    login_button.pack_forget()
    register_button.pack_forget()

    # Connection status label (default to 'Not Connected')
    connection_status = tk.Label(root, text="Connection Status: Not Connected", fg="red")
    connection_status.place(relx=1.0, rely=0.0, anchor="ne")  # Place at top-right corner

    # Function to update connection status (you can later use this when connection changes)
    def update_connection_status(status):
        connection_status.config(text=f"Connection Status: {status}")
        if status == "Connected":
            connection_status.config(fg="green")
        else:
            connection_status.config(fg="red")
    
    def sign_out():
        root.deiconify() 
        root.title("Pacemaker UI")
        
        login_button.pack(pady=50)
        register_button.pack(pady=50)

        param_button.pack_forget()
        mode_button.pack_forget()
        sign_out_button.pack_forget()


    # Button to access programmable parameters
    param_button = tk.Button(root, text="Programmable Parameters", command=lambda: show_programmable_parameters(username))
    param_button.pack(pady=30)

    # Button to change pacemaker operation mode
    mode_button = tk.Button(root, text="Change Operation Mode", command=lambda: change_operation_mode(username))
    mode_button.pack(pady=30)

    sign_out_button = tk.Button(root, text="Sign Out", command=sign_out)
    sign_out_button.pack(pady=30)


# Function to change pacemaker operation mode
def change_operation_mode(username):
    # Create a new window for operation mode selection
    mode_window = tk.Toplevel(root)
    mode_window.title("Change Operation Mode")
    mode_window.geometry("400x300")

    # Function to handle mode change and display message
    def set_mode(mode_name):
        messagebox.showinfo("Mode Change", f"Device is now in {mode_name} mode")

    # Create 4 buttons for different operation modes
    mode1_button = tk.Button(mode_window, text="VOO", command=lambda: set_mode("VOO"))
    mode1_button.pack(pady=20)

    mode2_button = tk.Button(mode_window, text="VVI", command=lambda: set_mode("VVI"))
    mode2_button.pack(pady=20)

    mode3_button = tk.Button(mode_window, text="AOO", command=lambda: set_mode("AOO"))
    mode3_button.pack(pady=20)

    mode4_button = tk.Button(mode_window, text="AAI", command=lambda: set_mode("AAI"))
    mode4_button.pack(pady=20)

def save_user_pacemaker_params(username, params):
    user_data_path = os.path.join('data', f"{username}_pacemaker_params.json")
    with open(user_data_path, 'w') as f:
        json.dump(params, f)

# Function to load pacemaker parameters for a user
def load_user_pacemaker_params(username):
    user_data_path = os.path.join('data', f"{username}_pacemaker_params.json")
    if os.path.exists(user_data_path):
        with open(user_data_path, 'r') as f:
            return json.load(f)
    return default_params  # Return default if user has no parameters

def show_programmable_parameters(username):
    params = load_user_pacemaker_params(username)  # Load current parameters for the user
    param_window = tk.Toplevel(root)
    param_window.title("Pacemaker Parameters")
    param_window.geometry("400x400")

    # Display current parameters
    param_label = tk.Label(param_window, text=f"Current Parameters for {username}:")
    param_label.pack(pady=10)

    # Create a frame to hold all parameter widgets
    param_frame = tk.Frame(param_window)
    param_frame.pack(fill="both", expand=True)

    # Dictionary to hold Label widgets for each parameter (initially read-only)
    param_labels = {}
    param_entries = {}

    # Dynamically create labels for each parameter (read-only initially)
    for param_name, param_value in params.items():
        param_label = tk.Label(param_frame, text=f"{param_name}: {param_value}")
        param_label.pack(pady=5)
        param_labels[param_name] = param_label  # Save labels in a dictionary for later access

    # Function to switch to "edit" mode and replace labels with Entry widgets
    def modify_parameters():
        for param_name, param_label in param_labels.items():
            param_label.pack_forget()  # Remove the label
            param_entry = tk.Entry(param_frame, width=30)
            param_entry.pack(pady=5)
            param_entry.insert(0, params[param_name])  # Insert current value into the entry
            param_entries[param_name] = param_entry  # Save entry in a dictionary for later access

        modify_button.pack_forget()  # Hide the modify button
        save_button.pack(pady=20)  # Show the save button

    # Function to save modified parameters
    def save_parameters():
        new_params = {param_name: entry.get() for param_name, entry in param_entries.items()}
        save_user_pacemaker_params(username, new_params)
        messagebox.showinfo("Success", "Parameters saved successfully!")
        param_window.destroy()  # Close window after saving

    # Button to modify parameters (switch to entry mode)
    modify_button = tk.Button(param_window, text="Modify Parameters", command=modify_parameters)
    modify_button.pack(pady=10)

    # Save button (hidden initially, only shown after modifying parameters)
    save_button = tk.Button(param_window, text="Save Parameters", command=save_parameters)
    save_button.pack_forget()  # Initially hidden


# Initialize the main window
root = tk.Tk()
root.title("Pacemaker UI")
root.geometry("400x400")

# Add two buttons: one for existing user login, and one for new user registration
login_button = tk.Button(root, text="Existing User Login", command=existing_user_login)
login_button.pack(pady=50)

register_button = tk.Button(root, text="New User Registration", command=new_user_registration)
register_button.pack(pady=50)

# Start the main event loop
root.mainloop()

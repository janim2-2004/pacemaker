import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import Utils.device_params as params
from Utils.login import UserManager
from Utils.user import User 

def show_home_screen(root, username):
    home_window = tk.Toplevel(root)
    home_window.title(f"Home - {username}")
    home_window.geometry("400x400")

    user = User(username)

    if user.authenticate_admin():
        tk.Label(home_window, text=f"Welcome, Practitioner {username}").pack()
        # Admin-specific features
        manage_users_button = tk.Button(home_window, text="Manage Patients", command=lambda: manage_users(home_window))
        manage_users_button.pack(pady=20)

        change_operation_mode_button = tk.Button(home_window, text="Change Operation Mode",
                                             command=lambda: params.change_operation_mode(home_window))
        change_operation_mode_button.pack(pady=20)
    else:
        tk.Label(home_window, text=f"Welcome, {username}").pack()
        view_operation_mode_button = tk.Button(home_window, text="Operation Mode",
                                             command=lambda: show_operation_mode(home_window))
        view_operation_mode_button.pack(pady=20)

    # Common features for both user types

    programmable_params_button = tk.Button(home_window, text="View Programmable Parameters",
                                           command=lambda: show_programmable_parameters(home_window, user))
    programmable_params_button.pack(pady=20)

    set_clock_button = tk.Button(home_window, text="Set Clock", command=lambda: set_clock(home_window))
    set_clock_button.pack(pady=20)

    sign_out_button = tk.Button(home_window, text="Sign Out", command=lambda: sign_out(home_window, root))
    sign_out_button.pack(pady=20)

def sign_out(home_window, root):
    # Close the user's home window
    home_window.destroy()

    # Show the login screen again (re-initialize the login UI)
    root.deiconify()

def manage_users(root):
    user_manager = UserManager()
    users = user_manager.get_users()

    manage_window = tk.Toplevel(root)
    manage_window.title("Manage Users")

    # Display a list of all registered users
    tk.Label(manage_window, text="Registered Users:").grid(row=0, column=0)
    for user in users:
        tk.Label(manage_window, text=f"User : {user['username']} ({user['role']})")

def show_programmable_parameters(parent_window, user):
    params = user.get_user_parameters()  # Load current parameters for the user
    param_window = tk.Toplevel(parent_window)
    param_window.title("Pacemaker Parameters")
    param_window.geometry("400x500")

    # Display current parameters
    param_label = tk.Label(param_window, text=f"Current Parameters for {user.get_username()}:")
    param_label.pack(pady=10)

    # Create a frame to hold all parameter widgets
    param_frame = tk.Frame(param_window)
    param_frame.pack(fill="both", expand=True)

    # Dictionary to hold Label widgets for each parameter (initially read-only)
    param_labels = {}
    param_entries = {}

    # Dynamically create labels for each parameter
    for param_name, param_value in params.items():
        param_label = tk.Label(param_frame, text=f"{param_name}: {param_value}")
        param_label.pack(pady=5)
        param_labels[param_name] = param_label  # Save labels in a dictionary for later access

    # Function to switch to "edit" mode and replace labels with Entry widgets
    def modify_parameters():
        for param_name, param_label in param_labels.items():
            param_label.pack_forget() 
            param_entry = tk.Entry(param_frame, width=30)
            param_entry.pack(pady=5)
            param_entry.insert(0, params[param_name]) 
            param_entries[param_name] = param_entry  # Save entry in a dictionary for later access

        modify_button.pack_forget()  
        save_button.pack(pady=20) 

    # Function to save modified parameters
    def save_parameters():
        new_params = {param_name: entry.get() for param_name, entry in param_entries.items()}
        save_programmable_parameters(user.get_username(), new_params)
        messagebox.showinfo("Success", "Parameters saved successfully!")
        param_window.destroy()  # Close window after saving

    if user.authenticate_admin():
        modify_button = tk.Button(param_window, text="Modify Parameters", command=modify_parameters)
        modify_button.pack(pady=10)

        save_button = tk.Button(param_window, text="Save Parameters", command=save_parameters)
        save_button.pack_forget()  # Initially hidden

def set_clock():
    clock_window = tk.Toplevel()
    clock_window.title("Set Device Clock")
    clock_window.geometry("300x200")

    tk.Label(clock_window, text="Current Date (YYYY-MM-DD):").pack(pady=5)
    date_entry = tk.Entry(clock_window)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    date_entry.pack(pady=5)

    tk.Label(clock_window, text="Current Time (HH:MM):").pack(pady=5)
    time_entry = tk.Entry(clock_window)
    time_entry.insert(0, datetime.now().strftime("%H:%M"))
    time_entry.pack(pady=5)

    apply_button = tk.Button(clock_window, text="Set Clock", command=lambda: apply_clock(date_entry.get(), time_entry.get(), clock_window))
    apply_button.pack(pady=10)

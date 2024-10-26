import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from Utils.device_params import apply_clock, change_operation_mode, get_programmable_parameters, save_programmable_parameters

def show_home_screen(root, username):
    home_window = tk.Toplevel(root)
    home_window.title("Pacemaker DCM")
    home_window.geometry("400x400")

    connection_status = tk.Label(home_window, text="Connection Status: Not Connected", fg="red")
    connection_status.place(relx=1.0, rely=0.0, anchor="ne")

    param_button = tk.Button(home_window, text="Programmable Parameters", command=lambda: show_programmable_parameters(home_window, username))
    param_button.pack(pady=30)

    mode_button = tk.Button(home_window, text="Change Operation Mode", command=lambda: change_operation_mode(home_window))
    mode_button.pack(pady=30)

    set_clock_button = tk.Button(home_window, text="Set Clock", command=set_clock)
    set_clock_button.pack(pady=30)

    sign_out_button = tk.Button(home_window, text="Sign Out", command=home_window.destroy)
    sign_out_button.pack(pady=30)

def show_programmable_parameters(parent_window, username):
    params = get_programmable_parameters(username)  # Load current parameters for the user
    param_window = tk.Toplevel(parent_window)
    param_window.title("Pacemaker Parameters")
    param_window.geometry("400x500")

    # Display current parameters
    param_label = tk.Label(param_window, text=f"Current Parameters for {username}:")
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
        save_programmable_parameters(username, new_params)
        messagebox.showinfo("Success", "Parameters saved successfully!")
        param_window.destroy()  # Close window after saving

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

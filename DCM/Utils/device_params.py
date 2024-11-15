import json
from datetime import datetime
import tkinter as tk

def save_programmable_parameters(username, parameters):
    with open(f"data/{username}_parameters.json", "w") as f:
        json.dump(parameters, f)

def apply_clock(date_str, time_str, clock_window):
    try:
        new_date_time = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        #print(f"Device date and time set to: {new_date_time}")
        tk.Label(clock_window, text="Clock updated successfully!", fg="green").pack(pady=5)
    except ValueError:
        tk.Label(clock_window, text="Invalid date or time format.", fg="red").pack(pady=5)


def change_operation_mode(home_window, user):
    mode_window = tk.Toplevel(home_window)
    mode_window.title("Operation Mode")
    mode_window.geometry("300x200")

    user.get_opperation_mode()


def change_operation_mode(home_window):
    mode_window = tk.Toplevel(home_window)
    mode_window.title("Change Operation Mode")
    mode_window.geometry("400x300")

    def set_mode(mode_name):
        tk.messagebox.showinfo("Mode Change", f"Device is now in {mode_name} mode")
        mode_window.destroy()

    VOO_button = tk.Button(mode_window, text="VOO", command=lambda: set_mode("VOO"))
    VOO_button.pack(pady=20)

    VVI_button = tk.Button(mode_window, text="VVI", command=lambda: set_mode("VVI"))
    VVI_button.pack(pady=20)

    AOO_button = tk.Button(mode_window, text="AOO", command=lambda: set_mode("AOO"))
    AOO_button.pack(pady=20)

    AII_button = tk.Button(mode_window, text="AAI", command=lambda: set_mode("AAI"))
    AII_button.pack(pady=20)
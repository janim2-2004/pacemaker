import json
import tkinter as tk

MAX_USERS = 10

#shell type for future implementation of egram charts
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


def authenticate_user(username, password):
    with open("data/users.json", "r") as f:
        users = json.load(f)
    return users.get(username) == password

def register_new_user(root):
    # Load existing users
    with open("data/users.json", "r") as f:
        users = json.load(f)

    # Check if user limit is reached
    if len(users) >= MAX_USERS:
        tk.Label(root, text="Max users reached. Cannot register new users.", fg="red").pack()
        return

    # Create a new window for user registration
    register_window = tk.Toplevel(root)
    register_window.title("Register New User")
    register_window.geometry("300x200")

    tk.Label(register_window, text="Enter New Username:").pack(pady=5)
    username_entry = tk.Entry(register_window)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Enter New Password:").pack(pady=5)
    password_entry = tk.Entry(register_window, show="*")
    password_entry.pack(pady=5)

    def save_new_user():
        username = username_entry.get()
        password = password_entry.get()

        if username in users:
            tk.Label(register_window, text="Username already exists.", fg="red").pack()
        else:
            # Register the new user with default parameters
            users[username] = password
            with open("data/users.json", "w") as f:
                json.dump(users, f)
            tk.Label(register_window, text="User registered successfully!", fg="green").pack()
            register_window.after(1500, register_window.destroy)

    tk.Button(register_window, text="Register", command=save_new_user).pack(pady=10)

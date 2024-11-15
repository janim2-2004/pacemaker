########################################################################################################################
#
#                              User class for backend processing of user data and credentials
#
########################################################################################################################

import json
import tkinter as tk
from tkinter import messagebox
from Utils.login import UserManager

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

DEFAULT_PARAMETERS = {
    "Lower Rate Limit": "60 BPM",
    "Upper Rate Limit": "120 BPM",
    "Atrial Amplitude": "3.5V",
    "Atrial Pulse Width": "10 ms",
    "Ventricle Amplitude": "3.5V",
    "Ventricle Pulse Width": "10 ms",
    "VRP": "250 ms",
    "ARP": "250 ms"
}

def get_users():
    try:
        with open('Data/users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Filepath Error")
        return 0
    
class User:
    def __init__(self, username):
        users = get_users()
        for user in users:
            if user['username'] == username :
                self.user = user

    def get_user(self):
        if(self.user):
            return self.user
        else:
            messagebox.showerror("Error", "User not initiated")
            return 0
        
    def get_role(self):
        return self.user['role']

    def get_username(self):
        return self.user['username']
    
    def get_user_parameters(self):
        try:
            with open(f"data/{self.user['username']}_parameters.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            messagebox.showwarning("Warning", "Patient parameters not initiated, using defualt parameters")
            return DEFAULT_PARAMETERS
        
    def save_user_parameters(self, parameters):
        with open(f"data/{self.user['username']}_parameters.json", "w") as f:
            json.dump(parameters, f)

    def authenticate_admin(self):
        return (self.user['role'] == "Practitioner")
    

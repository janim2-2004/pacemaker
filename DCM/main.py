import tkinter as tk
from tkinter import ttk
from Utils.login import Login, Register
from Utils.device import Mode

class MainWindow:
    # Pacemaker DCM main menu class

    def __init__(self):
        # Initialization of main menu

        self.app = tk.Tk()
        self.app.title("Pacemaker DCM Main Menu")
        self.app.geometry("300x200")
        self.label = tk.Label(self.app, text="Welcome to the Pacemaker UI")
        self.label.place(x=65, y=40)
        self.loginButton = tk.Button(self.app, text="Login", pady=5, padx=20, command=self.login)
        self.loginButton.place(x=107, y=60)
        self.regButton = tk.Button(self.app, text="Register", pady=5, padx=20, command=self.register)
        self.regButton.place(x=100, y=100)
        
    
    def login(self):
        # Trigger login window from the Login class
        # Note: loginWindow becomes a property of the MainWindow object, required in other methods to check for successful login

        self.app.deiconify()
        self.loginWindow = Login()
        self.loginWindow.run()
        
    
    def register(self):
        # Method that triggers register window from the Register class
        # Note: lack of self on regTk because it isn't required to interact with anything else in the MainWindow class

        self.app.deiconify()
        regTk = Register()
        regTk.run()

    def checkUserLogin(self):
        # Method constantly checks for a successful user log in before opening interface window
        try:
            if not self.loginWindow.loggedIn():
                self.app.after(1000, self.checkUserLogin)
            else:
                menuSelect = Mode(self.loginWindow.currentUser())
                menuSelect.run()
        except AttributeError:
            self.app.after(1000, self.checkUserLogin)

    def run(self):
        self.app.after(3000, self.checkUserLogin)
        self.app.mainloop()

app = MainWindow()
app.run()
import tkinter as tk
from tkinter import StringVar, messagebox
from tkinter.constants import FLAT
from Utils.database import Database

db = Database()
db.createtable()

class Login:
    # Login class that utilizes the sqlite3 database created by the Database class to validate user credentials

    def __init__(self):
        # Initialization of the login window

        self.loginWin = tk.Toplevel()
        self.loginWin.title("Pacemaker DCM Login")
        self.loginWin.geometry("300x150")
        self.loginWin.grid_columnconfigure((0,1), weight=1)
        self.label = tk.Label(self.loginWin, text="Please enter your username and password")
        self.label.grid(row=1, column=0, columnspan=2, pady=5)

        self.label1 = tk.Label(self.loginWin, text="Username:")
        self.label2 = tk.Label(self.loginWin, text="Password:")

        self.userStr = StringVar() 
        self.passStr = StringVar()

        self.userIn = tk.Entry(self.loginWin, relief=FLAT, textvariable=self.userStr)
        self.label1.grid(row=2, column=0, sticky="e")
        self.userIn.grid(row=2, column=1, sticky="w", pady=5)
        self.passIn = tk.Entry(self.loginWin, show="*", relief=FLAT, textvariable=self.passStr)
        self.label2.grid(row=3, column=0, sticky="e")
        self.passIn.grid(row=3, column=1, sticky="w", pady=5)

        self.loginButton = tk.Button(self.loginWin, text="Login", pady=10, padx=20)
        self.loginButton.place(x=110, y=100)
        self.loginButton.bind("<Button-1>", self.__validate) 
        self.loginWin.bind("<Return>", self.__validate)

        self.loginSuccess = False

    def __validate(self, event):
        # User validation method - cross-references the existing users in the database to the users' input

        username = self.userStr.get()
        password = self.passStr.get()

        user = (username, )
        userData = (username, password, )
        try:
            if(db.authenticate(user, userData)):
                messagebox.showinfo("Success", "You are now logged in")
                self.loginWin.destroy()
                self.loginSuccess = True
            else:
                messagebox.showinfo("Failed", "Username or password is invalid")
                self.loginWin.destroy()
        except IndexError:
            messagebox.showinfo("Failed", "Username or password is invalid")
            self.loginWin.focus()
    
    def loggedIn(self):
        return self.loginSuccess
    
    def currentUser(self):
        return self.userStr.get()

    def run(self):
        self.loginWin.mainloop()

class Register:
    # Register class that utilizes the database created by the Database class to add a new user

    def __init__(self):
        # Initialization of user registration window

        self.regWin = tk.Toplevel()
        self.regWin.title("Pacemaker DCM Registration")
        self.regWin.geometry("300x150")
        self.regWin.grid_columnconfigure((0,1), weight=1)
        self.label = tk.Label(self.regWin, text="Please enter your desired username and password")
        self.label.grid(row=0, column=0, columnspan=2, pady=5)

        self.label1 = tk.Label(self.regWin, text="Username:")
        self.label2 = tk.Label(self.regWin, text="Password:")

        self.userStr = StringVar() # Var used to store user input from tk.Entry field
        self.passStr = StringVar() # 

        self.userIn = tk.Entry(self.regWin, relief=FLAT, textvariable=self.userStr) # 
        self.label1.grid(row=2, column=0, sticky="e")
        self.userIn.grid(row=2, column=1, sticky="w", pady=5)
        self.passIn = tk.Entry(self.regWin, show="*", relief=FLAT, textvariable=self.passStr)
        self.label2.grid(row=3, column=0, sticky="e")
        self.passIn.grid(row=3, column=1, sticky="w", pady=5)

        self.regButton = tk.Button(self.regWin, text="Register", pady=10, padx=20)
        self.regButton.place(x=110, y=100)
        self.regButton.bind("<Button-1>", self.__adduser) # Pressing left-click on register button triggers adduser method
        self.regWin.bind("<Return>", self.__adduser) # Pressing enter triggers adduser method

    def __adduser(self, event):
        # Retrieves user input and references the database
        # Adds user credentials to database if username does not exist already and opens messagebox stating success
        # Fails to add user credentials to database if username already exists and opens messagebox stating failure

        username = self.userStr.get()
        password = self.passStr.get()

        user = (username, )
        result = db.searchusers(user)

        if (result != 0):
            userData = (username, password)
            if (db.insertuser(userData)):
                messagebox.showinfo("Success", "User has been registered")
                self.regWin.destroy()
            else:
                messagebox.showinfo("Failed", "User limited reached - 10 users are already registered")
                self.regWin.destroy()
        else:
            messagebox.showinfo("Failed", "Username taken")
            self.regWin.focus()

    def run(self):
        self.regWin.mainloop()
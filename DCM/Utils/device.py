import tkinter as tk
from tkinter import IntVar, ttk, StringVar, DoubleVar, messagebox, TclError
from tkinter.constants import BOTH, CENTER
from Utils.database import Database
from Utils.coms import COM
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from random import randint

db = Database()
ser = COM()

class Mode:
    # Mode class containing the different pacemaker modes separated into ttk.Notebook tabs

    def __init__(self, user):
        # Initialization of modeSelect window as a Notebook to separate pacemaker mode UIs into tabs

        self.modeWin = tk.Toplevel()
        self.modeWin.title("Mode Selection")
        self.modeWin.geometry("1280x760")


        self.tabControl = ttk.Notebook(self.modeWin)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        self.tab5 = ttk.Frame(self.tabControl)
        self.tab6 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text="\n"+f'{"AOO":^20s}'+"\n")
        self.tabControl.add(self.tab2, text="\n"+f'{"VOO":^20s}'+"\n")
        self.tabControl.add(self.tab3, text="\n"+f'{"AAI":^22s}'+"\n")
        self.tabControl.add(self.tab4, text="\n"+f'{"VVI":^22s}'+"\n")
        self.tabControl.add(self.tab5, text="\n"+f'{"COM Settings":^22s}'+"\n")
        self.tabControl.add(self.tab6, text="\n"+f'{"EGRAM":^22s}'+"\n")
        self.tabControl.pack(expand=1, fill=BOTH)
        
        # Initialize list of inputs to be passed through to pacemaker
        # Note: params = ((params),) hence list comprehension -> double for loop to extract parameter values
        username = (user,)
        params = db.searchparam(username)
        self.inputValues = [item for i in params for item in i]
        self.inputValues.pop(0) # Remove first item in list because not a valid parameter, just the rowid from database

        # Pacemaker Parameter Initialization
        # [mode, LRL, URL, PVARP, AVdelay, reactTime, resFactor, actThresh, recTime, MSR, A_Amp, A_pw, ARP, aThres, V_Amp, V_pw, VRP, vThres]

        self.lowerRateLimit = IntVar()
        IntVar.set(self.lowerRateLimit, self.inputValues[1])
        self.upperRateLimit = IntVar()
        IntVar.set(self.upperRateLimit, self.inputValues[2])
        self.pvarp = IntVar()
        IntVar.set(self.pvarp, self.inputValues[3])
        self.avDelay = IntVar()
        IntVar.set(self.avDelay, self.inputValues[4])
        self.reactTime = IntVar()
        IntVar.set(self.reactTime, self.inputValues[5])
        self.resFactor = IntVar()
        IntVar.set(self.resFactor, self.inputValues[6])
        self.actThres = DoubleVar()
        DoubleVar.set(self.actThres, self.inputValues[7])
        self.recTime = IntVar()
        IntVar.set(self.recTime, self.inputValues[8])
        self.msr = IntVar()
        IntVar.set(self.msr, self.inputValues[9])
        
        self.atrialAmp = DoubleVar()
        DoubleVar.set(self.atrialAmp, self.inputValues[10])
        self.atrialPulseWidth = DoubleVar()
        IntVar.set(self.atrialPulseWidth, self.inputValues[11])
        self.arp = IntVar()
        IntVar.set(self.arp, self.inputValues[12])
        self.atrialThres = DoubleVar()
        DoubleVar.set(self.atrialThres, self.inputValues[13])

        self.ventriAmp = DoubleVar()
        DoubleVar.set(self.ventriAmp, self.inputValues[14])
        self.ventriPulseWidth = DoubleVar()
        IntVar.set(self.ventriPulseWidth, self.inputValues[15])
        self.vrp = IntVar()
        IntVar.set(self.vrp, self.inputValues[16])
        self.ventriThres = DoubleVar()
        DoubleVar.set(self.ventriThres, self.inputValues[17])
        

        self.tabControl.select(self.inputValues[0]) # Default view to saved active mode

        # Exists solely for UI purposes, nothing to do with passing of parameters
        self.actThresTextValues = {1.1:"V-Low", 1.25:"Low", 1.75:"Med-Low", 2.0:"Med", 2.25:"Med-High", 2.5:"High", 2.8:"V-High"}
        
        self.TimeElapsed = 0
        self.TimeElapsed2 = 0
        self.solve = None
        self.atrialEgram = Figure(figsize=(5,5), dpi=100)
        self.ventriEgram = Figure(figsize=(5,5), dpi=100)
        self.a = self.atrialEgram.add_subplot(111)
        self.b = self.ventriEgram.add_subplot(111)
        self.xvals = []
        self.xvals2 = []
        self.atrvals = []
        self.vtrvals = []

        # Binding of tab change event to tabSelection method and settings confirmation
        self.tabControl.bind("<<NotebookTabChanged>>", self.__tabSelection)

        print(self.inputValues)

    def __tabSelection(self, event):
        # Retrieves current selected tab and runs it through a pseudo switch-case statement
        # using a dictionary
        # Returns a corresponding method to the current tab selection

        tabs = {0:"aooInterface", 1:"vooInterface", 2:"aaiInterface", 3:"vviInterface", 4:"commSettings", 5:"egram"}
        currentTab = self.tabControl.index("current")
        method=getattr(self, tabs.get(currentTab))
        
        # Confirm settings on tabSwitch
        try:
            self.__aooConfigConfirm()
            self.__vooConfigConfirm()
            self.__aaiConfigConfirm()
            self.__vviConfigConfirm()
            self.__commSettingsCleanup()
            self.__egramCleanup()
        except AttributeError:
            pass
        
        if (currentTab < 5):
            self.__updateValues() # To update active mode if tab is switched
        return method()

    def aooInterface(self):
        # AOO Interface Initialization

        try:
            self.settingsButton1.destroy()
        except AttributeError:
            pass

        self.tab1.grid_columnconfigure(4, weight=1)
        self.tab1.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.settingsButton1 = tk.Button(self.tab1, text="Configure Settings", bg="white", command=self.__aooInterfaceConfig)
        self.settingsButton1.grid(column=5, row=10, sticky="w", padx=5, pady=5)
        
        lowerRateLabel = ttk.Label(self.tab1, text="Lower Rate Limit:").grid(column=1, row=1, padx=20, pady=20, sticky="e")
        lowerRateValue = ttk.Label(self.tab1, text=self.lowerRateLimit.get()).grid(column=2, row=1, padx=20, pady=20)
        lowerRateUnit = ttk.Label(self.tab1, text="ppm").grid(column=3, row=1, padx=20, pady=20, sticky="w")

        upperRateLabel = ttk.Label(self.tab1, text="Upper Rate Limit:").grid(column=1, row=2, padx=20, pady=20, sticky="e")
        upperRateValue = ttk.Label(self.tab1, text=self.upperRateLimit.get()).grid(column=2, row=2, padx=20, pady=20)
        upperRateUnit = ttk.Label(self.tab1, text="ppm").grid(column=3, row=2, padx=20, pady=20, sticky="w")

        atrialAmpLabel = ttk.Label(self.tab1, text="Atrial Amplitude:").grid(column=1, row=3, padx=20, pady=20, sticky="e")
        atrialAmpValue = ttk.Label(self.tab1, text=self.atrialAmp.get()).grid(column=2, row=3, padx=20, pady=20)
        atrialAmpUnit = ttk.Label(self.tab1, text="V").grid(column=3, row=3, padx=20, pady=20, sticky="w")

        atrialPulseLabel = ttk.Label(self.tab1, text="Atrial Pulse Width:").grid(column=1, row=4, padx=20, pady=20, sticky="e")
        atrialPulseValue = ttk.Label(self.tab1, text=self.atrialPulseWidth.get()).grid(column=2, row=4, padx=20, pady=20)
        atrialPulseUnit = ttk.Label(self.tab1, text="ms").grid(column=3, row=4, padx=20, pady=20, sticky="w")

        # pvarpLabel = ttk.Label(self.tab1, text="PVARP:").grid(column=1, row=5, padx=20, pady=20, sticky="e")
        # pvarpValue = ttk.Label(self.tab1, text=self.pvarp.get()).grid(column=2, row=5, padx=20, pady=20)
        # pvarpUnit = ttk.Label(self.tab1, text="ms").grid(column=3, row=5, padx=20, pady=20, sticky="w")

        msrLabel = ttk.Label(self.tab1, text="Max. Sensor Rate:").grid(column=1, row=6, padx=20, pady=20, sticky="e")
        msrValue = ttk.Label(self.tab1, text=self.msr.get()).grid(column=2, row=6, padx=20, pady=20)
        msrUnit = ttk.Label(self.tab1, text="ppm").grid(column=3, row=6, padx=20, pady=20, sticky="w")

        actThresLabel = ttk.Label(self.tab1, text="Activity Threshold:").grid(column=1, row=7, padx=20, pady=20, sticky="e")
        actThresValue = ttk.Label(self.tab1, text=self.actThresTextValues[self.actThres.get()]).grid(column=2, row=7, padx=20, pady=20)

        reactTimeLabel = ttk.Label(self.tab1, text="Reaction Time:").grid(column=1, row=8, padx=20, pady=20, sticky="e")
        reactTimeValue = ttk.Label(self.tab1, text=self.reactTime.get()).grid(column=2, row=8, padx=20, pady=20)
        reactTimeUnit = ttk.Label(self.tab1, text="sec").grid(column=3, row=8, padx=20, pady=20, sticky="w")

        resFactorLabel = ttk.Label(self.tab1, text="Response Factor:").grid(column=1, row=9, padx=20, pady=20, sticky="e")
        resFactorValue = ttk.Label(self.tab1, text=self.resFactor.get()).grid(column=2, row=9, padx=20, pady=20)

        recTimeLabel = ttk.Label(self.tab1, text="Recovery Time:").grid(column=1, row=10, padx=20, pady=20, sticky="e")
        recTimeValue = ttk.Label(self.tab1, text=self.recTime.get()).grid(column=2, row=10, padx=20, pady=20)
        recTimeUnit = ttk.Label(self.tab1, text="min").grid(column=3, row=10, padx=20, pady=20, sticky="w")

    def __aooInterfaceConfig(self):
        # Config menu to edit parameters for the AOO Pacemaker mode
        
        self.settingsButton1.destroy()
        reg = self.tab1.register(self.validateInput)

        self.lowerRateInput = ttk.Entry(self.tab1, textvariable=self.lowerRateLimit, justify=CENTER)
        self.lowerRateInput.grid(column=2, row=1, padx=20, pady=20)
        self.lowerRateInput.config(validate="key", validatecommand=(reg, "%P"))

        self.upperRateInput = ttk.Entry(self.tab1, textvariable=self.upperRateLimit, justify=CENTER)
        self.upperRateInput.grid(column=2, row=2, padx=20, pady=20)
        self.upperRateInput.config(validate="key", validatecommand=(reg, "%P"))

        self.atrialAmpInput = ttk.Entry(self.tab1, textvariable=self.atrialAmp, justify=CENTER)
        self.atrialAmpInput.grid(column=2, row=3, padx=20, pady=20)
        self.atrialAmpInput.config(validate="key", validatecommand=(reg, "%P"))

        self.atrialPulseInput = ttk.Entry(self.tab1, textvariable=self.atrialPulseWidth, justify=CENTER)
        self.atrialPulseInput.grid(column=2, row=4, padx=20, pady=20)
        self.atrialPulseInput.config(validate="key", validatecommand=(reg, "%P"))

        # self.pvarpInput = ttk.Entry(self.tab1, textvariable=self.pvarp, justify=CENTER)
        # self.pvarpInput.grid(column=2, row=5, padx=20, pady=20)
        # self.pvarpInput.config(validate="key", validatecommand=(reg, "%P"))

        self.msrInput = ttk.Entry(self.tab1, textvariable=self.msr, justify=CENTER)
        self.msrInput.grid(column=2, row=6, padx=20, pady=20)
        self.msrInput.config(validate="key", validatecommand=(reg, "%P"))
        
        self.actThresInput = ttk.Combobox(self.tab1, values=list(self.actThresTextValues.values()))
        self.actThresInput.grid(column=2, row=7, padx=20, pady=20)
        self.actThresInput.set(self.actThresTextValues[self.actThres.get()])

        self.reactTimeInput = ttk.Combobox(self.tab1, values=[10,20,30,40,50])
        self.reactTimeInput.grid(column=2, row=8, padx=20, pady=20)
        self.reactTimeInput.set(self.reactTime.get())

        self.resFactorInput = ttk.Combobox(self.tab1, values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.resFactorInput.grid(column=2, row=9, padx=20, pady=20)
        self.resFactorInput.set(self.resFactor.get())

        self.recTimeInput = ttk.Combobox(self.tab1, values=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.recTimeInput.grid(column=2, row=10, padx=20, pady=20)
        self.recTimeInput.set(self.recTime.get())

        self.confirmButton1 = tk.Button(self.tab1, text="Confirm Changes", bg="white", command=self.__aooConfigConfirm)
        self.confirmButton1.grid(column=5, row=11, sticky="w", padx=10, pady=10)

    def __aooConfigConfirm(self):
        # AOO config confirm button -> Enforces value limits, cleans up ui to prevent memory leaking, and updates values

        invalid = False

        if (self.lowerRateLimit.get() < 30) or (self.lowerRateLimit.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Lower Rate Limit must be between 30-175")
        if (self.upperRateLimit.get() < 50) or (self.upperRateLimit.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Upper Rate Limit must be between 50-175")
        if (self.atrialAmp.get() < 0) or (self.atrialAmp.get() > 5.0):
            invalid = True
            messagebox.showerror("Value Error", "Atrial Amplitude must be between 0.1 and 5.0 or 0 for off")
        if (self.atrialPulseWidth.get() < 1) or (self.atrialPulseWidth.get() > 30):
            invalid = True
            messagebox.showerror("Value Error", "Atrial Pulse Width must be between 1 and 30")
        if (self.msr.get() < 50) or (self.msr.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Maxmium Sensor Rate must be between 50-175")
        if invalid:
            # Do nothing on invalid input to force user to correct error
            pass
        else:
            try:
                IntVar.set(self.actThres, list(self.actThresTextValues.keys())[self.actThresInput.current()])
                IntVar.set(self.reactTime, self.reactTimeInput.get())
                IntVar.set(self.resFactor, self.resFactorInput.get())
                IntVar.set(self.recTime, self.recTimeInput.get())
                for widget in self.tab1.winfo_children():
                    widget.destroy()
            except TclError:
                pass
            self.tab1.update()
            self.__updateValues()
            self.aooInterface()

    def vooInterface(self):
        # VOO Interface Initialization

        try:
            self.settingsButton2.destroy()
        except AttributeError:
            pass

        self.tab2.grid_columnconfigure(4, weight=1)
        self.tab2.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
        self.settingsButton2 = tk.Button(self.tab2, text="Configure Settings", bg="white", command=self.__vooInterfaceConfig)
        self.settingsButton2.grid(column=5, row=10, sticky="w", padx=5, pady=5)
        
        lowerRateLabel = ttk.Label(self.tab2, text="Lower Rate Limit:").grid(column=1, row=1, padx=20, pady=20, sticky="e")
        lowerRateValue = ttk.Label(self.tab2, text=self.lowerRateLimit.get()).grid(column=2, row=1, padx=20, pady=20)
        lowerRateUnit = ttk.Label(self.tab2, text="ppm").grid(column=3, row=1, padx=20, pady=20, sticky="w")

        upperRateLabel = ttk.Label(self.tab2, text="Upper Rate Limit:").grid(column=1, row=2, padx=20, pady=20, sticky="e")
        upperRateValue = ttk.Label(self.tab2, text=self.upperRateLimit.get()).grid(column=2, row=2, padx=20, pady=20)
        upperRateUnit = ttk.Label(self.tab2, text="ppm").grid(column=3, row=2, padx=20, pady=20, sticky="w")

        ventriAmpLabel = ttk.Label(self.tab2, text="Ventri. Amplitude:").grid(column=1, row=3, padx=20, pady=20, sticky="e")
        ventriAmpValue = ttk.Label(self.tab2, text=self.ventriAmp.get()).grid(column=2, row=3, padx=20, pady=20)
        ventriAmpUnit = ttk.Label(self.tab2, text="V").grid(column=3, row=3, padx=20, pady=20, sticky="w")

        ventriPulseLabel = ttk.Label(self.tab2, text="Ventri. Pulse Width:").grid(column=1, row=4, padx=20, pady=20, sticky="e")
        ventriPulseValue = ttk.Label(self.tab2, text=self.ventriPulseWidth.get()).grid(column=2, row=4, padx=20, pady=20)
        ventriPulseUnit = ttk.Label(self.tab2, text="ms").grid(column=3, row=4, padx=20, pady=20, sticky="w")

        # pvarpLabel = ttk.Label(self.tab2, text="PVARP:").grid(column=1, row=5, padx=20, pady=20, sticky="e")
        # pvarpValue = ttk.Label(self.tab2, text=self.pvarp.get()).grid(column=2, row=5, padx=20, pady=20)
        # pvarpUnit = ttk.Label(self.tab2, text="ms").grid(column=3, row=5, padx=20, pady=20, sticky="w")

        msrLabel = ttk.Label(self.tab2, text="Max. Sensor Rate:").grid(column=1, row=6, padx=20, pady=20, sticky="e")
        msrValue = ttk.Label(self.tab2, text=self.msr.get()).grid(column=2, row=6, padx=20, pady=20)
        msrUnit = ttk.Label(self.tab2, text="ppm").grid(column=3, row=6, padx=20, pady=20, sticky="w")

        actThresLabel = ttk.Label(self.tab2, text="Activity Threshold:").grid(column=1, row=7, padx=20, pady=20, sticky="e")
        actThresValue = ttk.Label(self.tab2, text=self.actThresTextValues[self.actThres.get()]).grid(column=2, row=7, padx=20, pady=20)

        reactTimeLabel = ttk.Label(self.tab2, text="Reaction Time:").grid(column=1, row=8, padx=20, pady=20, sticky="e")
        reactTimeValue = ttk.Label(self.tab2, text=self.reactTime.get()).grid(column=2, row=8, padx=20, pady=20)
        reactTimeUnit = ttk.Label(self.tab2, text="sec").grid(column=3, row=8, padx=20, pady=20, sticky="w")

        resFactorLabel = ttk.Label(self.tab2, text="Response Factor:").grid(column=1, row=9, padx=20, pady=20, sticky="e")
        resFactorValue = ttk.Label(self.tab2, text=self.resFactor.get()).grid(column=2, row=9, padx=20, pady=20)

        recTimeLabel = ttk.Label(self.tab2, text="Recovery Time:").grid(column=1, row=10, padx=20, pady=20, sticky="e")
        recTimeValue = ttk.Label(self.tab2, text=self.recTime.get()).grid(column=2, row=10, padx=20, pady=20)
        recTimeUnit = ttk.Label(self.tab2, text="min").grid(column=3, row=10, padx=20, pady=20, sticky="w")

    def __vooInterfaceConfig(self):
        # Config menu to edit parameters for the VOO Pacemaker mode
        
        self.settingsButton2.destroy()
        reg = self.tab2.register(self.validateInput)

        self.lowerRateInput2 = ttk.Entry(self.tab2, textvariable=self.lowerRateLimit, justify=CENTER)
        self.lowerRateInput2.grid(column=2, row=1, padx=20, pady=20)
        self.lowerRateInput2.config(validate="key", validatecommand="%P")

        self.upperRateInput2 = ttk.Entry(self.tab2, textvariable=self.upperRateLimit, justify=CENTER)
        self.upperRateInput2.grid(column=2, row=2, padx=20, pady=20)
        self.upperRateInput2.config(validate="key", validatecommand="%P")

        self.ventriAmpInput2 = ttk.Entry(self.tab2, textvariable=self.ventriAmp, justify=CENTER)
        self.ventriAmpInput2.grid(column=2, row=3, padx=20, pady=20)
        self.ventriAmpInput2.config(validate="key", validatecommand="%P")

        self.ventriPulseInput2 = ttk.Entry(self.tab2, textvariable=self.ventriPulseWidth, justify=CENTER)
        self.ventriPulseInput2.grid(column=2, row=4, padx=20, pady=20)
        self.ventriPulseInput2.config(validate="key", validatecommand="%P")

        # self.pvarpInput2 = ttk.Entry(self.tab2, textvariable=self.pvarp, justify=CENTER)
        # self.pvarpInput2.grid(column=2, row=5, padx=20, pady=20)
        # self.pvarpInput2.config(validate="key", validatecommand=(reg, "%P"))

        self.msrInput2 = ttk.Entry(self.tab2, textvariable=self.msr, justify=CENTER)
        self.msrInput2.grid(column=2, row=6, padx=20, pady=20)
        self.msrInput2.config(validate="key", validatecommand=(reg, "%P"))
        
        self.actThresInput2 = ttk.Combobox(self.tab2, values=list(self.actThresTextValues.values()))
        self.actThresInput2.grid(column=2, row=7, padx=20, pady=20)
        self.actThresInput2.set(self.actThresTextValues[self.actThres.get()])

        self.reactTimeInput2 = ttk.Combobox(self.tab2, values=[10,20,30,40,50])
        self.reactTimeInput2.grid(column=2, row=8, padx=20, pady=20)
        self.reactTimeInput2.set(self.reactTime.get())

        self.resFactorInput2 = ttk.Combobox(self.tab2, values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.resFactorInput2.grid(column=2, row=9, padx=20, pady=20)
        self.resFactorInput2.set(self.resFactor.get())

        self.recTimeInput2 = ttk.Combobox(self.tab2, values=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.recTimeInput2.grid(column=2, row=10, padx=20, pady=20)
        self.recTimeInput2.set(self.recTime.get())

        self.confirmButton2 = tk.Button(self.tab2, text="Confirm Changes", bg="white", command=self.__vooConfigConfirm)
        self.confirmButton2.grid(column=5, row=10, sticky="w", padx=5, pady=5)

    def __vooConfigConfirm(self):
        # VOO config confirm button -> Enforces value limits, cleans up ui to prevent memory leaking, and updates values

        invalid = False

        if (self.lowerRateLimit.get() < 30) or (self.lowerRateLimit.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Lower Rate Limit must be between 30-175")
        if (self.upperRateLimit.get() < 50) or (self.upperRateLimit.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Upper Rate Limit must be between 50-175")
        if (self.ventriAmp.get() < 0) or (self.ventriAmp.get() > 5.0):
            invalid = True
            messagebox.showerror("Value Error", "Ventricular Ampltiude must be between 0.1 and 5.0 or 0 for off")
        if (self.ventriPulseWidth.get() < 1) or (self.ventriPulseWidth.get() > 30):
            invalid = True
            messagebox.showerror("Value Error", "Ventricular Pulse Width must be between 1 and 30")
        if (self.msr.get() < 50) or (self.msr.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Maxmium Sensor Rate must be between 50-175")
        if invalid:
            # Do nothing on invalid input to force user to correct error
            pass
        else:
            try:
                IntVar.set(self.actThres, list(self.actThresTextValues.keys())[self.actThresInput2.current()])
                IntVar.set(self.reactTime, self.reactTimeInput2.get())
                IntVar.set(self.resFactor, self.resFactorInput2.get())
                IntVar.set(self.recTime, self.recTimeInput2.get())
                for widget in self.tab2.winfo_children():
                    widget.destroy()
            except TclError:
                pass
            self.tab2.update()
            self.__updateValues()
            self.vooInterface()

    def aaiInterface(self):
        # AAI Interface Initialization
        
        try:
            self.settingsButton3.destroy()
        except AttributeError:
            pass

        self.tab3.grid_columnconfigure(4, weight=1)
        self.tab3.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), weight=1)
        self.settingsButton3 = tk.Button(self.tab3, text="Configure Settings", bg="white", command=self.__aaiInterfaceConfig)
        self.settingsButton3.grid(column=5, row=15, sticky="w", padx=5, pady=5)
        
        lowerRateLabel = ttk.Label(self.tab3, text="Lower Rate Limit:").grid(column=1, row=1, padx=20, pady=10, sticky="e")
        lowerRateValue = ttk.Label(self.tab3, text=self.lowerRateLimit.get()).grid(column=2, row=1, padx=20, pady=10)
        lowerRateUnit = ttk.Label(self.tab3, text="ppm").grid(column=3, row=1, padx=20, pady=10, sticky="w")

        upperRateLabel = ttk.Label(self.tab3, text="Upper Rate Limit:").grid(column=1, row=2, padx=20, pady=10, sticky="e")
        upperRateValue = ttk.Label(self.tab3, text=self.upperRateLimit.get()).grid(column=2, row=2, padx=20, pady=10)
        upperRateUnit = ttk.Label(self.tab3, text="ppm").grid(column=3, row=2, padx=20, pady=10, sticky="w")

        atrialAmpLabel = ttk.Label(self.tab3, text="Atrial Amplitude:").grid(column=1, row=3, padx=20, pady=10, sticky="e")
        atrialAmpValue = ttk.Label(self.tab3, text=self.atrialAmp.get()).grid(column=2, row=3, padx=20, pady=10)
        atrialAmpUnit = ttk.Label(self.tab3, text="V").grid(column=3, row=3, padx=20, pady=10, sticky="w")

        atrialPulseLabel = ttk.Label(self.tab3, text="Atrial Pulse Width:").grid(column=1, row=4, padx=20, pady=10, sticky="e")
        atrialPulseValue = ttk.Label(self.tab3, text=self.atrialPulseWidth.get()).grid(column=2, row=4, padx=20, pady=10)
        atrialPulseUnit = ttk.Label(self.tab3, text="ms").grid(column=3, row=4, padx=20, pady=10, sticky="w")

        atrialSensLabel = ttk.Label(self.tab3, text="Atrial Sensitivity:").grid(column=1, row=5, padx=20, pady=10, sticky="e")
        atrialSensValue = ttk.Label(self.tab3, text=self.atrialThres.get()).grid(column=2, row=5, padx=20, pady=10)
        atrialSensUnit = ttk.Label(self.tab3, text="V").grid(column=3, row=5, padx=20, pady=10, sticky="w")

        arpLabel = ttk.Label(self.tab3, text="ARP:").grid(column=1, row=6, padx=20, pady=10, sticky="e")
        arpValue = ttk.Label(self.tab3, text=self.arp.get()).grid(column=2, row=6, padx=20, pady=10)
        arpUnit = ttk.Label(self.tab3, text="ms").grid(column=3, row=6, padx=20, pady=10, sticky="w")
        
        pvarpLabel = ttk.Label(self.tab3, text="PVARP:").grid(column=1, row=7, padx=20, pady=10, sticky="e")
        pvarpValue = ttk.Label(self.tab3, text=self.pvarp.get()).grid(column=2, row=7, padx=20, pady=10)
        pvarpUnit = ttk.Label(self.tab3, text="ms").grid(column=3, row=7, padx=20, pady=10, sticky="w")

        pvarpLabel = ttk.Label(self.tab1, text="PVARP:").grid(column=1, row=8, padx=20, pady=10, sticky="e")
        pvarpValue = ttk.Label(self.tab1, text=self.pvarp.get()).grid(column=2, row=5, padx=10, pady=20)
        pvarpUnit = ttk.Label(self.tab1, text="ms").grid(column=3, row=5, padx=20, pady=10, sticky="w")

        msrLabel = ttk.Label(self.tab3, text="Max. Sensor Rate:").grid(column=1, row=9, padx=20, pady=10, sticky="e")
        msrValue = ttk.Label(self.tab3, text=self.msr.get()).grid(column=2, row=9, padx=20, pady=10)
        msrUnit = ttk.Label(self.tab3, text="ppm").grid(column=3, row=9, padx=20, pady=10, sticky="w")

        actThresLabel = ttk.Label(self.tab3, text="Activity Threshold:").grid(column=1, row=10, padx=20, pady=10, sticky="e")
        actThresValue = ttk.Label(self.tab3, text=self.actThresTextValues[self.actThres.get()]).grid(column=2, row=10, padx=20, pady=10)

        reactTimeLabel = ttk.Label(self.tab3, text="Reaction Time:").grid(column=1, row=11, padx=20, pady=10, sticky="e")
        reactTimeValue = ttk.Label(self.tab3, text=self.reactTime.get()).grid(column=2, row=11, padx=20, pady=10)
        reactTimeUnit = ttk.Label(self.tab3, text="sec").grid(column=3, row=11, padx=20, pady=10, sticky="w")

        resFactorLabel = ttk.Label(self.tab3, text="Response Factor:").grid(column=1, row=12, padx=20, pady=10, sticky="e")
        resFactorValue = ttk.Label(self.tab3, text=self.resFactor.get()).grid(column=2, row=12, padx=20, pady=10)

        recTimeLabel = ttk.Label(self.tab3, text="Recovery Time:").grid(column=1, row=13, padx=20, pady=10, sticky="e")
        recTimeValue = ttk.Label(self.tab3, text=self.recTime.get()).grid(column=2, row=13, padx=20, pady=10)
        recTimeUnit = ttk.Label(self.tab3, text="min").grid(column=3, row=15, padx=20, pady=10, sticky="w")
    
    def __aaiInterfaceConfig(self):
        # Config menu to edit parameters for the AAI Pacemaker mode

        self.settingsButton3.destroy()
        self.hysteresisValue.destroy()
        self.rateSmoothValue.destroy()
        reg = self.tab3.register(self.validateInput)

        self.lowerRateInput3 = ttk.Entry(self.tab3, textvariable=self.lowerRateLimit, justify=CENTER)
        self.lowerRateInput3.grid(column=2, row=1, padx=20, pady=10)
        self.lowerRateInput3.config(validate="key", validatecommand=(reg, "%P"))

        self.upperRateInput3 = ttk.Entry(self.tab3, textvariable=self.upperRateLimit, justify=CENTER)
        self.upperRateInput3.grid(column=2, row=2, padx=20, pady=10)
        self.upperRateInput3.config(validate="key", validatecommand=(reg, "%P"))

        self.atrialAmpInput3 = ttk.Entry(self.tab3, textvariable=self.atrialAmp, justify=CENTER)
        self.atrialAmpInput3.grid(column=2, row=3, padx=20, pady=10)
        self.atrialAmpInput3.config(validate="key", validatecommand=(reg, "%P"))

        self.atrialPulseInput3 = ttk.Entry(self.tab3, textvariable=self.atrialPulseWidth, justify=CENTER)
        self.atrialPulseInput3.grid(column=2, row=4, padx=20, pady=10)
        self.atrialPulseInput3.config(validate="key", validatecommand=(reg, "%P"))

        self.atrialSensInput3 = ttk.Entry(self.tab3, textvariable=self.atrialSens, justify=CENTER)
        self.atrialSensInput3.grid(column=2, row=5, padx=20, pady=10)
        self.atrialSensInput3.config(validate="key", validatecommand=(reg, "%P"))

        self.arpInput3 = ttk.Entry(self.tab3, textvariable=self.arp, justify=CENTER)
        self.arpInput3.grid(column=2, row=6, padx=20, pady=10)
        self.arpInput3.config(validate="key", validatecommand=(reg, "%P"))

        self.pvarpInput3 = ttk.Entry(self.tab3, textvariable=self.pvarp, justify=CENTER)
        self.pvarpInput3.grid(column=2, row=7, padx=20, pady=10)
        self.pvarpInput3.config(validate="key", validatecommand=(reg, "%P"))

        self.pvarpInput3 = ttk.Entry(self.tab3, textvariable=self.pvarp, justify=CENTER)
        self.pvarpInput3.grid(column=2, row=8, padx=20, pady=20)
        self.pvarpInput3.config(validate="key", validatecommand=(reg, "%P"))

        self.msrInput3 = ttk.Entry(self.tab3, textvariable=self.msr, justify=CENTER)
        self.msrInput3.grid(column=2, row=9, padx=20, pady=10)
        self.msrInput3.config(validate="key", validatecommand=(reg, "%P"))
        
        self.actThresInput3 = ttk.Combobox(self.tab3, values=list(self.actThresTextValues.values()))
        self.actThresInput3.grid(column=2, row=10, padx=20, pady=10)
        self.actThresInput3.set(self.actThresTextValues[self.actThres.get()])

        self.reactTimeInput3 = ttk.Combobox(self.tab3, values=[10,20,30,40,50])
        self.reactTimeInput3.grid(column=2, row=11, padx=20, pady=10)
        self.reactTimeInput3.set(self.reactTime.get())

        self.resFactorInput3 = ttk.Combobox(self.tab3, values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.resFactorInput3.grid(column=2, row=12, padx=20, pady=10)
        self.resFactorInput3.set(self.resFactor.get())

        self.recTimeInput3 = ttk.Combobox(self.tab3, values=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.recTimeInput3.grid(column=2, row=13, padx=20, pady=10)
        self.recTimeInput3.set(self.recTime.get())

        self.confirmButton3 = tk.Button(self.tab3, text="Confirm Changes", bg="white", command=self.__aaiConfigConfirm)
        self.confirmButton3.grid(column=5, row=14, sticky="w", padx=5, pady=5)

    def __aaiConfigConfirm(self):
        # AAI config confirm button -> Enforces value limits, cleans up ui to prevent memory leaking, and updates values
        
        invalid = False

        if (self.lowerRateLimit.get() < 30) or (self.lowerRateLimit.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Lower Rate Limit must be between 30-175")
        if (self.upperRateLimit.get() < 50) or (self.upperRateLimit.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Upper Rate Limit must be between 50-175")
        if (self.atrialAmp.get() < 0) or (self.atrialAmp.get() > 5.0):
            invalid = True
            messagebox.showerror("Value Error", "Atrial Amplitude must be between 0.1 and 5.0 or 0 for off")
        if (self.atrialPulseWidth.get() < 1) or (self.atrialPulseWidth.get() > 30):
            invalid = True
            messagebox.showerror("Value Error", "Atrial Pulse Width must be between 1 and 30")
        if (self.arp.get() < 150) or (self.arp.get() > 500):
            invalid = True
            messagebox.showerror("Value Error", "ARP must be between 150 and 500")
        if (self.atrialSens.get() < 0) or (self.atrialThres.get() > 5.0):
            invalid = True
            messagebox.showerror("Value Error", "Atrial Sensitivity must be between 0 and 5.0")
        if (self.msr.get() < 50) or (self.msr.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Maxmium Sensor Rate must be between 50-175")
        if invalid:
            # Do nothing on invalid input to force user to correct error
            pass
        else:
            try:
                IntVar.set(self.actThres, list(self.actThresTextValues.keys())[self.actThresInput3.current()])
                IntVar.set(self.reactTime, self.reactTimeInput3.get())
                IntVar.set(self.resFactor, self.resFactorInput3.get())
                IntVar.set(self.recTime, self.recTimeInput3.get())
                for widget in self.tab3.winfo_children():
                    widget.destroy()
            except TclError:
                pass
            self.tab3.update()
            self.__updateValues()
            self.aaiInterface()

    def vviInterface(self):
        # VVI Interface Initialization

        try:
            self.settingsButton4.destroy()
        except AttributeError:
            pass

        self.tab4.grid_columnconfigure(4, weight=1)
        self.tab4.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14), weight=1)
        self.settingsButton4 = tk.Button(self.tab4, text="Configure Settings", bg="white", command=self.__vviInterfaceConfig)
        self.settingsButton4.grid(column=5, row=14, sticky="w", padx=5, pady=5)
        
        lowerRateLabel = ttk.Label(self.tab4, text="Lower Rate Limit:").grid(column=1, row=1, padx=20, pady=10, sticky="e")
        lowerRateValue = ttk.Label(self.tab4, text=self.lowerRateLimit.get()).grid(column=2, row=1, padx=20, pady=10)
        lowerRateUnit = ttk.Label(self.tab4, text="ppm").grid(column=3, row=1, padx=20, pady=10, sticky="w")

        upperRateLabel = ttk.Label(self.tab4, text="Upper Rate Limit:").grid(column=1, row=2, padx=20, pady=10, sticky="e")
        upperRateValue = ttk.Label(self.tab4, text=self.upperRateLimit.get()).grid(column=2, row=2, padx=20, pady=10)
        upperRateUnit = ttk.Label(self.tab4, text="ppm").grid(column=3, row=2, padx=20, pady=10, sticky="w")

        ventriAmpLabel = ttk.Label(self.tab4, text="Ventri. Amplitude:").grid(column=1, row=3, padx=20, pady=10, sticky="e")
        ventriAmpValue = ttk.Label(self.tab4, text=self.ventriAmp.get()).grid(column=2, row=3, padx=20, pady=10)
        ventriAmpUnit = ttk.Label(self.tab4, text="V").grid(column=3, row=3, padx=20, pady=10, sticky="w")

        ventriPulseLabel = ttk.Label(self.tab4, text="Ventri. Pulse Width:").grid(column=1, row=4, padx=20, pady=10, sticky="e")
        ventriPulseValue = ttk.Label(self.tab4, text=self.ventriPulseWidth.get()).grid(column=2, row=4, padx=20, pady=10)
        ventriPulseUnit = ttk.Label(self.tab4, text="ms").grid(column=3, row=4, padx=20, pady=10, sticky="w")

        ventriSensLabel = ttk.Label(self.tab4, text="Ventri. Threshold:").grid(column=1, row=5, padx=20, pady=10, sticky="e")
        ventriSensValue = ttk.Label(self.tab4, text=self.ventriThres.get()).grid(column=2, row=5, padx=20, pady=10)
        ventriSensUnit = ttk.Label(self.tab4, text="V").grid(column=3, row=5, padx=20, pady=10, sticky="w")

        vrpLabel = ttk.Label(self.tab4, text="VRP:").grid(column=1, row=6, padx=20, pady=10, sticky="e")
        vrpValue = ttk.Label(self.tab4, text=self.vrp.get()).grid(column=2, row=6, padx=20, pady=10)
        vrpUnit = ttk.Label(self.tab4, text="ms").grid(column=3, row=6, padx=20, pady=10, sticky="w")

        pvarpLabel = ttk.Label(self.tab3, text="PVARP:").grid(column=1, row=7, padx=20, pady=10, sticky="e")
        pvarpValue = ttk.Label(self.tab3, text=self.pvarp.get()).grid(column=2, row=7, padx=20, pady=10)
        pvarpUnit = ttk.Label(self.tab3, text="ms").grid(column=3, row=7, padx=20, pady=10, sticky="w")

        msrLabel = ttk.Label(self.tab4, text="Max. Sensor Rate:").grid(column=1, row=8, padx=20, pady=10, sticky="e")
        msrValue = ttk.Label(self.tab4, text=self.msr.get()).grid(column=2, row=8, padx=20, pady=10)
        msrUnit = ttk.Label(self.tab4, text="ppm").grid(column=3, row=8, padx=20, pady=10, sticky="w")

        actThresLabel = ttk.Label(self.tab4, text="Activity Threshold:").grid(column=1, row=9, padx=20, pady=10, sticky="e")
        actThresValue = ttk.Label(self.tab4, text=self.actThresTextValues[self.actThres.get()]).grid(column=2, row=9, padx=20, pady=10)

        reactTimeLabel = ttk.Label(self.tab4, text="Reaction Time:").grid(column=1, row=10, padx=20, pady=10, sticky="e")
        reactTimeValue = ttk.Label(self.tab4, text=self.reactTime.get()).grid(column=2, row=10, padx=20, pady=10)
        reactTimeUnit = ttk.Label(self.tab4, text="sec").grid(column=3, row=10, padx=20, pady=10, sticky="w")

        resFactorLabel = ttk.Label(self.tab4, text="Response Factor:").grid(column=1, row=11, padx=20, pady=10, sticky="e")
        resFactorValue = ttk.Label(self.tab4, text=self.resFactor.get()).grid(column=2, row=11, padx=20, pady=10)

        recTimeLabel = ttk.Label(self.tab4, text="Recovery Time:").grid(column=1, row=12, padx=20, pady=10, sticky="e")
        recTimeValue = ttk.Label(self.tab4, text=self.recTime.get()).grid(column=2, row=12, padx=20, pady=10)
        recTimeUnit = ttk.Label(self.tab4, text="min").grid(column=3, row=12, padx=20, pady=10, sticky="w")

    def __vviInterfaceConfig(self):
        # Config menu to edit parameters for the VVI Pacemaker mode

        self.settingsButton4.destroy()
        self.hysteresisValue2.destroy()
        self.rateSmoothValue2.destroy()
        reg = self.tab4.register(self.validateInput)

        self.lowerRateInput4 = ttk.Entry(self.tab4, textvariable=self.lowerRateLimit, justify=CENTER)
        self.lowerRateInput4.grid(column=2, row=1, padx=20, pady=10)
        self.lowerRateInput4.config(validate="key", validatecommand=(reg, "%P"))

        self.upperRateInput4 = ttk.Entry(self.tab4, textvariable=self.upperRateLimit, justify=CENTER)
        self.upperRateInput4.grid(column=2, row=2, padx=20, pady=10)
        self.upperRateInput4.config(validate="key", validatecommand=(reg, "%P"))

        self.ventriAmpInput4 = ttk.Entry(self.tab4, textvariable=self.ventriAmp, justify=CENTER)
        self.ventriAmpInput4.grid(column=2, row=3, padx=20, pady=10)
        self.ventriAmpInput4.config(validate="key", validatecommand=(reg, "%P"))

        self.ventriPulseInput4 = ttk.Entry(self.tab4, textvariable=self.ventriPulseWidth, justify=CENTER)
        self.ventriPulseInput4.grid(column=2, row=4, padx=20, pady=10)
        self.ventriPulseInput4.config(validate="key", validatecommand=(reg, "%P"))

        self.ventriSensInput4 = ttk.Entry(self.tab4, textvariable=self.ventriThres, justify=CENTER)
        self.ventriSensInput4.grid(column=2, row=5, padx=20, pady=10)
        self.ventriSensInput4.config(validate="key", validatecommand=(reg, "%P"))

        self.vrpInput4 = ttk.Entry(self.tab4, textvariable=self.vrp, justify=CENTER)
        self.vrpInput4.grid(column=2, row=6, padx=20, pady=10)
        self.vrpInput4.config(validate="key", validatecommand=(reg, "%P"))

        self.pvarpInput4 = ttk.Entry(self.tab3, textvariable=self.pvarp, justify=CENTER)
        self.pvarpInput4.grid(column=2, row=7, padx=20, pady=20)
        self.pvarpInput4.config(validate="key", validatecommand=(reg, "%P"))

        self.msrInput4 = ttk.Entry(self.tab4, textvariable=self.msr, justify=CENTER)
        self.msrInput4.grid(column=2, row=8, padx=20, pady=10)
        self.msrInput4.config(validate="key", validatecommand=(reg, "%P"))
        
        self.actThresInput4 = ttk.Combobox(self.tab4, values=list(self.actThresTextValues.values()))
        self.actThresInput4.grid(column=2, row=9, padx=20, pady=10)
        self.actThresInput4.set(self.actThresTextValues[self.actThres.get()])

        self.reactTimeInput4 = ttk.Combobox(self.tab4, values=[10,20,30,40,50])
        self.reactTimeInput4.grid(column=2, row=10, padx=20, pady=10)
        self.reactTimeInput4.set(self.reactTime.get())

        self.resFactorInput4 = ttk.Combobox(self.tab4, values=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.resFactorInput4.grid(column=2, row=11, padx=20, pady=10)
        self.resFactorInput4.set(self.resFactor.get())

        self.recTimeInput4 = ttk.Combobox(self.tab4, values=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        self.recTimeInput4.grid(column=2, row=12, padx=20, pady=10)
        self.recTimeInput4.set(self.recTime.get())

        self.confirmButton4 = tk.Button(self.tab4, text="Confirm Changes", bg="white", command=self.__vviConfigConfirm)
        self.confirmButton4.grid(column=5, row=13, sticky="w", padx=5, pady=5)

    def __vviConfigConfirm(self):
        # VVI config confirm button -> Enforces value limits, cleans up ui to prevent memory leaking, and updates values

        invalid = False

        if (self.lowerRateLimit.get() < 30) or (self.lowerRateLimit.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Lower Rate Limit must be between 30-175")
        if (self.upperRateLimit.get() < 50) or (self.upperRateLimit.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Upper Rate Limit must be between 50-175")
        if (self.ventriAmp.get() < 0) or (self.ventriAmp.get() > 5.0):
            invalid = True
            messagebox.showerror("Value Error", "Ventricular Ampltiude must be between 0.1 and 5.0 or 0 for off")
        if (self.ventriPulseWidth.get() < 1) or (self.ventriPulseWidth.get() > 30):
            invalid = True
            messagebox.showerror("Value Error", "Ventricular Pulse Width must be between 1 and 30")
        if (self.vrp.get() < 150) or (self.vrp.get() > 500):
            invalid = True
            messagebox.showerror("Value Error", "VRP must be between 150 and 500")
        if (self.ventriThres.get() < 0) or (self.ventriThres.get() > 5.0):
            invalid = True
            messagebox.showerror("Value Error", "Ventricular Sensitivity must be between 0 and 5.0")
        if (self.msr.get() < 50) or (self.msr.get() > 175):
            invalid = True
            messagebox.showerror("Value Error", "Maxmium Sensor Rate must be between 50-175")
        if invalid:
            # Do nothing on invalid input to force user to correct error
            pass
        else:
            try:
                IntVar.set(self.actThres, list(self.actThresTextValues.keys())[self.actThresInput4.current()])
                IntVar.set(self.reactTime, self.reactTimeInput4.get())
                IntVar.set(self.resFactor, self.resFactorInput4.get())
                IntVar.set(self.recTime, self.recTimeInput4.get())
                for widget in self.tab4.winfo_children():
                    widget.destroy()
            except TclError:
                pass
            self.tab4.update()
            self.__updateValues()
            self.vviInterface()

    def commSettings(self):
        # Serial Communications Menu initialization

        portSelectLabel = ttk.Label(self.tab6, text="Select serial port:")
        portSelectLabel.place(relx=0.4, rely=0.315)
        self.comPortSelect = ttk.Combobox(self.tab6, values=ser.serialList())
        self.comPortSelect.place(relx=0.475, rely=0.3)
        connButton = tk.Button(self.tab6, text="Connect", bg="white", command=self.__commConnect)
        connButton.place(relx=0.4, rely=0.38)
        disconnButton = tk.Button(self.tab6, text="Disconnect", bg="white", command=self.__commDC)
        disconnButton.place(relx=0.53, rely=0.38)
        echoParamButton = tk.Button(self.tab6, text="Echo Parameters", bg="white", command=self.__commEcho)
        echoParamButton.place(relx=0.6, rely=0.3075)
        self.connectedLabel = ttk.Label(self.tab6, text="Connected to Serial")
        self.disconnectedLabel = ttk.Label(self.tab6, text="Disconnected from Serial")
        if ser.serState()[0]:
            self.disconnectedLabel.place_forget()
            self.connectedLabel.place(relx=0.475, rely=0.25)
            self.comPortSelect.set(ser.serState()[1])
        else:
            self.connectedLabel.place_forget()
            self.disconnectedLabel.place(relx=0.475, rely=0.25)
            self.comPortSelect.set(ser.serialList()[0])

    def __commConnect(self):
        # Method to be binded to a button and executed on press
        # Connects to selected serial communications port in the dropdown menu

        ser.serOpen(self.comPortSelect.get()[0:4])
        if ser.serState()[0]:
            self.disconnectedLabel.place_forget()
            self.connectedLabel.place(relx=0.475, rely=0.25)
            ser.serWrite(self.inputValues) # Write params to board on connection
        else:
            # Do nothing on failed connection
            pass
    
    def __commDC(self):
        # Disconnects the DCM from the pacemaker board

        ser.serClose()
        self.connectedLabel.place_forget()
        self.disconnectedLabel.place(relx=0.475, rely=0.25)

    def __commSettingsCleanup(self):
        # Method used to cleanup ui elements in the serial communications menu
        # Serves to prevent redrawing of UI elements by clearing them, preventing memory leaking
        
        try:
            for widget in self.tab6.winfo_children():
                widget.destroy()
        except TclError:
            pass

        self.tab6.update()

    def __commEcho(self):
        # Method binded to button
        # Sends a request to the pacemaker board to echo the currently stored parameter values
        # Order -> [Mode, LRL, URL, A.amp, A.pw, V.amp, V.pw, VRP, ARP, aSens, vSens, rateAdapt, MSR, actThres, reactTime, resFactor, recTime, avDelay]
        
        if ser.serState()[0]:
            print(ser.serRead())
        else:
            pass

    def __updateValues(self):
        # Update list of inputs
        # [Mode, LRL, URL, A.amp, A.pw, V.amp, V.pw, VRP, ARP, aSens, vSens, rateAdapt, MSR, actThres, reactTime, resFactor, recTime, avDelay]

        # Rounding for Lower Rate Limit value
        lowerRateLimit = self.lowerRateLimit.get()
        if (30 < lowerRateLimit < 50) or (90 < lowerRateLimit < 175):
            lowerRateLimit = 5 * round(lowerRateLimit/5)
        IntVar.set(self.lowerRateLimit, lowerRateLimit)

        # Rounding for Upper Rate Limit value
        upperRateLimit = self.upperRateLimit.get()
        if (50 < upperRateLimit < 175):
            upperRateLimit = 5 * round(upperRateLimit/5)
        IntVar.set(self.upperRateLimit, upperRateLimit)

        # Rounding for Atrial Amp value
        atrialAmp = self.atrialAmp.get()
        DoubleVar.set(self.atrialAmp, round(atrialAmp, 1))

        # Rounding for Atrial PW value
        atrialPulseWidth = self.atrialPulseWidth.get()
        IntVar.set(self.atrialPulseWidth, round(atrialPulseWidth))

        # Rounding for Ventri Amp value
        ventriAmp = self.ventriAmp.get()
        DoubleVar.set(self.ventriAmp, round(ventriAmp, 1))

        # Rounding for Ventri PW value
        ventriPulseWidth = self.ventriPulseWidth.get()
        IntVar.set(self.ventriPulseWidth, round(ventriPulseWidth))

        # Rounding for VRP value
        vrp = self.vrp.get()
        vrp = 10 * round(vrp/10)
        IntVar.set(self.vrp, vrp)

        # Rounding for ARP value
        arp = self.arp.get()
        arp = 10 * round(arp/10)
        IntVar.set(self.arp, arp)

        # Rounding for Atrial Sensitivity value
        aSens = self.atrialThres.get()
        DoubleVar.set(self.atrialThres, round(aSens, 1))

        # Rounding for Ventricular Sensitivity value
        vSens = self.ventriThres.get()
        DoubleVar.set(self.ventriThres, round(vSens, 1))

        # Rounding for the Maximum Sensor Rate value
        msr = self.msr.get()
        msr = 5 * round(msr/5)
        IntVar.set(self.msr, msr)

        # Rounding for Fixed AV Delay
        avDelay = self.avDelay.get()
        avDelay = 10 * round(avDelay/10)
        IntVar.set(self.avDelay, avDelay)

        # [Mode, LRL, URL, A.amp, A.pw, V.amp, V.pw, VRP, ARP, aSens, vSens, rateAdapt, MSR, actThres, reactTime, resFactor, recTime]
        self.inputValues = [self.tabControl.index("current"), self.lowerRateLimit.get(), self.upperRateLimit.get(), self.pvarp.get(), 
                            self.avDelay.get(), self.reactTime.get(), self.resFactor.get(), self.actThres.get(), self.recTime.get(), self.msr.get(), 
                            self.atrialAmp.get(), self.atrialPulseWidth.get(), self.arp.get(), self.atrialThres.get(), 
                            self.ventriAmp.get(), self.ventriPulseWidth.get(), self.vrp.get(),  self.ventriThres.get()]
        db.updateParams(tuple(self.inputValues)) # Update values to the database for the current user

        if ser.serState()[0]:
            ser.serWrite(self.inputValues) # Update values to board only if serial communications port is open

    def validateInput(self, input):
        # Method used to validate user input
        # There should not be any string value input ever, therefore validation only checks for numerical input and "."

        try:
            if input:
                temp = int(input)   # Check to see if string input can be typecasted to integer
            return True
        except ValueError:
            try:
                if input:
                    temp = float(input) # If string input cannot be typecasted to integer, check to see if it can be typecasted to float
                return True
            except ValueError:
                messagebox.showerror("Input Error", "Error - Only numbers and '.' are accepted") # Otherwise, attempted input did not contain numbers or "." exclusively
                return False
    
    def egram(self):
        # EGram interface initialization

        self.canvas = FigureCanvasTkAgg(self.atrialEgram, self.tab7)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0, rely=0, relwidth=0.5)

        self.canvas2 = FigureCanvasTkAgg(self.ventriEgram, self.tab7)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().place(relx=0.5, rely=0, relwidth=0.5)

        toolbar_frame = tk.Frame(self.tab7, width=50, height=20)
        toolbar_frame.place(relx=0, rely=0.7, relwidth=0.5)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()

        toolbar_frame2 = tk.Frame(self.tab7, width=50, height=20)
        toolbar_frame2.place(relx=0.5, rely=0.7, relwidth=0.5)
        toolbar2 = NavigationToolbar2Tk(self.canvas2, toolbar_frame2)
        toolbar2.update()  

        startButton = tk.Button(self.tab7, text="Start", command=self.__startAnimate)
        startButton.place(relx=0.45, rely=0.8)
        stopButton = tk.Button(self.tab7, text="Stop", command=self.__stopAnimate)
        stopButton.place(relx=0.5, rely=0.8)
        
    def __animate(self, i, xvals, yvals):
        # Animation function for atrial graph plot

        self.TimeElapsed += 100
        xvals.append(self.TimeElapsed)
        xvals = xvals[-20:]
        data = ser.startEgram()
        ser.stopEgram()
        yvals.append(data[0])
        yvals = yvals[-20:]
        self.a.clear()
        self.a.set_title("Atrial")
        self.a.set_ylim(0,5)
        self.a.plot(xvals, yvals)
        self.canvas.draw_idle()
        self.canvas.flush_events()

    def __animate2(self, i, xvals, yvals):
        # Animation function for ventricular graph plot

        self.TimeElapsed2 += 100
        xvals.append(self.TimeElapsed2)
        xvals = xvals[-20:]
        data = ser.startEgram()
        ser.stopEgram()
        yvals.append(data[0])
        yvals = yvals[-20:]
        self.b.clear()
        self.b.set_title("Ventri.")
        self.b.set_ylim(0,5)
        self.b.plot(xvals, yvals)
        self.canvas2.draw_idle()
        self.canvas2.flush_events()

    def __startAnimate(self):
        # Method to be binded onto button
        # Forces a redraw of the UI (ensures there is only one instance of each plot running at a given time)
        # Starts graph animation functions
        
        self.__egramCleanup()
        self.egram()
        self.solve = animation.FuncAnimation(self.atrialEgram, self.__animate, fargs=(self.xvals, self.atrvals), interval=100)
        self.canvas.draw_idle()
        self.solve2 = animation.FuncAnimation(self.ventriEgram, self.__animate2, fargs=(self.xvals2, self.vtrvals), interval=100)
        self.canvas2.draw_idle()
        self.solve.event_source.start()
        self.solve2.event_source.start()
        
    def __stopAnimate(self):
        # Method to be binded onto button
        # Allows the user to stop graphical animation at any given point in time to analyze the output
        
        self.solve.event_source.stop()
        self.solve2.event_source.stop()
        ser.stopEgram()
        self.TimeElapsed = 0
        self.TimeElapsed2 = 0
        self.xvals = []
        self.xvals2 = []
        self.atrvals = []
        self.vtrvals = []

    def __egramCleanup(self):
        # Method used to clean up the UI by removing elements
        # This is to prevent memory leaking for redrawing elements to the frame

        try:
            for widget in self.tab7.winfo_children():
                widget.destroy()
        except TclError:
            pass

        self.tab7.update()

    def run(self):
        self.modeWin.mainloop()
import tkinter as tk
import tkinter.ttk as ttk
import serial.tools.list_ports

def serial_ports():
    return serial.tools.list_ports.comports()

def on_select(event=None):
    print("event.widget:", event.widget.get())
    print("combobox:", cb.get())

root = tk.Tk()

cb = ttk.Combobox(root, values=serial_ports())
cb.pack()

cb.bind('<<ComboboxSelected>>', on_select)

root.mainloop()
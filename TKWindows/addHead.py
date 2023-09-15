import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import main as mainwindow

headNameEntry, headTypeDropdown = None

def changedValue(dropDownMenu : ttk.Combobox):
    global headNameEntry
    if (not dropDownMenu.get() == "NEW HEAD TYPE") and (not headNameEntry == None):
        headNameEntry.configure(state="disabled")

def addHead(root, rigsDB, selected_rig):
    global headNameEntry, headTypeDropdown
    # Add head window
    addHeadWindow = tk.Toplevel(root)
    addHeadWindow.title("Add Head")
    addHeadWindow.geometry("300x200")
    addHeadWindow.resizable(False, False)

    # Head addition form
    #Get the existing head types
    HeadTypes = f"SELECT DISTINCT HeadType FROM {selected_rig}"
    HeadTypeRows = rigsDB.execute(HeadTypes)
    HeadTypeRows = [row[0] for row in HeadTypeRows]

    # Insert blank option at 0
    HeadTypeRows.insert(0, "NEW HEAD TYPE")

    # ./mockup/addheads.html
    # Head type
    headTypeLabel = tk.Label(addHeadWindow, text="Head Type:")
    headTypeLabel.grid(row=0, column=0, sticky="nw")

    headTypeDropdown = ttk.Combobox(addHeadWindow, values=HeadTypeRows)
    headTypeDropdown.bind("<<ComboboxSelected>>", changedValue(headTypeDropdown))
    headTypeDropdown.grid(row=1, column=0, sticky="nw")

    # Head name
    headNameLabel = tk.Label(addHeadWindow, text="Head Name:")
    headNameLabel.grid(row=2, column=0, sticky="nw")

    headNameEntry = tk.Entry(addHeadWindow)
    headNameEntry.grid(row=3, column=0, sticky="nw")
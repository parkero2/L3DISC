import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font

import os
import sys
import time
import threading
import asyncio
from stupidArtnet import StupidArtnet
import sqlite3

from PIL import Image, ImageTk

import TKWindows.setupWindow as setupWindow
import TKWindows.addHead as addHead

artnetConnection = None
rigsDB = None
selected_rig = None
root = None
headsList = None

try:
    with open(os.path.join(os.getcwd(), "info.txt"), 'r') as f:
        info = f.read().splitlines()
except FileNotFoundError:
    print('''info.txt not found, please download the latest version of OliQ from 
          https://github.com/parkero2/L3DISC/releases.''')

def getRigs() -> list:
    global rigsDB
     # Get all the tables in the database
    rows = rigsDB.execute("SELECT name FROM sqlite_schema WHERE type='table';")
    rigs = []
    for row in rows:
        rigs.append(row) # Make a list of each rig in the database
    return rigs

def main():
    atnetSetup = setupWindow.setupWindow()
    artnetConnection = StupidArtnet(atnetSetup[0], atnetSetup[3], atnetSetup[2]
                                    , atnetSetup[1])
    artnetConnection.start()

    #Initialal setup
    if (not os.path.exists(os.path.join(os.getcwd(), "heads"))):
        os.mkdir(os.path.join(os.getcwd(), "heads"))
    
    global rigsDB
    rigsDB = sqlite3.connect(os.path.join(os.getcwd(), "rigs.db"))
    rigs = getRigs()

    global root, headsList
    root = tk.Tk()
    root.title(f"OliQ V" + str(info[0].split("=")[1]))
    # mazimised window
    root.state("zoomed")
    root.bind("<Escape>", lambda e: root.destroy())

    # Show selector button, always in the top left corner
    showSelectorButton = tk.Button(root, text="Show Selector", 
                                   command=lambda: showSelector())
    showSelectorButton.grid(row=0, column=0, sticky="nw")

    # Create a resizable section on the left
    headsFrame = tk.Frame(root, width=200, height=1000)
    headsFrame.grid(row=1, column=0, sticky="nw")
    headsFrame.grid_propagate(False)

    #Add head button
    addHeadButton = tk.Button(headsFrame, text="Add Head",
                                command=lambda: addHead.addHead(root, rigsDB, selected_rig))
    addHeadButton.grid(row=0, column=0, sticky="nw")

    # Delete selected head(s) button
    deleteHeadButton = tk.Button(headsFrame, text="Delete Head(s)",
                                command=lambda: deleteHead(headsList.curselection()))
    deleteHeadButton.grid(row=0, column=1, sticky="nw")

    # Create a selection list for the heads
    headsList = tk.Listbox(headsFrame, width=200, height=1000)
    headsList.grid(row=1, column=0, sticky="nw")
    headsList.grid_propagate(False)

    # Main window
    root.mainloop()

def showSelector():
    # window with a dropdown menu allowing the user to select a rig
    rigSelector = tk.Toplevel(root)
    rigSelector.title("Select Rig")
    rigSelector.geometry("300x200")
    rigSelector.resizable(False, False)

    # Rig selector
    rigSelectorLabel = tk.Label(rigSelector, text="Select a rig:")
    rigSelectorLabel.grid(row=0, column=0, sticky="nw")

    rigSelectorDropdown = ttk.Combobox(rigSelector, values=getRigs())
    rigSelectorDropdown.grid(row=1, column=0, sticky="nw")

    rigSelectorButton = tk.Button(rigSelector, text="Select", 
                                  command=lambda: setRig(
                                      rigSelectorDropdown.get(), 
                                      rigSelector.destroy()))
    rigSelectorButton.grid(row=2, column=0, sticky="nw")

    # New rig button, this passes None to setRig, which will create a new rig
    newRigButton = tk.Button(rigSelector, text="New Rig", 
                             command=lambda: setRig(None, 
                                                    rigSelector.destroy()))
    newRigButton.grid(row=3, column=0, sticky="nw")

    rigSelector.mainloop()

def deleteHead(heads: tuple):
    global selected_rig
    if (selected_rig == None):
        messagebox.showerror("Error", "No rig selected")
        return
    if (len(heads) == 0):
        messagebox.showerror("Error", "No heads selected")
        return
    if (messagebox.askyesno("Delete Heads", "Are you sure you want to delete these heads?")):
        for head in heads:
            query = f"DELETE FROM {selected_rig} WHERE HeadID={head}"
            rigsDB.execute(query)
        rigsDB.commit()
        showRig(headsList)

def showRig(lbox: tk.Listbox):
    global selected_rig
    query = f"SELECT * FROM {selected_rig} ORDER BY HeadID ASC"
    rows = rigsDB.execute(query)
    for row in rows:
        lbox.insert(tk.END, f"{row[0]}: {row[1]}")

def setRig(rig: str = None, window: tk.Toplevel = None):
    global selected_rig, headsList
    selected_rig = rig
    showRig(headsList)


if __name__ == '__main__':
    main()
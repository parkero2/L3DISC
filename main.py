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

artnetConnection = None
rigsDB = None
selected_rig = None
root = None

try:
    with open(os.path.join(os.getcwd(), "info.txt"), 'r') as f:
        info = f.read().splitlines()
except FileNotFoundError:
    print("info.txt not found, please download the latest version of OliQ from https://github.com/parkero2/L3DISC/releases.")

def getRigs() -> list:
    global rigsDB
    rows = rigsDB.execute("SELECT name FROM sqlite_schema WHERE type='table';") # Get all the tables in the database
    rigs = []
    for row in rows:
        rigs.append(row) # Make a list of each rig in the database
    return rigs

def main():
    atnetSetup = setupWindow.setupWindow()
    artnetConnection = StupidArtnet(atnetSetup[0], atnetSetup[3], atnetSetup[2], atnetSetup[1])
    artnetConnection.start()

    #Initialal setup
    if (not os.path.exists(os.path.join(os.getcwd(), "heads"))):
        os.mkdir(os.path.join(os.getcwd(), "heads"))
    
    global rigsDB
    rigsDB = sqlite3.connect(os.path.join(os.getcwd(), "rigs.db"))
    rigs = getRigs()

    global root
    root = tk.Tk()
    root.title(f"OliQ %f" % float(info[0].split("=")[1]))
    # Fullscreen
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", lambda e: root.destroy())

    # Show selector button, always in the top left corner
    showSelectorButton = tk.Button(root, text="Show Selector", 
                                   command=lambda: showSelector())
    showSelectorButton.grid(row=0, column=0, sticky="nw")


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

def setRig(rig: str = None, window: tk.Toplevel = None):
    global selected_rig
    selected_rig = rig

if __name__ == '__main__':
    main()
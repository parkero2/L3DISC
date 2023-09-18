import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
import main as mainwindow

headNameEntry, headTypeDropdown = None, None


def changedValue(dropDownMenu: ttk.Combobox):
    global headNameEntry
    if (not dropDownMenu.get() == "NEW HEAD TYPE") and (not headNameEntry == None):
        headNameEntry.configure(state="disabled")


def submitHead(rigsDB, selected_rig, addHeadWindow, headTypeDropdown,
               headNameEntry, totalChannelsEntry, intensityChannelEntry,
               redChannelEntry, greenChannelEntry, blueChannelEntry,
               amberChannelEntry, whiteChannelEntry, panChannelEntry,
               tiltChannelEntry, shutterChannelEntry):
    pass


def addHead(root, rigsDB, selected_rig):
    global headNameEntry, headTypeDropdown
    # Add head window
    addHeadWindow = tk.Toplevel(root)
    addHeadWindow.title("Add Head")
    addHeadWindow.resizable(False, False)

    # Head addition form
    # Get the existing head types
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
    headTypeDropdown.bind("<<ComboboxSelected>>",
                          changedValue(headTypeDropdown))
    headTypeDropdown.grid(row=1, column=0, sticky="nw")

    # Head name
    headNameLabel = tk.Label(addHeadWindow, text="Head Name:")
    headNameLabel.grid(row=2, column=0, sticky="nw")

    headNameEntry = tk.Entry(addHeadWindow)
    headNameEntry.grid(row=3, column=0, sticky="nw")

    # Total number of channels
    totalChannelsLabel = tk.Label(addHeadWindow, text="Total Channels:")
    totalChannelsLabel.grid(row=4, column=0, sticky="nw")

    totalChannelsEntry = tk.Entry(addHeadWindow)
    totalChannelsEntry.grid(row=5, column=0, sticky="nw")

    # intensity channel
    intensityChannelLabel = tk.Label(addHeadWindow, text="Intensity Channel:")
    intensityChannelLabel.grid(row=6, column=0, sticky="nw")

    intensityChannelEntry = tk.Entry(addHeadWindow)
    intensityChannelEntry.grid(row=7, column=0, sticky="nw")

    # Red channel
    redChannelLabel = tk.Label(addHeadWindow, text="Red Channel:")
    redChannelLabel.grid(row=8, column=0, sticky="nw")

    redChannelEntry = tk.Entry(addHeadWindow)
    redChannelEntry.grid(row=9, column=0, sticky="nw")

    # Green channel
    greenChannelLabel = tk.Label(addHeadWindow, text="Green Channel:")
    greenChannelLabel.grid(row=10, column=0, sticky="nw")

    greenChannelEntry = tk.Entry(addHeadWindow)
    greenChannelEntry.grid(row=11, column=0, sticky="nw")

    # Blue channel
    blueChannelLabel = tk.Label(addHeadWindow, text="Blue Channel:")
    blueChannelLabel.grid(row=12, column=0, sticky="nw")

    blueChannelEntry = tk.Entry(addHeadWindow)
    blueChannelEntry.grid(row=13, column=0, sticky="nw")

    # Amber channel
    amberChannelLabel = tk.Label(addHeadWindow, text="Amber Channel:")
    amberChannelLabel.grid(row=16, column=0, sticky="nw")

    amberChannelEntry = tk.Entry(addHeadWindow)
    amberChannelEntry.grid(row=17, column=0, sticky="nw")

    # White channel
    whiteChannelLabel = tk.Label(addHeadWindow, text="White Channel:")
    whiteChannelLabel.grid(row=14, column=0, sticky="nw")

    whiteChannelEntry = tk.Entry(addHeadWindow)
    whiteChannelEntry.grid(row=15, column=0, sticky="nw")

    # Pan channel
    panChannelLabel = tk.Label(addHeadWindow, text="Pan Channel:")
    panChannelLabel.grid(row=18, column=0, sticky="nw")

    panChannelEntry = tk.Entry(addHeadWindow)
    panChannelEntry.grid(row=19, column=0, sticky="nw")

    # Tilt channel
    tiltChannelLabel = tk.Label(addHeadWindow, text="Tilt Channel:")
    tiltChannelLabel.grid(row=20, column=0, sticky="nw")

    tiltChannelEntry = tk.Entry(addHeadWindow)
    tiltChannelEntry.grid(row=21, column=0, sticky="nw")

    # Shutter channel
    shutterChannelLabel = tk.Label(addHeadWindow, text="Shutter Channel:")
    shutterChannelLabel.grid(row=22, column=0, sticky="nw")

    shutterChannelEntry = tk.Entry(addHeadWindow)
    shutterChannelEntry.grid(row=23, column=0, sticky="nw")

    # Submit button
    submitButton = tk.Button(addHeadWindow, text="Submit", command=lambda:
                             submitHead(rigsDB, selected_rig, addHeadWindow, 
                                        headTypeDropdown, headNameEntry, 
                                        totalChannelsEntry, 
                                        intensityChannelEntry, redChannelEntry, 
                                        greenChannelEntry, blueChannelEntry, 
                                        amberChannelEntry, whiteChannelEntry, 
                                        panChannelEntry, tiltChannelEntry, 
                                        shutterChannelEntry))
    submitButton.grid(row=24, column=0, sticky="nw")

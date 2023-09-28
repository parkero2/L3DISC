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


def submitHead(rigsDB: mainwindow.sqlite3.Connection, selected_rig: str, 
               addHeadWindow, headTypeEntry: tk.Entry, 
               headTypeDropdown: ttk.Combobox, patchEntry: tk.Entry, 
               headNameEntry: tk.Entry, totalChannelsEntry: tk.Entry, 
               intensityChannelEntry:tk.Entry,redChannelEntry: tk.Entry, 
               greenChannelEntry: tk.Entry, blueChannelEntry: tk.Entry, 
               amberChannelEntry: tk.Entry, whiteChannelEntry: tk.Entry, 
               panChannelEntry: tk.Entry,tiltChannelEntry: tk.Entry, 
               shutterChannelEntry: tk.Entry):
    # Example query
    # INSERT INTO example (Name, HeadType, Patch, Channels, Intensity, Red, Green, Blue, Amber, White, Pan, Tilt, Shutter) VALUES ("FOH1", "Fresnel", 3, 1, 1)
    headType = None
    print(headTypeDropdown.get())
    if headTypeDropdown.get() == "NEW HEAD TYPE":
        headType = headTypeDropdown.get()
    else:
        headType = headTypeEntry.get()
    
    query = f'''INSERT INTO {selected_rig} (Name, HeadType, Patch, Channels, 
    Intensity, Red, Green, Blue, Amber, White, Pan, Tilt, Shutter) VALUES (
        {"Unamed" if (headNameEntry.get() == "") else headNameEntry.get()}, {headType}, {int(patchEntry.get())}, 
        {int(totalChannelsEntry.get())}, 
        {int(intensityChannelEntry.get()) if (not intensityChannelEntry.get() == "") else None}, 
        {int(redChannelEntry.get()) if (not redChannelEntry.get() == "") else None},
        {int(greenChannelEntry.get()) if (not greenChannelEntry.get() == "") else None},
        {int(blueChannelEntry.get()) if (not blueChannelEntry.get() == "") else None},
        {int(amberChannelEntry.get()) if (not amberChannelEntry.get() == "") else None},
        {int(whiteChannelEntry.get()) if (not whiteChannelEntry.get() == "") else None},
        {int(panChannelEntry.get()) if (not panChannelEntry.get() == "") else None},
        {int(tiltChannelEntry.get()) if (not tiltChannelEntry.get() == "") else None},
        {int(shutterChannelEntry.get()) if (not shutterChannelEntry.get() == "") else None})'''.strip("\n")
    print(query.strip('''
'''))
    rigsDB.execute(query)

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

    # Head type label
    headTypeEntryLabel = tk.Label(addHeadWindow, text="Head Type Label (if not selected):")
    headTypeEntryLabel.grid(row=0, column=3, sticky="nw")

    # HeadType string input
    headTypeEntry = tk.Entry(addHeadWindow)
    headTypeEntry.grid(row=1, column=3, sticky="nw")

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

    # Patch input
    patchLabel = tk.Label(addHeadWindow, text="Patch:")
    patchLabel.grid(row=24, column=0, sticky="nw")

    patchEntry = tk.Entry(addHeadWindow)
    patchEntry.grid(row=25, column=0, sticky="nw")

    # Submit button
    submitButton = tk.Button(addHeadWindow, text="Submit", command=lambda:
                             submitHead(rigsDB, selected_rig, addHeadWindow, headTypeEntry,
                                        headTypeDropdown, patchEntry, headNameEntry, 
                                        totalChannelsEntry, 
                                        intensityChannelEntry, redChannelEntry, 
                                        greenChannelEntry, blueChannelEntry, 
                                        amberChannelEntry, whiteChannelEntry, 
                                        panChannelEntry, tiltChannelEntry, 
                                        shutterChannelEntry))
    submitButton.grid(row=26, column=0, sticky="nw")

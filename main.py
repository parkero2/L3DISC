try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import filedialog
    from tkinter import font
    from tkinter.colorchooser import askcolor

    import os
    import sys
    import time
    import threading
    import asyncio
    from stupidArtnet import StupidArtnet
    import sqlite3

    from PIL import Image, ImageTk

    import TKWindows.setupWindow as setup_window
    import TKWindows.addHead as addHead
    import classes.lighting_fixture as LightingFixture
except ImportError:
    # Some packages are not installed or available
    print("Please install the required modules before running OliQ.")
    exit(1)

artnetConnection = None
rigsDB = None
selected_rig = None
root = None
headsInRig = []
headsList = []
addHeadButton, delete_headButton = None, None
color = None
heads = None
amberSlider = None
whiteSlider = None
intensitySlider = None
panSlider = None
tiltSlider = None
shutterSlider = None
playbackSliders, bumpButtons = [], []
recordButton = None

try:
    with open(os.path.join(os.getcwd(), "src", "info.txt"), 'r') as f:
        info = f.read().splitlines()
except FileNotFoundError:
    print('''info.txt not found, please download the latest version of OliQ from 
          https://github.com/parkero2/L3DISC/releases.''')


def get_rigs() -> list:
    global rigsDB
    # Get all the tables in the database
    rows = rigsDB.execute("SELECT name FROM sqlite_schema WHERE type='table';")
    rigs = []
    for row in rows:
        rigs.append(row)  # Make a list of each rig in the database
    return rigs


def select_show():
    # window with a dropdown menu allowing the user to select a rig
    rigSelector = tk.Toplevel(root)
    rigSelector.title("Select Rig")
    rigSelector.resizable(False, False)

    # Rig selector
    rigSelectorLabel = tk.Label(rigSelector, text="Select a rig:")
    rigSelectorLabel.grid(row=0, column=0, sticky="nw")

    rigSelectorDropdown = ttk.Combobox(rigSelector, values=get_rigs())
    rigSelectorDropdown.grid(row=1, column=0, sticky="nw")

    tk.Label(rigSelector, text="Or create a new one").grid(row=2, column=0,
                                                           sticky="nw")
    nameInput = tk.Entry(rigSelector)
    nameInput.grid(row=3, column=0, sticky="nw")

    rigSelectorButton = tk.Button(rigSelector, text="Select",
                                  command=lambda: set_rig(
                                      rigSelectorDropdown.get(),
                                      rigSelector.destroy()))
    rigSelectorButton.grid(row=4, column=0, sticky="nw")

    # New rig button, this passes None to set_rig, which will create a new rig
    newRigButton = tk.Button(rigSelector, text="New Rig",
                             command=lambda: set_rig(nameInput.get(),
                                                    rigSelector.destroy(), True))
    newRigButton.grid(row=5, column=0, sticky="nw")

    rigSelector.mainloop()

# ATTRIBUTE HANDLERS


def change_color(root: tk.Tk):
    try:
        global color, headsInRig, amberSlider, whiteSlider, headsList
        color = askcolor(title="Select Color")
        # Set the color for each head selected
        print(headsInRig)
        for head in headsList.curselection():
            print(head)
            headsInRig[head].set_red(color[0][0])
            headsInRig[head].set_green(color[0][1])
            headsInRig[head].set_blue(color[0][2])
            headsInRig[head].set_amber(amberSlider.get())
            headsInRig[head].set_white(whiteSlider.get())
    except:
        messagebox.showwarning(
            "Warning", "Color is not supported on one or more selected heads")


def change_intensity():
    try:
        global headsInRig, intensitySlider, headsList
        for head in headsList.curselection():
            headsInRig[head].set_intensity(intensitySlider.get())
    except:
        messagebox.showwarning(
            "Warning", "Intensity is not supported on one or more selected heads")


def change_pan():
    try:
        global headsInRig, panSlider, headsList
        for head in headsList.curselection():
            headsInRig[head].set_pan(panSlider.get())
    except:
        messagebox.showwarning(
            "Warning", "Pan is not supported on one or more selected heads")


def change_tilt():
    try:
        global headsInRig, tiltSlider, headsList
        for head in headsList.curselection():
            headsInRig[head].set_tilt(tiltSlider.get())
    except:
        messagebox.showwarning(
            "Warning", "Tilt is not supported on one or more selected heads")


def change_shutter():
    try:
        global headsInRig, shutterSlider, headsList
        for head in headsList.curselection():
            headsInRig[head].set_shutter(shutterSlider.get())
    except:
        messagebox.showwarning(
            "Warning", "Shutter is not supported on one or more selected heads")


def delete_head(heads: tuple):
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
        show_rig(headsList)


def show_rig(lbox: tk.Listbox):
    global selected_rig, heads, artnetConnection, headsInRig
    query = f"SELECT * FROM '{selected_rig}' ORDER BY HeadID ASC"
    try:
        rows = rigsDB.execute(query)
    except:
        messagebox.showerror("Error", "Failed to find rig in database.")
        return
    headsInRig = []
    for row in rows:
        headsInRig.append(LightingFixture.LightingFixture(artnetConnection,
                                                            row[0], row[2],
                                                            row[3], row[4],
                                                            0 if (
                                                                row[5] == None) else row[5],
                                                            0 if (
                                                                row[6] == None) else row[6],
                                                            0 if (
                                                                row[7] == None) else row[7],
                                                            0 if (
                                                                row[8] == None) else row[8],
                                                            0 if (
                                                                row[9] == None) else row[9],
                                                            0 if (
                                                                row[10] == None) else row[10],
                                                            0 if (
                                                                row[11] == None) else row[11],
                                                            0 if (row[12] == None) else row[12]))
        lbox.insert(tk.END, f"{row[0]}: {row[1]}")


def set_rig(rig: str = None, window: tk.Toplevel = None, newRig: str = False):
    global selected_rig, headsList, delete_headButton, addHeadButton, rigsDB
    if (newRig):
        if (rig == ""):
            messagebox.showerror("Error", "Please enter a name for the rig")
            return
        if (rig in get_rigs()):
            messagebox.showerror("Error", "Rig already exists")
            return
        query = f"""CREATE TABLE '{rig.replace(" ", "")}' (
                        'HeadID'	INTEGER NOT NULL,
                        'HeadType'	TEXT NOT NULL,
                        'Channels'	INTEGER NOT NULL,
                        'Patch'	INTEGER NOT NULL,
                        'Intensity'	INTEGER,
                        'Red'	INTEGER,
                        'Green'	INTEGER,
                        'Blue'	INTEGER,
                        'Amber'	INTEGER,
                        'White'	INTEGER,
                        'Pan'	INTEGER,
                        'Tilt'	INTEGER,
                        'Shutter'	INTEGER
                    );"""
        try:
            rigsDB.execute(query)
            rigsDB.commit()
        except:
            messagebox.showerror("Error", "Failed to create new rig")
            return
        selected_rig = rig

    selected_rig = rig
    delete_headButton["state"] = "normal"
    addHeadButton["state"] = "normal"
    show_rig(headsList)


def create_attrtibute_frames(root: tk.Tk):
    # a 4x4 grid for attributes. Each frame has a black outline
    # Intensity | Color
    # Position  | Beam

    global amberSlider, whiteSlider, intensitySlider, panSlider, tiltSlider, shutterSlider

    # Intensity section
    intensityFrame = tk.Frame(root, width=200, height=200,
                              highlightbackground="black", highlightthickness=1)
    intensityFrame.grid(row=1, column=2, sticky="nw")
    intensityFrame.grid_propagate(False)

    # Intensity label
    intensityLabel = tk.Label(intensityFrame, text="Intensity:")
    intensityLabel.grid(row=0, column=0, sticky="nw")

    # Intensity slider
    intensitySlider = tk.Scale(
        intensityFrame, from_=0, to=255, orient=tk.HORIZONTAL)
    intensitySlider.grid(row=1, column=0, sticky="nw")
    intensitySlider.bind("<ButtonRelease-1>", lambda e: change_intensity())

    # Color section
    colorFrame = tk.Frame(root, width=200, height=200,
                          highlightbackground="black", highlightthickness=1)
    colorFrame.grid(row=1, column=3, sticky="nw")
    colorFrame.grid_propagate(False)

    # Color picker
    colorPicker = tk.Button(colorFrame, text="Color Picker", command=lambda:
                            change_color(root))
    colorPicker.grid(row=0, column=0, sticky="nw")

    # Amber and white sliders
    amberLabel = tk.Label(colorFrame, text="Amber:")
    amberLabel.grid(row=1, column=0, sticky="nw")
    amberSlider = tk.Scale(colorFrame, from_=0, to=255, orient=tk.HORIZONTAL)
    amberSlider.grid(row=2, column=0, sticky="nw")
    whiteLabel = tk.Label(colorFrame, text="White:")
    whiteLabel.grid(row=3, column=0, sticky="nw")
    whiteSlider = tk.Scale(colorFrame, from_=0, to=255, orient=tk.HORIZONTAL)
    whiteSlider.grid(row=4, column=0, sticky="nw")

    # Slider event handlers
    amberSlider.bind("<ButtonRelease-1>", lambda e: change_color(root))
    whiteSlider.bind("<ButtonRelease-1>", lambda e: change_color(root))

    # Position section
    positionFrame = tk.Frame(root, width=200, height=200,
                             highlightbackground="black", highlightthickness=1)
    positionFrame.grid(row=1, column=4, sticky="nw")
    positionFrame.grid_propagate(False)

    # Pan and tilt sliders
    panLabel = tk.Label(positionFrame, text="Pan:")
    panLabel.grid(row=0, column=0, sticky="nw")
    panSlider = tk.Scale(positionFrame, from_=0, to=255, orient=tk.HORIZONTAL)
    panSlider.grid(row=1, column=0, sticky="nw")
    tiltLabel = tk.Label(positionFrame, text="Tilt:")
    tiltLabel.grid(row=2, column=0, sticky="nw")
    tiltSlider = tk.Scale(positionFrame, from_=0, to=255, orient=tk.HORIZONTAL)
    tiltSlider.grid(row=3, column=0, sticky="nw")

    # Add event handlers
    panSlider.bind("<ButtonRelease-1>", lambda e: change_pan())
    tiltSlider.bind("<ButtonRelease-1>", lambda e: change_tilt())

    # Beam section
    beamFrame = tk.Frame(root, width=200, height=200,
                         highlightbackground="black", highlightthickness="1")
    beamFrame.grid(row=1, column=5, sticky="nw")
    beamFrame.grid_propagate(False)

    # Shutter slider
    shutterLabel = tk.Label(beamFrame, text="Shutter:")
    shutterLabel.grid(row=0, column=0, sticky="nw")
    shutterSlider = tk.Scale(beamFrame, from_=0, to=255, orient=tk.HORIZONTAL)
    shutterSlider.grid(row=1, column=0, sticky="nw")

    # Add event handler
    shutterSlider.bind("<ButtonRelease-1>", lambda e: change_shutter())


def playback_change(slider: tk.Scale, playback: int):
    global artnetConnection, playbackSliders
    # artnetConnection.set_playback(playback, slider.get())


def bump_playback(playback: int):
    global artnetConnection
    # artnetConnection.bump_playback(playback)


def create_playback_frames(root: tk.Tk):
    # slider 1 | slider 2 | slider 3 | slider 4 | slider 5
    #  bump 1 |  bump 2  |  bump 3  |  bump 4  |  bump 5
    global bumpButtons, playbackSliders, recordButton
    # Create a frame for the sliders
    sliderFrame = tk.Frame(root, width=325, height=200,
                           highlightbackground="black", highlightthickness="1")
    sliderFrame.grid(row=4, column=0, sticky="nw")
    sliderFrame.grid_propagate(False)
    for i in range(5):
        # Create a slider for each playback
        slider = tk.Scale(sliderFrame, from_=0, to=255, orient=tk.VERTICAL)
        slider.grid(row=0, column=i, sticky="nw")
        slider.bind("<ButtonRelease-1>", lambda e: playback_change(slider, i))
        playbackSliders.append(slider)

        # Create a bump button for each playback
        bumpButton = tk.Button(sliderFrame, text=f"Bump {i+1}")
        bumpButton.grid(row=1, column=i, sticky="nw")
        bumpButtons.append(bumpButton)
        bumpButton.bind("<ButtonRelease-1>", lambda e: bump_playback(i))

    # Record button
    recordButton = tk.Button(sliderFrame, text="Record")
    recordButton.grid(row=0, column=5, sticky="nw")


def main():
    global artnetConnection
    atnetSetup = setup_window.setup_window()
    artnetConnection = StupidArtnet(
        atnetSetup[0], atnetSetup[3], atnetSetup[2], atnetSetup[1])
    try:
        artnetConnection.start()
    except:
        # error message if not establishable

        pass

    # Initialal setup
    if (not os.path.exists(os.path.join(os.getcwd(), "heads"))):
        os.mkdir(os.path.join(os.getcwd(), "heads"))

    global rigsDB
    rigsDB = sqlite3.connect(os.path.join(os.getcwd(), "src", "rigs.db"))
    rigs = get_rigs()

    global root, headsList, addHeadButton, delete_headButton
    root = tk.Tk()
    root.title(f"OliQ V" + str(info[0].split("=")[1]))
    # mazimised window
    root.state("zoomed")
    root.bind("<Escape>", lambda e: root.destroy())

    # Show selector button, always in the top left corner
    select_showButton = tk.Button(root, text="Show Selector",
                                  command=lambda: select_show())
    select_showButton.grid(row=0, column=0, sticky="nw")

    # Create a resizable section on the left
    headsFrame = tk.Frame(root, width=200, height=500)
    headsFrame.grid(row=1, column=0, sticky="nw")
    headsFrame.grid_propagate(False)

    # Add head button
    addHeadButton = tk.Button(headsFrame, text="Add Head",
                              command=lambda: addHead.addHead(root, rigsDB,
                                                              selected_rig))
    addHeadButton.grid(row=0, column=0, sticky="nw")

    # Delete selected head(s) button
    delete_headButton = tk.Button(headsFrame, text="Delete Head(s)",
                                 command=lambda: delete_head(headsList.curselection()))
    delete_headButton.grid(row=0, column=1, sticky="nw")

    delete_headButton["state"] = "disabled"
    addHeadButton["state"] = "disabled"

    # Create a selection list for the heads
    headsList = tk.Listbox(headsFrame, width=200, height=1000)
    headsList.grid(row=1, column=0, sticky="nw")
    headsList.grid_propagate(False)

    create_attrtibute_frames(root)
    # create_playback_frames(root)

    # Main window
    root.mainloop()


if __name__ == '__main__':
    main()

import tkinter as tk
from tkinter.colorchooser import askcolor
from main import selectColor

def create_attrtibute_frames(root: tk.Tk):
    # a 4x4 grid for attributes. Each frame has a black outline
    # Intensity | Color
    # Position  | Beam

    #Intensity section
    intensityFrame = tk.Frame(root, width=200, height=100, 
                              highlightbackground="black", highlightthickness=1)
    intensityFrame.grid(row=1, column=2, sticky="nw")
    intensityFrame.grid_propagate(False)

    # Intensity label
    intensityLabel = tk.Label(intensityFrame, text="Intensity:")
    intensityLabel.grid(row=0, column=0, sticky="nw")

    # Intensity slider
    intensitySlider = tk.Scale(intensityFrame, from_=0, to=255, orient=tk.HORIZONTAL)
    intensitySlider.grid(row=0, column=0, sticky="nw")


    # Color section
    colorFrame = tk.Frame(root, width=200, height=500, 
                              highlightbackground="black", highlightthickness=1)
    colorFrame.grid(row=1, column=3, sticky="nw")
    colorFrame.grid_propagate(False)

    # Color picker
    colorPicker = tk.Button(colorFrame, text="Color Picker", command=lambda: 
                            selectColor())
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


    # Position section
    positionFrame = tk.Frame(root, width=200, height=500, 
                              highlightbackground="black", highlightthickness=1)
    positionFrame.grid(row=2, column=2, sticky="nw")
    positionFrame.grid_propagate(False)

    # Beam section
    beamFrame = tk.Frame(root, width=200, height=1000)
    beamFrame.grid(row=2, column=3, sticky="nw")
    beamFrame.grid_propagate(False)

def create_playbacks(root: tk.Tk):
    playbackFrame = tk.Frame(root, width=500, height=500, 
                              highlightbackground="black", highlightthickness=1)
    playbackFrame.grid(row=1, column=4, sticky="nw")
    playbackFrame.grid_propagate(False)

    playbackFaderFrame = tk.Frame(playbackFrame, width=500, height=500,
                                    highlightbackground="black", 
                                    highlightthickness=1)
    playbackFaderFrame.grid(row=1, column=0, sticky="nw")
    playbackFaderFrame.grid_propagate(False)

    playbackButtonFrame = tk.Frame(playbackFrame, width=500, height=500,
                                    highlightbackground="black", 
                                    highlightthickness=1)
    playbackButtonFrame.grid(row=2, column=0, sticky="nw")
    playbackButtonFrame.grid_propagate(False)

    global playbackButtons, playbackFaders
    for i in range(0, 10):
        playbackFaders.append(tk.Scale(playbackFaderFrame, from_=0, to=255, 
                                       orient=tk.VERTICAL))
        playbackFaders[i].grid(row=1, column=i, sticky="nw")
        playbackButtons.append(tk.Button(playbackButtonFrame, text=str(i+1)))
        playbackButtons[i].grid(row=0, column=i, sticky="nw")
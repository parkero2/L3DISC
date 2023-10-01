import tkinter as tk
import os
import sys
import ifaddr

# Return 
# target_IP from a list of available adapters
# universe from a list of available universes (default 0)
# packet_size from a list of available packet sizes (default 512)
# tans_rate from a list of available transmission rates (default 30)

targetIP_var, transRate_var, packetSize_var, universe_var = None, None, None, None

def setup_window() -> (str, int, int, int):
    setup_window_window()
    return (targetIP_var.get(), transRate_var.get(), packetSize_var.get(), universe_var.get())

def get_adaptor_addresses():
    adaptors = ifaddr.get_adapters()
    addresses = []
    for adaptor in adaptors:
        for ip in adaptor.ips:
            #For each IP of each adaptor
            if (ip.is_IPv4): #Filter non IPv4 addresses
                addresses.append(ip.ip)
    return addresses


def setup_window_window():
    root = tk.Tk()
    root.title("OliQ Setup")

    global targetIP_var, transRate_var, packetSize_var, universe_var

    targetIP_var = tk.StringVar(value=str(get_adaptor_addresses()[0]))
    transRate_var = tk.IntVar(value=30)
    packetSize_var = tk.IntVar(value=512)
    universe_var = tk.IntVar(value=0)

    # Target IP selection and formatting
    targetIP_label = tk.Label(root, text="Target IP\nThis is the IP your Artnet device is listening on")
    targetIP_label.grid(row=0, column=0, sticky="nsew")
    targetIP_droptdown = tk.OptionMenu(root, targetIP_var, *get_adaptor_addresses())
    targetIP_droptdown.grid(row=0, column=2, sticky="nsew")

    # Transmission rate selection and formatting
    transRate_label = tk.Label(root, text="Transmission Rate\nThis is the rate at which the Artnet device will receive data")
    transRate_label.grid(row=2, column=0, sticky="nsew")
    transRate_droptdown = tk.OptionMenu(root, transRate_var, *[30, 40, 50, 60, 70, 80, 90, 100])
    transRate_droptdown.grid(row=2, column=2, sticky="nsew")

    # Packet size selection and formatting
    packetSize_label = tk.Label(root, text="Packet Size\nThis is the size of the packet that will be sent to the Artnet device AKA universe size")
    packetSize_label.grid(row=3, column=0, sticky="nsew")
    packetSize_droptdown = tk.OptionMenu(root, packetSize_var, *[10, 100, 206, 512, 1024, 2048, 4096])
    packetSize_droptdown.grid(row=3, column=2, sticky="nsew")

    # Universe selection and formatting
    universe_label = tk.Label(root, text="Universe\nThis is the universe that will be sent to the Artnet device (usually 0)")
    universe_label.grid(row=4, column=0, sticky="nsew")
    universe_droptdown = tk.OptionMenu(root, universe_var, *range(0, 15))
    universe_droptdown.grid(row=4, column=2, sticky="nsew") 


    # Submit button, returns data to main.py
    submit_button=tk.Button(root, text="Submit", command=lambda: [root.destroy()])
    submit_button.grid(row=5, column=1, sticky="nsew")

    root.mainloop()
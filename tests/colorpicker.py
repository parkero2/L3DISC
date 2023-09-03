from stupidArtnet import StupidArtnet
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor

target_ip = '192.168.56.1'
universe = 0
packet_size = 100	

root = tk.Tk()
root.title('Tkinter Color Chooser')
root.geometry('300x150')

a = StupidArtnet(target_ip, universe, packet_size, 30, True, True)
a.clear()
a.start()
a.set_single_value(1, 255) #intensity channel

def change_color():
    colors = askcolor(title="Tkinter Color Chooser")
    a.set_single_value(2, colors[0][0])
    a.set_single_value(3, colors[0][1])
    a.set_single_value(4, colors[0][2])
    root.configure(bg=colors[1])


ttk.Button(root, text='Select a Color',command=change_color).pack(expand=True)


root.mainloop()

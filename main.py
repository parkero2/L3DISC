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
import pyartnet

from PIL import Image, ImageTk

import setupWindow


with open(os.path.join(os.getcwd(), "info.txt"), 'r') as f:
    info = f.read().splitlines()

def main():
    args = sys.argv #get args from command line
    setupWindow.setupWindow()
    

if not __name__ == '__main__':
    setupWindow.setupWindow()
else:
    main()
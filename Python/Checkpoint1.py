"""
Calls a series of pySimpleGUI demonstration functions and collects
output for use in GUI lab.
Author: Long Pham
Date: 10-Sep-2025
"""


"""
Displays a window showing all themes, then prints them out.
Parameters
width : int
Number of theme names printed per line. Default is 4.
Returns
Nothing.
Author: Jo Blo
"""

import FreeSimpleGUI as sg
from datetime import datetime
import matplotlib
import time
import matplotlib.pyplot as plt
import numpy as np
import csv
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

theme = "BlueMono"
themeList = sg.theme_list()

def initialiseGUI(windowName : str, theme : str, layout):
    """
    Displays a window showing all themes, then prints them out.

    Parameters
    ----------
    windowName : str
        The name of the window to be initialised
    theme : str
        The name of a valid theme string
    layout : Array[sg elements]
        An array containing the SG layout setup for the window
    ----------
    Returns
    Window class object.
    Author: Long Pham
    """

    try:
        if theme in themeList:
            sg.theme(theme)
        else:
            raise ValueError("Ensure that a correct PySimpleGUI theme is inputted. Default theme will be set to dark blue.") 
    except (ValueError) as e:
        print("Error", e)
    window = sg.Window(windowName, layout, finalize = True)
    return window

layout = [
            [sg.Canvas(key='-CANVAS-')],
            [sg.Text("Enter some text then push GO\n(note the time display in your command line interface):", font='All 10 italic', key="INSTRUCT_TEXT")],
            [sg.Input(key="INPUT_BOX")],
            [sg.Text(f"You are currently using Theme: {theme}", key="DISPLAY_TEXT")],
            [sg.Button("Exit", key="EXIT_BUTTON")]
]

window = initialiseGUI("Window 1", theme, layout)
event, values = window.read()

while True: 
        # read from window
        event, values = window.read(timeout=0)

        if event == "EXIT_BUTTON":
              break

window.close()
print("Exited correctly!")
print(initialiseGUI.__doc__)
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
NUM_BUTTONS = 5
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
    sg.Window 
        A Window class object.
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

def createButtonArray(numButtons):
    """
    Creates an array of sg.Button objects stored in an array.

    Parameters
    ----------
    numButtons : int
        Number of buttons to display. Minimum value is 1, maximum is 10
    ----------
    Returns
    Array[sg.Button]
        An array containing numButtons number of buttons
        The buttons are keyed by their name in the following format:
        "NORMAL_BUTTON_{i}"
        Where i is the index
    Author: Long Pham
    """
    if 0 < numButtons < 10:
        buttonArray = []
        for i in range(1,numButtons+1):
            buttonArray.append(sg.Button(f"Button {i}", key = f"NORMAL_BUTTON_{i}"))

    return buttonArray

buttonArray = createButtonArray(NUM_BUTTONS)
layout = [[sg.Text("Press a button!", key = "INSTRUCTION_TEXT")],
        [buttonArray],
        [sg.Text("Will return the button output!", key = "DISPLAY_TEXT")],
        [sg.Button("Exit", key="EXIT_BUTTON")]
        ]

window = initialiseGUI("Window 1", theme, layout)
event, values = window.read()

while True:
        
    # read from window
    event, values = window.read(timeout=0)

    if event == "EXIT_BUTTON" or sg.WIN_CLOSED:
        break

    elif event.startswith("NORMAL_BUTTON_"):
        input_text = f"You pressed {event}"
        print(input_text)
        window['DISPLAY_TEXT'].update(input_text)
    

window.close()
print("Exited correctly!")

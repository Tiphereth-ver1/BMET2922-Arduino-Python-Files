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
dim = (500,300)

def initialiseGUI(windowName : str, theme : str, layout, dim : tuple):
    """
    Displays a window showing all themes, then prints them out.

    Parameters
    ----------
    windowName : String
        The name of the window to be initialised
    theme : String
        The name of a valid theme string
    layout : Array[sg elements]
        An array containing the SG layout setup for the window
    dim : tuple
        A tuple containing the dimensions for the window
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
    window = sg.Window(windowName, layout, finalize = True, size = dim)
    return window

def createSliderArray(minVal : int, maxVal: int, numSliders : int, orient : str):
    """
    Creates an array of sg.Slider objects stored in an array.

    Parameters
    ----------
    minVal : int
        Smallest value on the created sliders
    maxVal : int
        Largest value on the created sliders
    numSliders : int
        Number of sliders to display. Minimum value is 1, maximum is 10
    orient : str
        Orientation of the sliders created
        May choose from vertical or horizontal
    ----------
    Returns
    Array[sg.Button]
        An array containing numButtons number of buttons
        The buttons are keyed by their name in the following format:
        "Slider{i}"
        Where i is the index
    Author: Long Pham
    """
    if 0 < numSliders < 10:
        sliderArray = []
        for i in range(1,numSliders+1):
            sliderArray.append(sg.Slider((minVal,maxVal), f"Slider {i}", orientation = orient, key = f"Slider{i}", enable_events = True))

    return sliderArray

def createListbox(data : list, name : str):
    """
    Creates a sg.Listbox object.

    Parameters
    ----------
    data : list
        A list of the data to be used in the listBox. The default is a list of integers 0-9.
    name : str
        The key to assign the created Listbox object.
    ----------
    Returns
    sg.Combo
        a Combo object with the data parameter as its list.
    Author: Long Pham
    """
    return sg.Combo(data, key = name, readonly=True, size=(20,10))

def changeTheme(theme : str):
    """
    Changes the theme used in pySimpleGUI. May be used during runtime at any point.

    Parameters
    ----------
    theme : str
        The name of the theme to change to
    ----------
    Returns
    Nothing.

    Author: Long Pham
    """
    try:
        if theme in themeList:
            sg.theme(theme)
        else:
            raise ValueError("Ensure that a correct PySimpleGUI theme is inputted. Default theme will be set to dark blue.") 
    except (ValueError) as e:
        print("Error", e)

def rebuild_window(theme, dim):
    sliderArray = createSliderArray(0,10,NUM_BUTTONS,"vertical")

    layout = [[createListbox(sg.theme_list(),"THEME_LISTBOX")],
          [sg.Text("Move a slider!!", key = "INSTRUCTION_TEXT")],
          [sliderArray],
          [sg.Text("Will return the slider output!", key = "DISPLAY_TEXT")],
          [sg.Button("Exit", key="EXIT_BUTTON"), sg.Button("Change theme", key = "CHANGE_BUTTON")]
        ]
    
    return initialiseGUI("Window 1", theme, layout, dim)




sliderArray = createSliderArray(0,10,NUM_BUTTONS, "vertical")
layout = [[createListbox(sg.theme_list(),"THEME_LISTBOX")],
          [sg.Text("Move a slider!!", key = "INSTRUCTION_TEXT")],
          [sliderArray],
          [sg.Text("Will return the slider output!", key = "DISPLAY_TEXT")],
          [sg.Button("Exit", key="EXIT_BUTTON"), sg.Button("Change theme", key = "CHANGE_BUTTON")]
        ]

window = initialiseGUI("Window 1", theme, layout, dim)
enable_events = True
event, values = window.read()

while True:
        
    # read from window
    event, values = window.read(timeout=0)

    if event == "EXIT_BUTTON" or sg.WIN_CLOSED:
        break

    if event == "CHANGE_BUTTON":
        new_theme = values["THEME_LISTBOX"] if values["THEME_LISTBOX"] else theme
        window.close()
        window = rebuild_window(new_theme, dim)
    elif event.startswith("Slider"):
        slider_value = values[event]
        input_text = f"You moved {event} to {slider_value}"
        print(input_text)
        window['DISPLAY_TEXT'].update(input_text)    

window.close()
print("Exited correctly!")

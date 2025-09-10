"""
This program provides a simple of example of how to create and run a PySimpleGUI window.

Author:
Daniel Babekuhl
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


# Step 0000: Import csv and have data prepared here!
SAMPLE_TIME = 0.02
total_length = 0

# Step 000: Import csv and have data prepared here!
with open('pulse.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    wave = []
    pulse = []
    for row in csvReader:
        wave.append(int(row[0]))
        pulse.append(float(row[1]))
    if len(wave) == len(pulse):
        total_length = len(wave)
    else:
        print("Ensure CSV is formatted correctly")

timer = np.arange(0, total_length*SAMPLE_TIME, SAMPLE_TIME)
count = 0
scope = 100
interval = 0.5
next_time = time.time() + interval
index = 0


# Step 00: Define all necessary functions and global variables here
matplotlib.use('TkAgg')
def draw_figure(canvas, figure):
    """
    Initialises a figure in matplotlib

    Parameters
    ----------
    canvas : str
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


    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def redraw_figure(figure_canvas_agg):
    """
    Updates the figure implementation figure in matplotlib.
    Uses the matlabFigure() function.

    ----------
    figure_canvas_agg : FigureCanvasTkAgg
        The object that assigns the figure to the canvas
    ----------
    Returns
        FigureCanvasTkAgg object. 

    Author: Long Pham
    """
    matlabFigure()
    figure_canvas_agg.draw()
    return figure_canvas_agg

def create_message(index):
      if (index%5 == 0):
            return f"You've tried to exit {index} times already? Baka, this ain't the right button."
      else:
            return f"Don't be so mean, you've already tried to leave {index} times already."


# Step 0: Implementing matplotlib data
dataFigure = plt.figure("Oh", figsize=(10,5))


def matlabFigure():
        """
        Creates a predefined matplotlib figure using predetermined elements
        Parameters
        ----------
        None
        ----------
        Returns
        None
        Author: Long Pham
        """

        plt.clf()
        plt.subplot(1,2,1)
        plt.title("Heart Rate data")
        plt.plot(timer[count:count+scope], wave[count:(count+scope)])
        plt.ylabel("HR (bpm)")
        plt.xlabel("Time (s)")

        plt.subplot(1,2,2)
        plt.title("Pulse Data")
        plt.plot(timer[count:count+scope], pulse[count:(count+scope)])
        plt.ylabel("Pulse (units)")
        plt.xlabel("Time (s)")

matlabFigure()

# Step 1: create window layout. Note that the layout in the code resembles the layout
sg.theme("BrightColors")
layout = [
            [sg.Canvas(key='-CANVAS-')],
            [sg.Text("Enter some text then push GO\n(note the time display in your command line interface):", font='All 10 italic', key="INSTRUCT_TEXT")],
            [sg.Input(key="INPUT_BOX")],
            [sg.Text("<your text will display here>", key="DISPLAY_TEXT")],
            [sg.Text("A fun message will display here", key="ALT_DISPLAY_TEXT")],
            [sg.Canvas(key='-CANVAS-')],
            [sg.Button("GO", key='GO_BUTTON'), sg.Button("Progress Plot", key="PROGRESS_BUTTON"), sg.Button("EXIT", key='EXIT_BUTTON_FALSE'), sg.Button("Exit", key="EXIT_BUTTON")]
]

# Step 2: create Window and pass it the layout.
window = sg.Window("Window 1", layout, finalize=True)
canvasFigure = draw_figure(window['-CANVAS-'].TKCanvas, dataFigure)
event, values = window.read()

layout2 = [[sg.Text("I lived bitch")]]

# Step 3: read from window in an infinite loop. If the user interacts, execute relevant
# code then return to reading from the window.
print()
while True:
        
        # read from window
        event, values = window.read(timeout=20)

        # process user interactions
        # User exits
        if event in (sg.WIN_CLOSED, "EXIT_BUTTON"):
              window2 = sg.Window("Window 1", layout2, finalize=True)
              event, values = window.read()
              break
        # User pressed GO button: update window to display the user's input text
        if event == "GO_BUTTON":
                input_text = values['INPUT_BOX']
                window['DISPLAY_TEXT'].update(input_text)
                window['ALT_DISPLAY_TEXT'].update("Ready... set... go!")
        
        if event == "EXIT_BUTTON_FALSE":
                index += 1
                alt_input_text = create_message(index)
                window['ALT_DISPLAY_TEXT'].update(alt_input_text)
        
        if event == "PROGRESS_BUTTON":
                window['ALT_DISPLAY_TEXT'].update("You do know it's progressing already?")
                
        #Automatic updating of the canvas
        if (count + scope < total_length):
              count += 3
              redraw_figure(canvasFigure)
        elif(count + scope > total_length):
              count = 0
              redraw_figure(canvasFigure)

        # Print current time to terminal to show that loop runs continuously
        print(f"{datetime.now()}        \r", end='')

# step 4: user pushed the exit button or closed the window.
window.close()
print("\nGoodbye.")

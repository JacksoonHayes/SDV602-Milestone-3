"""
Pan Left button controller
"""
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import view.data_explorer_view as dev

# The 'accept' function is the event handler for the pan left action.
def accept(event, values, state):
    keep_going = True

    if event == '>':
            fig, ax = plt.subplots()
            state['axis'] = ax 
            axis = state['axis']
            factor = 0.1  # The factor by which to pan

            # Perform the pan left action
            xmin, xmax = axis.get_xlim()
            shift = (xmax - xmin) * factor
            axis.set_xlim(xmin + shift, xmax + shift)
            
            dev

    return keep_going

"""
Exit button controller
"""
import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg


def accept(event, values, state):
    """
    Determines whether to keep the program running or exit based on the event.

    Parameters:
        event (str): The event triggered by the user.
        values (dict): The current values of the GUI elements.
        state (dict): The current state of the program.

    Returns:
        bool: True to keep the program running, False to exit.
    """
    keep_going = True
    if event == "Exit":
        sg.WIN_CLOSED
        keep_going = False
    else:
        keep_going = True

    return keep_going

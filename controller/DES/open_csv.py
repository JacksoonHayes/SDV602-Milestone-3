"""
OpenCSV button controller
"""
import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg
from model.model import Model

def accept(event, values, state):
    """
    Process the event and values to open a CSV file.

    Parameters:
        event (str): The event triggered by the user.
        values (dict): The values passed from the GUI.
        state (dict): The current state of the application.

    Returns:
        bool: True if the function successfully opens a CSV file, False otherwise.
    """
    keep_going = True
    if event == 'Open CSV':
        file_name = sg.PopupGetFile('Please select a CSV file to open', file_types=(("Comma separated value", "*.csv"),)) 
        if file_name is not None:
            view = state['view']
            view.update_data_from_csv(values, file_name)
    return keep_going
"""
Exit button controller
"""
import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg


def accept( event, values,state):
    
    keep_going = True
    if event == "Exit":
        sg.WIN_CLOSED
        keep_going = False
        
    else:
        keep_going = True

    return keep_going 
"""
Register Window controller
"""
import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def accept( event, values,state):
    from view.user_register_view import RegisterView
    keep_going = True
    if event == "Register":   
        # Just testing
        print("Got RegisterWindow")
        register_view = RegisterView()
        register_view.set_up_layout()
        register_view.render()
        register_view.accept_input()
    else:
        keep_going = True

    return keep_going 
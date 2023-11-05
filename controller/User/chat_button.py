"""
Chat Controller
"""
import sys
from time import sleep
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def accept( event, values,state):
    
    keep_going = True
    if event == "Send":   
        # Just testing
        print("Got Chat - just testing")

        # Work with a UserManager object
        from model.user_manager import UserManager
        a_user_manager = UserManager()
        # get user name and password from the "values" or "state"
        message = values['Message']
        print(f"Got Message = {message}  - just testing")

        message_result = a_user_manager.chat(message)
        print(f"Got login result: {message_result}")


    else:
        keep_going = True

    return keep_going 
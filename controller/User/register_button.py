"""
Register controller
"""
import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def accept(event, values, state):
    
    keep_going = True
    if event == "Submit":   
        
        # Work with a UserManager object
        from model.user_manager import UserManager
        a_user_manager = UserManager()

        # get user name and password from the "values" or "state"
        user_name = values['User']
        password = values['Password']
        
        register_result = a_user_manager.register(user_name,password)
        print(f"Register result: {register_result}")

    else:
        keep_going = True

    return keep_going 
"""
Login controller
"""
import sys
sys.dont_write_bytecode = True
from view.chat_view import ChatView
import PySimpleGUI as sg

def accept(event, values, state):
    
    keep_going = True
    if event == "Login":   

        # Work with a UserManager object
        from model.user_manager import UserManager
        a_user_manager = UserManager()

        # get user name and password from the "values" or "state"
        user_name = values['User']
        password = values['Password']

        login_result = a_user_manager.login(user_name,password)
        print(f"Login result: {login_result}")

        if login_result == "Login Success":
            UserManager.current_screen ="A TEST"
            chat_view = ChatView()
            chat_view.set_up_layout()
            chat_view.render()
            chat_view.accept_input()

        
    else:
        keep_going = True

    return keep_going 
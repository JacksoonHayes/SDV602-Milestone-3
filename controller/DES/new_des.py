"""
New DES button controller
"""
import sys
import PySimpleGUI as sg
from model.user_manager import UserManager

sys.dont_write_bytecode = True

def accept( event, values, state):
    from view.data_explorer_view import DES_View
    
    keep_going = True
    if event == 'New DES':
        user_manager = UserManager()
        if user_manager.current_screen != None:
            sg.popup_error('You already have an active Data Explorer screen.')
        else:
            des_obj = DES_View()
            des_obj.set_up_layout()
            des_obj.render()
            des_obj.accept_input()
            # Update the user's active screen status
            user_manager.update_active_screen(state['current_user'], des_obj)
    return keep_going
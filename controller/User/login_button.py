"""
Login controller
"""
import sys
sys.dont_write_bytecode = True
from view.data_explorer_view import DES_View
from model.network.jsn_drop_service import jsnDrop
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
        
        
        # <<<<<<<<<<<< function that selects user des number record self.jsnDrop.select("tblUser", f"PersonID = '{user_id}'") >>>>>>>>>>>>>>>>
        # put it in user_screen below.

        if login_result == "Login Success":
            # user_screen = 
            # UserManager.current_screen =
            
            des_obj = DES_View()
            des_obj.set_up_layout()
            des_obj.render()
            des_obj.accept_input()
            UserManager.set_current_DES(des_obj)
            des_obj.des_list.append(des_obj)

        
    else:
        keep_going = True

    return keep_going 
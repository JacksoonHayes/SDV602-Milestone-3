"""
Data Explorer
An example module. Read here about Python documentation: https://ecampus.nmit.ac.nz/moodle/mod/page/view.php?id=1140770

Details about this module.

This module is actually main app.
The main data explorer view is the default View.
It uses controllers for code that runs when GUI actions are happening.

The approach to be taken is to replace the PySimple GUI event loop - the "while" for a Window, with calls to controllers.
Each Controller decides which View to show, each View is linked to Controllers. 
Each controller accepts an input action from the GUI presented or rendered by View.

Thoughts 
This could be an equivalent to a Router ...



"""
import sys
from model.network.jsn_drop_service import jsnDrop
from view import chat_view
sys.dont_write_bytecode = True
from view.data_explorer_view import DES_View
from view.user_login_view import LoginView
from view.chat_view import ChatView



if __name__ == "__main__" :
    """
    Code that runs when this is the main module.
    """
    #des_obj = DES_View()
    #des_obj.set_up_layout()
    #des_obj.render()
    
    #des_obj.accept_input()
    
    # drop_service = jsnDrop("66d863d6-9ae2-43a2-b8b4-fac8deab3689", "https://newsimland.com/~todd/JSON")
    # drop_service.drop("tblUser")
    # drop_service.drop("tblChat")

    login_view = LoginView()
    login_view.set_up_layout()
    login_view.render()
    login_view.accept_input()

    pass

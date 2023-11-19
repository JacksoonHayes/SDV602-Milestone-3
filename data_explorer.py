"""
Data Explorer System

Details about this module.

This module is actually main app.
"""
import sys
sys.dont_write_bytecode = True
from view.data_explorer_view import DES_View
from view.user_login_view import LoginView



if __name__ == "__main__" :
    """
    Code that runs when this is the main module.
    """

    login_view = LoginView()
    login_view.set_up_layout()
    login_view.render()
    login_view.accept_input()

    pass

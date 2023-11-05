"""
Register controller
"""
import sys
sys.dont_write_bytecode = True
import PySimpleGUI as sg

def accept( event, values,state):
    
    keep_going = True
    if event == "Register":   
        # Just testing
        print("Got Register - just testing")
        
        # Work with a UserManager object
        
        from model.user_manager import UserManager
        a_user_manager = UserManager()

        # get user name and password from the "values" or "state"
        user_name = values['User']
        password = values['Password']
        print(f"Got User = {user_name} , Password = {password} - just testing")

        
        register_result = a_user_manager.register(user_name,password)
        print(f"REGISTER RESULT {register_result}")
        
        # Just a Test
        #from model.user_manager import testUserManager 
        #testUserManager()



    else:
        keep_going = True

    return keep_going 
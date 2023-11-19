"""
File for the login view of the application.
"""

import PySimpleGUI as sg
import controller.DES.exit_button as exit_button
import controller.User.login_button as login_button
import controller.User.register_window_button as register_window_button

class LoginView(object):
    """
    This class represents the login view of the application.
    It provides methods to set up the layout, render the view, and accept user input.
    """

    def __init__(self):
        self.window = None
        self.layout = []
        self.components = {"has_components": False}
        self.controls = []

    def set_up_layout(self, **kwargs):
        """
        Sets up the layout of the login view.
        """

        sg.theme('DarkGrey5')
        title = ("Century Gothic", 18)
        sg.set_options(font=('Century Gothic', 10))
        
        # define the form layout
        self.components['Title'] = sg.T("Login", font=title)
        self.components['Separator'] = sg.HSeparator(pad=(70, (10, 40)))
        
        self.components['User'] = sg.InputText('', key='User', size=(22, 1))
        self.components['Password'] = sg.InputText('', key='Password', password_char='•', size=(22, 1))
        
        self.components['Login'] = sg.Button(button_text="Login", size=(10, 1))
        self.controls += [login_button.accept]

        self.components['RegisterWindow'] = sg.Button(button_text="Register", size=(10, 1))
        self.controls += [register_window_button.accept]

        self.components['exit_button'] = sg.Exit(size=(5, 1))        
        self.controls += [exit_button.accept]

        row_buttons = [ 
                        self.components['Login'], 
                        self.components['RegisterWindow'],
                        self.components['exit_button'] 
                      ]
        self.layout = [
                        [self.components['Title']],
                        [self.components['Separator']],
                        [sg.Text('Username:'), self.components['User']], 
                        [sg.Text('Password: '), self.components['Password']], 
                        [sg.Text(pad=(0, 30))],
                        row_buttons
                      ]

    def render(self):
        """
        Renders the login view.
        """

        # create the form and show it without the plot
        if self.layout != []:
            self.window = sg.Window('Log in', self.layout, size=(400, 300), grab_anywhere=False, finalize=True, element_justification='c', margins=(0, 20))
  
    def accept_input(self):
        """
        Accepts user input for the login view.
        """

        if self.window != None:
            keep_going = True
            
            while keep_going == True:
                event, values = self.window.read()
                if event == sg.WIN_CLOSED or event == 'Exit':  # always, always give a way out!
                    break
                for accept_control in self.controls:
                    keep_going = accept_control(event, values, {'view': self})
            self.window.close()
        
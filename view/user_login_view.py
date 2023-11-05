import PySimpleGUI as sg
import controller.DES.exit_button as exit_button
import controller.User.login_button as login_button
import controller.User.register_window_button as register_window_button

class LoginView(object):

    def __init__(self):
        
        self.window = None
        self.layout = []
        self.components = {"has_components":False}
        self.controls = []

    def set_up_layout(self,**kwargs):

        sg.theme('LightGreen')
        
        # define the form layout
        
        # one variable per call to sg 
        # if there is a control / input with it add the name to the controls list
        self.components['User'] = sg.InputText('', key='User',size=(10,30))
        self.components['Password'] = sg.InputText('', key='Password', password_char='*',size=(10,30))

        self.components['Login'] = sg.Button(button_text="Login",size=(10, 2))
        self.controls += [login_button.accept]

        self.components['RegisterWindow'] = sg.Button(button_text="Register",size=(10, 2))
        self.controls += [register_window_button.accept]

        self.components['exit_button'] = sg.Exit(size=(5, 2))        
        self.controls += [exit_button.accept]

        row_buttons = [ 
                        self.components['Login'], 
                        self.components['RegisterWindow'],
                        self.components['exit_button'] 
                      ]
        self.components['header'] =   sg.Text('Log in', font=('current 18'))
        self.layout = [
                        
                        [sg.Text('User Name:'),self.components['User'] ], 
                        [sg.Text('Password : '),self.components['Password']], 
                        row_buttons
                      ]

    def render(self):

        # create the form and show it without the plot
        if self.layout != [] :
            self.window =sg.Window('Log in', self.layout, grab_anywhere=False, finalize=True)
  
    def accept_input(self):

        if self.window != None :
            keep_going = True
            
            while keep_going == True:
                event, values = self.window.read()
                for accept_control in self.controls:
                    keep_going = accept_control(event,values,{'view':self})
            self.window.close()
        
import PySimpleGUI as sg
import controller.DES.exit_button as exit_button
import controller.User.register_button as register_button

class RegisterView(object):

    def __init__(self):
        
        self.window = None
        self.layout = []
        self.components = {"has_components":False}
        self.controls = []

    def set_up_layout(self,**kwargs):

        sg.theme('DarkGrey5')
        title = ("Century Gothic", 18)
        sg.set_options(font=('Century Gothic', 10))
        # define the form layout
        
        # one variable per call to sg 
        # if there is a control / input with it add the name to the controls list
        self.components['Title'] = sg.T("Register", font=title)
        self.components['Separator'] = sg.HSeparator(pad=(40, (10, 40)))
        
        self.components['User'] = sg.InputText('', key='User',size=(22, 1))
        self.components['Password'] = sg.InputText('', key='Password', password_char='•',size=(22, 1))

        self.components['Register'] = sg.Button(button_text="Submit",size=(10, 1))
        self.controls += [register_button.accept]

        self.components['exit_button'] = sg.Exit(size=(5, 1))        
        self.controls += [exit_button.accept]

        row_buttons = [ 
                        self.components['Register'], 
                        self.components['exit_button'] 
                      ]
        self.layout = [
                        [self.components['Title']],
                        [self.components['Separator']],
                        [sg.Text('Username:'),self.components['User'] ], 
                        [sg.Text('Password: '),self.components['Password']], 
                        [sg.Text(pad=(0, 30))],
                        row_buttons
                      ]

    def render(self):

        # create the form and show it without the plot
        if self.layout != [] :
            self.window =sg.Window('Register', self.layout, grab_anywhere=False, finalize=True, element_justification='c')
  
    def accept_input(self):

        if self.window != None :
            keep_going = True
            
            while keep_going == True:
                event, values = self.window.read()
                for accept_control in self.controls:
                    keep_going = accept_control(event,values,{'view':self})
            self.window.close()
        
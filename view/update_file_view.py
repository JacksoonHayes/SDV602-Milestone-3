import sys

from PySimpleGUI.PySimpleGUI import timer_start
sys.dont_write_bytecode = True
from typing import Dict
import PySimpleGUI as sg
import inspect
import controller.Upload.get_target as get_target_csv
import controller.Upload.get_upload_file as get_upload_csv
import controller.Upload.merge_csv as merge_csv
import controller.DES.exit_button as exit_button

class UpdateView(object):
    """
    A class representing the update view for a file.

    Attributes:
        window: The window object for the view.
        layout: The layout of the view.
        components: A dictionary of components in the view.
        controls: A list of controls in the view.
        target_file_path: The path of the target file.
        upload_file_path: The path of the upload file.
        explorer_view: The explorer view object.
        explorer_values: The values of the explorer view.

    Methods:
        update_component_text: Updates the text of a component.
        update_upload_file: Updates the upload file path.
        update_target_file: Updates the target file path.
        set_up_layout: Sets up the layout of the view.
        render: Renders the view.
        accept_input: Accepts user input.
    """

    def __init__(self):
        self.window = None
        self.layout = []
        self.components = {"has_components": False}
        self.controls = []
        self.target_file_path = ""
        self.upload_file_path = ""
        self.explorer_view = None
        self.explorer_values = None

    def update_component_text(self, component_name, text):
        """
        Updates the text of a component.

        Args:
            component_name: The name of the component.
            text: The new text for the component.
        """
        if component_name in self.components:
            self.components[component_name].update(text)

    def update_upload_file(self, text):
        """
        Updates the upload file path.

        Args:
            text: The new upload file path.
        """
        self.upload_file_path = text
        self.update_component_text('upload_data_file_name', text)

    def update_target_file(self, text):
        """
        Updates the target file path.

        Args:
            text: The new target file path.
        """
        self.target_file_path = text
        self.update_component_text('target_data_file_name', text)

    def set_up_layout(self, **kwargs):
        """
        Sets up the layout of the view.

        Args:
            **kwargs: Additional keyword arguments.
        """
        sg.theme('DarkGrey5')
        figure_w, figure_h = 650, 650
        # define the form layout

        # one variable per call to sg
        # if there is a control / input with it add the name to the controls list
        self.components['upload_data_file_name'] = sg.Text('No data')
        self.components['select_upload_file'] = sg.Button(button_text="Select Upload CSV", size=(10, 2))
        self.controls += [get_upload_csv.accept]

        self.components['target_data_file_name'] = sg.Text('No data')
        self.components['select_target_file'] = sg.Button(button_text="Select Target CSV", size=(10, 2))
        self.controls += [get_target_csv.accept]

        self.components['merge'] = sg.Button(button_text="Merge CSV", size=(10, 2))
        self.controls += [merge_csv.accept]

        self.components['exit_button'] = sg.Exit(size=(5, 2))
        self.controls += [exit_button.accept]

        row_buttons = [
            self.components['select_upload_file'],
            self.components['select_target_file'],
            self.components['merge'],
            self.components['exit_button']
        ]
        self.components['header'] = sg.Text('Upload data', font=('current 18'))
        self.layout = [
            [self.components['header']],
            [sg.Text('Upload File is:'), self.components['upload_data_file_name']],
            [sg.Text('Target File is: '), self.components['target_data_file_name']],
            row_buttons
        ]

    def render(self):
        """
        Renders the view.
        """
        # create the form and show it without the plot
        if self.layout != []:
            self.window = sg.Window('Upload data', self.layout, grab_anywhere=False, finalize=True)

    def accept_input(self):
        """
        Accepts user input.
        """
        if self.window is not None:
            keep_going = True

            while keep_going:
                event, values = self.window.read()
                for accept_control in self.controls:
                    keep_going = accept_control(event, values, {'view': self})
            self.window.close()
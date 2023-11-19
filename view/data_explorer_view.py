
"""
This file contains the implementation of the DES_View class, which represents the view component of the Data Explorer Screen.
The DES_View class is responsible for creating and managing the graphical user interface (GUI) of the Data Explorer Screen.
It utilizes various libraries such as PySimpleGUI, Matplotlib, and NumPy to display and interact with data visualizations.

The DES_View class provides methods for updating the displayed data, drawing figures, handling user interactions, and managing the chat functionality.
It also includes a set of controls and components that allow users to select different types of data visualizations and interact with them.

The file also imports other modules and classes related to the Data Explorer Screen, such as ChartExamples, exit_button, figure_list_select, new_des, open_csv, chat_button, and uploader.
"""

import threading
import signal
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import inspect
import matplotlib
import sys
sys.dont_write_bytecode = True

import threading
import signal
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import inspect
import matplotlib
import sys
sys.dont_write_bytecode = True

import view.ChartExamples as ce 
import controller.DES.exit_button as exit_button
import controller.DES.figure_list_select as figure_list_select
import controller.DES.new_des as new_des
import controller.DES.open_csv as open_csv
import controller.User.chat_button as chat_button
import controller.Upload.uploader as uploader

from model.user_manager import UserManager 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,  NavigationToolbar2Tk
from model.network.jsn_drop_service import jsnDrop
from threading import Thread

matplotlib.use('TkAgg')

class DES_View(object):
    
    def __init__(self):
        self.jsnDrop = jsnDrop(UserManager.jsn_tok,"https://newsimland.com/~todd/JSON")
        
        self.window = None
        self.figure_agg = None
        self.layout = []
        self.components = {"has_components":False}
        self.controls = []
        self.my_lastfig = None
        self.fig_dict = {'Line Plot':(ce.line_plot,{}),'Plot Dots(discrete plot)':(ce.discrete_plot,{}),
                        'Name and Label':(ce.names_labels,{}),'Plot many Lines':(ce.multiple_plots,{}),
                        'Bar Chart':(ce.bar_chart,{}),'Histogram':(ce.histogram,{'title':'Our Histogram Name'}),
                        'Scatter Plots':(ce.scatter_plots,{}),'Stack Plot':(ce.stack_plot,{}),
                        'Pie Chart 1':(ce.pie_chart1,{}), 'Pie Chart 2':(ce.pie_chart2,{})}
        self.values = None
        # The following will only work if we have logged in!
        # self.JsnDrop = UserManager.this_user_manager.jsnDrop
        # Thread for chat
        self.chat_count = 0
        self.exit_event = threading.Event()
        signal.signal(signal.SIGINT, self.signal_handler)

    def have_selected_graph(self,values):
        return len(values['-LISTBOX-']) > 0
  
    def update_component_text(self,component_name, text):
        if component_name in self.components:
            self.components[component_name].update(text)

    def update_data_from_csv(self,values,file_name):
        from model.model import Model
        model = Model(data_source = file_name)
        fin_liabilities = model.get_column('    D3. Total interest payments as a percentage of household disposable income')
        stats_months = model.get_column('Year')
        self.update_current_data(values,file_name,data=fin_liabilities,x_values=stats_months,y_values=fin_liabilities,
                                    x_label='Year Month',y_label='Interest %',title_label='Interest payments % of disposable income')

    def update_current_data(self,values,file_name=None, **kwargs):
        if self.have_selected_graph(values) : 
            the_file_name = file_name
            choice = values['-LISTBOX-'][0] 
            (func,args) = self.fig_dict[choice]
            for arg_name in kwargs:
                args[arg_name] = kwargs[arg_name]
            
            if 'file_name' in args :
                the_file_name = args['file_name']
            if the_file_name != None :
                args['file_name'] = the_file_name
            else:
                the_file_name = "No data"
            self.update_component_text('data_file_name',the_file_name)
            self.fig_dict[choice] = (func,args)
            self.figure_list_draw(values)

        
    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()

        # Check if a toolbar already exists and delete or hide it
        if hasattr(self, 'toolbar'):
            self.toolbar.destroy()

        self.toolbar = NavigationToolbar2Tk(figure_canvas_agg, self.window['-CANVAS TOOLS-'].TKCanvas)
        self.toolbar.update()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

        return figure_canvas_agg

    def delete_figure_agg(self, figure_agg):
        if self.figure_agg:
            self.figure_agg.get_tk_widget().forget()
        plt.close('all')

        # Also delete or hide the toolbar
        if hasattr(self, 'toolbar'):
            self.toolbar.destroy()

    def figure_list_draw(self,values):
        
        if self.have_selected_graph(values) :
            choice = values['-LISTBOX-'][0]                 # get first listbox item chosen (returned as a list)
            func_tuple = self.fig_dict[choice]                         # get function to call from the dictionary
            kwargs = func_tuple[1]
            
            func = func_tuple[0]
            
            
            self.window['-SUMMARY-'].update(inspect.getsource(func))  # show source code to function in multiline
            
            fig = func(**kwargs)                                    # call function to get the figure
            
            # ** IMPORTANT ** Clean up previous drawing before drawing again
            self.delete_figure_agg(self.figure_agg)


            the_file_name = "No Data"
            if 'file_name' in kwargs:
                the_file_name = kwargs['file_name']
            self.update_component_text('data_file_name',the_file_name)
            
            self.figure_agg = self.draw_figure(self.window['-CANVAS-'].TKCanvas, fig)  # draw the figure

    def signal_handler(self,signum, frame):
        self.exit_event.set()   

    def set_up_chat_thread(self):
        UserManager.chat_thread = Thread(target=self.chat_display_update,args=(UserManager,))
        UserManager.chat_thread.setDaemon(True)
        UserManager.stop_thread = False
        UserManager.chat_thread.start()

    def chat_display_update(self, UserManager):
        # Check there is a window before sending an event to it
        if self.window is not None:
            self.chat_count += 1
            # Go to network service to get the Chats
            result = self.jsnDrop.select("tblChat", f"DESNumber = '{UserManager.current_screen}'")
            print(result)

            # Check if result is a list of dictionaries and has data to process
            if isinstance(result, list) and all(isinstance(item, dict) and 'Time' in item for item in result):
                # Sort the result records by the Time field
                sorted_chats = sorted(result, key=lambda k: k['Time'])

                for record in sorted_chats:
                    if UserManager.latest_time is None or record['Time'] > UserManager.latest_time:
                        # Format and append new message to chat list
                        new_message = f"{record['PersonID']}[{record['Chat']}]\n"
                        UserManager.chat_list.append(new_message)

                # Update latest_time with the timestamp of the latest message
                if sorted_chats:
                    latest_record = sorted_chats[-1]
                    UserManager.latest_time = latest_record['Time']

                # Keep number of messages down to a desired history length (e.g., 5)
                history_length = 5
                if len(UserManager.chat_list) > history_length:
                    UserManager.chat_list = UserManager.chat_list[-history_length:]

                # Makes a string of messages to update the display
                Update_Messages = ''.join(UserManager.chat_list)

                # Send the Event back to the window if we haven't already stopped
                if not UserManager.stop_thread:
                    # Send the event back to the window
                    self.window.write_event_value('-CHATTHREAD-', Update_Messages)


   

    def set_up_layout(self,**kwargs):
        
        sg.theme('DarkBrown6')
        figure_w, figure_h = 640, 480
        # define the form layout
        listbox_values = list(self.fig_dict)
        
        # print(f"GOT List box {listbox_values}")
        
        # one variable per call to sg 
        # if there is a control / input with it add the name to the controls list
        
        # COL 1
        self.components['figures_list'] =  sg.Listbox(values=listbox_values, enable_events=True, size=(24, len(listbox_values)), key='-LISTBOX-')
        self.controls += [figure_list_select.accept]

        self.components['uploader'] = sg.Button(button_text="Upload CSV",size=(10, 2))
        self.controls += [uploader.accept]
        
        self.components['select_file'] = sg.Button(button_text="Open CSV",size=(10, 2))
        self.controls += [open_csv.accept]
        
        col_listbox = [
            [sg.Text('', pad=(0, (10, 0)), background_color='#3F3F3F')],
            [self.components['figures_list']],
            [self.components['uploader'], self.components['select_file']]
        ]
        
        self.components['list_box_col'] = sg.Col(col_listbox, element_justification='c', background_color='#3F3F3F')
        
        # COL 2
        self.components['canvas'] = sg.Canvas(size=(figure_w, figure_h), key='-CANVAS-')
        self.components['toolbar'] = sg.Canvas(size=(figure_w, 40), key='-CANVAS TOOLS-')
        
        col_canvas = [
            [self.components['canvas']],
            [self.components['toolbar']]
        ]
        
        self.components['canvas_col'] = sg.Col(col_canvas, element_justification='c', background_color='#3F3F3F')
        
        # COL 3
        self.components['summary'] = sg.MLine(size=(28, 12), key='-SUMMARY-')
        self.components['ChatDisplay'] = sg.Multiline(autoscroll=True,disabled=True, key='ChatDisplay',size=(28,13))
        self.components['Message'] =sg.Input(key='Message',size=(22,1))
        self.components['Send'] = sg.Button('Send', key='Send', size=(5,1))
        self.controls += [chat_button.accept]
          
        col_multiline = [
            [sg.Text('Summary', background_color='#3F3F3F')],
            [self.components['summary']],
            [sg.Text('Chat', pad=(0, (21, 0)), background_color='#3F3F3F')],
            [self.components['ChatDisplay']], 
            [self.components['Message'], self.components['Send']]   
        ]
        self.components['summary_chat_col'] = sg.Col(col_multiline, element_justification='c', background_color='#3F3F3F')
        
        
        self.layout = [
            [self.components['list_box_col'],
            self.components['canvas_col'],
            self.components['summary_chat_col']]
        ]
        

    def render(self):

        # create the form and show it without the plot
        if self.layout != [] :
            self.window =sg.Window('Data Explorer Screen', self.layout, grab_anywhere=False, finalize=True, background_color='#8A8A8A')
        # self.set_up_chat_thread()
        des_screen = UserManager.current_screen  
        record = self.jsnDrop.allWhere("tblChat", f"DESNumber = '{des_screen}'")
        message = f"{record[0]['PersonID']}: {record[0]['Chat']}\n"
        UserManager.chat_list = message
        result = UserManager.chat_list
        self.components['ChatDisplay'].Update(result)
        

    def accept_input(self):
 
            if self.window != None :
                keep_going = True
                
                while keep_going == True:
                    event, values = self.window.read()
                    
                    if event == sg.WIN_CLOSED:
                        keep_going = False
                        break
                    
                    if event == "-CHATTHREAD-" and not UserManager.stop_thread:
                        # This is where the event come back to the window from the Thread
                        
                        # Lock until the Window is updated
                        UserManager.stop_thread = True
                        
                        self.window['ChatDisplay'].Update(values[event])
                        # This should always be True here
                        if UserManager.stop_thread:
                            # Unlock so we can start another long task thread
                            UserManager.stop_thread = False
                            # Start another long task thread
                            self.set_up_chat_thread()
                            
                    for accept_control in self.controls:
                        keep_going = accept_control(event,values,{'view':self})
                self.window.close()
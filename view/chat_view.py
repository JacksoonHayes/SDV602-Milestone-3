import PySimpleGUI as sg
import controller.DES.exit_button as exit_button
import controller.User.chat_button as chat_button
from model.user_manager import UserManager 
from time import sleep
from threading import Thread
import threading
import signal
from datetime import datetime

from view import update_file_view

class ChatView(object):

    def __init__(self):
        
        self.window = None
        self.layout = []
        self.components = {"has_components":False}
        self.controls = []
        self.values = None
        # The following will only work if we have logged in!
        # self.JsnDrop = UserManager.this_user_manager.jsnDrop
        # Thread for chat
        self.chat_count = 0
        self.exit_event = threading.Event()
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self,signum, frame):
        self.exit_event.set()   

    def set_up_chat_thread(self):
        UserManager.chat_thread = Thread(target=self.chat_display_update,args=(UserManager,))
        UserManager.chat_thread.setDaemon(True)
        UserManager.stop_thread = False
        UserManager.chat_thread.start()

    def chat_display_update(self, UserManager):
        print("Thread chat")
        #sleep(2)

        # Check there is a window before sending an event to it
        if self.window != None:
            self.chat_count += 1
            # Go to network service to get the Chats
            result = self.JsnDrop.select("tblChat",f"DESNumber = '{UserManager.current_screen}'")
            print(result)
            if result != "Data error. Nothing selected from tblChat":
                messages = ""
                # Sort the result records by the Time field
                sorted_chats = sorted(result,key = lambda i : i['Time'] )

                for record in sorted_chats:
                    new_display = ""
                    if not (UserManager.latest_time is None):
                        # Only add if the record's time is after the latest_time
                        if record['Time'] > UserManager.latest_time:
                            new_display = f"{record['PersonID']}[{record['Chat']}]\n"
                    else: # Not entirely happy with this one - just what to do until there is a time?
                        new_display = f"{record['PersonID']}[{record['Chat']}]\n"
                    messages +=   new_display

                UserManager.chat_list = [messages]

                # Keep number of messages down to 5
                if len(UserManager.chat_list) > 5:
                    UserManager.chat_list = UserManager.chat_list[:-5]
                
                # Makes a string of messages to update the display
                Update_Messages = ""
                for messages in UserManager.chat_list:
                    Update_Messages+= messages
                
                # Send the Event back to the window if we have n't already stopped
                if not UserManager.stop_thread:

                    # Time stamp the latest record
                    latest_record = sorted_chats[:-1][0]
                    UserManager.latest_time = latest_record['Time']

                    # Send the event back to the window
                    self.window.write_event_value('-CHATTHREAD-', Update_Messages)
        # The Thread stops - no loop - when the event is caught by the Window it starts a new long task
                                
                
    def set_up_layout(self,**kwargs):
        
        # define the form layout
        
        # one variable per call to sg 
        # if there is a control / input with it add the name to the controls list
        self.components['ChatDisplay'] = sg.Multiline(autoscroll=True,disabled=True, key='ChatDisplay',size=(20,10))
        self.components['Message'] =sg.Input(key='Message',size=(20,50))
        self.components['Send'] = sg.Button('Send', key='Send', size=(5,1))
        self.controls += [chat_button.accept]

        self.layout = [
                        
                        [self.components['ChatDisplay'] ], 
                        [self.components['Message'], self.components['Send']],
                      ]

    # def render(self):
    #     if self.layout != [] :
    #         self.window =sg.Window('Chat', self.layout, grab_anywhere=False, finalize=True)
    #         # Need a window before chat
    #         self.set_up_chat_thread()
  
    def accept_input(self):

        if self.window != None :
            keep_going = True
            
            while keep_going == True:
                event, values = self.window.read()
                   
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
        
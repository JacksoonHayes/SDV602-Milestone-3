"""
File to manage user registration, login, chat, and logout functionality.
"""

from model.network.jsn_drop_service import jsnDrop
from time import gmtime  #  gmt_time returns UTC time struct  
from datetime import datetime

from datetime import datetime

class UserManager(object):
    """
    UserManager class manages user registration, login, chat, and logout functionality.
    """

    current_user = None
    current_pass = None
    current_status = None
    current_screen = None
    chat_list = []
    chat_thread = None
    stop_thread = False
    this_user_manager = None
    thread_lock = False
    jsn_tok = "66d863d6-9ae2-43a2-b8b4-fac8deab3689"
    latest_time = None
    DES_screen = None
    des_list = []

    def now_time_stamp(self):
        """
        Get the current timestamp.

        Returns:
            float: The current timestamp.
        """
        time_now = datetime.now()
        time_now.timestamp()
        return time_now.timestamp()

    def __init__(self) -> None:
        super().__init__()

        self.jsnDrop = jsnDrop(UserManager.jsn_tok,"https://newsimland.com/~todd/JSON")

        # SCHEMA Make sure the tables are  CREATED - jsnDrop does not wipe an existing table if it is recreated
        result = self.jsnDrop.create("tblUser",{"PersonID PK":"A_LOOONG_NAME"+('X'*50),
                                                "Password":"A_LOOONG_PASSWORD"+('X'*50),
                                                "DESNumber":"A_LOOONG_DES_ID"+('X'*50),
                                                "Status":"STATUS_STRING"})

        result = self.jsnDrop.create("tblChat",{"PersonID PK":"A_LOOONG_NAME"+('X'*50),
                                                "DESNumber":"A_LOOONG_DES_ID"+('X'*50),
                                                "Chat":"A_LOONG____CHAT_ENTRY"+('X'*255),
                                                "Time": self.now_time_stamp()})
        UserManager.this_user_manager = self

    def register(self, user_id, password):
        """
        Register a new user.

        Args:
            user_id (str): The user ID.
            password (str): The user's password.

        Returns:
            str: The registration result.
        """
        api_result = self.jsnDrop.select("tblUser", f"PersonID = '{user_id}'")
        if "DATA_ERROR" in self.jsnDrop.jsnStatus:
            record_count = len(self.jsnDrop.allWhere("tblUser", f"Status = 'Registered'"))
            if record_count == 41:
                des_number = 1
            else:
                des_number = record_count + 1
            result = self.jsnDrop.store("tblUser", [{'PersonID': user_id, 'Password': password,
                                                    'Status': 'Registered', "DESNumber": f"DES_{des_number}"}])
            UserManager.currentUser = user_id
            UserManager.current_status = 'Logged Out'
            UserManager.DES_screen = f"DES_{des_number}"
            result = "Registration Success"
        else:
            result = "User Already Exists"
        return result

    def login(self, user_id, password):
        """
        Log in a user.

        Args:
            user_id (str): The user ID.
            password (str): The user's password.

        Returns:
            str: The login result.
        """
        result = None
        api_result = self.jsnDrop.select("tblUser",f"PersonID = '{user_id}' AND Password = '{password}'")
        if "DATA_ERROR" in self.jsnDrop.jsnStatus:
            result = "Login Fail"
            UserManager.current_status = "Logged Out"
            UserManager.current_user = None
        else:
            UserManager.current_status = "Logged In"
            UserManager.current_user = user_id
            UserManager.current_pass = password
            UserManager.current_screen = self.jsnDrop.jsnResult[0]['DESNumber']
            print(f"Current Screen: {UserManager.current_screen}")
            api_result = self.jsnDrop.store("tblUser",[{"PersonID":user_id,"Password":password,"Status":"Logged In"}])
            result = "Login Success"
        return result

    def set_current_DES(self, DESScreen):
        """
        Set the current screen.

        Args:
            DESScreen (str): The DES screen to set.

        Returns:
            str: The result of setting the screen.
        """
        result = None
        if UserManager.current_status == "Logged In":
            UserManager.current_screen = DESScreen
            result = "Set Screen"
            print(f"Set Screen to {DESScreen}")
        else:
            result = "Log in to set the current screen"
        return result

    def get_user_des(self):
        """
        Get the DES screen of the current user.

        Returns:
            str: The DES screen of the current user.
        """
        api_result = self.jsnDrop.select("tblUser",f"PersonID = '{UserManager.current_user}'")
        if not ('DATA_ERROR' in api_result):
            UserManager.DES_screen = self.jsnDrop.jsnResult[0]['DESNumber']
            result = UserManager.DES_screen
            return result

    def chat(self,message):
        """
        Send a chat message.

        Args:
            message (str): The chat message to send.

        Returns:
            str: The result of sending the chat message.
        """
        result = None
        if UserManager.current_status != "Logged In":
            result = "You must be logged in to chat"
        elif UserManager.current_screen == None:
            result = "Chat not sent. A current screen must be set before sending chat"
        else: 
            user_id = UserManager.current_user
            des_screen = UserManager.current_screen
            api_result = self.jsnDrop.store("tblChat",[{'PersonID':user_id,
                                                        'DESNumber':f'{des_screen}',
                                                        'Chat':message,
                                                        'Time': self.now_time_stamp()}])
            if "ERROR" in api_result:
                result = self.jsnDrop.jsnStatus
            else:
                result = "Chat sent"
        return result

    def logout(self):
        """
        Log out the current user.

        Returns:
            str: The logout result.
        """
        result = "Must be 'Logged In' to 'LogOut' "
        if UserManager.current_status == "Logged In":
            api_result = self.jsnDrop.store("tblUser",[{"PersonID": UserManager.current_user,
                                                        "Password": UserManager.current_pass,
                                                        "Status":"Logged Out"}])
            if not("ERROR" in api_result):
                UserManager.current_status = "Logged Out"
                result = "Logged Out"
            else:
                result = self.jsnDrop.jsnStatus
        return result

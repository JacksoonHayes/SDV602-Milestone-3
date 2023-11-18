from model.network.jsn_drop_service import jsnDrop
from time import gmtime  #  gmt_time returns UTC time struct  
from datetime import datetime

class UserManager(object):
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

    def now_time_stamp(self):
        time_now = datetime.now()
        #timestamp_str = f"{time_now.tm_year}-{time_now.tm_mon}-{time_now.tm_mday} {time_now.tm_hour}:{time_now.tm_min}:{time_now.tm_sec}"
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

        # self.test_api()

    def register(self, user_id, password):
        api_result = self.jsnDrop.select("tblUser", f"PersonID = '{user_id}'")
        if "DATA_ERROR" in self.jsnDrop.jsnStatus:
            # Generate a DES number, increments by 1.
            record_count = len(self.jsnDrop.allWhere("tblUser", f"Status = 'Registered'"))
            if record_count == 41:
                des_number = 1
            else:
                des_number = record_count + 1
            # Store user details with des_screen
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
        result = None
        api_result = self.jsnDrop.select("tblUser",f"PersonID = '{user_id}' AND Password = '{password}'") # Danger SQL injection attack via user_id?? Is JsnDrop SQL injection attack safe??
        if( "DATA_ERROR" in self.jsnDrop.jsnStatus): # then the (user_id,password) pair do not exist - so bad login
            result = "Login Fail"
            UserManager.current_status = "Logged Out"
            UserManager.current_user = None
        else:
            UserManager.current_status = "Logged In"
            UserManager.current_user = user_id
            UserManager.current_pass = password
            api_result = self.jsnDrop.store("tblUser",[{"PersonID":user_id,"Password":password,"Status":"Logged In"}])
            result = "Login Success"
        return result

    def set_current_DES(self, DESScreen):
        result = None
        if UserManager.current_status == "Logged In":
            UserManager.current_screen = DESScreen
            result = "Set Screen"
        else:
            result = "Log in to set the current screen"
        return result


    def chat(self,message):
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
            if "ERROR" in api_result :
                result = self.jsnDrop.jsnStatus
            else:
                result = "Chat sent"

        return result

    def get_chat(self):

         if UserManager.current_status == "Logged In" and UserManager.current_screen is not None:
            des_screen = UserManager.current_screen  
            if not(des_screen is None):
                api_result = self.jsnDrop.select("tblChat",f"DESNumber = '{des_screen}'")
                if not ('DATA_ERROR' in api_result) :
                    UserManager.chat_list = self.jsnDrop.jsnResult
                    result = UserManager.chat_list
                    return result
                else:
                    return None
         
    def logout(self):
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
    
    
        # def populate_data(self):
        # if UserManager.current_status == "Logged In":
        #     data = pd.read_csv("data/bd-dec17-births-deaths-by-region.csv")
        #     df = pd.DataFrame(data)
        #     for row in df.itertuples():
        #         api_result = self.jsnDrop.store("tblData",[{
        #                                                 "Period":row.Period,
        #                                                 "Birth_Death":row.Birth_Death,
        #                                                 "Region":row.Region,
        #                                                 "Count":row.Count}])     
        #     if not("ERROR" in api_result):
        #         UserManager.current_status = "Logged Out"
        #         result = "Logged Out"
        #     else:
        #         result = self.jsnDrop.jsnStatus


    def test_api(self):
        # Should this be in jsn_drop_service ?
        result = self.jsnDrop.create("tblTestUser",{"PersonID PK":"Todd","Score":21})
        print(f"Create Result from UserManager {result}")

        self.jsnDrop.store("tblTestUser",[{"PersonID":"Todd","Score":21},{"PersonID":"Jane","Score":201}])
        print(f"Store Result from UserManager {result}")

        result = self.jsnDrop.all("tblTestUser")
        print(f"All Result from UserManager {result}")

        result = self.jsnDrop.select("tblTestUser","Score > 200") # select from tblUser where Score > 200
        print(f"Select Result from UserManager {result}")

        result = self.jsnDrop.delete("tblTestUser","Score > 200") # delete from tblUser where Score > 200
        print(f"Delete Result from UserManager {result}")

        result = self.jsnDrop.drop("tblTestUser")
        print(f"Drop Result from UserManager {result}")



def testUserManager():
    # Just a Test

    # Start with no user table and no chat table
    a_jsnDrop = jsnDrop(UserManager.jsn_tok,"https://newsimland.com/~todd/JSON")
    a_jsnDrop.drop('tblUser')
    a_jsnDrop.drop('tblChat')
    # Now start a User manager with a clean slate

    # Get a User Maanager
    a_user_manager = UserManager()

    #register
    register_status = a_user_manager.register("Todd", "12345") 
    print(f"REGISTER STATUS: {register_status}")

    #login 
    login_status = a_user_manager.login("Todd","12345")
    print(f"LOGIN STATUS: {login_status}")

    # when logged in set current screen
    set_screen_status = a_user_manager.set_current_DES("DES_1")  
    print(f"SET CURRENT SCREEN: {set_screen_status}") 

    # when logged in send a chat   
    chat_status = a_user_manager.chat("Hello 1")
    print(f"SEND CHAT STATUS: {chat_status}")

    # when logged in get chat
    chat_status = a_user_manager.get_chat()
    print(f"GET CHAT STATUS: {chat_status}")

    # log out
    logout_status = a_user_manager.logout()
    print(f"LOGOUT STATUS: {logout_status}")

    # attempt bad login (logs out)
    login_status = a_user_manager.login("Todd","12")
    print(f"LOGIN STATUS: {login_status}")

    # attempt send chat when not logged in, after bad login 
    chat_status = a_user_manager.chat("Hello 2")
    print(f"SEND CHAT STATUS after bad login: {chat_status}")

    # attempt get chat when not logged in, after bad login
    chat_status = a_user_manager.get_chat()
    print(f"GET CHAT STATUS after bad login: {chat_status}")
    


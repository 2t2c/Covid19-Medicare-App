"""
Main Medicare Application Client
"""

# imports
import warnings
import mysql.connector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from .code import social_distancing, mask_detection, chatbot

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)

Clock.max_iteration = 50

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    password="root",
    database="register_page"
)

mycursor = mydb.cursor(buffered=True)
Window.size = (380, 588)

kv = """
ScreenManager:
    LoginScreen:
    RegisterScreen:
    HomeScreen:
    Account:
    MaskDetection:
    SocialDistancing:
    Blogs:
    WritingBlog:
    Chatbox:
    
<LoginScreen>:
    name: 'login'
    BackgroundLayer:
    MDCard:
        orientation: 'vertical'
        size_hint: [0.8, 0.6]
        pos_hint : {'center_x': 0.5, 'center_y': 0.5}
        padding: [15, 7, 15, 7]
        spacing: 8
        BoxLayout:
            orientation: 'vertical'
            MDLabel:
                text: 'COVID MEDICARE'
                text_size: self.size
                font_size: 30
                bold: True
                halign: 'center'
                valign: 'middle'
            MDLabel:
                markup: True
                text: "[color=00FF00]SIGN IN[/color]"
                text_size: self.size
                bold: True
                halign: 'center'
                valign: 'middle'
        MDTextField:
            id: user_sign_in_email
            hint_text: 'Email'
            required: True
        MDTextField:
            id: user_sign_in_password
            hint_text: 'Password'
            password: True
            required: True
            
        MDFillRoundFlatButton:
            text: 'Sign In'
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}
            disabled: True if root.sign_in(user_sign_in_email.text, user_sign_in_password.text) == 1 else False
            on_press: root.manager.current = 'home'
               
        MDRectangleFlatButton:
            text: 'Register'
            on_press: root.manager.current = 'register'
            size_hint_x: 0.5
            pos_hint: {'center_x': 0.5}
            
<RegisterScreen>:
    name: 'register'
    id: r
    BackgroundLayer:
    MDCard:
        orientation: 'vertical'
        size_hint: [0.8, 0.8]
        pos_hint : {'center_x': 0.5, 'center_y': 0.5}
        padding: [15, 7, 15, 7]
        spacing: 8
        BoxLayout:
            orientation: 'vertical'
            MDLabel:
                text: 'COVID MEDICARE'
                text_size: self.size
                font_size: 30
                bold: True
                halign: 'center'
                valign: 'middle'
            MDLabel:
                markup: True
                text: "[color=00FF00]REGISTER[/color]"
                text_size: self.size
                bold: True
                halign: 'center'
                valign: 'middle'
        MDTextField:
            id: user_email
            hint_text: 'E-mail'
            required: True
        MDTextField:
            id: user_name
            hint_text: 'Enter Full Name'
            required: True
        MDTextField:
            id: user_username
            hint_text: 'Enter Username'
            required: True
        MDTextField:
            id: user_address
            hint_text: 'Address'
            required: True
        MDTextField:
            id: user_password
            hint_text: 'Password'
            password: True
            required: True
        MDFillRoundFlatButton:
            text: 'Register'
            size_hint_x: 0.8
            pos_hint: {'center_x': 0.5}
            on_release: app.get_name(user_email.text, user_name.text, user_username.text, user_address.text, user_password.text)
        MDRectangleFlatButton:
            text: 'Sign In'
            size_hint_x: 0.5
            pos_hint: {'center_x': 0.5}   
            on_press: root.manager.current = 'login'
<HomeScreen>:
    name : 'home'
    canvas.before:
        Color:
            rgba: rgba('#F4ECF7')
        RoundedRectangle:
            pos: self.pos
            size: self.size

    Screen:
        NavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:                        
                        orientation: 'vertical'
                        MDToolbar:
                            title: 'Navigation Bar'
                            elevation: 10
                            left_action_items : [['menu', lambda x: nav_drawer.set_state('open')]]
                        ScrollView:
                            GridLayout:
                                cols: 1
                                row:1
                                size_hint_y: None
                                height: self.minimum_height
                                padding: 7
                                spacing: 10

                                MDLabel:
                                    markup : True
                                    text: '[color=3365FF]CORONAVIRUS - COVID 19[/color]'
                                    font_size: 30
                                    bold : True
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1] 

                                MDLabel:
                                    spacing: 5
                                    text: 'What is Coronavirus?'
                                    bold : True
                                    font_size: 23
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1]   
                                MDLabel:
                                    spacing: 5
                                    text: "     Coronaviruses are a type of virus. It emerged in China in December 2019. Although health officials are still tracing the exact source of this new coronavirus, early hypotheses thought it may be linked to a seafood market in Wuhan, China."
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1] 
                                MDLabel:
                                    spacing: 5
                                    text: "Symptoms"
                                    bold : True
                                    text_size : self.size
                                    font_size: 23
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1] 
                                MDLabel:
                                    spacing: 5
                                    text: 'cough, fever or chills, shortness of breath or difficulty breathing, muscle or body aches, sore throat, new loss of taste or smell, diarrhea, headache, new fatigue, nausea or vomiting and congestion or runny nose.'
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1] 
                                MDLabel:
                                    spacing: 5
                                    text: "Causes"
                                    bold : True
                                    text_size : self.size
                                    font_size: 23
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1]  
                                MDLabel:
                                    spacing: 5
                                    text: 'The new coronavirus can be spread from person to person.'
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1]  
                                MDLabel:
                                    spacing: 5
                                    text: 'Diagnosis'
                                    bold : True
                                    font_size: 23
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1] 
                                MDLabel:
                                    spacing: 5
                                    text: 'Diagnosis may be difficult with only a physical exam because mild cases of COVID-19 may appear similar to the flu or a bad cold. A laboratory test can confirm the diagnosis. '
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1] 
                                MDLabel:
                                    spacing: 5
                                    text: 'Treatment'
                                    bold: True
                                    font_size: 23
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1]
                                MDLabel:
                                    spacing: 5
                                    text: 'As of now, there is not a specific treatment for the virus. People who become sick from COVID-19 should be treated with supportive measures: those that relieve symptoms. For severe cases, there may be additional options for treatment, including research drugs and therapeutics.'
                                    size_hint_x: 1
                                    size_hint_y: None
                                    text_size: self.width, None
                                    height: self.texture_size[1]
                    Widget:
            MDNavigationDrawer:
                id: nav_drawer
                ScreenManager:
                    Screen:
                        BoxLayout:
                            orientation: 'vertical'
                            padding: '8dp'
                            spacing: '8dp'
                            AnchorLayout:
                                anchor_x: 'left'
                                size_hint_y :  None
                                height: avatar.height
                                Image:
                                    id: avatar
                                    size_hint: None, None
                                    source: 'assets/pic.jpg'
                            MDLabel:
                                text: 'Your Account'
                                font_style: 'Button'
                                size_hint_y: None
                                height: self.texture_size[1]
                            MDLabel:
                                text: 'Welcome to Medicare App'
                                font_style: 'Caption'
                                size_hint_y:  None
                                height: self.texture_size[1]
                            ScrollView:
                                MDList:
                                    OneLineIconListItem:
                                        text: 'Account'
                                        on_press: root.manager.current = 'account'
                                        IconLeftWidget:
                                            icon: 'account-box'
                                    OneLineIconListItem:
                                        text: 'Mask Detection'
                                        on_press: root.manager.current = 'mask_detect'
                                        IconLeftWidget:
                                            icon: 'camera'
                                    OneLineIconListItem:
                                        text: 'Social Distancing'
                                        on_press: root.manager.current = 'social_distance'
                                        IconLeftWidget:
                                            icon: 'map-marker-distance'
                                    OneLineIconListItem:
                                        text: 'Blogs'
                                        on_press: root.manager.current = 'blogs'
                                        IconLeftWidget:
                                            icon: 'book'
                                    OneLineIconListItem:
                                        text: 'Chatbox'
                                        on_press: root.manager.current = 'chatbox'
                                        IconLeftWidget:
                                            icon: 'chat'
                                    OneLineIconListItem:
                                        text: 'Exit'
                                        on_press: app.stop()
                                        IconLeftWidget:
                                            icon: 'exit-to-app'
<Account>:
    name: 'account'
    BackgroundLayer:

    MDCard:
        orientation: 'vertical'
        size_hint: [0.8, 0.8]
        pos_hint : {'center_x': 0.5, 'center_y': 0.5}
        padding: [15, 0, 15, 0]
        spacing: 8

        BoxLayout:
            orientation: 'vertical'

            MDLabel:
                text: 'Your Account'
                text_size: self.size
                bold : True
                halign: 'center'
                valign: 'middle'
                font_size : 25

            AnchorLayout:
                anchor_x: 'center'
                anchor_y: 'top'
                size_hint_y :  None
                height: avatar.height

                Image:
                    id: avatar
                    size_hint: None, None
                    source: 'cute.png'
                    
            MDLabel:
                text: "Enter Old Email:"
                text_size: self.size
                halign: 'center'
                
            MDTextField:
                id: old_email
                hint_text: 'Old Email'
                
            MDLabel:
                text: "Enter Old Password:"
                text_size: self.size
                halign: 'center'
                
            MDTextField:
                id: old_password
                hint_text: 'Old Password'

            MDLabel:
                text: 'Name:'
                text_size : self.size
                halign: 'center'

            MDTextField:
                id: edit_name
                hint_text: 'Name'

            MDLabel:
                text: 'Enter New Email:'
                text_size: self.size
                halign: 'center'
                

            MDTextField:
                id: edit_email
                hint_text: 'Username'

            MDLabel:
                text: 'Enter New Password:'
                text_size: self.size
                halign: 'center'

            MDTextField:
                id: edit_password
                hint_text: 'Password'

    MDFillRoundFlatButton:
        text: 'Edit'
        pos_hint: {'x' : 0.3, 'y': 0.02}
        on_press: app.edit_details(old_email.text, old_password.text, edit_name.text, edit_email.text, edit_password.text)

    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint: {'x' : 0.55, 'y': 0.02}
        on_press: root.manager.current = 'home'
        
<MaskDetection>:
    name: 'mask_detect'
    BackgroundLayer:
    MDCard:
        orientation: 'vertical'
        size_hint: [0.8, 0.5]
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        padding: [15, 0, 15, 0]
        spacing: 8
    
        BoxLayout:
            orientation: 'vertical'
        
            MDLabel:
                text: 'Mask Detection'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                font_size: 25
                bold: True
                pos_hint: {'x': 0, 'y': 0.1}
            
            MDLabel:
                text: 'This is the screen where we look for mask detection. To continue the process, click on the detect button.'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                font_size: 15
            
    MDFillRoundFlatButton:
        text: 'Detect'
        pos_hint: {'x': 0.25, 'y': 0.02}
        on_press: root.run_mask_detection()
    
    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint: {'x': 0.50, 'y': 0.02}
        on_press: root.manager.current = 'home'
        
<SocialDistancing>:
    name: 'social_distance'
    BackgroundLayer:
    MDCard:
        orientation: 'vertical'
        size_hint: [0.8, 0.5]
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        padding: [15, 0, 15, 0]
        spacing: 8

        BoxLayout:
            orientation: 'vertical'
    
            MDLabel:
                text: 'Social Distancing Monitor'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                font_size: 25
                bold: True
                pos_hint: {'x': 0, 'y': 0.1}
        
            MDLabel:
                text: 'This is the screen where we look for social distancing. To continue the process, click on the detect button.'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                font_size: 15

    MDFillRoundFlatButton:
        text: 'Detect'
        pos_hint: {'x': 0.25, 'y': 0.02}
        on_press: root.run_social_distancing()

    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint: {'x': 0.50, 'y': 0.02}
        on_press: root.manager.current = 'home'
        
<Chatbox>:
    name: 'chatbox'
    BackgroundLayer:
    MDCard:
        orientation: 'vertical'
        size_hint: [0.8, 0.5]
        pos_hint : {'center_x': 0.5, 'center_y': 0.5}
        padding: [15, 0, 15, 0]
        spacing: 8

        BoxLayout:
            orientation: 'vertical'
            
            MDLabel:
                text: 'Chatbot'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                font_size : 25
                bold : True
                pos_hint: {'x': 0, 'y': 0.1}
                

            MDLabel:
                text: 'This is the screen where you can ask any question regarding Covid. Click on the Chat button to talk!'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                font_size : 15
                
    MDFillRoundFlatButton:
        text: 'Chat'
        pos_hint: {'x' : 0.3, 'y': 0.02}
        on_press: root.run_covid_bot()

    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint: {'x' : 0.55, 'y': 0.02}
        on_press: root.manager.current = 'home'
        
<Blogs>:
    name: 'blogs'
    BackgroundLayer:
    Screen:
        NavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:                        
                        orientation: 'vertical'
                        MDToolbar:
                            title: 'Blogs'
                            height: self.height
                            valign: 'top'
                            elevation: 10
                            padding: 5
                            MDRoundFlatIconButton:
                                markup: True
                                md_bg_color: 1,1,1,1
                                text: 'Write your blog!'
                                icon: 'typewriter'
                                pos_hint: {'center_x': 0.8, 'center_y':  0.55}  
                                spacing: 8
                                padding: 5
                                on_release: root.manager.current = 'writeblog'
                        MDCard:
                            orientation: 'vertical'
                            size_hint: [0.9, 0.6]
                            pos_hint : {'center_x': 0.5, 'center_y': 0.5}
                            padding: [15, 7, 15, 7]
                            spacing: 8
                            BoxLayout:
                                orientation: 'vertical'
                                MDLabel:
                                    markup: True
                                    text: "[color=EF1610]THE TITLE[/color]"
                                    halign: 'center'
                                    valign: 'middle'
                                    font_size: 28
                                    bold : True
                                MDLabel:
                                    text: 'Dr _______'
                                    halign: 'left'
                                MDLabel:
                                    text: 'BODY'
                                    halign: 'center'
                                    valign: 'middle'
                        MDFillRoundFlatButton:
                            text: 'Back'
                            pos_hint: {'x' : 0.4, 'y': 0.02}
                            on_press: root.manager.current = 'home'
<WritingBlog>
    name: 'writeblog'
    BackgroundLayer:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        MDToolbar:
            title: 'Write your Blog!'
            height: self.height
            valign: 'top'
            elevation: 10
            padding: 5
        MDLabel:
            text: ' '
    MDCard:
        id : write
        orientation: 'vertical'
        size_hint: [0.9, 0.75]
        pos_hint : {'center_x': 0.5, 'center_y': 0.5}
        padding: [15, 7, 15, 7]
        spacing: 8
        MDTextField:
            mode: 'rectangle'
            hint_text: 'Enter Title Here!'
            required: True
            halign: 'center'
            valign: 'top'
            pos_hint: {"center_y": 1}
        MDTextFieldRect:
            mode: 'rectangle'
            hint_text: 'Enter your content here!'
            required: True
            multiline: True
            max_text_length: 250
            height: "130dp"
            width: write.height/2
            fill_color: 1,1,1,1
    MDFillRoundFlatButton:
        text: 'Submit'
        pos_hint: {'x' : 0.2, 'y': 0.009}
    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint: {'x' : 0.6, 'y': 0.009}
        on_press: root.manager.current = 'blogs'
        
<BackgroundLayer@BoxLayout>:
    orientation: 'vertical'
    Image:
        source: "assets/bg.png"
"""

class HomeScreen(Screen):
    name = StringProperty('home')

class OpenDialog(Screen):
    pass

class LoginScreen(Screen):
    def switching_function(self, x=1):
        return x

    def fail(self):
        self.dialog = MDDialog(title="Invalid",
                               text="Wrong email or password",
                               buttons=[MDFlatButton(text="Close")],
                               size_hint=[0.9, None], )
        self.dialog.open()

    def sign_in(self, email, password):
        sql = '''SELECT EXISTS (
              SELECT * FROM reg 
              WHERE email = (%s) AND password = (%s)
            )'''

        record = (email, password,)
        mycursor.execute(sql, record)
        mydb.commit()
        num = int(mycursor.fetchall()[0][0])

        if len(email)==0 or len(password)==0:
            x = self.switching_function(x=1)
            return x
        elif num==1:
            x = self.switching_function(x=0)
            return x
        else:
            x = self.switching_function(x=1)
            return x


class RegisterScreen(Screen):
    pass


class Account(Screen):
    pass


class MaskDetection(Screen):
    def run_mask_detection(self):
        mask_detection.run()


class SocialDistancing(Screen):
    def run_social_distancing(self):
        social_distancing.run_sd(live=False)


class Blogs(Screen):
    pass


class Chatbox(Screen):
    def run_covid_bot(self):
        chatbot.run()

class WritingBlog(Screen):
    pass


sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(OpenDialog(name='dialog'))
sm.add_widget(RegisterScreen(name='register'))
sm.add_widget(Account(name='account'))
sm.add_widget(MaskDetection(name='mask_detect'))
sm.add_widget(SocialDistancing(name='social_distancing'))
sm.add_widget(Blogs(name='blogs'))
sm.add_widget(Chatbox(name='chatbox'))
sm.add_widget(WritingBlog(name='writeblog'))

count = 0


class DemoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        self.title = "COVID MEDICARE"
        self.screen = Builder.load_string(kv)
        return self.screen

    def get_name(self, email, name, username, address, password):
        sql = '''INSERT INTO reg (email, name, username, address, password) VALUES (%s, %s, %s, %s, %s)'''
        record_inserted = (email, name, username, address, password)
        if ((len(email) == 0) or (len(name) == 0) or (len(username) == 0) or (len(address) == 0) or (len(password) == 0)):
            self.dialog = MDDialog(title="Error!",
                                   text="Please fill out the empty details!",
                                   buttons=[MDFlatButton(text="Close")],
                                   size_hint=[0.9, None], )
            self.dialog.open()
        else:
            mycursor.execute(sql, record_inserted)
            self.dialog = MDDialog(title="Registered!",
                                   text="Thank you for registering! Please click on the sign in button to sign in to te app!",
                                   buttons=[MDFlatButton(text="Close")],
                                   size_hint=[0.9, None], )
            self.dialog.open()
            mydb.commit()

    def edit_details(self, old_email, old_password, name, email, password):
        sql_verify = '''SELECT EXISTS (
              SELECT * FROM reg 
              WHERE email = (%s) AND password = (%s)
            )'''

        record_verify = (old_email, old_password,)
        mycursor.execute(sql_verify, record_verify)
        num = int(mycursor.fetchall()[0][0])

        sql_update = '''UPDATE reg SET email = (%s), name = (%s), password = (%s) WHERE email = (%s) AND password=(%s)'''
        record_inserted = (email, name, password, old_email, old_password)
        if ((len(old_email)==0) or (len(old_password)==0) or (len(name)==0) or (len(email)==0) or (len(password)==0)):
            self.dialog = MDDialog(title="Error!",
                                   text="Please fill out the empty details!",
                                   buttons=[MDFlatButton(text="Close")],
                                   size_hint=[0.9, None], )
            self.dialog.open()
        elif num==0:
            self.dialog = MDDialog(title="Invalid Credentials!",
                                   text="Wrong email or password!",
                                   buttons=[MDFlatButton(text="Close")],
                                   size_hint=[0.9, None], )
            self.dialog.open()
        else:
            mycursor.execute(sql_update, record_inserted)
            self.dialog = MDDialog(title="Updated!",
                                   text="Your details have been updated!",
                                   buttons=[MDFlatButton(text="Close")],
                                   size_hint=[0.9, None], )
            self.dialog.open()
            mydb.commit()


DemoApp().run()
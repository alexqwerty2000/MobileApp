from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
import random
from datetime import datetime
from pathlib import Path
from hoverable import HoverBehavior

Builder.load_file("design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password" 


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, upass):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {"username": uname, "password": upass,
        "created": datetime.now().strftime('%Y-%m-%d  %H:%M:%S')}

        with open("users.json", 'w') as file:
            json.dump(users, file)
        
        self.manager.transition.direction = 'right'
        self.manager.current = "sign_up_success"

class SignUpScreenSuccess(Screen):
    def go_to_logscreen(self):
        self.manager.current = "login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    
    def get_quotes(self, feel):
        feel = feel.lower()
        available_quotes = glob.glob("quotes/*txt")
        available_quotes = [Path(filename).stem for filename in available_quotes]

        if feel in available_quotes:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(HoverBehavior, ButtonBehavior, Image) :
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__ == "__main__":
    MainApp().run()
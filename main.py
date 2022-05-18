import asyncio

from kivy.app import App
from kivy.app import async_runTouchApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from tlagent import TLAgent


class LoginCodeWindow(Screen):
    code = ObjectProperty(None)

    def submit(self):
        print("ERROR SUBMITING")
        #TODO submit


    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.code.text = ""


class LoginWindow(Screen):
    phone = ObjectProperty(None)
    username = ObjectProperty(None)
    agent = TLAgent("", "")
    wrong_login = ObjectProperty(None)

    async def getUsersTL(self):
        print("Getting users")
        agent = TLAgent("Mihash08", "+7925185096")
        result = await agent.getUsers()
        if result == -1:
            print("ERROR WHILE GETTING USERS")
        else:
            print("Got users")

    async def logIn(self):
        agent = TLAgent(self.username.text, self.phone.text)

        result = await agent.logIn()
        if result == -1:
            self.wrong_login.text = "Wrong phone or (and) username"
        elif result == 0:
            self.wrong_login.text = ""
            sm.current = "code"
        else:
            self.wrong_login.text = ""
            await agent.getUsers()
            #sm.current = "main"
            #await agent.getUsers()


    async def logOut(self):
        agent = TLAgent(self.username.text, self.phone.text)
        await agent.logOut()

    def loginBtn(self):
        self.wrong_login.text = "Connecting..."
        thisloop = asyncio.get_event_loop()
        coroutine = self.logIn()
        thisloop.run_until_complete(coroutine)

    def logOutBtn(self):
        thisloop = asyncio.get_event_loop()
        coroutine = self.logOut()
        thisloop.run_until_complete(coroutine)

    def reset(self):
        self.phone.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("data.txt")

screens = [LoginWindow(name="login"), LoginCodeWindow(name="code"), MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()

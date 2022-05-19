import asyncio

from kivy.app import App
from kivy.app import async_runTouchApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
from tlagent import TLAgent


class Table(BoxLayout):
    orientation = 'vertical'
    size_hint_y = None
        # height = minimum_height
        # padding = 50, 50, 50, 50
    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)

    def add(self, row):
        self.add_widget(row)


    def addAll(self, rows):
        for row in rows:
            self.add_widget(row)


my_users = []

class Row(BoxLayout):
    txt = ObjectProperty(None)
    phone = ObjectProperty(None)
    id = -1

    def __init__(self, name, phone, id, **kwargs):
        super(Row, self).__init__(**kwargs)
        self.name.text = name
        self.phone.text = phone
        self.id = id

    @staticmethod
    def initArr(users):
        rows = []
        count = 0
        for user in users:
            text = str(user.first_name) + "\n" + str(user.last_name)
            rows.append(Row(text, "+" + str(user.phone), count))
            count += 1
        return rows
    def analyse(self):
        print(self.id)
        print(my_users[self.id])


class LoginCodeWindow(Screen):
    code = ObjectProperty(None)

    async def _submit(self):
        try:
            await TLAgent.tryCode(int(self.code.text))
            await LoginWindow.getUsersTL()
            sm.current = "main"
        except Exception:
            print("Wrong code")

    def submit(self):
        thisloop = asyncio.get_event_loop()
        coroutine = self._submit()
        thisloop.run_until_complete(coroutine)


    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.code.text = ""


class LoginWindow(Screen):
    phone = ObjectProperty(None)
    username = ObjectProperty(None)
    wrong_login = ObjectProperty(None)

    @staticmethod
    async def getUsersTL():
        print("Getting users")
        result = await TLAgent.getUsers()
        if result == -1:
            print("ERROR WHILE GETTING USERS")
        else:
            for user in result:
                my_users.append(user)
                if (user.last_name is None):
                    user.last_name = ""
                if (user.first_name is None):
                    user.first_name = ""
            print("Got users")

    async def logIn(self):
        # TODO uncomment this and delete next line
        # TLAgent.set(self.username.text, self.phone.text)
        TLAgent.set("Mihash08", "+79251851096")

        result = await TLAgent.logIn()
        if result == -1:
            self.wrong_login.text = "Wrong phone or (and) username"
        elif result == 0:
            self.wrong_login.text = ""
            sm.current = "code"
        else:
            self.wrong_login.text = ""
            await LoginWindow.getUsersTL()

            sm.current = "main"
            # await agent.getUsers()

    async def logOut(self):
        await TLAgent.logOut()

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
    table = ObjectProperty(None)
    current = ""

    def on_enter(self, *args):
        self.table.addAll(Row.initArr(my_users))

    def logOut(self):
        sm.current = "login"

class UserWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass



kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("data.txt")

screens = [LoginWindow(name="login"), LoginCodeWindow(name="code"), MainWindow(name="main"), UserWindow(name="user")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()

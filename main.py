import asyncio

import telethon.tl.types
from kivy.app import App
from kivy.app import async_runTouchApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from tlagent import TLAgent
from tlagent import TLUSer


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

    def clearRows(self):
        self.clear_widgets()


my_users = []

class Row(BoxLayout):
    txt = ObjectProperty(None)
    phone = ObjectProperty(None)
    count = ObjectProperty(None)
    id = -1

    def __init__(self, name, phone, id, count, **kwargs):
        super(Row, self).__init__(**kwargs)
        self.name.text = name
        self.phone.text = phone
        self.id = id
        if count != -1:
            self.count.text = str(count)

    @staticmethod
    def initArr(users):
        rows = []
        id_count = 0
        for user in users:
            text = str(user.first_name) + "\n" + str(user.last_name)
            rows.append(Row(text, "+" + str(user.phone), id_count, user.message_count))
            id_count += 1
        return rows

    def analyse(self):
        print(my_users[self.id])
        TLAgent.user_num = self.id
        UserWindow.current_user = my_users[self.id]
        sm.current = 'user'


class LoginCodeWindow(Screen):
    code = ObjectProperty(None)
    wrong_code = ObjectProperty(None)

    async def _submit(self):
        try:
            await TLAgent.tryCode(int(self.code.text))
            await LoginWindow.getUsersTL()
            self.wrong_code.text = ""
            sm.current = "main"
        except Exception:
            print("Wrong code")
            self.wrong_code.text = "Wrong code"


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
        self.table.clearRows()
        self.table.addAll(Row.initArr(my_users))

    def logOut(self):
        sm.current = "login"

    def refresh(self):
        thisloop = asyncio.get_event_loop()
        coroutine = self._refresh()
        thisloop.run_until_complete(coroutine)

    async def _refresh(self):
        result = await TLAgent.downloadUsers()
        if result is not None:
            my_users.clear()
            for user in result:
                my_users.append(user)
            self.table.clearRows()
            self.table.addAll(Row.initArr(my_users))

    def back(self):
        sm.current = "login"


class UserWindow(Screen):
    username = ObjectProperty(None)
    login = ObjectProperty(None)
    phone = ObjectProperty(None)
    count = ObjectProperty(None)
    rate = ObjectProperty(None)
    length = ObjectProperty(None)
    hour = ObjectProperty(None)
    wait = ObjectProperty(None)
    word = ObjectProperty(None)
    current_user = TLUSer(id=-1, message_count=-1)

    def on_enter(self, *args):
        self.username.text = self.current_user.first_name + " " + self.current_user.last_name
        self.phone.text = "+" + str(self.current_user.phone)
        self.login.text = self.current_user.username
        self.wait.text = ''
        if self.current_user.stats.count != -1:
            self.count.text = "Message count: " + str(self.current_user.stats.count)
            self.rate.text = "Message rate: " + str(self.current_user.stats.rate)
            self.length.text = "Total message length: " + str(self.current_user.stats.total_length)
            self.hour.text = "Most active hour: " + str(self.current_user.stats.max_time)
            self.word.text = "Most used word: " + str(self.current_user.stats.word)
        else:
            self.count.text = "Message count unknown"
            self.rate.text = "Message rate unknown"
            self.length.text = "Total message length unknown"
            self.hour.text = "Most active hour unknown"
            self.word.text = "Most used word unknown"

    def back(self):
        sm.current = 'main'
        self.wait.text = ''

    def analyse(self):
        thisloop = asyncio.get_event_loop()
        coroutine = self._analyse()
        thisloop.run_until_complete(coroutine)
        self.wait.text = 'Finished analysing'

    async def _analyse(self):
        self.wait.text = 'Please wait... Loading messages...'
        stats = await TLAgent.getMessages(self.current_user)
        self.current_user.message_count = stats.count
        if stats.count != -1:
            self.count.text = "Message count: " + str(stats.count)
            self.rate.text = "Message rate: " + str(stats.rate)
            self.length.text = "Total message length: " + str(stats.total_length)
            self.hour.text = "Most active hour: " + str(stats.max_time)
            self.word.text = "Most used word: " + str(stats.word)
        else:
            self.count.text = "Message count unknown"
            self.rate.text = "Message rate unknown"
            self.length.text = "Total message length unknown"
            self.hour.text = "Most active hour unknown"
            self.word.text = "Most used word unknown"



class WindowManager(ScreenManager):
    pass



kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [LoginWindow(name="login"), LoginCodeWindow(name="code"), MainWindow(name="main"), UserWindow(name="user")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()

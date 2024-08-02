import asyncio

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from telethon import errors

from View.Shared import tlAgent, sm, my_users
from tlagent import TLAgent


class LoginWindow(Screen):
    phone = ObjectProperty(None)
    username = ObjectProperty(None)
    wrong_login = ObjectProperty(None)

    def my_thread_job(self):
        print("result")

        result =-1
        tlAgent.set(self.username.text, self.phone.text)
        async def asyncfunc():
            result = await tlAgent.logIn()
        asyncio.run(asyncfunc())

        print(result)
        return result


    def cb(self, result):
        print(result)
        if result == -1:
            self.wrong_login.text = "Wrong phone or (and) username"
        elif result == 0:
            self.wrong_login.text = ""
            sm.current = "code"
        else:
            self.wrong_login.text = ""
            LoginWindow.getUsersTL()

            sm.current = "main"

    @staticmethod
    async def getUsersTL():
        print("Getting users")
        result = await tlAgent.getUsers()
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
        TLAgent.set(self.username.text, self.phone.text)

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
        await tlAgent.logOut()

    def loginBtn(self):
        self.wrong_login.text = "Connecting..."
        thisloop = asyncio.get_event_loop()
        coroutine = self.logIn()
        thisloop.run_until_complete(coroutine)
        # self.wrong_login.text = "Connecting..."
        # self.add_widget(LoadingScreen())
        # self.logIn()
        # thisloop = asyncio.get_event_loop()
        # asyncio.run(coroutine)

    def logOutBtn(self):
        thisloop = asyncio.new_event_loop()
        coroutine = self.logOut()
        thisloop.run_until_complete(coroutine)


    def reset(self):
        self.phone.text = ""
        self.password.text = ""

class LoginCodeWindow(Screen):
    code = ObjectProperty(None)
    wrong_code = ObjectProperty(None)

    async def _submit(self):
        try:
            await tlAgent.tryCode(int(self.code.text))
            await LoginWindow.getUsersTL()
            self.wrong_code.text = ""
            sm.current = "main"
        except errors.SessionPasswordNeededError:
            self.wrong_code.text = "Two-factor error"
        except Exception as e:
            print("Wrong code")
            print(e)
            self.wrong_code.text = "Wrong code"


    def submit(self):
        thisloop = asyncio.get_event_loop()
        coroutine = self._submit()
        thisloop.run_until_complete(coroutine)

    def on_enter(self, *args):
        thisloop = asyncio.get_event_loop()
        coroutine = tlAgent.clearJSON()
        # thisloop.run_until_complete(coroutine)

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.code.text = ""


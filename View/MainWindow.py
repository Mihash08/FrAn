import asyncio

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from View.Shared import my_users, tlAgent, sm
from View.Row import Row


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

    def sort(self):
        thisloop = asyncio.get_event_loop()
        coroutine = self._sort()
        thisloop.run_until_complete(coroutine)

    async def _sort(self):
        my_users.sort(key=lambda x: x.message_count, reverse=True)
        self.table.clearRows()
        self.table.addAll(Row.initArr(my_users))

    def refresh(self):
        thisloop = asyncio.get_event_loop()
        coroutine = self._refresh()
        thisloop.run_until_complete(coroutine)

    async def _refresh(self):
        result = await tlAgent.fetchUsers()
        if result is not None:
            my_users.clear()
            for user in result:
                my_users.append(user)
            self.table.clearRows()
            self.table.addAll(Row.initArr(my_users))

    def back(self):
        thisloop = asyncio.get_event_loop()
        coroutine = tlAgent.logOut()
        thisloop.run_until_complete(coroutine)
        sm.current = "login"
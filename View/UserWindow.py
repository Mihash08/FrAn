import asyncio

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from View.Shared import tlAgent, sm
from tlagent import TLUSer


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
        self.login.text = str(self.current_user.username)
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
        stats = await tlAgent.getMessages(self.current_user)
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
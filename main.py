import kivy

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import  Screen, ScreenManager
from kivy.properties import ObjectProperty

from telethon import TelegramClient, functions
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest

dev_username = "Mihash08"
api_id = 9770358
api_hash = "e9d3d03202a6d1c827187ac8cbc604b9"
dev_phone = "+79251851096"


class Widgets(Widget):
    def btn(self):
        show_popup()

class P(FloatLayout):
    pass

class MyApp(App):
    def build(self):
        return Widgets();


def show_popup():
    show = P()
    popupWindow = Popup(title="ERROR", content=show, size_hint=(None,None), size=(400,400))

    popupWindow.open()

if __name__ == "__main__":
    MyApp().run()

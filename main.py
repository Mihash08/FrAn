from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder

from View.LoginWindow import LoginWindow, LoginCodeWindow
from View.MainWindow import MainWindow
from View.Shared import tlAgent, sm
from View.Table import Table
from View.UserWindow import UserWindow

Window.size = (800, 400)
Window.minimum_width, Window.minimum_height = Window.size



# class BaseThread(threading.Thread):
#     def __init__(self, target, callback, callback_args, *args, **kwargs):
#         super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
#         self.callback = callback
#         self.method = target
#         self.callback_args = callback_args
#
#     def target_with_callback(self):
#         res = self.method()
#         if self.callback is not None:
#             self.callback(res)

table = Table()

kv = Builder.load_file("my.kv")

screens = [LoginWindow(name="login"), LoginCodeWindow(name="code"), MainWindow(name="main"), UserWindow(name="user")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"

class MyMainApp(App):
    def build(self):
        tlAgent.clearJSON()
        return sm



if __name__ == "__main__":
    MyMainApp().run()

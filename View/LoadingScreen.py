from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label


class LoadingScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)

        # Create the label
        self.label = Label(text="Loading...", font_size=50)
        self.label.size_hint = (0.8, 0.2)
        self.label.pos_hint = {'x': 0.1, 'y': 0.7}
        self.add_widget(self.label)

        # Schedule the label update
        self.event = Clock.schedule_interval(self.update_label, 1 / 2.)

    def update_label(self, dt):
        if self.label.text.endswith("..."):
            self.label.text = "Loading"
        else:
            self.label.text += "."

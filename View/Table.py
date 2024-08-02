from kivy.uix.boxlayout import BoxLayout


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
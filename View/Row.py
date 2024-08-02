from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from View import UserWindow
from View.Shared import tlAgent, sm, my_users


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
        tlAgent.user_num = self.id
        UserWindow.current_user = my_users[self.id]
        sm.current = 'user'
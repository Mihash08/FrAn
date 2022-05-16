import datetime


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.username = ""
        self.phone = ""

    def load(self):
        self.file = open(self.filename, "r")

        for line in self.file:
            phone, username = line.strip().split(";")
            self.username = username
            self.phone = phone

        self.file.close()

    def get_username(self):
        if self.username != "":
            return self.username
        else:
            return -1
    def get_phone(self):
        if self.phone != "":
            return self.phone
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email exists already")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]
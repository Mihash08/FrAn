import datetime


class UserStat:

    def __init__(self, messages=None):
        if not messages:
            self.count = -1
            self.rate = datetime.timedelta(seconds=0)
            self.total_length = -1
            self.word = ""
            self.max_time = ""
            self.max_time_messages = 0
            return
        self.count = len(messages)
        self.rate = datetime.timedelta(seconds=0)
        self.total_length = -1
        self.word = ""
        self.max_time = ""
        self.max_time_messages = 0
        if (len(messages) < 2):
            return
        last_time = messages[0]['date']
        first_time = messages[len(messages) - 1]['date']
        self.rate = datetime.timedelta(seconds=(last_time - first_time).total_seconds() / self.count)
        time_dict = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 0,
            17: 0,
            18: 0,
            19: 0,
            20: 0,
            21: 0,
            22: 0,
            23: 0,
        }

        word_dict = {
            "": 0
        }

        self.total_length = 0
        for mes in messages:
            if 'message' in mes:
                for word in mes['message'].split(" "):
                    if word != "":
                        if word in word_dict.keys():
                            word_dict[word] += 1
                        else:
                            word_dict[word] = 1
                self.total_length += len(str(mes['message']))
            time_dict[mes['date'].hour] += 1
        max_hour = 0
        max_messages = 0
        for key in time_dict.keys():
            if time_dict[key] > max_messages:
                max_messages = time_dict[key]
                max_hour = key
        self.max_time = max_hour
        self.max_time_messages = max_messages
        max_word = 0
        for key in word_dict.keys():
            if word_dict[key] > max_word:
                max_word = word_dict[key]
                self.word = key

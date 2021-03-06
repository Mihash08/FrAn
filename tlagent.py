import json
import inspect
import os
import sys
import datetime

from datetime import timedelta, datetime as dt
from typing import Optional, List

import telethon.tl.types
from telethon import TelegramClient, functions, utils, errors
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel, PeerUser

# username = "Mihash08"
api_id = 9770358
api_hash = "e9d3d03202a6d1c827187ac8cbc604b9"


# phone = "+79251851096"


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, dt):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)


class TLUSer(telethon.tl.types.User):
    message_count = -1

    def __init__(self, id: int, message_count,
                 first_name: Optional[str] = None, last_name: Optional[str] = None, username: Optional[str] = None,
                 phone: Optional[str] = None):
        telethon.tl.types.User.__init__(self, id=id, first_name=first_name, last_name=last_name, username=username,
                                        phone=phone)
        self.message_count = message_count
        self.stats = UserStat()


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

class TLAgent:
    client = None
    phone = ""
    username = ""
    user_num = -1

    @staticmethod
    def set(username, phone):
        TLAgent.username = username
        TLAgent.phone = phone
        TLAgent.client = TelegramClient(username, api_id, api_hash)

    @staticmethod
    async def _start(phone):
        if not TLAgent.client.is_connected():
            await TLAgent.client.connect()
        me = await TLAgent.client.get_me()
        if me is not None:
            return TLAgent.client
        while callable(phone):
            value = phone()
            if inspect.isawaitable(value):
                value = await value
            phone = utils.parse_phone(value) or phone
        await TLAgent.client.send_code_request(phone)

    @staticmethod
    async def tryCode(code):
        try:
            value = code
            if inspect.isawaitable(value):
                value = await value
            if not value:
                raise errors.PhoneCodeEmptyError(request=None)
            me = await TLAgent.client.sign_in(TLAgent.phone, code=value)
        except (errors.PhoneCodeEmptyError,
                errors.PhoneCodeExpiredError,
                errors.PhoneCodeHashEmptyError,
                errors.PhoneCodeInvalidError):
            print('Invalid code. Please try again.', file=sys.stderr)
            raise errors.PhoneCodeInvalidError
        return me

    @staticmethod
    async def logOut():
        await TLAgent.client.log_out()

    @staticmethod
    async def logIn():
        try:
            await TLAgent._start(phone=TLAgent.phone)
            # if not await TLAgent.client.is_user_authorized():
            #    await TLAgent.tryCode(phone=TLAgent.phone, code=int(input("input code")))
            # self.client.start(phone=self.phone)
        except Exception as e:
            print("LOGIN ERROR: " + str(e))
            return -1
        print("Client Created")
        # Ensure you're authorized
        if await TLAgent.client.is_user_authorized():
            return 1
        else:
            return 0

    @staticmethod
    async def getUsersFromJSON():
        users = []

        f = open('dat\\data_users.json')

        data = json.load(f)
        for input in data:
            users.append(TLUSer(int(input['id']), first_name=input['first_name'],
                                last_name=input['last_name'], phone=input['phone'],
                                username=input['username'], message_count=input['messages']))
        return users

    @staticmethod
    async def getUsers():
        if os.path.exists('dat\\data_users.json'):
            if os.stat('dat\\data_users.json').st_size != 0:
                print("GETTING USERS FROM JSON")
                return await TLAgent.getUsersFromJSON()
        print("DOWNLOADING USERS")
        return await TLAgent.downloadUsers()

    @staticmethod
    async def downloadUsers():
        contacts = None
        try:
            contacts = await TLAgent.client(functions.contacts.GetContactsRequest(hash=0))
            print('All contacts collected successfully')
        except Exception as e:
            print(e)
        all_contacts = []
        tlusers = []
        for user in contacts.users:
            if user.id != None:
                id = str(user.id)
            else:
                id = -1
            if user.first_name != None:
                name = user.first_name
            else:
                name = " "
            if user.last_name != None:
                lname = user.last_name
            else:
                lname = " "
            # print(user)
            tlusers.append(TLUSer(id=user.id, message_count=-1, first_name=user.first_name, last_name=user.last_name,
                                  username=user.username, phone=user.phone))
            all_contacts.append({"id": user.id, "first_name": user.first_name, "last_name": user.last_name,
                                 "username": user.username, "phone": user.phone, "messages": -1})
            with open('dat\\data_users.json', 'w', encoding='utf-8') as outfile:
                json.dump(all_contacts, outfile)
        return tlusers

    @staticmethod
    async def getMessages(user):
        print("Getting messages")
        user_id = user.id
        entity = user_id

        my_channel = await TLAgent.client.get_entity(entity)

        offset_id = 0
        limit = 5000
        all_messages = []
        total_messages = 0
        total_count_limit = 0
        serializeble_messages = []
        while True:
            history = await TLAgent.client(GetHistoryRequest(
                peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            messages = history.messages
            for this_message in messages:
                all_messages.append(this_message.to_dict())
                serializeble_messages.append({"text": this_message.message, "out": this_message.out,
                                              "date": this_message.date, "id": this_message.id})
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            print(all_messages[len(all_messages) - 1])
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        print(total_messages)
        with open('dat\\' + str(user.username) + str(user.phone) + '.json', 'w', encoding='utf-8') as outfile:
            json.dump(serializeble_messages, outfile, cls=DateTimeEncoder)
        stats = UserStat(all_messages)
        user.stats = stats
        return stats

    @staticmethod
    def clearJSON():
        if not os.path.exists("dat"):
            os.mkdir('dat')
        if os.path.exists('dat\\data_users.json'):
            open('dat\\data_users.json', 'w').close()


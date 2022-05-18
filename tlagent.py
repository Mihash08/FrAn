import json
import asyncio
import getpass
import inspect
import os
import sys
import typing
import warnings

from datetime import date, datetime

from telethon import TelegramClient, types, functions, utils, errors
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest, GetMessagesRequest
from telethon.tl.types import PeerChannel, PeerUser

#username = "Mihash08"
api_id = 9770358
api_hash = "e9d3d03202a6d1c827187ac8cbc604b9"
#phone = "+79251851096"


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)


class TLAgent:
    #client = TelegramClient("", 0, "")
    #phone = ""
    #username = ""

    def __init__(self, username, phone):
        self.username = username
        self.phone = phone
        self.client = TelegramClient(username, api_id, api_hash)

    async def _start(
            self, phone):
        if not self.client.is_connected():
            await self.client.connect()

        me = await self.client.get_me()
        if me is not None:
            return self.client

        while callable(phone):
            value = phone()
            if inspect.isawaitable(value):
                value = await value

            phone = utils.parse_phone(value) or phone

        me = None
        attempts = 0
        # two_step_detected = False
        await self.client.send_code_request(phone)

    @staticmethod
    async def tryCode(self, phone, code):
        # sign_up = False
        try:
            value = code
            if inspect.isawaitable(value):
                value = await value

            if not value:
                raise errors.PhoneCodeEmptyError(request=None)

            # Raises SessionPasswordNeededError if 2FA enabled
            me = await self.client.sign_in(phone, code=value)
        # except errors.SessionPasswordNeededError:
        #    two_step_detected = True
        #    break

        except (errors.PhoneCodeEmptyError,
                errors.PhoneCodeExpiredError,
                errors.PhoneCodeHashEmptyError,
                errors.PhoneCodeInvalidError):
            print('Invalid code. Please try again.', file=sys.stderr)
            raise errors.PhoneCodeInvalidError
        return me

    async def logOut(self):
        await self.client.log_out()


    async def logIn(self):
        try:
            await self._start(phone=self.phone)
            if not await self.client.is_user_authorized():
                await self.tryCode(phone=self.phone, code=int(input("input code")))
            # self.client.start(phone=self.phone)
        except Exception as e:
            print("LOGIN ERROR: " + str(e))
            return -1
        print("Client Created")
        # Ensure you're authorized
        if await self.client.is_user_authorized():
            return 1
        else:
            return 0

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input('Password: '))
        return 1
    async def getUsers(self):

        contact_ids = None
        contacts = None
        try:
            contacts = await self.client(functions.contacts.GetContactsRequest(hash=0))
            contact_ids = (user.id for user in contacts.users)
            print('All contacts collected successfully')
        except Exception as e:
            print(e)

        all_contacts = []
        with open("dat\\users.txt", "w", encoding="utf-8") as f:
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
                print(user)
                f.write(id + ";" + name + ";" + lname + "\n")
                all_contacts.append({"id": user.id, "first_name": user.first_name, "last_name": user.last_name,
                                     "username": user.username, "phone": user.phone, "messages": None})
            f.close()
            with open('dat\\data_users.json', 'w', encoding='utf-8') as outfile:
                json.dump(all_contacts, outfile)
        return contact_ids

    async def getMessages(self):
        user_id = self.entity
        entity = user_id
        print(self.user.first_name, " ", self.user.last_name)

        my_channel = await self.client.get_entity(entity)

        offset_id = 0
        limit = 5000
        all_messages = []
        total_messages = 0
        total_count_limit = 0

        while True:
            history = await self.client(GetHistoryRequest(
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
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            print(all_messages[len(all_messages) - 1])
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        print(total_messages)
        return all_messages

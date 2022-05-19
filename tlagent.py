import json
import asyncio
import getpass
import inspect
import os
import sys
import typing
import warnings

from datetime import date, datetime

import telethon.tl.types
from telethon import TelegramClient, types, functions, utils, errors
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest, GetMessagesRequest
from telethon.tl.types import PeerChannel, PeerUser

# username = "Mihash08"
api_id = 9770358
api_hash = "e9d3d03202a6d1c827187ac8cbc604b9"


# phone = "+79251851096"


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)


class TLAgent:
    client = None
    phone = ""
    username = ""

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

        me = None
        attempts = 0
        # two_step_detected = False
        await TLAgent.client.send_code_request(phone)

    @staticmethod
    async def tryCode(code):
        # sign_up = False
        try:
            value = code
            if inspect.isawaitable(value):
                value = await value

            if not value:
                raise errors.PhoneCodeEmptyError(request=None)

            # Raises SessionPasswordNeededError if 2FA enabled
            me = await TLAgent.client.sign_in(TLAgent.phone, code=value)
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

        if not await TLAgent.client.is_user_authorized():
            await TLAgent.client.send_code_request(TLAgent.phone)
            try:
                await TLAgent.client.sign_in(TLAgent.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await TLAgent.client.sign_in(password=input('Password: '))
        return 1

    @staticmethod
    async def scanUsers():
        users = []

        f = open('dat\\data_users.json')

        data = json.load(f)
        for input in data:
            users.append(telethon.tl.types.User(int(input['id']), first_name=input['first_name'],
                                               last_name=input['last_name'], phone=input['phone'],
                                               username=input['username']))
        return users


    @staticmethod
    async def getUsers():
        if os.stat('dat\\data_users.json').st_size == 0:
            print("SCANNING USERS")
        else:
            print("GETTING USERS FROM JSON")
            return await TLAgent.scanUsers()
        contact_ids = None
        contacts = None
        try:
            contacts = await TLAgent.client(functions.contacts.GetContactsRequest(hash=0))
            contact_ids = (user.id for user in contacts.users)
            print('All contacts collected successfully')
        except Exception as e:
            print(e)

        all_contacts = []
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
            all_contacts.append({"id": user.id, "first_name": user.first_name, "last_name": user.last_name,
                                 "username": user.username, "phone": user.phone, "messages": None})
            with open('dat\\data_users.json', 'w', encoding='utf-8') as outfile:
                json.dump(all_contacts, outfile)
        return contacts.users

    @staticmethod
    async def getMessages():
        user_id = TLAgent.entity
        entity = user_id
        print(TLAgent.user.first_name, " ", TLAgent.user.last_name)

        my_channel = await TLAgent.client.get_entity(entity)

        offset_id = 0
        limit = 5000
        all_messages = []
        total_messages = 0
        total_count_limit = 0

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
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            print(all_messages[len(all_messages) - 1])
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
        print(total_messages)
        return all_messages

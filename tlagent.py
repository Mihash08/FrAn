import json
import asyncio

from datetime import date, datetime

from telethon import TelegramClient, types, functions
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
    def __init__(self, username, phone):
        self.username = username
        self.phone = phone
        self.client = TelegramClient(username, api_id, api_hash)

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

    async def getUsers(self):
        await self.client.start()
        print("Client Created")
        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input('Password: '))
        contact_ids = None
        contacts = None
        try:
            contacts = await self.client(functions.contacts.GetContactsRequest(hash=0))
            contact_ids = (user.id for user in contacts.users)
            print('All contacts collected successfully')
        except Exception as e:
            print(e)

        with open('channel_messages.json', 'w') as outfile:
            json.dump(contact_ids, outfile, cls=DateTimeEncoder)
        return contact_ids

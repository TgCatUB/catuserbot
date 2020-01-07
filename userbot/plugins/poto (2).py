# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging

from userbot.utils import admin_cmd

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location

logger = logging.getLogger(__name__)



if 1 == 1:
    """Description for module"""
    name = "Profile Photos"
    client = borg

    @borg.on(admin_cmd(pattern="poto(.*)"))
    async def potocmd(event):
        """Gets the profile photos of replied users, channels or chats"""
        id = event.raw_text.split(maxsplit=2)[1]
        user = await event.get_reply_message()
        chat = message.input_chat
        if user:
            photos = await event.client.get_profile_photos(user.sender)
        else:
            photos = await event.client.get_profile_photos(chat)
        if id.strip() == "":
            try:
                await event.client.send_file(message.chat_id, photos)
            except a:
                photo = await event.client.download_profile_photo(chat)
                await borg.send_file(message.chat_id, photo)
        else:
            try:
                id = int(id)
                if id <= 0:
                    await event.edit("<code>ID number you entered is invalid</code>")
                    return
            except:
                 await message.edit("<code>ID number you entered is invalid</code>")
                 return
            if int(id) <= (len(photos)):
                send_photos = await event.client.download_media(photos[id - 1])
                await borg.send_file(message.chat_id, send_photos)
            else:
                await event.edit("<code>No photo found with that id</code>")
                return
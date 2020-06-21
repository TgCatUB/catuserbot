# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern=r"tagall", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    mentions = "Hello"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, 100):
        mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    await event.reply(mentions)
    await event.delete()

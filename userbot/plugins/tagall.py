# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""A Plugin to tagall in the chat for @UniBorg and cmd is `.all`"""

from telethon import events
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=r"tagall", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    mentions = "@all"
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await borg.send_message(
        chat, mentions, reply_to=event.message.reply_to_msg_id)

@borg.on(admin_cmd(pattern=r"all (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    else:
    	await event.edit("`What I am Supposed to find `")
    	return
    await event.delete()
    mentions = query 
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await borg.send_message(
        chat, mentions, reply_to=event.message.reply_to_msg_id)
    

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""A Plugin to tagall in the chat for @UniBorg and cmd is `.all`"""

from telethon import events
from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern="tagall"))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    mentions = "@all"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await reply_to_id.reply(mentions)
    await event.delete()

@borg.on(admin_cmd(pattern="all (.*)"))
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    input_str = event.pattern_match.group(1)

    if not input_str:
        return await event.edit("what should i do try `.all hello`.")

    mentions = input_str 
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, 100):
        mentions += f"[\u2063](tg://user?id={x.id})"
    await reply_to_id.reply(mentions)
    await event.delete()
    

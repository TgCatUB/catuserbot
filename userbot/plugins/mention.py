# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""A Plugin to tagall in the chat for @UniBorg and cmd is `.all`"""
# Mention By: @INF1N17Y

from telethon.tl.types import ChannelParticipantsAdmins

from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="admins"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "@admin: **Spam Spotted**"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f"[\u2063](tg://user?id={x.id})"
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()


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


@borg.on(admin_cmd(pattern="men (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        input_str = event.pattern_match.group(1)
        reply_msg = await event.get_reply_message()
        caption = """<a href='tg://user?id={}'>{}</a>""".format(
            reply_msg.from_id, input_str
        )
        await event.delete()
        await borg.send_message(event.chat_id, caption, parse_mode="HTML")
    else:
        await event.edit("Reply to user with `.mention <your text>`")

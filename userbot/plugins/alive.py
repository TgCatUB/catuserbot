""".admin Plugin for @UniBorg"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from userbot.utils import admin_cmd


@borg.on(admin_cmd("alive"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "` Jinda Hu Sarr ^.^ \nYour bot is running\n\nTelethon version: 6.9.0\nPython: 3.7.3\nfork by:` @A_Dark_Princ3\n`Database Status: Databases functioning normally!`"
    chat = await event.get_input_chat()
    async for x in borg.iter_participants(chat, filter=ChannelParticipantsAdmins):
        mentions += f""
    reply_message = None
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        await reply_message.reply(mentions)
    else:
        await event.reply(mentions)
    await event.delete()

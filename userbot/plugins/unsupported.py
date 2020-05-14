"""Command: `.repo` , .session"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="session"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**telethon.errors.rpcerrorlist.AuthKeyDuplicatedError: The authorization key (session file) was used under two different IP addresses simultaneously, and can no longer be used. Use the same session exclusively, or use different sessions (caused by GetMessagesRequest)**"
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

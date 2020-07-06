import asyncio
from userbot.utils import admin_cmd
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins



@borg.on(admin_cmd(pattern="session$"))
async def _(event):
    if event.fwd_from:
        return
    mentions = "**telethon.errors.rpcerrorlist.AuthKeyDuplicatedError: The authorization key (session file) was used under two different IP addresses simultaneously, and can no longer be used. Use the same session exclusively, or use different sessions (caused by GetMessagesRequest)**"
    await event.edit(mentions)

@borg.on(admin_cmd(pattern="ccry$"))
async def cry(e):
        await e.edit("(;´༎ຶД༎ຶ`)")

@borg.on(admin_cmd(pattern="fp$"))
async def facepalm(e):
        await e.edit("🤦‍♂")

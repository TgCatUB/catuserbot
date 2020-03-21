"""Count the Number of Dialogs you have in your Telegram Account
Syntax: .stat"""
from telethon import events
import asyncio
from datetime import datetime
from telethon.tl.types import User, Chat, Channel
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="stat"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    u = 0 # number of users
    g = 0 # number of basic groups
    c = 0 # number of super groups
    bc = 0 # number of channels
    b = 0 # number of bots
    await event.edit("Retrieving Telegram Count(s)")
    async for d in borg.iter_dialogs(limit=None):
        if d.is_user:
            if d.entity.bot:
                b += 1
            else:
                u += 1
        elif d.is_channel:
            if d.entity.broadcast:
                bc += 1
            else:
                c += 1
        elif d.is_group:
            g += 1
        else:
            logger.info(d.stringify())
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("""Obtained in {} seconds.\n
`Users:`\t**{}**
`Groups:`\t**{}**
`Super Groups:`\t**{}**
`Channels:`\t**{}**
`Bots:`\t**{}**""".format(ms, u, g, c, bc, b))

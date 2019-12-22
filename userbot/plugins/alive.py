""".admin Plugin for @XtraTgBot"""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from platform import uname
from userbot import ALIVE_NAME
from userbot.utils import admin_cmd

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node

@borg.on(outgoing=True, pattern="^.alive$")
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    await alive.edit("`Jinda Hu Sarr ^.^ \nYour bot is running\n\n`"
                     "`Telethon version: 6.9.0\nPython: 3.7.3\nfork by:` @A_Dark_Princ3\n`Database Status: Databases functioning normally!\n\n Always with you, my master!\n`"
                     "[Deploy Now](https://github.com/Dark-Princ3/X-tra-Telegram)
                     f"Owner: {DEFAULTUSER}")
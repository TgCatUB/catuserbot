"""Check if userbot alive. If you change these, you become the gayest gay such that even the gay world will disown you."""
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from platform import uname
from userbot import ALIVE_NAME
from userbot.utils import admin_cmd

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"

@command(outgoing=True, pattern="^.alive$")
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
<<<<<<< HEAD
    await alive.edit("**MY BOT IS RUNNING SUCCESFULLY**\n\n"
                     "`Telethon version: 1.11.3\nPython: 3.8.2\nBot was build by:` @mrconfused\n"
                     "`fork by :` [Sandeep](tg://user?id=916234223)\n"
                     "`Database Status: Databases functioning normally!\n\nAlways with you, my master!\n`"
                     f"`My peru owner`: {DEFAULTUSER}\n"
                     #"[Deploy this userbot Now](https://github.com/sandy1709/userbot)"
                    )
=======
    await alive.edit("`Currently Alive!` **ψ(｀∇´)ψ**\n\n"
                     "`Telethon version: 6.9.0\nPython: 3.7.3\n`"
                     "`Bot created by:` [SnapDragon](tg://user?id=719877937), @anubisxx\n"
                     f"`My peru owner`: {DEFAULTUSER}\n\n"
                     "https://github.com/Dark-Princ3/X-tra-Telegram")
>>>>>>> e5ef0b3993bbed07fa8182df63a2a5da234c5941

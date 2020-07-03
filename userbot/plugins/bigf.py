"""command: .kk"""
"""By @Grandpaa_please """

from telethon import events
import random
import logging
from userbot.utils import admin_cmd

@borg.on(admin_cmd(outgoing=True, pattern="kf$(.*)"))
async def _(event):                             
                 r = random.randint(0, 3)
                 logger.debug(r)
                 if r == 0:
                     await event.edit("┏━━━┓\n┃┏━━┛\n┃┗━━┓\n┃┏━━┛\n┃┃\n┗┛")
                 else:
                     r == 1            
                     await event.edit("╭━━━╮\n┃╭━━╯\n┃╰━━╮\n┃╭━━╯\n┃┃\n╰╯")

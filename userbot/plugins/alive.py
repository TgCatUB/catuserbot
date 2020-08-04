"""Check if userbot alive or not . """

import asyncio , time
from telethon import events
from userbot import StartTime
from platform import uname
from userbot import CMD_HELP, ALIVE_NAME, catversion , catdef
from userbot.utils import admin_cmd,sudo_cmd
from telethon import version
from platform import python_version, uname
import requests
import re
from PIL import Image
import os
import nekos

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
CAT_IMG = Config.ALIVE_PIC

@borg.on(admin_cmd(outgoing=True, pattern="alive$"))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = alive.message
    uptime = await catdef.get_readable_time((time.time() - StartTime))
    if alive.reply_to_msg_id:
        reply_to_id = await alive.get_reply_message()
    if CAT_IMG:
         cat_caption  = f"**MY BOT IS RUNNING SUCCESFULLY**\n\n"
         cat_caption += f"**Database Status: Databases functioning normally!\n**"   
         cat_caption += f"☞Telethon version : `{version.__version__}\n`"
         cat_caption += f"☞Catuserbot Version : `{catversion}`\n"
         cat_caption += f"☞Python Version : `{python_version()}\n\n`"
         cat_caption += f"**cat🐱 is always with you, my master!\n**"
         cat_caption += f"☞My peru Master: {DEFAULTUSER}\n"
         cat_caption += f"☞uptime : `{uptime}\n`"
         cat_caption +=	f"☞**Click **[here](https://github.com/sandy1709/catuserbot) to deploy catuserbot"
         await borg.send_file(alive.chat_id, CAT_IMG, caption=cat_caption, reply_to=reply_to_id)
         await alive.delete()
    else:
        await alive.edit(f"**MY BOT IS RUNNING SUCCESFULLY**\n\n"
                         "**Database Status: Databases functioning normally!\n**" 
                         f"☞Telethon version : `{version.__version__}\n`"
			 f"☞Catuserbot Version : `{catversion}`\n"
                         f"☞Python Version : `{python_version()}\n\n`"
                         "**cat🐱 is always with you, my master!\n**"
                         f"☞My peru Master: {DEFAULTUSER}\n"
                         f"☞uptime : `{uptime}\n`"
                         f"☞**Click **[here](https://github.com/sandy1709/catuserbot) to deploy catuserbot"
                        )         

@borg.on(sudo_cmd(pattern="sudo", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    uptime = await catdef.get_readable_time((time.time() - StartTime))
    await event.reply(" SUDO COMMANDS ARE WORKING PERFECTLY \n\n"
                     f"☞Telethon version: {version.__version__}\n"
                     f"☞Python: {python_version()}\n"
                     f"☞My peru owner: {DEFAULTUSER}\n"
                     f"**uptime :** `{uptime}\n`"
                     #"Deploy this userbot Now"
                    )

@borg.on(admin_cmd(pattern="cat$"))
async def _(event):
    await event.delete() 
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.cat()).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    img.seek(0)
    await bot.send_file(event.chat_id , open("temp.webp", "rb"),reply_to=reply_to_id) 
	
CMD_HELP.update({"alive": "`.alive` :\
      \n**USAGE:** Type .alive to see wether your bot is working or not.\
      \n\n`.cat`\
      \n**USAGE : **Random cat stickers"
})

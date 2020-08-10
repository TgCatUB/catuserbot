"""Check if userbot alive or not . """


import asyncio , time
from telethon import events
from userbot import StartTime 
from platform import uname
from userbot import CMD_HELP, ALIVE_NAME, catdef , catversion
from userbot.utils import admin_cmd,sudo_cmd
from telethon import version
from platform import python_version, uname
import requests
import re
from PIL import Image
import os
import nekos


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
USERNAME = str(Config.LIVE_USERNAME) if Config.LIVE_USERNAME else "@Jisan7509"
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
         cat_caption  = f"__**༄ MY BOT IS RUNNING SUCCESFULLY ༄**__\n\n"
         cat_caption += f"**✧✧ Database :** `Functioning normally!`\n"   
         cat_caption += f"**✧✧ Telethon version :** `{version.__version__}\n`"
         cat_caption += f"**✧✧ Catuserbot Version :** `{catversion}`\n"
         cat_caption += f"**✧✧ Python Version :** `{python_version()}\n\n`"
         cat_caption += f"**ღ** __**Cat**__🐱 __**is always with you, my master ღ\n\n**__"
         cat_caption += f"**✧✧ My peru Master:** [{DEFAULTUSER}]({USERNAME})\n"
         cat_caption += f"**✧✧ Uptime :** `{uptime}\n`"
         cat_caption += f"**✧✧ Contact [Hatake Kakashi](@kakashi_robot) For notes**\n\n"
         cat_caption +=	f"           **ღ** __**[DEPLOY MY REPO]**__(https://github.com/Jisan09/catuserbot) **ღ**"
         await borg.send_file(alive.chat_id, CAT_IMG, caption=cat_caption, reply_to=reply_to_id)
         await alive.delete()
    else:
        await alive.edit(f"__**༄ MY BOT IS RUNNING SUCCESFULLY ༄**__\n\n"
                         "**✧✧ Database :** `Functioning normally!`\n"   
                         f"**✧✧ Telethon Version :** `{version.__version__}\n`"
                         f"**✧✧ Catuserbot Version :** `{catversion}`\n"
                         f"**✧✧ Python Version :** `{python_version()}\n\n`"
                         "**ღ** __**Cat**__🐱 __**is always with you, my master ღ\n\n**__"
                         f"**✧✧ My Peru Master:** [{DEFAULTUSER}]({USERNAME})\n"
                         f"**✧✧ Uptime :** `{uptime}\n`"
                         f"**✧✧ Contact [Hatake Kakashi](@kakashi_robot) For notes**\n\n"
                         f"           **ღ** __**[DEPLOY MY REPO]**__(https://github.com/Jisan09/catuserbot) **ღ**"
                        )         


@borg.on(sudo_cmd(pattern="sudo", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    uptime = await catdef.get_readable_time((time.time() - StartTime))
    await event.reply("__**༄ SUDO COMMANDS ARE WORKING PERFECTLY ༄**__\n\n"
                     f"**✧✧ Telethon Version :** `{version.__version__}\n`"
                     f"**✧✧ Python Version :** `{python_version()}\n\n`"
                     f"**✧✧ My Peru Owner:** [{DEFAULTUSER}]({USERNAME})\n"
                     f"**✧✧ Uptime :** `{uptime}\n`"
                    )   
@borg.on(admin_cmd(outgoing=True, pattern="live$"))
async def amireallyalive(alive):
    if alive.fwd_from:
        return
    reply_to_id = alive.message
    uptime = await catdef.get_readable_time((time.time() - StartTime))
    if alive.reply_to_msg_id:
        reply_to_id = await alive.get_reply_message()
    if CAT_IMG:
         cat_caption  = f"__**✮ MY BOT IS RUNNING SUCCESFULLY ✮**__\n\n"
         cat_caption += f"**✧ Database :** `Functioning normally!`\n"   
         cat_caption += f"**✧ Telethon version :** `{version.__version__}\n`"
         cat_caption += f"**✧ Catuserbot Version :** `{catversion}`\n"
         cat_caption += f"**✧ Python Version :** `{python_version()}\n`"
         cat_caption += f"**✧ My peru Master:** [{DEFAULTUSER}]({USERNAME})\n"
         cat_caption += f"**✧ Uptime :** `{uptime}\n`"
         await borg.send_file(alive.chat_id, CAT_IMG, caption=cat_caption, reply_to=reply_to_id)
         await alive.delete()
    else:
        await alive.edit(f"__**✮ MY BOT IS RUNNING SUCCESFULLY ✮**__\n\n"
                         "**✧ Database :** `Functioning normally!`\n"   
                         f"**✧ Telethon Version :** `{version.__version__}\n`"
                         f"**✧ Catuserbot Version :** `{catversion}`\n"
                         f"**✧ Python Version :** `{python_version()}\n`"
                         f"**✧ My Peru Master:** [{DEFAULTUSER}]({USERNAME})\n"
                         f"**✧ Uptime :** `{uptime}\n`"
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
      \n\n`.live`\
      \n**USAGE : **status of bot.\
      \n\n`.cat`\
      \n**USAGE : **Random cat stickers"
})

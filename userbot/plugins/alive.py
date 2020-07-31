"""Check if userbot alive or not . """
import os
import time
import asyncio
from telethon import events
from userbot import StartTime
from userbot import ALIVE_NAME, CMD_HELP, catdef, catversion
from userbot.utils import admin_cmd, sudo_cmd
from telethon import version
from platform import python_version, uname
import requests
import re
from PIL import Image
import os
import nekos

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "Sur_vivor"

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
         cat_caption  = f"🚴‍♂️**MY BOT IS RUNNING SUCCESFULLY**\n\n"
         cat_caption += f"**Database Status: Databases Functioning Normally!**\n"   
         cat_caption += f"⏳`Telethon Version:` **{version.__version__}**\n"
         cat_caption += f"⏳`Python Version:` **{python_version()}**\n"
         cat_caption += f"⏳`CatUserbot Version:` **{catversion}**\n"
         cat_caption += f"⏳`Cat Uptime:` **{uptime}**\n\n"         
         cat_caption += f"**Cat is Always With You, My Masters!**\n"
         cat_caption += f"⏳`Owner Name:` {DEFAULTUSER}\n"   
         cat_caption += f"⏳`Modified by:` [✰Sᴀͥʀᴀͣᴛͫʜ™️✰](t.me/Sur_vivor)\n\n"         
         cat_caption += f"**[⚜️DEPLOY CATUSERBOT⚜️](https://github.com/Sur-vivor/CatUserbot)**"
         await borg.send_file(alive.chat_id, CAT_IMG, caption=cat_caption)
         await alive.delete()
    else:
        await alive.edit("🚴‍♂️**MY BOT IS RUNNING SUCCESFULLY**\n\n"
                         "**Database Status: Databases Functioning Normally!**\n"
                         f"⏳`Telethon Version:` **{version.__version__}**\n"
                         f"⏳`Python Version:` **{python_version()}**\n"
                         f"⏳`Catuserbot Version:` **{catversion}**\n"
                         f"⏳`Cat Uptime:` **{uptime}**\n\n"                        
                         "**Cat is Always With You, My Masters!**\n"                                                
                         f"⏳`Owner Name:` {DEFAULTUSER}\n"
                         "⏳`Modified by:` [✰Sᴀͥʀᴀͣᴛͫʜ™️✰](t.me/Sur_vivor)\n\n"
                         f"**[⚜️DEPLOY CATUSERBOT⚜️](https://github.com/Sur-vivor/CatUserbot)**"
                        )

@borg.on(sudo_cmd(pattern="sudo", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    uptime = await catdef.get_readable_time((time.time() - StartTime))
    await event.reply(" SUDO COMMANDS ARE WORKING PERFECTLY \n\n"
                     f"☞Telethon version: {version.__version__}\n"
                     f"☞Python: {python_version()}\n"
                     f"☞My Owner: {DEFAULTUSER}\n"
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

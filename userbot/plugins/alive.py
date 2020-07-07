"""Check if userbot alive or not . """
import os
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from userbot import ALIVE_NAME, CMD_HELP
from userbot.utils import admin_cmd
from telethon import version
from platform import python_version, uname

ALIVE_PIC = os.environ.get("ALIVE_PIC", None)
if ALIVE_PIC is None:
  CAT_IMG = "https://telegra.ph/file/4117e39218991cdd7379f.jpg"
else:
  CAT_IMG = ALIVE_PIC


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@Sur_vivor"

cat_caption = "🚴‍♂️**MY BOT IS RUNNING SUCCESFULLY**\n\n"
cat_caption += f"⏳`Telethon Version:` **{version.__version__}**\n"
cat_caption += f"⏳`Python Version:` **{python_version()}**\n"
cat_caption += "⏳`Database Status :` Databases Functioning Normally!\n"
cat_caption += "💠**Always With You, My Masters!**\n"
cat_caption += "⏳`Modified by :` [✰Sᴀͥʀᴀͣᴛͫʜ™️✰](http://t.me/Sur_vivor)\n"
cat_caption += "⏳`Created by :` Snapdragon, Anubis, Sandeep\n"
cat_caption += f"⏳`Owner Name :` {DEFAULTUSER}\n\n"
cat_caption += "**[⚜️DEPLOY CATUSERBOT⚜️](https://github.com/Sur-vivor/CatUserbot)**"


@borg.on(admin_cmd(outgoing=True, pattern="alive$"))
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running."""    
    await borg.send_file(alive.chat_id, CAT_IMG, caption=cat_caption)
    await alive.delete()

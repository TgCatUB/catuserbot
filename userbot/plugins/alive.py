"""Check if userbot alive or not . """
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from userbot import ALIVE_NAME, CMD_HELP
from userbot.utils import admin_cmd
from telethon import version
from platform import python_version, uname


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@Sur_vivor"
CAT_IMG = "https://telegra.ph/file/be15be483400f07f7e442.jpg"
cat_caption = "**MY BOT IS RUNNING SUCCESFULLY**\n\n"
cat_caption += f"🛡`Telethon Version:` **{version.__version__}**\n\n"
cat_caption += f"🛡`Python Version:` **{python_version()}**\n\n"
cat_caption += "🛡**Bot Was Modified by**:[✰Şสͥℝสͣ✞ͫђ™✰](http://t.me/Sur_vivor)\n\n"
cat_caption += "🛡**Created by**: Snapdragon,Anubis,Sandeep\n\n"
cat_caption += "🛡**Database Status**: Databases Functioning Normally!\n\n"
cat_caption += "🛡**Always With You, My Master!**\n\n"
cat_caption += f"🛡**Owner Name**: {DEFAULTUSER}\n\n\n"
cat_caption += "[⚜️**DEPLOY THIS USERBOT**⚜️](https://github.com/Sur-vivor/CatUserbot)"


@borg.on(admin_cmd(pattern=r"alive"))
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    await alive.delete()
    await borg.send_file(alive.chat_id, CAT_IMG, caption=cat_caption)

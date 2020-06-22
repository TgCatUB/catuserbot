"""Check if userbot alive or not . """
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from userbot import ALIVE_NAME, CMD_HELP
from userbot.utils import admin_cmd
from telethon import version
from platform import python_version, uname


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@Sur_vivor"
PM_IMG = "https://telegra.ph/file/be15be483400f07f7e442.jpg"
pm_caption = "**MY BOT IS RUNNING SUCCESFULLY**\n\n"
pm_caption += f"🛡`Telethon Version:` **{version.__version__}**\n\n"
pm_caption += f"🛡`Python Version:` **{python_version()}**\n\n"
pm_caption += "🛡**Bot Was Modified by**:[✰Şสͥℝสͣ✞ͫђ™✰](http://t.me/Sur_vivor)\n\n"
pm_caption += "🛡**Created by**: Snapdragon,Anubis,Sandeep\n\n"
pm_caption += "🛡**Database Status: Databases Functioning Normally!**\n\n"
pm_caption += "🛡**Always With You, My Master!**\n\n"
pm_caption += f"🛡**Owner Name**: {DEFAULTUSER}\n\n\n"
pm_caption += "**[⚜️DEPLOY THIS USERBOT⚜️](https://github.com/Sur-vivor/CatUserbot)**"


@borg.on(admin_cmd(pattern=r"alive"))
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    await alive.delete()
    await borg.send_file(await borg.send_file(alive.chat_id, PM_IMG, caption=pm_caption)

    
CMD_HELP.update({
    "alive":
    ".alive\
    \nUsage: Type .alive to see wether your bot is working or not.\
    "
})

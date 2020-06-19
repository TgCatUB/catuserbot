"""Check if userbot alive or not . """
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from userbot import ALIVE_NAME, CMD_HELP
from userbot.utils import admin_cmd
from telethon import version
from platform import python_version, uname


DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "@Sur_vivor"

@command(outgoing=True, pattern="^.alive$")
async def amireallyalive(alive):
    """ For .alive command, check if the bot is running.  """
    await alive.edit("**MY BOT IS RUNNING SUCCESFULLY**\n\n"
                     f"`🛡Telethon Version: {version.__version__}\n\n`"
                     f"`🛡Python Version: {python_version()}\n\n`"
                     "`🛡Bot Was Modified by:`[✰Şสͥℝสͣ✞ͫђ™✰](http://t.me/Sur_vivor)\n\n"
                     "`🛡Created by :` Snapdragon,Anubis,Sandeep\n\n"
                     "`🛡Database Status: Databases Functioning Normally!\n\n`"
                     "`🛡Always With You, My Master!\n\n`"
                     f"`🛡Owner Name`: {DEFAULTUSER}\n\n\n"
                     "[⚜️DEPLOY THIS USERBOT⚜️](https://github.com/Sur-vivor/CatUserbot)"
                    )

    
CMD_HELP.update({
    "alive":
    ".alive\
    \nUsage: Type .alive to see wether your bot is working or not.\
    "
})    

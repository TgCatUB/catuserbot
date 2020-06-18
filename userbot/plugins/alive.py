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
                     f"`☞Telethon version: {version.__version__}\n`"
                     f"`☞Python: {python_version()}\n`"
                     "`☞Bot was modified by:` @Sur_vivor\n"
                     "`☞Created by :` snapdragon,anubis,sandeep\n"
                     "`☞Database Status: Databases functioning normally!\n\n`"
                     "`☞Always with you, my master!\n`"
                     f"`☞Owner Name`: [{DEFAULTUSER}](t.me/Sur_vivor)\n"
                     "☞[Deploy this userbot Now](https://github.com/Sur-vivor/CatUserbot)"
                    )

    
CMD_HELP.update({
    "alive":
    ".alive\
    \nUsage: Type .alive to see wether your bot is working or not.\
    "
})    

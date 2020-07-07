"""Check if userbot alive or not . """
import asyncio
from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from platform import uname
from userbot import CMD_HELP, ALIVE_NAME 
from userbot.utils import admin_cmd,sudo_cmd
from telethon import version
from platform import python_version, uname

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"

PIC = Config.ALIVE_PIC

@borg.on(admin_cmd(outgoing=True, pattern="alive$"))
async def amireallyalive(alive):
    if event.fwd_from:
        return
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
        
    if PIC is none:
        """ For .alive command, check if the bot is running.  """
        await alive.edit("**MY BOT IS RUNNING SUCCESFULLY**\n\n"
                         f"`☞Telethon version: {version.__version__}\n`"
                         f"`☞Python: {python_version()}\n`"
                         "`☞Bot was modified by:` sandeep\n"
                         "`☞and created by :` snapdragon,anubis\n"
                         "`☞Database Status: Databases functioning normally!\n\n`"
                         "`☞Always with you, my master!\n`"
                         f"`☞My peru owner`: [{DEFAULTUSER}](https://github.com/sandy1709/catuserbot)\n"
                         "[Deploy Catuserbot Now](https://github.com/sandy1709/catuserbot)"
                        )
    
    else:
         cat_caption  = "**MY BOT IS RUNNING SUCCESFULLY**\n\n"
         cat_caption += f"`☞Telethon version: {version.__version__}\n`"
         cat_caption += f"`☞Python: {python_version()}\n`"
         cat_caption += "`☞Bot was modified by:` sandeep\n"
         cat_caption += "`☞and created by :` snapdragon,anubis\n"
         cat_caption += "`☞Database Status: Databases functioning normally!\n\n`"
         cat_caption += "`☞Always with you, my master!\n`"
         cat_caption += f"`☞My peru owner`: [{DEFAULTUSER}](https://github.com/sandy1709/catuserbot)\n"
         cat_caption += "[Deploy Catuserbot Now](https://github.com/sandy1709/catuserbot)"        
         await reply_to_id.reply( file = CAT_IMG, cat_caption)
         await alive.delete()

@borg.on(sudo_cmd(pattern="sudo", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await event.reply("YOU ARE SUDO FOR THIS BOT \n\n"
                     f"☞Telethon version: {version.__version__}\n"
                     f"☞Python: {python_version()}\n"
                     f"☞My peru owner: {DEFAULTUSER}\n"
                     #"Deploy this userbot Now"
                    )
       
CMD_HELP.update({"alive": "`.alive` :\
      \nUSAGE: Type .alive to see wether your bot is working or not. "
}) 

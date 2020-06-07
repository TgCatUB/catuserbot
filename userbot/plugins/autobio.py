from telethon import events
import asyncio
import time
from telethon.tl import functions
from telethon.errors import FloodWaitError
from userbot.utils import admin_cmd
from userbot import DEFAULT_BIO, CMD_HELP
import random, re
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
import shutil


DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else " ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ  "

DEL_TIME_OUT = 60

@borg.on(admin_cmd(pattern="autobio"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"Auto bio has been started by my Master") 
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        logger.info(bio)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=bio
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Changed Profile Picture"
            # )
        await asyncio.sleep(DEL_TIME_OUT)
     
     
BIO_STRINGS = [
     "👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔳",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️🔳",
     "⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️🔳",
     "⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️🔳",
     "⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️🔳",
     "⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️🔳",
     "⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "🐵",
     "🙈",
     "🙉",
     "🙊",
     "🐵",
     "🐵",
     "🙈",
     "🙉",
     "🙊",
     "🐵",
     "👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬛️🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔲",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉🔳",
     "⬜️⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️🔳",
     "⬜️⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️🔳",
     "⬜️⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️🔳",
     "⬜️⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️🔳",
     "⬜️⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️🔳",
     "⬜️⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "⬜️👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "👉⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️🔳",
     "🐵",
     "🙈",
     "🙉",
     "🙊",
     "🐵",
     "🐵",
     "🙈",
     "🙉",
     "🙊",
     "🐵",

]



@borg.on(admin_cmd(pattern="monkeybio"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"monkey has been started by my Master") 
    while True:
        bro = random.randint(0, len(BIO_STRINGS) - 1)    
        #input_str = event.pattern_match.group(1)
        Bio = BIO_STRINGS[bro]
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        #bio = f"📅 {DMY} | ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ | ⌚️ {HM}"
        logger.info(Bio)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=Bio
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Successfully Changed Profile Bio"
            # )
        await asyncio.sleep(DEL_TIME_OUT)
        
        
        
CMD_HELP.update({
    "autoprofile":
    ".autobio\
\nuseage:for time along with your bio to work this you must set `DEFAULT_BIO` in the heroku vars first \
\n\n.monkeybio\
\nuseage:set of funny monkey bio's\
\n\n for stoping these type .restart and change them manually\
"
})         

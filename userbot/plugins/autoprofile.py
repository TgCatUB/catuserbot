"""Auto Profile Updation Commands
.autoname for time along name 
.autopic tilted image along with time
.autobio  for time along with your bio
.monkeybio set of funny bio's
"""
from telethon import events
import asyncio
import time
from telethon.tl import functions
from telethon.errors import FloodWaitError
from userbot.utils import admin_cmd
from userbot import AUTONAME, DEFAULT_BIO, CMD_HELP
import random, re
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
import shutil


DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else " ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ  "

DEL_TIME_OUT = 30
DEFAULTUSER = str(AUTONAME) if AUTONAME else "cat" 




FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

@command(pattern="^.autopic", outgoing=True)
async def autopic(event):
    await event.edit(f"Autopic has been started by my Master") 
    downloaded_file_name = "userbot/original_pic.png"
    downloader = SmartDL(Var.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    photo = "userbot/photo_pfp.png"
    while not downloader.isFinished():
        place_holder = None
    counter = -30
    while True:
        shutil.copy(downloaded_file_name, photo)
        im = Image.open(photo)
        file_test = im.rotate(counter, expand=False).save(photo, "PNG")
        current_time = datetime.now().strftime("⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡ \n  Time: %H:%M \n  Date: %d.%m.%y \n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((350, 350), current_time, font=fnt, fill=(255, 255, 255))
        img.save(photo)
        file = await bot.upload_file(photo)  # pylint:disable=E0602
        try:
            await bot(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                file
            ))
            os.remove(photo)
            counter -= 30
            await asyncio.sleep(30)
        except:
            return
        
@borg.on(admin_cmd(pattern="autoname"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"Auto Name has been started by my Master ") 
    while True:
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"{HM} {DEFAULTUSER} {DM}"
        logger.info(name)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                first_name=name
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
    
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Successfully Changed Profile Name"
            # )
        await asyncio.sleep(DEL_TIME_OUT)
    



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
    ".autoname\
    \n usage:for time along name to work this you must set AUTONAME in the heroku vars first \
\n\n.autopic\
\n useage:tilted image along with time to work this you must set DOWNLOAD_PFP_URL_CLOCK in the heroku vars first by telegraph link of that image \
\n\n.autobio\
\nuseage:for time along with your bio to work this you must set DEFAULT_BIO in the heroku vars first \
\n\n.monkeybio\
\nuseage:set of funny monkey bio's\
\n\n for stoping these type .restart and change them manually\
"
})         

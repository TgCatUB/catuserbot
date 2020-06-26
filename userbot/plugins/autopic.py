from telethon import events
import asyncio
import time
from telethon.tl import functions
from telethon.errors import FloodWaitError
from userbot.utils import admin_cmd
from userbot import CMD_HELP
import random, re
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
import shutil


FONT_FILE_TO_USE = "userbot/helpers/styles/digital.ttf"

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
        current_time = datetime.now().strftime("%H:%M\n%d.%m.%y")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 50)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(255, 255, 255))
        img.save(photo)
        file = await bot.upload_file(photo)  # pylint:disable=E0602
        try:
            await bot(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                file
            ))
            os.remove(photo)
            counter -= 30
            await asyncio.sleep(60)
        except:
            return
        
        
CMD_HELP.update({
    "autopic":
    ".autopic\
\n **USAGE:** Rotating image along with the time on it .\
\n for working this you must set `DOWNLOAD_PFP_URL_CLOCK` in the heroku vars first with telegraph link of required image\
"
})

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


FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

@borg.on(admin_cmd(pattern="autopic$"))
async def autopic(event):
    await event.edit(f"Autopic has been started by my Master") 
    downloaded_file_name = "userbot/original_pic.png"
    downloader = SmartDL(Var.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    photo = "userbot/photo_pfp.png"
    while not downloader.isFinished():
        place_holder = None
    counter = -60
    while True:
        shutil.copy(downloaded_file_name, photo)
        im = Image.open(photo)
        file_test = im.rotate(counter, expand=False).save(photo, "PNG")
        current_time = datetime.now().strftime("⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡ \n  Time: %H:%M \n  Date: %d.%m.%y \n⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡⚡")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(124, 252, 0))
        img.save(photo)
        file = await bot.upload_file(photo)  # pylint:disable=E0602
        try:
            await bot(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                file
            ))
            os.remove(photo)
            counter -= 60
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

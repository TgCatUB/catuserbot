""" 
syntax: .digitalpfp 
"""
#modified by @mrconfused don't edit credits

from telethon import events
import asyncio
import time
from telethon.tl import functions
from telethon.errors import FloodWaitError
import pybase64
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
import shutil
import requests , re , random 
import urllib , os 
from time import sleep
from userbot.utils import admin_cmd
from userbot import CMD_HELP

    
@borg.on(admin_cmd(pattern="digitalpfp"))
async def main(event):
    await event.edit("Starting digital Profile Pic see magic in 5 sec.") 
    poto = "userbot/poto_pfp.png"
    cat = str( pybase64.b64decode("aHR0cHM6Ly90ZWxlZ3JhLnBoL2ZpbGUvYWVhZWJlMzNiMWYzOTg4YTBiNjkwLmpwZw==") )[2:51]
    downloaded_file_name = "userbot/digital_pic.png"
    downloader = SmartDL(cat, downloaded_file_name, progress_bar=True)
    downloader.start(blocking=False)
    await asyncio.sleep(5)
    while True:
        shutil.copy(downloaded_file_name, poto)
        im = Image.open(poto)
        current_time = datetime.now().strftime("%H:%M")
        img = Image.open(poto)
        drawn_text = ImageDraw.Draw(img)
        cat = str( pybase64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9kaWdpdGFsLnR0Zg==") )[2:36]
        fnt = ImageFont.truetype(cat, 200)
        drawn_text.text((350, 100), current_time, font=fnt, fill=(124, 252, 0))
        img.save(poto)
        file = await event.client.upload_file(poto)
        await event.client(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit=1)))
        await event.client(functions.photos.UploadProfilePhotoRequest( file))
        os.remove(poto)
        await asyncio.sleep(60)
        
CMD_HELP.update({
    "digitalpfp":
    "`.digitalpfp`\
\nUSAGE:Your profile pic changes to digitaltime profile picutre \
"
})

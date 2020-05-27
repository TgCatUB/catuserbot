"""
Time In Profile Pic.....
Command: `.bloom`
Hmmmm U need to config DOWNLOAD_PFP_URL_CLOCK var in Heroku with any telegraph image link
:::::Credit Time::::::
1) Coded By: @s_n_a_p_s
2) Ported By: @r4v4n4 (Noodz Lober)
3) End Game Help By: @spechide
4) Better Colour Profile Pic By @PhycoNinja13b
#curse: who ever edits this credit section will goto hell
⚠️DISCLAIMER⚠️
USING THIS PLUGIN CAN RESULT IN ACCOUNT BAN. WE DONT CARE ABOUT BAN, SO WE ARR USING THIS.
"""
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.tl import functions
from userbot.utils import admin_cmd
import asyncio
import shutil 
import random

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

@borg.on(admin_cmd(pattern="bloom ?(.*)"))
async def autopic(event): 
    await event.edit("Bloom colour profile pic have been enabled by my master") 
    downloaded_file_name = "userbot/original_pic.png"
    downloader = SmartDL(Var.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=True)
    downloader.start(blocking=False)
    photo = "userbot/photo_pfp.png"
    while not downloader.isFinished():
        place_holder = None

    while True:
        #RIP Danger zone Here no editing here plox
        R = random.randint(0,256)
        B = random.randint(0,256)
        G = random.randint(0,256)
        FR = (256 - R) 
        FB = (256 - B) 
        FG = (256 - G) 
        shutil.copy(downloaded_file_name, photo)
        image = Image.open(photo)
        image.paste( (R, G, B), [0,0,image.size[0],image.size[1]])
        image.save(photo)
        
        current_time = datetime.now().strftime("\n Time: %H:%M:%S \n \n Date: %d/%m/%y")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 60)
        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 250)
        drawn_text.text((350, 350), current_time, font=fnt, fill=(FR,FG,FB))
        drawn_text.text((350, 350), "      🌝", font = ofnt, fill=(FR,FG,FB))
        img.save(photo)
        file = await event.client.upload_file(photo)  # pylint:disable=E0602
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
                file
            ))
            os.remove(photo)
            await asyncio.sleep(30)
        except:
            return

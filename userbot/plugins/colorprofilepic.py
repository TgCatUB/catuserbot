

import os

from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from pySmartDL import SmartDL

from telethon.tl import functions

from userbot import ALIVE_NAME

from userbot.utils import admin_cmd

import asyncio

import shutil 

import random



FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"



DEFAULTUSER = str(ALIVE_NAME)



@borg.on(admin_cmd(pattern="clpp ?(.*)"))

async def autopic(event): 

    await event.edit("colour profile pic have been enabled") 

    downloaded_file_name = "./userbot/original_pic.png"

    downloader = SmartDL(Var.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=False)

    downloader.start(blocking=False)

    photo = "photo_pfp.png"

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

        

        #Edit only Below part ð Or esle u will be responsible ð¤·ââ

        current_time = datetime.now().strftime("\n\n Time: %H:%M:%S \n \n Date: %d/%m/%y")

        img = Image.open(photo)

        drawn_text = ImageDraw.Draw(img)

        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 40)

        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 50)

        drawn_text.text((200, 400), current_time, font=fnt, fill=(FR,FG,FB))

        drawn_text.text((250, 250), f"{DEFAULTUSER}", font = ofnt, fill=(FR,FG,FB))

        img.save(photo)

        file = await event.client.upload_file(photo)  # pylint:disable=E0602

        try:

            await event.client(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602

                file

            ))

            os.remove(photo)

            await asyncio.sleep(60)

        except:

            return

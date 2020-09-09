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
import asyncio
import os
import random
import shutil
import time
from datetime import datetime

import pybase64
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions

from userbot import AUTONAME, CMD_HELP, DEFAULT_BIO
from userbot.utils import admin_cmd

DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else " ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ  "
DEL_TIME_OUT = 60
DEFAULTUSER = str(AUTONAME) if AUTONAME else "cat"

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"


@borg.on(admin_cmd(pattern="autopic$"))
async def autopic(event):
    await event.edit(f"Autopic has been started by my Master")
    downloaded_file_name = "userbot/original_pic.png"
    downloader = SmartDL(
        Var.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=False
    )
    downloader.start(blocking=False)
    photo = "userbot/photo_pfp.png"
    while not downloader.isFinished():
        pass
    counter = -60
    while True:
        shutil.copy(downloaded_file_name, photo)
        im = Image.open(photo)
        file_test = im.rotate(counter, expand=False).save(photo, "PNG")
        current_time = datetime.now().strftime("  Time: %H:%M \n  Date: %d.%m.%y ")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((150, 250), current_time, font=fnt, fill=(124, 252, 0))
        img.save(photo)
        file = await bot.upload_file(photo)  # pylint:disable=E0602
        try:
            await bot(
                functions.photos.UploadProfilePhotoRequest(file)  # pylint:disable=E0602
            )
            os.remove(photo)
            counter -= 60
            await asyncio.sleep(60)
        except BaseException:
            return


@borg.on(admin_cmd(pattern="digitalpfp$"))
async def main(event):
    await event.edit("Starting digital Profile Pic see magic in 5 sec.")
    poto = "userbot/poto_pfp.png"
    cat = str(
        pybase64.b64decode(
            "aHR0cHM6Ly90ZWxlZ3JhLnBoL2ZpbGUvYWVhZWJlMzNiMWYzOTg4YTBiNjkwLmpwZw=="
        )
    )[2:51]
    downloaded_file_name = "userbot/digital_pic.png"
    downloader = SmartDL(cat, downloaded_file_name, progress_bar=True)
    downloader.start(blocking=False)
    await asyncio.sleep(5)
    while True:
        shutil.copy(downloaded_file_name, poto)
        Image.open(poto)
        current_time = datetime.now().strftime("%H:%M")
        img = Image.open(poto)
        drawn_text = ImageDraw.Draw(img)
        cat = str(
            pybase64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9kaWdpdGFsLnR0Zg==")
        )[2:36]
        fnt = ImageFont.truetype(cat, 200)
        drawn_text.text((350, 100), current_time, font=fnt, fill=(124, 252, 0))
        img.save(poto)
        file = await event.client.upload_file(poto)
        await event.client(
            functions.photos.DeletePhotosRequest(
                await event.client.get_profile_photos("me", limit=1)
            )
        )
        await event.client(functions.photos.UploadProfilePhotoRequest(file))
        os.remove(poto)
        await asyncio.sleep(60)


@borg.on(admin_cmd(pattern="bloom$"))
async def autopic(event):
    await event.edit("Bloom colour profile pic have been enabled by my master")
    downloaded_file_name = "userbot/original_pic.png"
    downloader = SmartDL(
        Var.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=True
    )
    downloader.start(blocking=False)
    photo = "userbot/photo_pfp.png"
    while not downloader.isFinished():
        pass
    while True:
        # RIP Danger zone Here no editing here plox
        R = random.randint(0, 256)
        B = random.randint(0, 256)
        G = random.randint(0, 256)
        FR = 256 - R
        FB = 256 - B
        FG = 256 - G
        shutil.copy(downloaded_file_name, photo)
        image = Image.open(photo)
        image.paste((R, G, B), [0, 0, image.size[0], image.size[1]])
        image.save(photo)
        current_time = datetime.now().strftime("\n Time: %H:%M:%S \n \n Date: %d/%m/%y")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 60)
        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 250)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(FR, FG, FB))
        drawn_text.text((95, 250), "      😈", font=ofnt, fill=(FR, FG, FB))
        img.save(photo)
        file = await event.client.upload_file(photo)  # pylint:disable=E0602
        try:
            await event.client(
                functions.photos.UploadProfilePhotoRequest(file)  # pylint:disable=E0602
            )
            os.remove(photo)
            await asyncio.sleep(30)
        except BaseException:
            return


@borg.on(admin_cmd(pattern="autoname$"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"Auto Name has been started by my Master ")
    while True:
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"⌚️ {HM}||›  {DEFAULTUSER} ‹||📅 {DM}"
        logger.info(name)
        try:
            await borg(
                functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    first_name=name
                )
            )
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


@borg.on(admin_cmd(pattern="autobio$"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"Auto bio has been started by my Master")
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        logger.info(bio)
        try:
            await borg(
                functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    about=bio
                )
            )
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


@borg.on(admin_cmd(pattern="monkeybio$"))  # pylint:disable=E0602
async def _(event):
    await event.edit(f"monkey has been started by my Master")
    while True:
        bro = random.randint(0, len(BIO_STRINGS) - 1)
        # input_str = event.pattern_match.group(1)
        Bio = BIO_STRINGS[bro]
        time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        # bio = f"📅 {DMY} | ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ | ⌚️ {HM}"
        logger.info(Bio)
        try:
            await borg(
                functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                    about=Bio
                )
            )
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


CMD_HELP.update(
    {
        "autoprofile": "**autoprofile**\
    \n**Syntax : **`.autopic`\
\n**Usage : **Rotating image along with the time on it .\
\nfor working this you must set `DOWNLOAD_PFP_URL_CLOCK` in the heroku vars first with telegraph link of required image\
\n\n**Syntax : **`.digitalpfp`\
\n**Usage : **Your profile pic changes to digitaltime profile picutre \
\n\n**Syntax : **`.bloom`\
\n**Usage : **Random colour profile pics will be setted along with time on it.\
\nfor working this you must set `DOWNLOAD_PFP_URL_CLOCK` in the heroku vars first with telegraph link of required image\
\n\n**Syntax : **`.autoname`\
\n**Usage : **for time along name to work this you must set `AUTONAME`in the heroku vars first \
\n\n**Syntax : **`.autobio`\
\n**Usage : **for time along with your bio to work this you must set `DEFAULT_BIO` in the heroku vars first \
\n\n**Syntax : **`.monkeybio`\
\n**Usage : **set of funny monkey bio's\
\n\n for stoping these aby command you need to do `.restart` and change them manually\
"
    }
)

# ported from uniborg thanks to @s_n_a_p_s , @r4v4n4 ,  @spechide and @PhycoNinja13b
#:::::Credit Time::::::
# 1) Coded By: @s_n_a_p_s
# 2) Ported By: @r4v4n4 (Noodz Lober)
# 3) End Game Help By: @spechide
# 4) Better Colour Profile Pic By @PhycoNinja13b
import asyncio
import base64
import os
import random
import shutil
import time
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions

from ..utils import admin_cmd
from . import AUTONAME, CMD_HELP, DEFAULT_BIO

DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else " ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ  "
CHANGE_TIME = Config.CHANGE_TIME
DEFAULTUSER = str(AUTONAME) if AUTONAME else "cat"

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
global AUTOPICSTART
global DIGITALPICSTART
global BLOOMSTART
global AUTONAMESTART
global AUTOBIOSTART

BLOOMSTART = False
AUTOPICSTART = False
AUTOBIOSTART = False
AUTONAMESTART = False
DIGITALPICSTART = False


@bot.on(admin_cmd(pattern="autopic ?(.*)"))
async def autopic(event):
    if event.fwd_from:
        return
    global AUTOPICSTART
    downloaded_file_name = "userbot/original_pic.png"
    downloader = SmartDL(
        Config.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=False
    )
    downloader.start(blocking=False)
    photo = "userbot/photo_pfp.png"
    while not downloader.isFinished():
        pass
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            input_str = -int(input_str)
        except ValueError:
            input_str = -60
    else:
        input_str = 0
    if AUTOPICSTART:
        return await edit_delete(event, f"`Autopic is already enabled`")
    else:
        AUTOPICSTART = True
    counter = input_str
    await edit_delete(event, f"`Autopic has been started by my Master`")
    while AUTOPICSTART:
        shutil.copy(downloaded_file_name, photo)
        im = Image.open(photo)
        file_test = im.rotate(counter, expand=False).save(photo, "PNG")
        current_time = datetime.now().strftime("  Time: %H:%M \n  Date: %d.%m.%y ")
        img = Image.open(photo)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((150, 250), current_time, font=fnt, fill=(124, 252, 0))
        img.save(photo)
        file = await event.client.upload_file(photo)
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(photo)
            counter -= input_str
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return


@bot.on(admin_cmd(pattern="digitalpfp$"))
async def main(event):
    if event.fwd_from:
        return
    global DIGITALPICSTART
    poto = "userbot/poto_pfp.png"
    cat = str(
        base64.b64decode(
            "aHR0cHM6Ly90ZWxlZ3JhLnBoL2ZpbGUvYWVhZWJlMzNiMWYzOTg4YTBiNjkwLmpwZw=="
        )
    )[2:51]
    downloaded_file_name = "userbot/digital_pic.png"
    downloader = SmartDL(cat, downloaded_file_name, progress_bar=False)
    downloader.start(blocking=False)
    if DIGITALPICSTART:
        return await edit_delete(event, f"`Digitalpfp is already enabled`")
    else:
        DIGITALPICSTART = True
    await edit_delete(event, f"`digitalpfp has been started by my Master`")
    while DIGITALPICSTART:
        shutil.copy(downloaded_file_name, poto)
        Image.open(poto)
        current_time = datetime.now().strftime("%H:%M")
        img = Image.open(poto)
        drawn_text = ImageDraw.Draw(img)
        cat = str(base64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9kaWdpdGFsLnR0Zg=="))[
            2:36
        ]
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
        await asyncio.sleep(CHANGE_TIME)


@bot.on(admin_cmd(pattern="bloom$"))
async def autopic(event):
    if event.fwd_from:
        return
    global BLOOMSTART
    downloaded_file_name = "userbot/original_pic.png"
    downloader = SmartDL(
        Config.DOWNLOAD_PFP_URL_CLOCK, downloaded_file_name, progress_bar=True
    )
    downloader.start(blocking=False)
    photo = "userbot/photo_pfp.png"
    while not downloader.isFinished():
        pass
    if BLOOMSTART:
        return await edit_delete(event, f"`Bloom is already enabled`")
    else:
        BLOOMSTART = True
    await edit_delete(
        event, "`Bloom colour profile pic have been enabled by my master`"
    )
    while BLOOMSTART:
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
        file = await event.client.upload_file(photo)
        try:
            await event.client(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(photo)
            await asyncio.sleep(CHANGE_TIME)
        except BaseException:
            return


@bot.on(admin_cmd(pattern="autoname$"))
async def _(event):
    if event.fwd_from:
        return
    global AUTONAMESTART
    if AUTONAMESTART:
        return await edit_delete(event, f"`Autoname is already enabled`")
    else:
        AUTONAMESTART = True
    await edit_delete(event, "`Auto Name has been started by my Master `")
    while AUTONAMESTART:
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"⌚️ {HM}||›  {DEFAULTUSER} ‹||📅 {DM}"
        logger.info(name)
        try:
            await event.client(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)


@bot.on(admin_cmd(pattern="autobio$"))
async def _(event):
    global AUTOBIOSTART
    if event.fwd_from:
        return
    if AUTOBIOSTART:
        return await edit_delete(event, f"`Autobio is already enabled`")
    else:
        AUTOBIOSTART = True
    await edit_delete(event, "`Autobio has been started by my Master`")
    while AUTOBIOSTART:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        logger.info(bio)
        try:
            await event.client(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(CHANGE_TIME)


@bot.on(admin_cmd(pattern="end (.*)"))
async def _(event):
    if event.fwd_from:
        return
    global AUTOPICSTART
    global DIGITALPICSTART
    global BLOOMSTART
    global AUTONAMESTART
    global AUTOBIOSTART
    input_str = event.pattern_match.group(1)
    if input_str == "autopic":
        if AUTOPICSTART:
            AUTOPICSTART = False
            await edit_delete(event, "`Autopic has been stopped now`")
        else:
            await edit_delete(event, "`Autopic haven't enabled`")
    elif input_str == "digitalpfp":
        if DIGITALPICSTART:
            DIGITALPICSTART = False
            await edit_delete(event, "`Digital profile pic has been stopped now`")
        else:
            await edit_delete(event, "`Digital profile pic haven't enabled`")
    elif input_str == "bloom":
        if BLOOMSTART:
            BLOOMSTART = False
            await edit_delete(event, "`Bloom has been stopped now`")
        else:
            await edit_delete(event, "`Bloom haven't enabled`")
    elif input_str == "autoname":
        if AUTONAMESTART:
            AUTONAMESTART = False
            await edit_delete(event, "`Autoname has been stopped now`")
        else:
            await edit_delete(event, "`Autoname haven't enabled`")
    elif input_str == "autobio":
        if AUTOBIOSTART:
            AUTOBIOSTART = False
            await edit_delete(event, "`Autobio has been stopped now`")
        else:
            await edit_delete(event, "`Autobio haven't enabled`")
    else:
        await edit_delete(event, "`What should i end ?..`")


CMD_HELP.update(
    {
        "autoprofile": "__**PLUGIN NAME :** Autoprofile__\
\n\n📌** CMD ➥** `.autopic`\
\n**USAGE   ➥  **Rotating image along with the time on it .\
\nfor working this you must set `DOWNLOAD_PFP_URL_CLOCK` in the heroku vars first with telegraph link of required image\
\n\n📌** CMD ➥** `.digitalpfp`\
\n**USAGE   ➥  **Your profile pic changes to digitaltime profile picutre \
\n\n📌** CMD ➥** `.bloom`\
\n**USAGE   ➥  **Random colour profile pics will be setted along with time on it.\
\nfor working this you must set `DOWNLOAD_PFP_URL_CLOCK` in the heroku vars first with telegraph link of required image\
\n\n📌** CMD ➥** `.autoname`\
\n**USAGE   ➥  **For time along name to work this you must set `AUTONAME`in the heroku vars first \
\n\n📌** CMD ➥** `.autobio`\
\n**USAGE   ➥  **For time along with your bio to work this you must set `DEFAULT_BIO` in the heroku vars first \
\n\n📌** CMD ➥** `.monkeybio`\
\n**USAGE   ➥  **Set of funny monkey bio's\
\n\n for stoping these aby command you need to do `.restart` and change them manually\
"
    }
)

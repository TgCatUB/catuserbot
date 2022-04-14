# batmanpfp and thorpfp by @Nihinivi

import asyncio
import base64
import os
import random
import re
import shutil
import time
import urllib
from datetime import datetime

import requests
from PIL import Image, ImageDraw, ImageFont
from pySmartDL import SmartDL
from telethon.errors import FloodWaitError
from telethon.tl import functions
from urlextract import URLExtract

from ..Config import Config
from ..helpers.utils import _format
from ..sql_helper.global_list import (
    add_to_list,
    get_collection_list,
    is_in_list,
    rm_from_list,
)
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import (
    AUTONAME,
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    _catutils,
    catub,
    edit_delete,
    logging,
)

plugin_category = "tools"
DEFAULTUSERBIO = DEFAULT_BIO or " ᗯᗩᏆᎢᏆᑎᏀ ᏞᏆᏦᗴ ᎢᏆᗰᗴ  "
DEFAULTUSER = AUTONAME or Config.ALIVE_NAME
LOGS = logging.getLogger(__name__)

FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

autopic_path = os.path.join(os.getcwd(), "userbot", "original_pic.png")
digitalpic_path = os.path.join(os.getcwd(), "userbot", "digital_pic.png")
autophoto_path = os.path.join(os.getcwd(), "userbot", "photo_pfp.png")

digitalpfp = Config.DIGITAL_PIC or "https://telegra.ph/file/aeaebe33b1f3988a0b690.jpg"

COLLECTION_STRINGS = {
    "batmanpfp_strings": [
        "awesome-batman-wallpapers",
        "batman-arkham-knight-4k-wallpaper",
        "batman-hd-wallpapers-1080p",
        "the-joker-hd-wallpaper",
        "dark-knight-joker-wallpaper",
    ],
    "thorpfp_strings": [
        "thor-wallpapers",
        "thor-wallpaper",
        "thor-iphone-wallpaper",
        "thor-wallpaper-hd",
    ],
}


async def autopicloop():
    AUTOPICSTART = gvarstatus("autopic") == "true"
    if AUTOPICSTART and Config.DEFAULT_PIC is None:
        if BOTLOG:
            return await catub.send_message(
                BOTLOG_CHATID,
                "**Error**\n`For functing of autopic you need to set DEFAULT_PIC var in Heroku vars`",
            )
        return
    if gvarstatus("autopic") is not None:
        try:
            counter = int(gvarstatus("autopic_counter"))
        except Exception as e:
            LOGS.warn(str(e))
    while AUTOPICSTART:
        if not os.path.exists(autopic_path):
            downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(autopic_path, autophoto_path)
        im = Image.open(autophoto_path)
        file_test = im.rotate(counter, expand=False).save(autophoto_path, "PNG")
        current_time = datetime.now().strftime("  Time: %H:%M \n  Date: %d.%m.%y ")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
        drawn_text.text((150, 250), current_time, font=fnt, fill=(124, 252, 0))
        img.save(autophoto_path)
        file = await catub.upload_file(autophoto_path)
        try:
            await catub(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            counter += counter
            await asyncio.sleep(Config.CHANGE_TIME)
        except BaseException:
            return
        AUTOPICSTART = gvarstatus("autopic") == "true"


async def custompfploop():
    CUSTOMPICSTART = gvarstatus("CUSTOM_PFP") == "true"
    i = 0
    while CUSTOMPICSTART:
        if len(get_collection_list("CUSTOM_PFP_LINKS")) == 0:
            LOGS.error("No custom pfp images to set.")
            return
        pic = random.choice(list(get_collection_list("CUSTOM_PFP_LINKS")))
        urllib.request.urlretrieve(pic, "donottouch.jpg")
        file = await catub.upload_file("donottouch.jpg")
        try:
            if i > 0:
                await catub(
                    functions.photos.DeletePhotosRequest(
                        await catub.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await catub(functions.photos.UploadProfilePhotoRequest(file))
            os.remove("donottouch.jpg")
            await asyncio.sleep(Config.CHANGE_TIME)
        except BaseException:
            return
        CUSTOMPICSTART = gvarstatus("CUSTOM_PFP") == "true"


async def digitalpicloop():
    DIGITALPICSTART = gvarstatus("digitalpic") == "true"
    i = 0
    while DIGITALPICSTART:
        if not os.path.exists(digitalpic_path):
            downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        shutil.copy(digitalpic_path, autophoto_path)
        Image.open(autophoto_path)
        current_time = datetime.now().strftime("%H:%M")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        cat = str(base64.b64decode("dXNlcmJvdC9oZWxwZXJzL3N0eWxlcy9kaWdpdGFsLnR0Zg=="))[
            2:36
        ]
        fnt = ImageFont.truetype(cat, 200)
        drawn_text.text((350, 100), current_time, font=fnt, fill=(124, 252, 0))
        img.save(autophoto_path)
        file = await catub.upload_file(autophoto_path)
        try:
            if i > 0:
                await catub(
                    functions.photos.DeletePhotosRequest(
                        await catub.get_profile_photos("me", limit=1)
                    )
                )
            i += 1
            await catub(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(60)
        except BaseException:
            return
        DIGITALPICSTART = gvarstatus("digitalpic") == "true"


async def bloom_pfploop():
    BLOOMSTART = gvarstatus("bloom") == "true"
    if BLOOMSTART and Config.DEFAULT_PIC is None:
        if BOTLOG:
            return await catub.send_message(
                BOTLOG_CHATID,
                "**Error**\n`For functing of bloom you need to set DEFAULT_PIC var in Heroku vars`",
            )
        return
    while BLOOMSTART:
        if not os.path.exists(autopic_path):
            downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        # RIP Danger zone Here no editing here plox
        R = random.randint(0, 256)
        B = random.randint(0, 256)
        G = random.randint(0, 256)
        FR = 256 - R
        FB = 256 - B
        FG = 256 - G
        shutil.copy(autopic_path, autophoto_path)
        image = Image.open(autophoto_path)
        image.paste((R, G, B), [0, 0, image.size[0], image.size[1]])
        image.save(autophoto_path)
        current_time = datetime.now().strftime("\n Time: %H:%M:%S \n \n Date: %d/%m/%y")
        img = Image.open(autophoto_path)
        drawn_text = ImageDraw.Draw(img)
        fnt = ImageFont.truetype(FONT_FILE_TO_USE, 60)
        ofnt = ImageFont.truetype(FONT_FILE_TO_USE, 250)
        drawn_text.text((95, 250), current_time, font=fnt, fill=(FR, FG, FB))
        drawn_text.text((95, 250), "      😈", font=ofnt, fill=(FR, FG, FB))
        img.save(autophoto_path)
        file = await catub.upload_file(autophoto_path)
        try:
            await catub(functions.photos.UploadProfilePhotoRequest(file))
            os.remove(autophoto_path)
            await asyncio.sleep(Config.CHANGE_TIME)
        except BaseException:
            return
        BLOOMSTART = gvarstatus("bloom") == "true"


async def autoname_loop():
    AUTONAMESTART = gvarstatus("autoname") == "true"
    while AUTONAMESTART:
        DM = time.strftime("%d-%m-%y")
        HM = time.strftime("%H:%M")
        name = f"⌚️ {HM}||›  {DEFAULTUSER} ‹||📅 {DM}"
        LOGS.info(name)
        try:
            await catub(functions.account.UpdateProfileRequest(first_name=name))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTONAMESTART = gvarstatus("autoname") == "true"


async def autobio_loop():
    AUTOBIOSTART = gvarstatus("autobio") == "true"
    while AUTOBIOSTART:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M")
        bio = f"📅 {DMY} | {DEFAULTUSERBIO} | ⌚️ {HM}"
        LOGS.info(bio)
        try:
            await catub(functions.account.UpdateProfileRequest(about=bio))
        except FloodWaitError as ex:
            LOGS.warning(str(ex))
            await asyncio.sleep(ex.seconds)
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTOBIOSTART = gvarstatus("autobio") == "true"


async def animeprofilepic(collection_images):
    rnd = random.randint(0, len(collection_images) - 1)
    pack = collection_images[rnd]
    pc = requests.get("http://getwallpapers.com/collection/" + pack).text
    f = re.compile(r"/\w+/full.+.jpg")
    f = f.findall(pc)
    fy = "http://getwallpapers.com" + random.choice(f)
    if not os.path.exists("f.ttf"):
        urllib.request.urlretrieve(
            "https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf",
            "f.ttf",
        )
    img = requests.get(fy)
    with open("donottouch.jpg", "wb") as outfile:
        outfile.write(img.content)
    return "donottouch.jpg"


async def autopfp_start():
    if gvarstatus("autopfp_strings") is not None:
        AUTOPFP_START = True
        string_list = COLLECTION_STRINGS[gvarstatus("autopfp_strings")]
    else:
        AUTOPFP_START = False
    i = 0
    while AUTOPFP_START:
        await animeprofilepic(string_list)
        file = await catub.upload_file("donottouch.jpg")
        if i > 0:
            await catub(
                functions.photos.DeletePhotosRequest(
                    await catub.get_profile_photos("me", limit=1)
                )
            )
        i += 1
        await catub(functions.photos.UploadProfilePhotoRequest(file))
        await _catutils.runcmd("rm -rf donottouch.jpg")
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTOPFP_START = gvarstatus("autopfp_strings") is not None


@catub.cat_cmd(
    pattern="batmanpfp$",
    command=("batmanpfp", plugin_category),
    info={
        "header": "Changes profile pic with random batman pics every 1 minute",
        "description": "Changes your profile pic every 1 minute with random batman pics.\
        If you like to change the time then set CHANGE_TIME var in Heroku with time (in seconds) between each change of profilepic.",
        "note": "To stop this do '.end batmanpfp'",
        "usage": "{tr}batmanpfp",
    },
)
async def _(event):
    "To set random batman profile pics"
    if gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        return await edit_delete(event, f"`{pfp_string} is already running.`")
    addgvar("autopfp_strings", "batmanpfp_strings")
    await event.edit("`Starting batman Profile Pic.`")
    await autopfp_start()


@catub.cat_cmd(
    pattern="thorpfp$",
    command=("thorpfp", plugin_category),
    info={
        "header": "Changes profile pic with random thor pics every 1 minute",
        "description": "Changes your profile pic every 1 minute with random thor pics.\
        If you like to change the time then set CHANGE_TIME var in Heroku with time(in seconds) between each change of profilepic.",
        "note": "To stop this do '.end thorpfp'",
        "usage": "{tr}thorpfp",
    },
)
async def _(event):
    "To set random thor profile pics"
    if gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        return await edit_delete(event, f"`{pfp_string} is already running.`")
    addgvar("autopfp_strings", "thorpfp_strings")
    await event.edit("`Starting thor Profile Pic.`")
    await autopfp_start()


@catub.cat_cmd(
    pattern="autopic ?([\s\S]*)",
    command=("autopic", plugin_category),
    info={
        "header": "Changes profile pic every 1 minute with the custom pic with time",
        "description": "If you like to change the time interval for every new pic change \
            then set CHANGE_TIME var in Heroku with time(in seconds) between each change of profilepic.",
        "options": "you can give integer input with cmd like 40,55,75 ..etc.\
             So that your profile pic will rotate with that specific angle",
        "note": "For functioning of this cmd you need to set DEFAULT_PIC var in heroku. \
            To stop this do '.end autopic'",
        "usage": [
            "{tr}autopic",
            "{tr}autopic <any integer>",
        ],
    },
)
async def _(event):
    "To set time on your profile pic"
    if Config.DEFAULT_PIC is None:
        return await edit_delete(
            event,
            "**Error**\nFor functing of autopic you need to set DEFAULT_PIC var in Heroku vars",
            parse_mode=_format.parse_pre,
        )
    downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    input_str = event.pattern_match.group(1)
    if input_str:
        try:
            input_str = int(input_str)
        except ValueError:
            input_str = 60
    elif gvarstatus("autopic_counter") is None:
        addgvar("autopic_counter", 30)
    if gvarstatus("autopic") is not None and gvarstatus("autopic") == "true":
        return await edit_delete(event, "`Autopic is already enabled`")
    addgvar("autopic", True)
    if input_str:
        addgvar("autopic_counter", input_str)
    await edit_delete(event, "`Autopic has been started by my Master`")
    await autopicloop()


@catub.cat_cmd(
    pattern="digitalpfp$",
    command=("digitalpfp", plugin_category),
    info={
        "header": "Updates your profile pic every 1 minute with time on it",
        "description": "Deletes old profile pic and Update profile pic with new image with time on it.\
             You can change this image by setting DIGITAL_PIC var in heroku with telegraph image link",
        "note": "To stop this do '.end digitalpfp'",
        "usage": "{tr}digitalpfp",
    },
)
async def _(event):
    "To set random colour pic with time to profile pic"
    downloader = SmartDL(digitalpfp, digitalpic_path, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
        return await edit_delete(event, "`Digitalpic is already enabled`")
    addgvar("digitalpic", True)
    await edit_delete(event, "`digitalpfp has been started by my Master`")
    await digitalpicloop()


@catub.cat_cmd(
    pattern="bloom$",
    command=("bloom", plugin_category),
    info={
        "header": "Changes profile pic every 1 minute with the random colour pic with time on it",
        "description": "If you like to change the time interval for every new pic chnage \
            then set CHANGE_TIME var in Heroku with time(in seconds) between each change of profilepic.",
        "note": "For functioning of this cmd you need to set DEFAULT_PIC var in heroku. \
            To stop this do '.end bloom'",
        "usage": "{tr}bloom",
    },
)
async def _(event):
    "To set random colour pic with time to profile pic"
    if Config.DEFAULT_PIC is None:
        return await edit_delete(
            event,
            "**Error**\nFor functing of bloom you need to set DEFAULT_PIC var in Heroku vars",
            parse_mode=_format.parse_pre,
        )
    downloader = SmartDL(Config.DEFAULT_PIC, autopic_path, progress_bar=True)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    if gvarstatus("bloom") is not None and gvarstatus("bloom") == "true":
        return await edit_delete(event, "`Bloom is already enabled`")
    addgvar("bloom", True)
    await edit_delete(event, "`Bloom has been started by my Master`")
    await bloom_pfploop()


@catub.cat_cmd(
    pattern="c(ustom)?pfp(?: |$)([\s\S]*)",
    command=("custompfp", plugin_category),
    info={
        "header": "Set Your Custom pfps",
        "description": "Set links of pic to use them as auto profile. You can use cpfp or custompp as command",
        "flags": {
            "a": "To add links for custom pfp",
            "r": "To remove links for custom pfp",
            "l": "To get links of custom pfp",
            "s": "To stop custom pfp",
        },
        "usage": [
            "{tr}cpfp - to start",
            "{tr}cpfp <flags> <links(optional)>",
        ],
    },
)
async def useless(event):  # sourcery no-metrics
    """Custom profile pics"""
    input_str = event.pattern_match.group(2)
    ext = re.findall(r"-\w+", input_str)
    try:
        flag = ext[0].replace("-", "")
        input_str = input_str.replace(ext[0], "").strip()
    except IndexError:
        flag = None
    list_link = get_collection_list("CUSTOM_PFP_LINKS")
    if flag is None:
        if gvarstatus("CUSTOM_PFP") is not None and gvarstatus("CUSTOM_PFP") == "true":
            return await edit_delete(event, "`Custom pfp is already enabled`")
        if not list_link:
            return await edit_delete(event, "**ಠ∀ಠ  There no links for custom pfp...**")
        addgvar("CUSTOM_PFP", True)
        await edit_delete(event, "`Starting custom pfp....`")
        await custompfploop()
        return
    if flag == "l":
        if not list_link:
            return await edit_delete(
                event, "**ಠ∀ಠ  There no links set for custom pfp...**"
            )
        links = "**Available links for custom pfp are here:-**\n\n"
        for i, each in enumerate(list_link, start=1):
            links += f"**{i}.**  {each}\n"
        await edit_delete(event, links, 60)
        return
    if flag == "s":
        if gvarstatus("CUSTOM_PFP") is not None and gvarstatus("CUSTOM_PFP") == "true":
            delgvar("CUSTOM_PFP")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "`Custompfp has been stopped now`")
        return await edit_delete(event, "`Custompfp haven't enabled`")
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(
            event, "**ಠ∀ಠ  Reply to valid link or give valid link url as input...**"
        )
    extractor = URLExtract()
    plink = extractor.find_urls(input_str)
    if len(plink) == 0:
        return await edit_delete(
            event, "**ಠ∀ಠ  Reply to valid link or give valid link url as input...**"
        )
    if flag == "a":
        for i in plink:
            if not is_in_list("CUSTOM_PFP_LINKS", i):
                add_to_list("CUSTOM_PFP_LINKS", i)
        await edit_delete(
            event, f"**{len(plink)} pictures sucessfully added to custom pfps**"
        )
    elif flag == "r":
        for i in plink:
            if is_in_list("CUSTOM_PFP_LINKS", i):
                rm_from_list("CUSTOM_PFP_LINKS", i)
        await edit_delete(
            event, f"**{len(plink)} pictures sucessfully removed from custom pfps**"
        )


@catub.cat_cmd(
    pattern="autoname$",
    command=("autoname", plugin_category),
    info={
        "header": "Changes your name with time",
        "description": "Updates your profile name along with time. Set AUTONAME var in heroku with your profile name,",
        "note": "To stop this do '.end autoname'",
        "usage": "{tr}autoname",
    },
)
async def _(event):
    "To set your display name along with time"
    if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
        return await edit_delete(event, "`Autoname is already enabled`")
    addgvar("autoname", True)
    await edit_delete(event, "`AutoName has been started by my Master `")
    await autoname_loop()


@catub.cat_cmd(
    pattern="autobio$",
    command=("autobio", plugin_category),
    info={
        "header": "Changes your bio with time",
        "description": "Updates your profile bio along with time. Set DEFAULT_BIO var in heroku with your fav bio,",
        "note": "To stop this do '.end autobio'",
        "usage": "{tr}autobio",
    },
)
async def _(event):
    "To update your bio along with time"
    if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
        return await edit_delete(event, "`Autobio is already enabled`")
    addgvar("autobio", True)
    await edit_delete(event, "`Autobio has been started by my Master `")
    await autobio_loop()


@catub.cat_cmd(
    pattern="end ([\s\S]*)",
    command=("end", plugin_category),
    info={
        "header": "To stop the functions of autoprofile",
        "description": "If you want to stop autoprofile functions then use this cmd.",
        "options": {
            "autopic": "To stop autopic",
            "digitalpfp": "To stop difitalpfp",
            "bloom": "To stop bloom",
            "autoname": "To stop autoname",
            "autobio": "To stop autobio",
            "thorpfp": "To stop thorpfp",
            "batmanpfp": "To stop batmanpfp",
            "spam": "To stop spam",
        },
        "usage": "{tr}end <option>",
        "examples": ["{tr}end autopic"],
    },
)
async def _(event):  # sourcery no-metrics
    "To stop the functions of autoprofile plugin"
    input_str = event.pattern_match.group(1)
    if input_str == "thorpfp" and gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        if pfp_string != "thorpfp":
            return await edit_delete(event, "`thorpfp is not started`")
        await event.client(
            functions.photos.DeletePhotosRequest(
                await event.client.get_profile_photos("me", limit=1)
            )
        )
        delgvar("autopfp_strings")
        return await edit_delete(event, "`thorpfp has been stopped now`")
    if input_str == "batmanpfp" and gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        if pfp_string != "batmanpfp":
            return await edit_delete(event, "`batmanpfp is not started`")
        await event.client(
            functions.photos.DeletePhotosRequest(
                await event.client.get_profile_photos("me", limit=1)
            )
        )
        delgvar("autopfp_strings")
        return await edit_delete(event, "`batmanpfp has been stopped now`")
    if input_str == "autopic":
        if gvarstatus("autopic") is not None and gvarstatus("autopic") == "true":
            delgvar("autopic")
            if os.path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(functions.photos.UploadProfilePhotoRequest(file))
                    os.remove(autopic_path)
                except BaseException:
                    return
            return await edit_delete(event, "`Autopic has been stopped now`")
        return await edit_delete(event, "`Autopic haven't enabled`")
    if input_str == "digitalpfp":
        if gvarstatus("digitalpic") is not None and gvarstatus("digitalpic") == "true":
            delgvar("digitalpic")
            await event.client(
                functions.photos.DeletePhotosRequest(
                    await event.client.get_profile_photos("me", limit=1)
                )
            )
            return await edit_delete(event, "`Digitalpfp has been stopped now`")
        return await edit_delete(event, "`Digitalpfp haven't enabled`")
    if input_str == "bloom":
        if gvarstatus("bloom") is not None and gvarstatus("bloom") == "true":
            delgvar("bloom")
            if os.path.exists(autopic_path):
                file = await event.client.upload_file(autopic_path)
                try:
                    await event.client(functions.photos.UploadProfilePhotoRequest(file))
                    os.remove(autopic_path)
                except BaseException:
                    return
            return await edit_delete(event, "`Bloom has been stopped now`")
        return await edit_delete(event, "`Bloom haven't enabled`")
    if input_str == "autoname":
        if gvarstatus("autoname") is not None and gvarstatus("autoname") == "true":
            delgvar("autoname")
            await event.client(
                functions.account.UpdateProfileRequest(first_name=DEFAULTUSER)
            )
            return await edit_delete(event, "`Autoname has been stopped now`")
        return await edit_delete(event, "`Autoname haven't enabled`")
    if input_str == "autobio":
        if gvarstatus("autobio") is not None and gvarstatus("autobio") == "true":
            delgvar("autobio")
            await event.client(
                functions.account.UpdateProfileRequest(about=DEFAULTUSERBIO)
            )
            return await edit_delete(event, "`Autobio has been stopped now`")
        return await edit_delete(event, "`Autobio haven't enabled`")
    if input_str == "spam":
        if gvarstatus("spamwork") is not None and gvarstatus("spamwork") == "true":
            delgvar("spamwork")
            return await edit_delete(event, "`Spam cmd has been stopped now`")
        return await edit_delete(event, "`You haven't started spam`")
    END_CMDS = [
        "autopic",
        "digitalpfp",
        "bloom",
        "autoname",
        "autobio",
        "thorpfp",
        "batmanpfp",
        "spam",
    ]
    if input_str not in END_CMDS:
        await edit_delete(
            event,
            f"{input_str} is invalid end command.Mention clearly what should i end.",
            parse_mode=_format.parse_pre,
        )


catub.loop.create_task(autopfp_start())
catub.loop.create_task(autopicloop())
catub.loop.create_task(digitalpicloop())
catub.loop.create_task(bloom_pfploop())
catub.loop.create_task(autoname_loop())
catub.loop.create_task(autobio_loop())
catub.loop.create_task(custompfploop())

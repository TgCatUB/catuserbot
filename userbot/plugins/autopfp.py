# Made By @Nihinivi Keep Credits If You Are Goanna Kang This Lol
# And Thanks To The Creator Of Autopic This Script Was Made from Snippets From That Script
# Usage .gamerpfp  Im Not Responsible For Any Ban caused By This
import asyncio
import os
import random
import re
import urllib

import requests
from telethon.tl import functions

from .sql_helper.globals import addgvar, delgvar, gvarstatus

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
    urllib.request.urlretrieve(fy, "donottouch.jpg")


async def autopfp_start():
    if gvarstatus("autopfp_strings") is not None:
        AUTOPFP_START = True
        string_list = COLLECTION_STRINGS[gvarstatus("autopfp_strings")]
    else:
        AUTOPFP_START = False
    i = 0
    while AUTOPFP_START:
        await animeprofilepic(string_list)
        file = await bot.upload_file("donottouch.jpg")
        if i > 0:
            await bot(
                functions.photos.DeletePhotosRequest(
                    await bot.get_profile_photos("me", limit=1)
                )
            )
        i += 1
        await bot(functions.photos.UploadProfilePhotoRequest(file))
        await _catutils.runcmd("rm -rf donottouch.jpg")
        await asyncio.sleep(Config.CHANGE_TIME)
        AUTOPFP_START = gvarstatus("autopfp_strings") is not None


@bot.on(admin_cmd(pattern="batmanpfp$"))
async def main(event):
    if event.fwd_from:
        return
    if gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        return await edit_delete(event, f"`{pfp_string} is already running.`")
    addgvar("autopfp_strings", "batmanpfp_strings")
    await event.edit("`Starting batman Profile Pic.`")
    await autopfp_start()


@bot.on(admin_cmd(pattern="thorpfp$"))
async def main(event):
    if event.fwd_from:
        return
    if gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        return await edit_delete(event, f"`{pfp_string} is already running.`")
    addgvar("autopfp_strings", "thorpfp_strings")
    await event.edit("`Starting thor Profile Pic.`")
    await autopfp_start()


@bot.on(admin_cmd(pattern="end (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str == "thorpfp" and gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        if pfp_string != "thorpfp":
            return await edit_delete(event, f"`thorpfp is not started`")
        await event.client(
            functions.photos.DeletePhotosRequest(
                await bot.get_profile_photos("me", limit=1)
            )
        )
        delgvar("autopfp_strings")
        return await edit_delete(event, "`thorpfp has been stopped now`")
    if input_str == "batmanpfp" and gvarstatus("autopfp_strings") is not None:
        pfp_string = gvarstatus("autopfp_strings")[:-8]
        if pfp_string != "batmanpfp":
            return await edit_delete(event, f"`batmanpfp is not started`")
        await event.client(
            functions.photos.DeletePhotosRequest(
                await bot.get_profile_photos("me", limit=1)
            )
        )
        delgvar("autopfp_strings")
        return await edit_delete(event, "`batmanpfp has been stopped now`")
    END_CMDS = [
        "autopic",
        "digitalpfp",
        "bloom",
        "autoname",
        "autobio",
        "thorpfp",
        "batmanpfp",
    ]
    if input_str not in END_CMDS:
        await edit_delete(
            event,
            f"{input_str} is invalid end command.Mention clearly what should i end.",
            parse_mode=parse_pre,
        )


bot.loop.create_task(autopfp_start())

CMD_HELP.update(
    {
        "autopfp": """**Plugin : **`autopfp`
    
**Commands found in autopfp are **
  •  `.batmanpfp`
  •  `.thorpfp`


**Function : **__Changes your profile pic every 1 minute with the command you used (mean the batman or thor pics ).\
If you like to chnge the time then set CHNAGE_TIME var in Heroku with time between each chnage in seconds.__"""
    }
)

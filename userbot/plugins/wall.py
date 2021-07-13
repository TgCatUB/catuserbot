import os
import random

import requests
from bs4 import BeautifulSoup
from pySmartDL import SmartDL

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "extra"


@catub.cat_cmd(
    pattern="wall([\s\S]*)",
    command=("wall", plugin_category),
    info={
        "header": "Searches and uploads wallpaper",
        "usage": ["{tr}wall <query>", "{tr}wall <query> ; <1-10>"],
        "examples": ["{tr}wall one piece", "{tr}wall one piece ; 2"],
    },
)
async def noods(event):
    "Wallpaper searcher"
    query = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    limit = 1
    if not query:
        return await edit_delete(event, "`What should i search ?`")
    if ";" in query:
        query, limit = query.split(";")
    if int(limit) > 10:
        return await edit_delete(event, f"`Wallpaper search limit is 1-10`", 10)
    string = "⏳ `Processing..`"
    await edit_or_reply(event, "🔍 `Searching...`")
    r = requests.get(
        f"https://wall.alphacoders.com/search.php?search={query.replace(' ','+')}"
    )
    soup = BeautifulSoup(r.content, "lxml")
    walls = soup.find_all("img", class_="img-responsive")
    if not walls:
        return await edit_delete(
            event, f"**Can't find any wallpaper releated to** `{query}`", 10
        )
    i = count = 0
    files = []
    caption = []
    for x in walls:
        await edit_or_reply(event, string)
        string += "`.`"
        wall = random.choice(walls)["src"][8:-4]
        server = wall.split(".")[0]
        fileid = wall.split("-")[-1]
        url2 = "https://api.alphacoders.com/content/get-download-link"
        data = {
            "content_id": fileid,
            "content_type": "wallpaper",
            "file_type": "jpg",
            "image_server": server,
        }
        res = requests.post(url2, data=data)
        url = res.json()["link"]
        if "We are sorry," not in requests.get(url).text:
            await edit_or_reply(event, "📥** Downloading...**")
            directory = os.path.join(Config.TEMP_DIR, query)
            if not os.path.isdir(directory):
                os.mkdir(directory)
            path = f"{directory}/{fileid}.jpg"
            x = SmartDL(url, path, progress_bar=False)
            x.start(blocking=False)
            x.wait("finished")
            files.append(path)
            caption.append("")
            count += 1
            i = 0
        else:
            i += 1
        if count == int(limit):
            cap = f"**➥ Query :-** `{query.title()}`"
            caption = caption[:-1]
            caption = caption.append(cap)
            await event.client.send_file(
                event.chat_id,
                files,
                caption=caption,
                reply_to=reply_to_id,
                force_document=True,
            )
            await event.delete()
            os.rmdir(directory)
            break
    if i == 5:
        return await edit_delete(event, "`Max search limit exceed..`")

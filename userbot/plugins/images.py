# Adapted from OpenUserBot for Uniborg

"""Download & Upload Images on Telegram\n
Syntax: `.img <Name>` or `.img (replied message)`
\n Upgraded and Google Image Error Fixed by @NeoMatrix90 aka @kirito6969
"""

from google_images_download import google_images_download
import os
import shutil
from re import findall
from userbot.utils import admin_cmd
from userbot import CMD_HELP
import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from userbot.uniborgConfig import Config

@borg.on(admin_cmd(pattern="img ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    response = google_images_download.googleimagesdownload()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    arguments = {
        "keywords": input_str,
        "limit": Config.TG_GLOBAL_ALBUM_LIMIT,
        "format": "jpg",
        "delay": 1,
        "safe_search": True,
        "output_directory": Config.TMP_DOWNLOAD_DIRECTORY
    }
    paths = response.download(arguments)
    logger.info(paths)
    lst = paths[0].get(input_str)
    if len(lst) == 0:
        await event.delete()
        return
    await borg.send_file(
        event.chat_id,
        lst,
        caption=input_str,
        reply_to=event.message.id,
        progress_callback=progress
    )
    logger.info(lst)
    for each_file in lst:
        os.remove(each_file)
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("searched Google for {} in {} seconds.".format(input_str, ms), link_preview=False)
    await asyncio.sleep(5)
    await event.delete()

    
CMD_HELP.update({"images": "`.img <Name>` or `.img (replied message)`\
    \nUSAGE: do google image search and sends 5 images." 
})    

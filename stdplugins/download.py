"""Download Files to your local server
Syntax:
.download
.download url | file.name to download files from a Public Link"""

import aiohttp
import asyncio
import math
import os
import time
from datetime import datetime
from pySmartDL import SmartDL
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter


@borg.on(admin_cmd(pattern="download ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    elif input_str:
        start = datetime.now()
        url = input_str
        file_name = os.path.basename(url)
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        if "|" in input_str:
            url, file_name = input_str.split("|")
        url = url.strip()
        file_name = file_name.strip()
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        display_message = ""
        c_time = time.time()
        while not downloader.isFinished():
            total_length = downloader.filesize if downloader.filesize else None
            downloaded = downloader.get_dl_size()
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            elapsed_time = round(diff) * 1000
            progress_str = "[{0}{1}]\nProgress: {2}%".format(
                ''.join(["█" for i in range(math.floor(percentage / 5))]),
                ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2))
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"trying to download\n"
                current_message += f"URL: {url}\n"
                current_message += f"File Name: {file_name}\n"
                current_message += f"{progress_str}\n"
                current_message += f"{humanbytes(downloaded)} of {humanbytes(total_length)}\n"
                current_message += f"ETA: {estimated_total_time}"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    await mone.edit(current_message)
                    display_message = current_message
            except Exception as e:
                logger.info(str(e))
        end = datetime.now()
        ms = (end - start).seconds
        if downloader.isSuccessful():
            await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
        else:
            await mone.edit("Incorrect URL\n {}".format(input_str))
    else:
        await mone.edit("Reply to a message to download to my local server.")

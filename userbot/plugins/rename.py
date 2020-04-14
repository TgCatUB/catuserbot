# Code from pro sar Spechide's fork of Uniborg.
"""Rename Telegram Files
Syntax:
.rnupload file.name"""

import asyncio
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from base64 import b64decode
import io
import math
import os
from pySmartDL import SmartDL
from telethon.tl.types import DocumentAttributeVideo
from uniborg.util import progress, humanbytes, time_formatter, admin_cmd


thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@borg.on(admin_cmd(pattern="rnupload (.*)"))
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    await event.edit("⚡️`Rename and upload in progress, please wait!`⚡️")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        end = datetime.now()
        file_name = input_str
        reply_message = await event.get_reply_message()
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloaded_file_name = await borg.download_media(
            reply_message,
            downloaded_file_name,
            )
        ms_one = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            c_time = time.time()
            await borg.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=event.message.id,
                thumb=thumb,
                )
            end_two = datetime.now()
            os.remove(downloaded_file_name)
            ms_two = (end_two - end).seconds
            await event.edit("Downloaded in {} seconds. Uploaded in {} seconds.".format(ms_one, ms_two))
        else:
            await event.edit("File Not Found {}".format(input_str))
    else:
        await event.edit("Syntax // .rnupload file.name as reply to a Telegram media")


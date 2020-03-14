#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) M.Furkan

import asyncio
import os
import subprocess
import time
from datetime import datetime
import re
import telethon
from telethon import *
from telethon.tl.types import *

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from userbot.uniborgConfig import Config

from userbot.utils import admin_cmd, humanbytes, progress, time_formatter
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
# thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "thumb_image.jpg"

@borg.on(admin_cmd(pattern="converttovideo ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    thumb = None
    thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "thumb_image.jpg"
    logger.info(thumb_image_path)
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
            await mone.edit("Downloaded now preparing to streaming upload")
        # if os.path.exists(input_str):
            
            if os.path.exists(Config.TMP_DOWNLOAD_DIRECTORY):
                if not downloaded_file_name.endswith((".mkv", ".mp4", ".mp3", ".flac",".webm",".ts",".mov")):
                    await mone.edit(
                        "**Supported Formats**: MKV, MP4, MP3, FLAC"
                    )
                    return False
                if downloaded_file_name.upper().endswith(("MKV", "MP4", "WEBM")):
                    metadata = extractMetadata(createParser(downloaded_file_name))
                    duration = 0
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    width = 0
                    height = 0
                    thumb = None
                if os.path.exists(thumb_image_path):
                    thumb = thumb_image_path   
                else:
                    thumb =  await take_screen_shot(
                        downloaded_file_name,
                        os.path.dirname(os.path.abspath(downloaded_file_name)),
                        (duration / 2)
                    )
                start = datetime.now()
                metadata = extractMetadata(createParser(downloaded_file_name))
                # duration = 0
                width = 0
                height = 0
                # if metadata.has("duration"):
                    # duration = metadata.get('duration').seconds
                if os.path.exists(thumb_image_path):
                    metadata = extractMetadata(createParser(thumb_image_path))
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                c_time = time.time()
                try:
                    await borg.send_file(
                        event.chat_id,
                        downloaded_file_name,
                        thumb=thumb,
                        caption=input_str,
                        force_document=False,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True
                            )
                        ],
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, mone, c_time, "trying to upload")
                        )
                    )
                except Exception as e:
                    await mone.edit(str(e))
                else:
                    end = datetime.now()
                    # os.remove(input_str)

                    ms = (end - start).seconds
                    await mone.edit("Uploaded in {} seconds.".format(ms))
                os.remove(thumb)
                await asyncio.sleep(5)
                os.remove(downloaded_file_name)
            else:
                await mone.edit("404: File Not Found")



def get_video_thumb(file, output=None, width=90):
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen([
        'ffmpeg', '-i', file,
        '-ss', str(int((0, metadata.get('duration').seconds)[metadata.has('duration')] / 2)),
        '-filter:v', 'scale={}:-1'.format(width),
        '-vframes', '1',
        output,
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if not p.returncode and os.path.lexists(file):
        return output

async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = os.path.join(
        output_directory,
        str(time.time()) + ".jpg"
    )
    if video_file.upper().endswith(("MKV", "MP4", "WEBM")):
        file_genertor_command = [
            "ffmpeg",
            "-ss",
            str(ttl),
            "-i",
            video_file,
            "-vframes",
            "1",
            out_put_file_name
        ]
        # width = "90"
        process = await asyncio.create_subprocess_exec(
            *file_genertor_command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
    #
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None





def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst

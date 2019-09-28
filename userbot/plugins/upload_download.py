# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except
# 'download, uploadir, uploadas, upload' which is MPL
# License: MPL and OSSRPL
""" Userbot module which contains everything related to \
    downloading/uploading from/to the server. """

import json
import os
import subprocess
import time
import math

from pySmartDL import SmartDL
import asyncio
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for both
    upload.py and download.py"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}]\nProgress: {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        if file_name:
            await event.edit("{}\nFile Name: `{}`\n{}".format(
                type_of_ps, file_name, tmp))
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " day(s), ") if days else "") + \
        ((str(hours) + " hour(s), ") if hours else "") + \
        ((str(minutes) + " minute(s), ") if minutes else "") + \
        ((str(seconds) + " second(s), ") if seconds else "") + \
        ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    return tmp[:-2]


@command(pattern="^.download(?: |)(.*)", outgoing=True)
async def download(target_file):
    """ For .download command, download files to the userbot's server. """
    if not target_file.text[0].isalpha() and target_file.text[0] not in (
            "/", "#", "@", "!"):
        if target_file.fwd_from:
            return
        await target_file.edit("Processing ...")
        input_str = target_file.pattern_match.group(1)
        if not os.path.isdir(Var.TEMP_DOWNLOAD_DIRECTORY):
            os.makedirs(Var.TEMP_DOWNLOAD_DIRECTORY)
        if input_str.startswith("http"):
            if "|" in input_str:
                url, file_name = input_str.split("|")
            else:
                url = input_str
                file_name = os.path.basename(url)
            url = url.strip()
            # https://stackoverflow.com/a/761825/4723940
            file_name = file_name.strip()
            head, tail = os.path.split(file_name)
            if head:
                if not os.path.isdir(
                        os.path.join(Var.TEMP_DOWNLOAD_DIRECTORY, head)):
                    os.makedirs(os.path.join(Var.TEMP_DOWNLOAD_DIRECTORY, head))
                    file_name = os.path.join(head, tail)
            downloaded_file_name = Var.TEMP_DOWNLOAD_DIRECTORY + "" + file_name
            downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
            downloader.start(blocking=False)
            c_time = time.time()
            display_message = None
            while not downloader.isFinished():
                status = downloader.get_status().capitalize()
                total_length = downloader.filesize if downloader.filesize else None
                downloaded = downloader.get_dl_size()
                now = time.time()
                diff = now - c_time
                percentage = downloader.get_progress() * 100
                speed = downloader.get_speed()
                elapsed_time = round(diff) * 1000
                progress_str = "[{0}{1}]\nProgress: {2}%".format(
                    ''.join(["█" for i in range(math.floor(percentage / 5))]),
                    ''.join(
                        ["░" for i in range(20 - math.floor(percentage / 5))]),
                    round(percentage, 2))
                estimated_total_time = downloader.get_eta(human=True)
                try:
                    current_message = f"{status}..\
                    \nURL: {url}\
                    \nFile Name: {file_name}\
                    \n{progress_str}\
                    \n{humanbytes(downloaded)} of {humanbytes(total_length)}\
                    \nETA: {estimated_total_time}"
                    if current_message != display_message:
                        await target_file.edit(current_message)
                        display_message = current_message
                        await asyncio.sleep(1)
                except Exception as e:
                    await target_file.edit(str(e))
                    pass
            if downloader.isSuccessful():
                await target_file.edit(
                    "Downloaded to `{}` successfully !!".format(
                        downloaded_file_name))
            else:
                await target_file.edit("Incorrect URL\n{}".format(url))
        elif target_file.reply_to_msg_id:
            try:
                c_time = time.time()
                file_media = await target_file.get_reply_message()
                downloaded_file_name = await target_file.client.download_media(
                    file_media.media,
                    Var.TEMP_DOWNLOAD_DIRECTORY,
                    progress_callback=lambda d, t: asyncio.get_event_loop(
                    ).create_task(
                        progress(d, t, target_file, c_time, "Downloading...")))
                await target_file.edit(
                    "Downloaded to `{}` successfully !!".format(
                        downloaded_file_name))
            except Exception as e:  # pylint:disable=C0103,W0703
                await target_file.edit(str(e))
        else:
            await target_file.edit(
                "Reply to a message to download to my local server.")


@command(pattern="^.uploadir (.*)", outgoing=True)
async def uploadir(udir_event):
    """ For .uploadir command, allows you to upload everything from a folder in the server"""
    if not udir_event.text[0].isalpha() and udir_event.text[0] not in (
            "/", "#", "@", "!"):
        if udir_event.fwd_from:
            return
        input_str = udir_event.pattern_match.group(1)
        if os.path.exists(input_str):
            await udir_event.edit("Processing ...")
            lst_of_files = []
            for r, d, f in os.walk(input_str):
                for file in f:
                    lst_of_files.append(os.path.join(r, file))
                for file in d:
                    lst_of_files.append(os.path.join(r, file))
            await udir_event.edit(lst_of_files)
            uploaded = 0
            await udir_event.edit(
                "Found {} files. Uploading will start soon. Please wait!".
                format(len(lst_of_files)))
            for single_file in lst_of_files:
                if os.path.exists(single_file):
                    # https://stackoverflow.com/a/678242/4723940
                    caption_rts = os.path.basename(single_file)
                    c_time = time.time()
                    if not caption_rts.lower().endswith(".mp4"):
                        await udir_event.client.send_file(
                            udir_event.chat_id,
                            single_file,
                            caption=caption_rts,
                            force_document=False,
                            allow_cache=False,
                            reply_to=udir_event.message.id,
                            progress_callback=lambda d, t: asyncio.
                            get_event_loop().create_task(
                                progress(d, t, udir_event, c_time,
                                         "Uploading...", single_file)))
                    else:
                        thumb_image = os.path.join(input_str, "thumb.jpg")
                        c_time = time.time()
                        metadata = extractMetadata(createParser(single_file))
                        duration = 0
                        width = 0
                        height = 0
                        if metadata.has("duration"):
                            duration = metadata.get("duration").seconds
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                        await udir_event.client.send_file(
                            udir_event.chat_id,
                            single_file,
                            caption=caption_rts,
                            thumb=thumb_image,
                            force_document=False,
                            allow_cache=False,
                            reply_to=udir_event.message.id,
                            attributes=[
                                DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height,
                                    round_message=False,
                                    supports_streaming=True,
                                )
                            ],
                            progress_callback=lambda d, t: asyncio.
                            get_event_loop().create_task(
                                progress(d, t, udir_event, c_time,
                                         "Uploading...", single_file)))
                    os.remove(single_file)
                    uploaded = uploaded + 1
            await udir_event.edit(
                "Uploaded {} files successfully !!".format(uploaded))
        else:
            await udir_event.edit("404: Directory Not Found")


@command(pattern="^.upload (.*)", outgoing=True)
async def upload(u_event):
    """ For .upload command, allows you to upload a file from the userbot's server """
    if not u_event.text[0].isalpha() and u_event.text[0] not in ("/", "#", "@",
                                                                 "!"):
        if u_event.fwd_from:
            return
        if u_event.is_channel and not u_event.is_group:
            await u_event.edit("`Uploading isn't permitted on channels`")
            return
        await u_event.edit("Processing ...")
        input_str = u_event.pattern_match.group(1)
        if input_str in ("userbot.session", "config.env"):
            await u_event.edit("`That's a dangerous operation! Not Permitted!`"
                               )
            return
        if os.path.exists(input_str):
            c_time = time.time()
            await u_event.client.send_file(
                u_event.chat_id,
                input_str,
                force_document=True,
                allow_cache=False,
                reply_to=u_event.message.id,
                progress_callback=lambda d, t: asyncio.get_event_loop(
                ).create_task(
                    progress(d, t, u_event, c_time, "Uploading...", input_str))
            )
            await u_event.edit("Uploaded successfully !!")
        else:
            await u_event.edit("404: File Not Found")


def get_video_thumb(file, output=None, width=90):
    """ Get video thumbnail """
    metadata = extractMetadata(createParser(file))
    popen = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            str(
                int((0, metadata.get("duration").seconds
                     )[metadata.has("duration")] / 2)),
            "-filter:v",
            "scale={}:-1".format(width),
            "-vframes",
            "1",
            output,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if not popen.returncode and os.path.lexists(file):
        return output
    return None


def extract_w_h(file):
    """ Get width and height of media """
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file,
    ]
    # https://stackoverflow.com/a/11236144/4723940
    try:
        t_response = subprocess.check_output(command_to_run,
                                             stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warning(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@command(pattern="^.uploadas(stream|vn|all) (.*)", outgoing=True)
async def uploadas(uas_event):
    """ For .uploadas command, allows you to specify some arguments for upload. """
    if not uas_event.text[0].isalpha() and uas_event.text[0] not in ("/", "#",
                                                                     "@", "!"):
        if uas_event.fwd_from:
            return
        await uas_event.edit("Processing ...")
        type_of_upload = uas_event.pattern_match.group(1)
        supports_streaming = False
        round_message = False
        spam_big_messages = False
        if type_of_upload == "stream":
            supports_streaming = True
        if type_of_upload == "vn":
            round_message = True
        if type_of_upload == "all":
            spam_big_messages = True
        input_str = uas_event.pattern_match.group(2)
        thumb = None
        file_name = None
        if "|" in input_str:
            file_name, thumb = input_str.split("|")
            file_name = file_name.strip()
            thumb = thumb.strip()
        else:
            file_name = input_str
            thumb_path = "a_random_f_file_name" + ".jpg"
            thumb = get_video_thumb(file_name, output=thumb_path)
        if os.path.exists(file_name):
            metadata = extractMetadata(createParser(file_name))
            duration = 0
            width = 0
            height = 0
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
            try:
                if supports_streaming:
                    c_time = time.time()
                    await uas_event.client.send_file(
                        uas_event.chat_id,
                        file_name,
                        thumb=thumb,
                        caption=input_str,
                        force_document=False,
                        allow_cache=False,
                        reply_to=uas_event.message.id,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True,
                            )
                        ],
                        progress_callback=lambda d, t: asyncio.get_event_loop(
                        ).create_task(
                            progress(d, t, uas_event, c_time, "Uploading...",
                                     file_name)))
                elif round_message:
                    c_time = time.time()
                    await uas_event.client.send_file(
                        uas_event.chat_id,
                        file_name,
                        thumb=thumb,
                        allow_cache=False,
                        reply_to=uas_event.message.id,
                        video_note=True,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=0,
                                w=1,
                                h=1,
                                round_message=True,
                                supports_streaming=True,
                            )
                        ],
                        progress_callback=lambda d, t: asyncio.get_event_loop(
                        ).create_task(
                            progress(d, t, uas_event, c_time, "Uploading...",
                                     file_name)))
                elif spam_big_messages:
                    await uas_event.edit("TBD: Not (yet) Implemented")
                    return
                os.remove(thumb)
                await uas_event.edit("Uploaded successfully !!")
            except FileNotFoundError as err:
                await uas_event.edit(str(err))
        else:
            await uas_event.edit("404: File Not Found")

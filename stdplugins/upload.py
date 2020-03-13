# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
"""Uploads Files to Telegram
Available Commands:
.upload <Path To File>
.uploadir <Path To Directory>
.uploadasstream <Path To File>"""

import asyncio
import os
import subprocess
import time
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from telethon.tl.types import DocumentAttributeAudio
from uniborg.util import progress, admin_cmd


thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


@borg.on(admin_cmd(pattern="uploadir (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if os.path.exists(input_str):
        start = datetime.now()
        # await event.edit("Processing ...")
        lst_of_files = sorted(get_lst_of_files(input_str, []))
        logger.info(lst_of_files)
        u = 0
        await event.edit(
            "Found {} files. ".format(len(lst_of_files)) + \
            "Uploading will start soon. " + \
            "Please wait!"
        )
        thumb = None
        if os.path.exists(thumb_image_path):
            thumb = thumb_image_path
        for single_file in lst_of_files:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                width = 0
                height = 0
                if os.path.exists(thumb_image_path):
                    metadata = extractMetadata(createParser(thumb_image_path))
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                if single_file.upper().endswith(Config.TL_VID_STREAM_TYPES):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ]
                    supports_streaming = True
                    force_document = False
                if single_file.upper().endswith(Config.TL_MUS_STREAM_TYPES):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    title = ""
                    artist = ""
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    if metadata.has("title"):
                        title = metadata.get("title")
                    if metadata.has("artist"):
                        artist = metadata.get("artist")
                    document_attributes = [
                        DocumentAttributeAudio(
                            duration=duration,
                            voice=False,
                            title=title,
                            performer=artist,
                            waveform=None
                        )
                    ]
                    supports_streaming = True
                    force_document = False
                try:
                    await borg.send_file(
                        event.chat_id,
                        single_file,
                        caption=caption_rts,
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        thumb=thumb,
                        attributes=document_attributes,
                        # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        #     progress(d, t, event, c_time, "trying to upload")
                        # )
                    )
                except Exception as e:
                    await borg.send_message(
                        event.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id
                    )
                    # some media were having some issues
                    continue
                os.remove(single_file)
                u = u + 1
                # await event.edit("Uploaded {} / {} files.".format(u, len(lst_of_files)))
                # @ControllerBot was having issues,
                # if both edited_updates and update events come simultaneously.
                await asyncio.sleep(5)
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Uploaded {} files in {} seconds.".format(u, ms))
    else:
        await event.edit("404: Directory Not Found")


@borg.on(admin_cmd(pattern="upload (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    input_str = event.pattern_match.group(1)
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    if os.path.exists(input_str):
        start = datetime.now()
        c_time = time.time()
        await borg.send_file(
            event.chat_id,
            input_str,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
            thumb=thumb,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to upload")
            )
        )
        end = datetime.now()
        # os.remove(input_str)
        ms = (end - start).seconds
        await mone.edit("Uploaded in {} seconds.".format(ms))
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


@borg.on(admin_cmd(pattern="uploadasstream (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    input_str = event.pattern_match.group(1)
    thumb = None
    file_name = input_str
    if os.path.exists(file_name):
        if not file_name.endswith((".mkv", ".mp4", ".mp3", ".flac")):
            await mone.edit(
                "Sorry. But I don't think {} is a streamable file.".format(file_name) + \
                " Please try again.\n" + \
                "**Supported Formats**: MKV, MP4, MP3, FLAC"
            )
            return False
        if os.path.exists(thumb_image_path):
            thumb = thumb_image_path
        else:
            thumb = get_video_thumb(file_name, thumb_image_path)
        start = datetime.now()
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if os.path.exists(thumb_image_path):
            metadata = extractMetadata(createParser(thumb_image_path))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
        # Telegram only works with MP4 files
        # this is good, since with MKV files sent as streamable Telegram responds,
        # Bad Request: VIDEO_CONTENT_TYPE_INVALID
        c_time = time.time()
        try:
            await borg.send_file(
                event.chat_id,
                file_name,
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
            os.remove(input_str)
            ms = (end - start).seconds
            await mone.edit("Uploaded in {} seconds.".format(ms))
    else:
        await mone.edit("404: File Not Found")

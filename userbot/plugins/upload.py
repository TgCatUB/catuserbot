import asyncio
import io
import os
import pathlib
import subprocess
import time
from datetime import datetime
from pathlib import Path
from shutil import copyfile

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pymediainfo import MediaInfo
from telethon.tl import types
from telethon.tl.types import DocumentAttributeVideo
from telethon.utils import get_attributes

from userbot import catub

from ..Config import Config
from ..helpers.utils import _catutils, reply_id
from . import (edit_delete, edit_or_reply, make_gif, progress, reply_id,
               thumb_from_audio)

plugin_category = "misc"

PATH = os.path.join("./temp", "temp_vid.mp4")
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
plugin_category = "misc"
downloads = pathlib.Path("./downloads/").absolute()
NAME = "untitled"


class UPLOAD:
    def __init__(self):
        self.uploaded = 0


UPLOAD_ = UPLOAD()


async def catlst_of_files(path):
    files = []
    for dirname, dirnames, filenames in os.walk(path):
        # print path to all filenames.
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files


def get_video_thumb(file, output=None, width=320):
    output = file + ".jpg"
    metadata = extractMetadata(createParser(file))
    cmd = [
        "ffmpeg",
        "-i",
        file,
        "-ss",
        str(int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)),
        # '-filter:v', 'scale={}:-1'.format(width),
        "-vframes",
        "1",
        output,
    ]
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    p.communicate()
    if not p.returncode and os.path.lexists(file):
        return output


def sortthings(contents, path):
    catsort = []
    contents.sort()
    for file in contents:
        catpath = os.path.join(path, file)
        if os.path.isfile(catpath):
            catsort.append(file)
    for file in contents:
        catpath = os.path.join(path, file)
        if os.path.isdir(catpath):
            catsort.append(file)
    return catsort


async def _get_file_name(path: pathlib.Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


async def upload(path, event, udir_event, catflag=None):  # sourcery no-metrics
    catflag = catflag or False
    reply_to_id = await reply_id(event)
    if os.path.isdir(path):
        await event.client.send_message(
            event.chat_id,
            f"**Folder : **`{str(path)}`",
        )
        Files = os.listdir(path)
        Files = sortthings(Files, path)
        for file in Files:
            catpath = os.path.join(path, file)
            await upload(Path(catpath), event, udir_event)
    elif os.path.isfile(path):
        fname = os.path.basename(path)
        c_time = time.time()
        thumb = None
        if os.path.exists(thumb_image_path):
            thumb = thumb_image_path
        f = path.absolute()
        attributes, mime_type = get_attributes(str(f))
        ul = io.open(f, "rb")
        uploaded = await event.client.fast_upload_file(
            file=ul,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to upload", file_name=fname)
            ),
        )
        ul.close()
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type=mime_type,
            attributes=attributes,
            force_file=catflag,
            thumb=await event.client.upload_file(thumb) if thumb else None,
        )
        await event.client.send_file(
            event.chat_id,
            file=media,
            caption=f"**File Name : **`{fname}`",
            reply_to=reply_to_id,
        )

        UPLOAD_.uploaded += 1


@catub.cat_cmd(
    pattern="upload( -f)? (.*)",
    command=("upload", plugin_category),
    info={
        "header": "To upload files from server to telegram",
        "description": "To upload files which downloaded to bot.",
        "flags": {"f": "Use this to make upload files as documents."},
        "examples": [
            "{tr}upload <file/folder path>",
            "{tr}upload -f <file/folder path>",
        ],
    },
)
async def uploadir(event):
    "To upload files to telegram."
    input_str = event.pattern_match.group(2)
    path = Path(input_str)
    start = datetime.now()
    flag = event.pattern_match.group(1)
    flag = bool(flag)
    if not os.path.exists(path):
        return await edit_or_reply(
            event,
            f"`there is no such directory/file with the name {path} to upload`",
        )
    udir_event = await edit_or_reply(event, "Uploading....")
    if os.path.isdir(path):
        await edit_or_reply(udir_event, f"`Gathering file details in directory {path}`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event, catflag=flag)
        end = datetime.now()
        ms = (end - start).seconds
        await edit_delete(
            udir_event,
            f"`Uploaded {UPLOAD_.uploaded} files successfully in {ms} seconds. `",
        )
    else:
        await edit_or_reply(udir_event, f"`Uploading file .....`")
        UPLOAD_.uploaded = 0
        await upload(path, event, udir_event, catflag=flag)
        end = datetime.now()
        ms = (end - start).seconds
        await edit_delete(
            udir_event, f"`Uploaded file {str(path)} successfully in {ms} seconds. `"
        )


@catub.cat_cmd(
    pattern="circle(?: |$)(.*)",
    command=("circle", plugin_category),
    info={
        "header": "To make circular video note.",
        "description": "crcular video note supports atmost 60 sec so give appropariate video.",
        "usage": "{tr}circle <reply to video or provide video path>",
    },
)
async def video_catfile(event):  # sourcery no-metrics
    "To make circular video note."
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    if input_str:
        path = Path(input_str)
        if not os.path.exists(path):
            return await edit_or_reply(
                event,
                f"`there is no such directory/file with the name {path} to upload`",
            )
        catevent = await edit_or_reply(event, "`Converting to video note..........`")
        filename = os.path.basename(path)
        catfile = os.path.join("./temp", filename)
        copyfile(path, catfile)
    else:
        if not reply or not reply.media:
            return await edit_delete(event, "`Reply to supported media`", 5)
        catevent = await edit_or_reply(event, "`Converting to video note..........`")
        catfile = await reply.download_media(file="./temp/")
    if not catfile.endswith((".mp4", ".tgs", ".mp3", ".mov", ".gif", ".opus")):
        os.remove(catfile)
        return await edit_delete(catevent, "```Supported Media not found...```", 5)
    if catfile.endswith((".mp4", ".tgs", ".mov", ".gif")):
        if catfile.endswith((".tgs")):
            hmm = await make_gif(catevent, catfile)
            if hmm.endswith(("@tgstogifbot")):
                os.remove(catfile)
                return await catevent.edit(hmm)
            os.rename(hmm, "./temp/circle.mp4")
            catfile = "./temp/circle.mp4"
        media_info = MediaInfo.parse(catfile)
        aspect_ratio = 1
        for track in media_info.tracks:
            if track.track_type == "Video":
                aspect_ratio = track.display_aspect_ratio
                height = track.height
                width = track.width
        if aspect_ratio != 1:
            crop_by = width if (height > width) else height
            await _catutils.runcmd(
                f'ffmpeg -i {catfile} -vf "crop={crop_by}:{crop_by}" {PATH}'
            )
        else:
            copyfile(catfile, PATH)
        if str(catfile) != str(PATH):
            os.remove(catfile)
    else:
        thumb_loc = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
        catthumb = None
        try:
            catthumb = await reply.download_media(thumb=-1)
        except Exception:
            catthumb = os.path.join("./temp", "thumb.jpg")
            await thumb_from_audio(catfile, catthumb)
        if catthumb is None:
            catthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, catthumb)
        if (
            catthumb is not None
            and not os.path.exists(catthumb)
            and os.path.exists(thumb_loc)
        ):
            catthumb = os.path.join("./temp", "thumb.jpg")
            copyfile(thumb_loc, catthumb)
        if catthumb is not None and os.path.exists(catthumb):
            await _catutils.runcmd(
                f"ffmpeg -loop 1 -i {catthumb} -i {catfile} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -vf \"scale='iw-mod (iw,2)':'ih-mod(ih,2)',format=yuv420p\" -shortest -movflags +faststart {PATH}"
            )
            os.remove(catfile)
        else:
            os.remove(catfile)
            return await edit_delete(
                catevent, "`No thumb found to make it video note`", 5
            )
    if os.path.exists(PATH):
        catid = event.reply_to_msg_id
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            PATH,
            allow_cache=False,
            reply_to=catid,
            video_note=True,
            attributes=[
                DocumentAttributeVideo(
                    duration=60,
                    w=1,
                    h=1,
                    round_message=True,
                    supports_streaming=True,
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, catevent, c_time, "Uploading...", PATH)
            ),
        )
        os.remove(PATH)
    await catevent.delete()

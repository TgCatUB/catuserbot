import asyncio
import io
import math
import os
import pathlib
import time
from datetime import datetime

from pySmartDL import SmartDL
from telethon.tl import types
from telethon.utils import get_extension

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import humanbytes, progress
from ..helpers.utils import _format

plugin_category = "misc"

NAME = "untitled"

downloads = pathlib.Path(os.path.join(os.getcwd(), Config.TMP_DOWNLOAD_DIRECTORY))


async def _get_file_name(path: pathlib.Path, full: bool = True) -> str:
    return str(path.absolute()) if full else path.stem + path.suffix


@catub.cat_cmd(
    pattern="d(own)?l(oad)?(?:\s|$)([\s\S]*)",
    command=("download", plugin_category),
    info={
        "header": "To download the replied telegram file",
        "description": "Will download the replied telegram file to server .",
        "note": "The downloaded files will auto delete if you restart heroku.",
        "usage": [
            "{tr}download <reply>",
            "{tr}dl <reply>",
            "{tr}download custom name<reply>",
        ],
    },
)
async def _(event):  # sourcery no-metrics  # sourcery skip: low-code-quality
    "To download the replied telegram file"
    mone = await edit_or_reply(event, "`Downloading....`")
    input_str = event.pattern_match.group(3)
    name = NAME
    path = None
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    reply = await event.get_reply_message()
    if reply:
        start = datetime.now()
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        if input_str:
            path = pathlib.Path(os.path.join(downloads, input_str.strip()))
        else:
            path = pathlib.Path(os.path.join(downloads, name))
        ext = get_extension(reply.document)
        if path and not path.suffix and ext:
            path = path.with_suffix(ext)
        if name == NAME:
            name += "_" + str(getattr(reply.document, "id", reply.id)) + ext
        if path and path.exists():
            if path.is_file():
                newname = f"{str(path.stem)}_OLD"
                path.rename(path.with_name(newname).with_suffix(path.suffix))
                file_name = path
            else:
                file_name = path / name
        elif path and not path.suffix and ext:
            file_name = downloads / path.with_suffix(ext)
        elif path:
            file_name = path
        else:
            file_name = downloads / name
        file_name.parent.mkdir(parents=True, exist_ok=True)
        c_time = time.time()
        if (
            not reply.document
            and reply.photo
            and file_name
            and file_name.suffix
            or not reply.document
            and not reply.photo
        ):
            await reply.download_media(
                file=file_name.absolute(),
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
        elif not reply.document:
            file_name = await reply.download_media(
                file=downloads,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
        else:
            dl = io.FileIO(file_name.absolute(), "a")
            await event.client.fast_download_file(
                location=reply.document,
                out=dl,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
            dl.close()
        end = datetime.now()
        ms = (end - start).seconds
        await mone.edit(
            f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded to :- **  `{os.path.relpath(file_name,os.getcwd())}`\n   "
        )
    elif input_str:
        start = datetime.now()
        if "|" in input_str:
            url, file_name = input_str.split("|")
        else:
            url = input_str
            file_name = None
        url = url.strip()
        file_name = os.path.basename(url) if file_name is None else file_name.strip()
        downloaded_file_name = pathlib.Path(os.path.join(downloads, file_name))
        if not downloaded_file_name.suffix:
            ext = os.path.splitext(url)[1]
            downloaded_file_name = downloaded_file_name.with_suffix(ext)
        downloader = SmartDL(url, str(downloaded_file_name), progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        delay = 0
        oldmsg = ""
        while not downloader.isFinished():
            total_length = downloader.filesize or None
            downloaded = downloader.get_dl_size()
            now = time.time()
            delay = now - c_time
            percentage = downloader.get_progress() * 100
            dspeed = downloader.get_speed()
            progress_str = "`{0}{1} {2}`%".format(
                "".join("▰" for _ in range(math.floor(percentage / 5))),
                "".join("▱" for _ in range(20 - math.floor(percentage / 5))),
                round(percentage, 2),
            )

            estimated_total_time = downloader.get_eta(human=True)
            current_message = f"Downloading the file\
                                \n\n**URL : **`{url}`\
                                \n**File Name :** `{file_name}`\
                                \n{progress_str}\
                                \n`{humanbytes(downloaded)} of {humanbytes(total_length)} @ {humanbytes(dspeed)}`\
                                \n**ETA : **`{estimated_total_time}`"
            if oldmsg != current_message and delay > 5:
                await mone.edit(current_message)
                delay = 0
                c_time = time.time()
                oldmsg = current_message
            await asyncio.sleep(1)
        end = datetime.now()
        ms = (end - start).seconds
        if downloader.isSuccessful():
            await mone.edit(
                f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded file location :- ** `{os.path.relpath(downloaded_file_name,os.getcwd())}`"
            )
        else:
            await mone.edit(f"Incorrect URL\n {input_str}")
    else:
        await mone.edit("`Reply to a message to download to my local server.`")


@catub.cat_cmd(
    pattern="d(own)?l(oad)?to(?:\s|$)([\s\S]*)",
    command=("dlto", plugin_category),
    info={
        "header": "To download the replied telegram file to specific directory",
        "description": "Will download the replied telegram file to server that is your custom folder.",
        "note": "The downloaded files will auto delete if you restart heroku.",
        "usage": [
            "{tr}downloadto <folder path>",
            "{tr}dlto <folder path>",
        ],
    },
)
async def _(event):  # sourcery no-metrics  # sourcery skip: low-code-quality
    pwd = os.getcwd()
    input_str = event.pattern_match.group(3)
    name = NAME
    path = None
    if not input_str:
        return await edit_delete(
            event,
            "Where should i save this file. mention folder name",
            parse_mode=_format.parse_pre,
        )

    location = os.path.join(pwd, input_str)
    if not os.path.isdir(location):
        os.makedirs(location)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(
            event,
            "Reply to media file to download it to bot server",
            parse_mode=_format.parse_pre,
        )
    mone = await edit_or_reply(
        event, "Downloading the file ...", parse_mode=_format.parse_pre
    )
    start = datetime.now()
    for attr in getattr(reply.document, "attributes", []):
        if isinstance(attr, types.DocumentAttributeFilename):
            name = attr.file_name
    path = pathlib.Path(os.path.join(location, name))
    ext = get_extension(reply.document)
    if path and not path.suffix and ext:
        path = path.with_suffix(ext)
    if name == NAME:
        name += "_" + str(getattr(reply.document, "id", reply.id)) + ext
    if path and path.exists():
        if path.is_file():
            newname = f"{str(path.stem)}_OLD"
            path.rename(path.with_name(newname).with_suffix(path.suffix))
            file_name = path
        else:
            file_name = path / name
    elif path and not path.suffix and ext:
        file_name = location / path.with_suffix(ext)
    elif path:
        file_name = path
    else:
        file_name = location / name
    file_name.parent.mkdir(parents=True, exist_ok=True)
    c_time = time.time()
    if (
        not reply.document
        and reply.photo
        and file_name
        and file_name.suffix
        or not reply.document
        and not reply.photo
    ):
        await reply.download_media(
            file=file_name.absolute(),
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            ),
        )
    elif not reply.document:
        file_name = await reply.download_media(
            file=location,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            ),
        )
    else:
        dl = io.FileIO(file_name.absolute(), "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            ),
        )
        dl.close()
    end = datetime.now()
    ms = (end - start).seconds
    await mone.edit(
        f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded to :- **  `{os.path.relpath(file_name,os.getcwd())}`\n   "
    )

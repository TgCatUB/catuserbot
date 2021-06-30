import asyncio
import os
import time
from datetime import datetime

from userbot import catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id
from . import progress, reply_id

plugin_category = "utils"

thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@catub.cat_cmd(
    pattern="rnup ?(-f)? ([\s\S]*)",
    command=("rnup", plugin_category),
    info={
        "header": "To rename and upload the replied file.",
        "flags": {"f": "will upload as file that is document not streamable."},
        "description": "If flag is not used then will upload as steamable file",
        "usage": [
            "{tr}rnup <new file name>",
            "{tr}rnup -f <new file name>",
        ],
    },
)
async def _(event):
    "To rename and upload the file"
    thumb = thumb_image_path if os.path.exists(thumb_image_path) else None
    flags = event.pattern_match.group(1)
    forcedoc = bool(flags)
    supsstream = not flags
    catevent = await edit_or_reply(
        event,
        "`Rename & Upload in process 🙄🙇‍♂️🙇‍♂️🙇‍♀️ It might take some time if file size is big`",
    )
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(2)
    if not event.reply_to_msg_id:
        return await catevent.edit(
            "**Syntax : **`.rnup file name` as reply to a Telegram media"
        )
    start = datetime.now()
    file_name = input_str
    reply_message = await event.get_reply_message()
    c_time = time.time()
    downloaded_file_name = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, file_name)
    downloaded_file_name = await event.client.download_media(
        reply_message,
        downloaded_file_name,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, catevent, c_time, "trying to download", file_name)
        ),
    )
    end = datetime.now()
    ms_one = (end - start).seconds
    try:
        thumb = await reply_message.download_media(thumb=-1)
    except Exception:
        thumb = thumb
    if not os.path.exists(downloaded_file_name):
        return await catevent.edit(f"File Not Found {input_str}")
    c_time = time.time()
    caat = await event.client.send_file(
        event.chat_id,
        downloaded_file_name,
        force_document=forcedoc,
        supports_streaming=supsstream,
        allow_cache=False,
        reply_to=reply_to_id,
        thumb=thumb,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "trying to upload", downloaded_file_name)
        ),
    )
    end_two = datetime.now()
    os.remove(downloaded_file_name)
    ms_two = (end_two - end).seconds
    await edit_delete(
        catevent,
        f"`Downloaded file in {ms_one} seconds.\nAnd Uploaded in {ms_two} seconds.`",
    )

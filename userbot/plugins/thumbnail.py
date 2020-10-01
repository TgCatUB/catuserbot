# Thumbnail Utilities ported from uniborg 
#credits @spechide

import os
import asyncio
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from ..utils import admin_cmd,sudo_cmd , edit_or_reply
from . import CMD_HELP

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"

async def get_video_thumb(video_file, output_directory=None, width=320):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(time.time()) + ".jpg"
    metadata = extractMetadata(createParser(video_file))
    ttl = 0
    if metadata and metadata.has("duration"):
        ttl = metadata.get("duration").seconds / 2
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
    if os.path.lexists(out_put_file_name):
        return out_put_file_name


@borg.on(admin_cmd(pattern="savethumbnail$"))
@borg.on(sudo_cmd(pattern="savethumbnail$",allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    catevent = await edit_or_reply(event , "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        downloaded_file_name = await event.client.download_media(
            await event.get_reply_message(),
            Config.TMP_DOWNLOAD_DIRECTORY
        )
        if downloaded_file_name.endswith(".mp4"):
            downloaded_file_name = await get_video_thumb(
                downloaded_file_name,
                Config.TMP_DOWNLOAD_DIRECTORY
            )
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(
            downloaded_file_name
        ).convert("RGB").save(
            thumb_image_path, "JPEG"
        )
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        os.remove(downloaded_file_name)
        await catevent.edit(
            "Custom video / file thumbnail saved. " + \
            "This image will be used in the upload, till `.clearthumbnail`."
        )
    else:
        await catevent.edit("Reply to a photo to save custom thumbnail")


@borg.on(admin_cmd(pattern="clearthumbnail$"))
@borg.on(sudo_cmd(pattern="clearthumbnail$",allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    else:
        await edit_or_reply(event , "No thumbnail is setted to clear")
    await edit_or_reply(event , "✅ Custom thumbnail cleared succesfully.")


@borg.on(admin_cmd(pattern="getthumbnail$"))
@borg.on(sudo_cmd(pattern="getthumbnail$",allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        try:
            a = await r.download_media(thumb=-1)
        except Exception as e:
            await edit_or_reply(event , str(e))
            return
        try:
            await event.client.send_file(
                event.chat_id,
                a,
                force_document=False,
                allow_cache=False,
                reply_to=event.reply_to_msg_id,
            )
            os.remove(a)
            await event.delete()
        except Exception as e:
            await edit_or_reply(event , str(e))
    elif os.path.exists(thumb_image_path):
        caption_str = "Currently Saved Thumbnail"
        await event.client.send_file(
            event.chat_id,
            thumb_image_path,
            caption=caption_str,
            force_document=False,
            allow_cache=False,
            reply_to=event.message.id
        )
        await edit_or_reply(event , caption_str)
    else:
        await edit_or_reply(event , "Reply `.gethumbnail` as a reply to a media")


CMD_HELP.update(
    {
        "thumbnail": "**Plugin :** `thumbnail`\
    \n\n**Syntax :** `.savethumbnail`\
    \n**Usage : **Reply to file or video to save it as temporary thumbimage\
    \n\n**Syntax : **`.clearthumbnail`\
    \n**Usage : **To clear Thumbnail no longer you uploads uses custom thumbanail\
    \n\n**Syntax : **`.getthumbnail`\
    \n**Usage : **To get thumbnail of given video or gives your present thumbnail\
    "
    }
)

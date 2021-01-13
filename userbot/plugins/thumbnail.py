# Thumbnail Utilities ported from uniborg
# credits @spechide

import os

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@bot.on(admin_cmd(pattern="savethumb$"))
@bot.on(sudo_cmd(pattern="savethumb$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    catevent = await edit_or_reply(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        downloaded_file_name = await event.client.download_media(
            await event.get_reply_message(), Config.TMP_DOWNLOAD_DIRECTORY
        )
        if downloaded_file_name.endswith(".mp4"):
            metadata = extractMetadata(createParser(downloaded_file_name))
            if metadata and metadata.has("duration"):
                duration = metadata.get("duration").seconds
            downloaded_file_name = await _cattools.take_screen_shot(
                downloaded_file_name, duration
            )
        # https://stackoverflow.com/a/21669827/4723940
        Image.open(downloaded_file_name).convert("RGB").save(thumb_image_path, "JPEG")
        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
        os.remove(downloaded_file_name)
        await catevent.edit(
            "Custom video/file thumbnail saved. This image will be used in the upload, till `.clearthumb`."
        )
    else:
        await catevent.edit("Reply to a photo to save custom thumbnail")


@bot.on(admin_cmd(pattern="clearthumb$"))
@bot.on(sudo_cmd(pattern="clearthumb$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    else:
        await edit_or_reply(event, "No thumbnail is set to clear")
    await edit_or_reply(event, "✅ Custom thumbnail cleared succesfully.")


@bot.on(admin_cmd(pattern="getthumb$"))
@bot.on(sudo_cmd(pattern="getthumb$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        try:
            a = await r.download_media(thumb=-1)
        except Exception as e:
            await edit_or_reply(event, str(e))
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
            await edit_or_reply(event, str(e))
    elif os.path.exists(thumb_image_path):
        caption_str = "Currently Saved Thumbnail"
        await event.client.send_file(
            event.chat_id,
            thumb_image_path,
            caption=caption_str,
            force_document=False,
            allow_cache=False,
            reply_to=event.message.id,
        )
        await edit_or_reply(event, caption_str)
    else:
        await edit_or_reply(event, "Reply `.gethumbnail` as a reply to a media")


CMD_HELP.update(
    {
        "thumbnail": "**Plugin :** `thumbnail`\
    \n\n**Syntax :** `.savethumb`\
    \n**Usage : **Reply to file or video to save it as temporary thumbimage\
    \n\n**Syntax : **`.clearthumb`\
    \n**Usage : **To clear Thumbnail no longer you uploads uses custom thumbanail\
    \n\n**Syntax : **`.getthumb`\
    \n**Usage : **To get thumbnail of given video or gives your present thumbnail\
    "
    }
)

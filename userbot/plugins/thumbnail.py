import os

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

from userbot import catub

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.utils import _cattools
from . import CMD_HELP

plugin_category = "utils"

# Thumbnail Utilities ported from uniborg
# credits @spechide


thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@catub.cat_cmd(
    pattern="savethumb$",
    command=("savethumb", plugin_category),
    info={
        "header": "To save replied image as temporary thumb.",
        "usage": "{tr}savethumb",
    },
)
async def _(event):
    "To save replied image as temporary thumb."
    catevent = await edit_or_reply(event, "`Processing ...`")
    if not event.reply_to_msg_id:
        return await catevent.edit("`Reply to a photo to save custom thumbnail`")
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


@catub.cat_cmd(
    pattern="clearthumb$",
    command=("clearthumb", plugin_category),
    info={
        "header": "To delete thumb image.",
        "usage": "{tr}clearthumb",
    },
)
async def _(event):
    "To delete thumb image."
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    else:
        await edit_or_reply(event, "`No thumbnail is set to clear`")
    await edit_or_reply(event, "✅ Custom thumbnail cleared successfully.")


@catub.cat_cmd(
    pattern="getthumb$",
    command=("getthumb", plugin_category),
    info={
        "header": "To get thumbnail of given video or gives your present thumbnail.",
        "usage": "{tr}getthumb",
    },
)
async def _(event):
    "To get thumbnail of given video or gives your present thumbnail"
    if event.reply_to_msg_id:
        r = await event.get_reply_message()
        try:
            a = await r.download_media(thumb=-1)
        except Exception as e:
            return await edit_or_reply(event, str(e))
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

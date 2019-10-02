# (c) Shrimadhav U K - UniBorg
# Thanks to Prakasaka for porting.

import io
import os
import requests
from userbot.events import register
from telethon.tl.types import MessageMediaPhoto
from userbot.__init__ import CMD_HELP 
from userbot.uniborgConfig import REM_BG_API_KEY, TEMP_DOWNLOAD_DIRECTORY


@borg.on(outgoing=True, pattern="^.rbg(?: |$)(.*)")
async def kbg(remob):
    """ For .rbg command, Remove Image Background. """
    if not remob.text[0].isalpha() and remob.text[0] not in ("/", "#", "@", "!"):
        if REM_BG_API_KEY is None:
            await remob.edit("`Error: Remove.BG API key missing! Add it to environment vars or config.env.`")
            return
        input_str = remob.pattern_match.group(1)
        message_id = remob.message.id
        if remob.reply_to_msg_id:
            message_id = remob.reply_to_msg_id
            reply_message = await remob.get_reply_message()
            await remob.edit("`Processing..`")
            try:
                if isinstance(reply_message.media, MessageMediaPhoto) or "image" in reply_message.media.document.mime_type.split('/'):
                    downloaded_file_name = await remob.client.download_media(
                        reply_message,
                        TEMP_DOWNLOAD_DIRECTORY
                    )
                    await remob.edit("`Removing background from this image..`")
                    output_file_name = ReTrieveFile(downloaded_file_name)
                    os.remove(downloaded_file_name)
                else:
                    await remob.edit("`How do I remove the background from this ?`")
            except Exception as e:
                await remob.edit(str(e))
                return
        elif input_str:
            await remob.edit(f"`Removing background from online image hosted at`\n{input_str}")
            output_file_name = ReTrieveURL(input_str)
        else:
            await remob.edit("`I need something to remove the background from.`")
            return
        contentType = output_file_name.headers.get("content-type")
        if "image" in contentType:
            with io.BytesIO(output_file_name.content) as remove_bg_image:
                remove_bg_image.name = "removed_bg.png"
                await remob.client.send_file(
                    remob.chat_id,
                    remove_bg_image,
                    caption="Background removed By [Spyder](https://t.me/spyderzzz/) using his Gawd skills !",
                    force_document=True,
                    reply_to=message_id
                )
                await remob.delete()
        else:
            await remob.edit("**Error (Invalid API key, I guess ?)**\n`{}`".format(output_file_name.content.decode("UTF-8")))


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True
    )
    return r


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    data = {
      "image_url": input_url
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True
    )
    return r


CMD_HELP.update({
    "remove_bg": ".rbg <Link to Image> or reply to any image\
\nUsage: Removes the background of images, using remove.bg API"
})

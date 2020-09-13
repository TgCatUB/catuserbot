# (c) Shrimadhav U K
#
# This file is part of @UniBorg
#
# @UniBorg is free software; you cannot redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# @UniBorg is not distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import io
import os

import requests

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import convert_toimage


@borg.on(admin_cmd(pattern="(rmbg|srmbg) ?(.*)"))
@borg.on(sudo_cmd(pattern="(rmbg|srmbg) ?(.*)", allow_sudo=True))
async def remove_background(event):
    if event.fwd_from:
        return
    if Config.REM_BG_API_KEY is None:
        return await edit_or_reply(
            event, "`You need API token from remove.bg to use this plugin.`"
        )
    cmd = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    message_id = None
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        # check if media message
        event = await edit_or_reply(event, "Ooh Analysing dis pic...")
        file_name = "rmbg.png"
        if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        try:
            downloaded_file_name = await bot.download_media(
                reply_message, downloaded_file_name
            )
        except Exception as e:
            await event.edit(str(e))
            return
        else:
            await event.edit("`Removing Back ground of this media`")
            downloaded_file_name = convert_toimage(downloaded_file_name)
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    elif input_str:
        await event.edit("`Removing Back ground of this media`")
        output_file_name = ReTrieveURL(input_str)
    else:
        await event.edit(
            "`.rmbg`/`.srmbg` as reply to a media, or give a link as an argument to this command"
        )
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        if cmd == "rmbg":
            with io.BytesIO(output_file_name.content) as remove_bg_image:
                remove_bg_image.name = "CATBG_less.png"
                await borg.send_file(
                    event.chat_id,
                    remove_bg_image,
                    force_document=True,
                    caption="__**➥ Removed dat annoying Background just for you.**__🥳",
                    reply_to=message_id,
                )
            await event.delete()
        elif cmd == "srmbg":
            with io.BytesIO(output_file_name.content) as remove_bg_image:
                remove_bg_image.name = "CAT.webp"
                await borg.send_file(
                    event.chat_id,
                    remove_bg_image,
                    force_document=True,
                    reply_to=message_id,
                )
            await event.delete()
    else:
        await edit_or_reply(
            event, "`{}`".format(output_file_name.content.decode("UTF-8"))
        )


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )
    return r


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    data = {"image_url": input_url}
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )
    return r


CMD_HELP.update(
    {
        "removebg": "__**PLUGIN NAME :** Removebg__\
\n\n📌** CMD ➥** `.rmbg` <Link to Image> or reply to any image \
\n**USAGE   ➥  **Removes the background of images and send as png format\
\n\n📌** CMD ➥** `.srmbg` <reply to any image>\
\n**USAGE   ➥  **Removes the background of images & send as a sticker format"
    }
)

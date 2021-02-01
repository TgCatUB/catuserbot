# ported from uniborg (@spechide)

import os

import requests

from . import convert_toimage, convert_tosticker


@bot.on(admin_cmd(pattern="(rmbg|srmbg) ?(.*)"))
@bot.on(sudo_cmd(pattern="(rmbg|srmbg) ?(.*)", allow_sudo=True))
async def remove_background(event):
    if Config.REM_BG_API_KEY is None:
        return await edit_delete(
            event,
            "`You have to set REM_BG_API_KEY in Config vars with API token from remove.bg to use this plugin .`",
            5,
        )
    cmd = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    message_id = await reply_id(event)
    if event.reply_to_msg_id and not input_str:
        reply_message = await event.get_reply_message()
        catevent = await edit_or_reply(event, "`Analysing this Image/Sticker...`")
        file_name = os.path.join(Config.TEMP_DIR, "rmbg.png")
        try:
            await event.client.download_media(reply_message, file_name)
        except Exception as e:
            await edit_delete(catevent, f"`{str(e)}`", 5)
            return
        else:
            await catevent.edit("`Removing Background of this media`")
            file_name = convert_toimage(file_name)
            response = ReTrieveFile(file_name)
            os.remove(file_name)
    elif input_str:
        catevent = await edit_or_reply(event, "`Removing Background of this media`")
        response = ReTrieveURL(input_str)
    else:
        await edit_delete(
            event,
            "`Reply to any image or sticker with rmbg/srmbg to get background less png file or webp format or provide image link along with command`",
            5,
        )
        return
    contentType = response.headers.get("content-type")
    remove_bg_image = "backgroundless.png"
    if "image" in contentType:
        with open("backgroundless.png", "wb") as removed_bg_file:
            removed_bg_file.write(response.content)
    else:
        await edit_delete(catevent, f"`{response.content.decode('UTF-8')}`", 5)
        return
    if cmd == "srmbg":
        file = convert_tosticker(remove_bg_image, filename="backgroundless.webp")
        await event.client.send_file(
            event.chat_id,
            file,
            reply_to=message_id,
        )
    else:
        file = remove_bg_image
        await event.client.send_file(
            event.chat_id,
            file,
            force_document=True,
            reply_to=message_id,
        )
    await catevent.delete()


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True,
    )


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": Config.REM_BG_API_KEY,
    }
    data = {"image_url": input_url}
    return requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True,
    )


CMD_HELP.update(
    {
        "removebg": """**Plugin : **`removebg`
        
  •  **Syntax : **`.rmbg <Link to Image> or reply to any image/sticker`
  •  **Function : **__Removes the background of an image/sticker and send as png format__
  
  •  **Syntax : **`.srmbg <Link to Image> or reply to any image/sticker`
  •  **Function : **__Removes the background an image/sticker and send as sticker format__
"""
    }
)

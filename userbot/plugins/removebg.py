# Special credits: @spechide (ported from uniborg)

import base64
import os

import aiofiles
import httpx

from userbot import Convert, catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "utils"


# remove.bg's API moved to Leonardo.Ai on December 1, 2026.
# https://docs.leonardo.ai/docs/migrate-from-the-removebg-api-to-leonardoai
async def remove_bg(image):
    headers = {
        "Authorization": f"Bearer {Config.LEONARDO_API_KEY}",
    }
    payload = {
        "model": "remove-bg",
        "ephemeral": True,
        "parameters": {
            "format": "png",
            "guidances": {"image_reference": [{"image": image}]},
        },
    }
    async with httpx.AsyncClient(follow_redirects=True, timeout=60) as client:
        response = await client.post(
            "https://cloud.leonardo.ai/api/rest/v2/generationssync",
            headers=headers,
            json=payload,
        )
        try:
            data = response.json()
        except ValueError:
            data = None
        results = data.get("results") if isinstance(data, dict) else None
        if not results or not results[0].get("url"):
            # Errors are JSON (often with HTTP 200), the caller shows the body.
            return response
        result = await client.get(results[0]["url"])
        if result.status_code != 200:
            return result
        content_type = results[0].get("contentType") or "image/png"
        return httpx.Response(200, headers={"content-type": content_type}, content=result.content)


# this method will call the API, and return in the appropriate format
# with the name provided.
async def ReTrieveFile(input_file_name):
    async with aiofiles.open(input_file_name, "rb") as image:
        data = base64.b64encode(await image.read()).decode()
    return await remove_bg({"type": "BASE64", "data": data})


async def ReTrieveURL(input_url):
    return await remove_bg({"type": "URL", "url": input_url})


@catub.cat_cmd(
    pattern=r"(rmbg|srmbg)(?:\s|$)([\s\S]*)",
    command=("rmbg", plugin_category),
    info={
        "header": "To remove background of a image/sticker/image link.",
        "options": {
            "rmbg": "to get output as png format",
            "srmbg": "To get output as webp format(sticker).",
        },
        "usage": [
            "{tr}rmbg",
            "{tr}srmbg",
            "{tr}rmbg image link",
            "{tr}srmbg image link",
        ],
    },
)
async def remove_background(event):
    "To remove background of a image."
    if Config.LEONARDO_API_KEY is None:
        return await edit_delete(
            event,
            "`You have to set LEONARDO_API_KEY in Config vars with an API key from Leonardo.Ai to use this plugin. remove.bg moved its API there, so old REM_BG_API_KEY keys won't work.`",
            10,
        )
    cmd = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    message_id = await reply_id(event)
    if event.reply_to_msg_id and not input_str:
        reply_message = await event.get_reply_message()
        catevent = await edit_or_reply(event, "`Analysing this Media...`")
        file_name = await Convert.to_image(event, reply_message, dirct="./temp", file="rmbgimage.png", noedits=True)
        if not file_name[1]:
            return await edit_delete(event, "**Error:** __Unable to process with this media__")
        response = await ReTrieveFile(file_name[1])
        os.remove(file_name[1])
    elif input_str:
        catevent = await edit_or_reply(event, "`Removing Background of this media`")
        response = await ReTrieveURL(input_str)
    else:
        return await edit_delete(
            event,
            "__Reply to any media file with rmbg/srmbg to get background less png file or webp format or provide image link along with command__",
        )
    contentType = response.headers.get("content-type")
    remove_bg_image = "./temp/backgroundless.png"
    if "image" not in contentType:
        return await edit_delete(catevent, f"`{response.content.decode('UTF-8')}`", 5)
    async with aiofiles.open("./temp/backgroundless.png", "wb") as file:
        await file.write(response.content)
    await catevent.delete()
    if cmd == "srmbg":
        file = (await Convert.to_sticker(catevent, remove_bg_image, file="rmbgsticker.webp", noedits=True))[1]
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
    if os.path.exists(file):
        os.remove(file)

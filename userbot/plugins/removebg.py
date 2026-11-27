# Special credits: @spechide (ported from uniborg)

import base64
from html import escape
import os

import aiofiles
import httpx

from userbot import Convert, catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

plugin_category = "utils"


def is_https_url(value):
    if not isinstance(value, str):
        return False
    try:
        url = httpx.URL(value)
    except httpx.InvalidURL:
        return False
    return url.scheme == "https" and bool(url.host)


# remove.bg's self-service API migrates to Leonardo on December 1, 2026.
# https://docs.leonardo.ai/docs/migrate-from-the-removebg-api-to-leonardoai
async def remove_bg(image):
    headers = {
        "Authorization": f"Bearer {Config.LEONARDO_API_KEY}",
    }
    payload = {
        "model": "remove-bg",
        "ephemeral": True,
        "parameters": {
            "size": "auto",
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
        if response.status_code != 200:
            return response
        try:
            data = response.json()
        except ValueError as error:
            raise ValueError("Leonardo returned an invalid JSON response.") from error
        if not isinstance(data, dict):
            raise ValueError("Leonardo returned an invalid JSON response.")
        if errors := data.get("errors"):
            message = errors[0].get("message") if isinstance(errors, list) and isinstance(errors[0], dict) else None
            raise ValueError(message if isinstance(message, str) else "Leonardo could not remove the background.")
        results = data.get("results")
        if not isinstance(results, list) or not results or not isinstance(results[0], dict):
            raise ValueError("Leonardo returned no background removal image.")
        if not is_https_url(results[0].get("url")):
            raise ValueError("Leonardo returned no valid HTTPS image download URL.")
        result = await client.get(results[0]["url"])
        if result.status_code != 200:
            return result
        # Storage errors can arrive with HTTP 200; check the requested PNG format.
        if not result.content.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Leonardo returned an invalid PNG image.")
        return httpx.Response(200, headers={"content-type": "image/png"}, content=result.content)


# this method will call the API, and return in the appropriate format
# with the name provided.
async def ReTrieveFile(input_file_name):
    async with aiofiles.open(input_file_name, "rb") as image:
        data = base64.b64encode(await image.read()).decode()
    return await remove_bg({"type": "BASE64", "data": data})


async def ReTrieveURL(input_url):
    input_url = input_url.strip()
    if not is_https_url(input_url):
        raise ValueError("Provide an HTTPS image URL for Leonardo background removal.")
    return await remove_bg({"type": "URL", "url": input_url})


async def show_error(event, message):
    # Bound escaped provider text to fit a Telegram message.
    return await edit_delete(event, f"<b>Error:</b> {escape(str(message)[:600])}", 5, parse_mode="html")


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
    if not (Config.LEONARDO_API_KEY or "").strip():
        return await edit_delete(
            event,
            "`Set LEONARDO_API_KEY in Config vars with a new API key from https://app.leonardo.ai/api-access. Old remove.bg REM_BG_API_KEY keys cannot be used with Leonardo.`",
            10,
        )
    cmd = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2).strip()
    message_id = await reply_id(event)
    try:
        if event.reply_to_msg_id and not input_str:
            reply_message = await event.get_reply_message()
            catevent = await edit_or_reply(event, "`Analysing this Media...`")
            file_name = await Convert.to_image(event, reply_message, dirct="./temp", file="rmbgimage.png", noedits=True)
            if not file_name[1]:
                return await edit_delete(catevent, "**Error:** __Unable to process with this media__")
            try:
                response = await ReTrieveFile(file_name[1])
            finally:
                os.remove(file_name[1])
        elif input_str:
            catevent = await edit_or_reply(event, "`Removing Background of this media`")
            response = await ReTrieveURL(input_str)
        else:
            return await edit_delete(
                event,
                "__Reply to any media file with rmbg/srmbg to get background less png file or webp format or provide image link along with command__",
            )
    except httpx.RequestError:
        return await show_error(catevent, "Could not reach Leonardo or download the result. Please try again later.")
    except ValueError as error:
        return await show_error(catevent, error)
    content_type = response.headers.get("content-type", "").lower()
    remove_bg_image = "./temp/backgroundless.png"
    if response.status_code != 200 or not content_type.startswith("image/"):
        return await show_error(catevent, f"HTTP {response.status_code}: {response.text or 'No image returned.'}")
    os.makedirs("./temp", exist_ok=True)
    async with aiofiles.open(remove_bg_image, "wb") as file:
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

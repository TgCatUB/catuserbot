import os

import requests

from userbot import catub

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers import media_type

plugin_category = "utils"


async def ocr_space_file(
    filename, overlay=False, api_key=Config.OCR_SPACE_API_KEY, language="eng"
):
    """OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {
        "isOverlayRequired": overlay,
        "apikey": api_key,
        "language": language,
    }
    with open(filename, "rb") as f:
        r = requests.post(
            "https://api.ocr.space/parse/image",
            files={filename: f},
            data=payload,
        )
    return r.json()


@catub.cat_cmd(
    pattern="ocr(?:\s|$)([\s\S]*)",
    command=("ocr", plugin_category),
    info={
        "header": "To read text in image and print it.",
        "description": "Reply to an image or sticker to extract text from it.\n\nGet language codes from [here](https://ocr.space/ocrapi).",
        "usage": "{tr}ocr <language code>",
        "examples": "{tr}ocr eng",
    },
)
async def ocr(event):
    "To read text in image."
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if mediatype is None or mediatype not in ["Photo", "Document"]:
        return await edit_delete(event, "__Reply to image to read text on it__")
    catevent = await edit_or_reply(event, "`Reading...`")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await event.client.download_media(reply, Config.TEMP_DIR)
    test_file = await ocr_space_file(filename=downloaded_file_name, language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await catevent.edit("`Couldn't read it.`\n`I guess I need new glasses.`")
    else:
        await catevent.edit(f"**Here's what I could read from it:**\n\n`{ParsedText}`")
    os.remove(downloaded_file_name)

import os

import requests
from googletrans import LANGUAGES

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import getTranslate
from ..sql_helper.globals import gvarstatus
from . import Convert, catub, soft_deEmojify

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
    pattern="(|t)ocr(?:\s|$)([\s\S]*)",
    command=("ocr", plugin_category),
    info={
        "header": "To read text in image/gif/sticker/video and print it.",
        "description": "Reply to an image or sticker to extract text from it.\n\nGet language codes from [here](https://ocr.space/ocrapi).",
        "usage": "{tr}ocr <language code>",
        "examples": "{tr}ocr eng",
    },
)
async def ocr(event):
    "To read text in media."
    reply = await event.get_reply_message()
    if not event.reply_to_msg_id or not reply.media:
        return await edit_delete(event, "__Reply to a media to read text on it__")
    catevent = await edit_or_reply(event, "`Reading...`")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    cmd = event.pattern_match.group(1)
    lang_code = event.pattern_match.group(2)
    output_file = await Convert.to_image(
        event, reply, dirct="./temp", file="image.png", rgb=True, noedits=True
    )
    if not output_file[1]:
        return await catevent.edit(
            "`Couldn't find image. Are you sure you replied to image?`"
        )
    test_file = await ocr_space_file(filename=output_file[1], language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await catevent.edit("`Couldn't read it.`\n`I guess I need new glasses.`")
    else:
        if cmd == "":
            await catevent.edit(
                f"**Here's what I could read from it:**\n\n`{ParsedText}`"
            )
        if cmd == "t":
            TRT_LANG = gvarstatus("TOCR_LANG") or "en"
            try:
                reply_text = await getTranslate(
                    soft_deEmojify(ParsedText), dest=TRT_LANG
                )
            except ValueError:
                return await edit_delete(
                    trans, "`Invalid destination language.`", time=5
                )
            source_lan = LANGUAGES[f"{reply_text.src.lower()}"]
            transl_lan = LANGUAGES[f"{reply_text.dest.lower()}"]
            tran_text = f"📜**Translate :-\nFrom {source_lan.title()}({reply_text.src.lower()}) to {transl_lan.title()}({reply_text.dest.lower()}) :**\n\n`{reply_text.text}`"
            await catevent.edit(
                f"🧧**Here's what I could read from it:**\n\n`{ParsedText}`\n\n{tran_text}"
            )
    if os.path.exists(output_file[1]):
        os.remove(output_file[1])


@catub.cat_cmd(
    pattern="tocr",
    command=("tocr", plugin_category),
    info={
        "header": "To read text in image/gif/sticker/video and print it with its translation.",
        "description": "Reply to an image/gif/sticker/video to extract text from it and print it with its translation.\n\nGet language codes from [here](https://ocr.space/ocrapi).",
        "note": "for this command transalted language set lanuage by `.lang tocr` command.",
        "usage": "{tr}tocr <language code>",
        "examples": "{tr}tocr eng",
    },
)
async def ocr(event):
    "To read text in media & paste with translated."

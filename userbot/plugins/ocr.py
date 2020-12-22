# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.


import os

import requests

OCR_SPACE_API_KEY = Config.OCR_SPACE_API_KEY


async def ocr_space_file(
    filename, overlay=False, api_key=OCR_SPACE_API_KEY, language="eng"
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


@bot.on(admin_cmd(pattern="ocr(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="ocr(?: |$)(.*)", allow_sudo=True))
async def ocr(event):
    catevent = await edit_or_reply(event, "`Reading...`")
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    lang_code = event.pattern_match.group(1)
    downloaded_file_name = await bot.download_media(
        await event.get_reply_message(), Config.TEMP_DIR
    )
    test_file = await ocr_space_file(filename=downloaded_file_name, language=lang_code)
    try:
        ParsedText = test_file["ParsedResults"][0]["ParsedText"]
    except BaseException:
        await catevent.edit("`Couldn't read it.`\n`I guess I need new glasses.`")
    else:
        await catevent.edit(f"`Here's what I could read from it:`\n\n{ParsedText}")
    os.remove(downloaded_file_name)


CMD_HELP.update(
    {
        "ocr": "**Plugin : **`ocr`\
        \n\n**Syntax : **`.ocr <language>`\
        \n**Function : **Reply to an image or sticker to extract text from it.\n\nGet language codes from [here](https://ocr.space/ocrapi)"
    }
)

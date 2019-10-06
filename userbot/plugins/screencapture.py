"""Take screenshot of any website
Syntax: .screencapture <Website URL>"""

import io
import requests
from telethon import events
from userbot.utils import admin_cmd


@borg.on(admin_cmd("screencapture (.*)"))
async def _(event):
    if event.fwd_from:
        return
    if Config.SCREEN_SHOT_LAYER_ACCESS_KEY is None:
        await event.edit("Need to get an API key from https://screenshotlayer.com/product \nModule stopping!")
        return
    await event.edit("Processing ...")
    sample_url = "https://api.screenshotlayer.com/api/capture?access_key={}&url={}&fullpage={}&viewport={}&format={}&force={}"
    input_str = event.pattern_match.group(1)
    response_api = requests.get(sample_url.format(
        Config.SCREEN_SHOT_LAYER_ACCESS_KEY,
        input_str,
        "1",
        "2560x1440",
        "PNG",
        "1"
    ))
    # https://stackoverflow.com/a/23718458/4723940
    contentType = response_api.headers['content-type']
    if "image" in contentType:
        with io.BytesIO(response_api.content) as screenshot_image:
            screenshot_image.name = "screencapture.png"
            try:
                await borg.send_file(
                    event.chat_id,
                    screenshot_image,
                    caption=input_str,
                    force_document=True,
                    reply_to=event.message.reply_to_msg_id
                )
                await event.delete()
            except Exception as e:
                await event.edit(str(e))
    else:
        await event.edit(response_api.text)

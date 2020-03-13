""" It does not do to dwell on dreams and forget to live
Syntax: .getime"""

import asyncio
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from uniborg.util import admin_cmd


FONT_FILE_TO_USE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


@borg.on(admin_cmd(pattern="getime ?(.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    current_time = datetime.now().strftime("%H : %M : %S")
    start = datetime.now()
    input_str = event.pattern_match.group(1)
    reply_msg_id = event.message.id
    if input_str:
        current_time = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        reply_msg_id = previous_message.id
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    # pylint:disable=E0602
    required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + " " + str(datetime.now()) + ".webp"
    img = Image.new("RGB", (250, 50), color=(0, 0, 0))
    fnt = ImageFont.truetype(FONT_FILE_TO_USE, 30)
    drawn_text = ImageDraw.Draw(img)
    drawn_text.text((10, 10), current_time, font=fnt, fill=(255, 255, 255))
    img.save(required_file_name)
    await borg.send_file(  # pylint:disable=E0602
        event.chat_id,
        required_file_name,
        caption="Time: Powered by @UniBorg",
        # Courtesy: @ManueI15
        reply_to=reply_msg_id
    )
    os.remove(required_file_name)
    end = datetime.now()
    time_taken_ms = (end - start).seconds
    await event.edit("Created sticker in {} seconds".format(time_taken_ms))
    await asyncio.sleep(5)
    await event.delete()


@borg.on(admin_cmd(pattern="time (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    logger.info(input_str)  # pylint:disable=E0602

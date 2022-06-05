"""
designed By @Krishna_Singhal in userge
ported to telethon by @mrconfused and @sandy1709
"""

import os

from glitch_this import ImageGlitcher
from PIL import Image

from userbot import Convert, catub

from ..core.managers import edit_delete
from ..helpers import reply_id, unsavegif

plugin_category = "fun"


@catub.cat_cmd(
    pattern="glitch(s)?(?: |$)([1-8])?",
    command=("glitch", plugin_category),
    info={
        "header": "Glitches the given Image.",
        "description": "Glitches the given mediafile (gif , stickers , image, videos) to a sticker/image and glitch range is from 1 to 8.\
                    If nothing is mentioned then by default it is 2",
        "options": {
            "glitch": "To output result as gif.",
            "glitchs": "To output result as sticker.",
        },
        "usage": ["{tr}glitch <1-8>", "{tr}glitch", "{tr}glitchs", "{tr}glitchs <1-8>"],
    },
)
async def glitch(event):
    "Glitches the given Image."
    cmd = event.pattern_match.group(1)
    catinput = event.pattern_match.group(2)
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(event, "`Reply to supported Media...`")
    catid = await reply_id(event)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    catinput = int(catinput) if catinput else 2
    glitch_file = await Convert.to_image(
        event,
        reply,
        dirct="./temp",
        file="glitch.png",
    )
    if glitch_file[1] is None:
        return await edit_delete(
            glitch_file[0], "__Unable to extract image from the replied message.__"
        )
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file[1])
    if cmd:
        glitched = os.path.join("./temp", "glitched.webp")
        glitch_img = glitcher.glitch_image(img, catinput, color_offset=True)
        glitch_img.save(glitched)
        await event.client.send_file(event.chat_id, glitched, reply_to=catid)
    else:
        glitched = os.path.join("./temp", "glitched.gif")
        glitch_img = glitcher.glitch_image(img, catinput, color_offset=True, gif=True)
        DURATION = 200
        LOOP = 0
        glitch_img[0].save(
            glitched,
            format="GIF",
            append_images=glitch_img[1:],
            save_all=True,
            duration=DURATION,
            loop=LOOP,
        )
        sandy = await event.client.send_file(event.chat_id, glitched, reply_to=catid)
        await unsavegif(event, sandy)
    await glitch_file[0].delete()
    for files in (glitch_file[1], glitched):
        if files and os.path.exists(files):
            os.remove(files)

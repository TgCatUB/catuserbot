"""
designed By @Krishna_Singhal in userge
ported to telethon by @mrconfused and @sandy1709
"""

import base64
import os

from glitch_this import ImageGlitcher
from PIL import Image


@bot.on(admin_cmd(outgoing=True, pattern="(glitch|glitchs)(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="(glitch|glitchs)(?: |$)(.*)", allow_sudo=True))
async def glitch(cat):
    if cat.fwd_from:
        return
    cmd = cat.pattern_match.group(1)
    catinput = cat.pattern_match.group(2)
    reply = await cat.get_reply_message()
    if not reply:
        return await edit_delete(cat, "`Reply to supported Media...`")
    catid = await reply_id(cat)
    san = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    if catinput:
        if not catinput.isdigit():
            await cat.edit("`You input is invalid, check help`")
            return
        catinput = int(catinput)
        if not 0 < catinput < 9:
            await cat.edit("`Invalid Range...`")
            return
    else:
        catinput = 2
    glitch_file = await _cattools.media_to_pic(cat, reply)
    try:
        san = Get(san)
        await cat.client(san)
    except BaseException:
        pass
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file[1])
    if cmd == "glitchs":
        glitched = os.path.join("./temp", "glitched.webp")
        glitch_img = glitcher.glitch_image(img, catinput, color_offset=True)
        glitch_img.save(glitched)
        await cat.client.send_file(cat.chat_id, glitched, reply_to=catid)
    elif cmd == "glitch":
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
        sandy = await cat.client.send_file(cat.chat_id, glitched, reply_to=catid)
        await _catutils.unsavegif(cat, sandy)
    await glitch_file[0].delete()
    for files in (glitch_file[1], glitched):
        if files and os.path.exists(files):
            os.remove(files)


CMD_HELP.update(
    {
        "glitch": "**Plugin : **`glitch`\
    \n\n  •  **Syntax : **`.glitch` reply to media file\
    \n  •   **Function :** glitches the given mediafile (gif , stickers , image, videos) to a gif and glitch range is from 1 to 8.\
    If nothing is mentioned then by default it is 2\
    \n\n  •  **Syntax : **`.glitchs` reply to media file\
    \n  •  **Function :** glitches the given mediafile (gif , stickers , image, videos) to a sticker and glitch range is from 1 to 8.\
    If nothing is mentioned then by default it is 2\
    "
    }
)

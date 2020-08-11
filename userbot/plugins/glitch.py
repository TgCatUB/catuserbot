"""
designed By @Krishna_Singhal in userge
ported to telethon by @mrconfused and @sandy1709
"""

import os
from PIL import Image
from ..utils import admin_cmd 
from .. import LOGS , CMD_HELP
from glitch_this import ImageGlitcher
from . import take_screen_shot ,runcmd

@borg.on(admin_cmd(outgoing=True, pattern="(glitch|glitchs)(?: |$)(.*)"))
async def glitch(cat):
    await cat.edit("```Glitching... 😁```")
    cmd = cat.pattern_match.group(1)
    catinput = cat.pattern_match.group(2)
    reply = await cat.get_reply_message()
    if not (reply and (reply.media)):
        await cat.edit("`Media not found...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    catid = cat.reply_to_msg_id
    catsticker = await reply.download_media(file = "./temp/")
    if not catsticker.endswith(('.mp4','.webp','.tgs','.png','.jpg')):
        os.remove(catsticker)
        await cat.edit("`Media not found...`")
        return
    file = os.path.join("./temp/", "glitch.png")
    if catinput:
        if not catinput.isdigit():
            await cat.edit("`You input is invalid, check help`")
            return
        catinput = int(catinput)
        if not 0 < catinput< 9:
            await cat.edit("`Invalid Range...`")
            return
    else:
        catinput = 2
    if catsticker.endswith(".tgs"):
        catfile = os.path.join("./temp/", "glitch.png")
        catcmd = f"lottie_convert.py --frame 0 -if lottie -of png {catsticker} {catfile}"
        stdout, stderr = (await runcmd(catcmd))[:2]
        if not os.path.lexists(catfile):
            await cat.edit("`catsticker not found...`")
            LOGS.info(stdout + stderr)
        glitch_file = catfile
    elif catsticker.endswith(".webp"):
        catfile = os.path.join("./temp/", "glitch.png")
        os.rename(catsticker , catfile)
        if not os.path.lexists(catfile):
            await cat.edit("`catsticker not found... `")
            return
        glitch_file = catfile
    elif catsticker.endswith(".mp4"):
        catfile = os.path.join("./temp/", "glitch.png")
        await take_screen_shot(catsticker , 0, catfile)
        if not os.path.lexists(catfile):
            await cat.edit("```catsticker not found...```")
            return
        glitch_file = catfile
    else:
        glitch_file = catsticker
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file)
    if cmd == "glitchs":
        glitched = "./temp/" + "glitched.webp"
        glitch_img = glitcher.glitch_image(img, catinput, color_offset=True)
        glitch_img.save(glitched)
        await borg.send_file(
            cat.chat_id,
            glitched,
            reply_to_message_id= catid)
        os.remove(glitched)
        await cat.delete()
    elif cmd == "glitch":
        Glitched = "./temp/" + "glitch.gif"
        glitch_img = glitcher.glitch_image(img, catinput, color_offset=True, gif=True)
        DURATION = 200
        LOOP = 0
        glitch_img[0].save(
            Glitched,
            format='GIF',
            append_images=glitch_img[1:],
            save_all=True,
            duration=DURATION,
            loop=LOOP)
        await borg.send_file(
            cat.chat_id,
            Glitched,
            reply_to_message_id=catid)
        os.remove(Glitched)
        await cat.delete()
    for files in (catsticker, glitch_file):
        if files and os.path.exists(files):
            os.remove(files)

CMD_HELP.update({
    "glitch":
    "**SYNTAX : **`.glitch` reply to media file\
    \n**USAGE :** glitches the given mediafile(gif , stickers , image, videos) to a gif and glitch range is from 1 to 8.\
    If nothing is mentioned then by default it is 2\
    \n\n**SYNTAX : **`.glitchs` reply to media file\
    \n**USAGE :** glitches the given mediafile(gif , stickers , image, videos) to a sticker and glitch range is from 1 to 8.\
    If nothing is mentioned then by default it is 2\
    "
})

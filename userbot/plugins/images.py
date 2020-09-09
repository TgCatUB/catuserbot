"""
Download & Upload Images on Telegram\n
Syntax: `.img <Name>` or `.img (replied message)`
\n Upgraded and Google Image Error Fixed by @NeoMatrix90 aka @kirito6969
from oub
"""
import os
import shutil

from .. import CMD_HELP
from ..helpers.google_image_download import googleimagesdownload
from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(admin_cmd(pattern=r"img(?: |$)(\d*)? ?(.*)"))
@borg.on(sudo_cmd(pattern=r"img(?: |$)(\d*)? ?(.*)", allow_sudo=True))
async def img_sampler(event):
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    if event.is_reply and not event.pattern_match.group(2):
        query = await event.get_reply_message()
        query = str(query.message)
    else:
        query = str(event.pattern_match.group(2))
    if not query:
        return await edit_or_reply(
            event, "Reply to a message or pass a query to search!"
        )
    cat = await edit_or_reply(event, "`Processing...`")
    if event.pattern_match.group(1) != "":
        lim = int(event.pattern_match.group(1))
        if lim > 10:
            lim = int(10)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(3)
    response = googleimagesdownload()
    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory",
    }
    # passing the arguments to the function
    try:
        paths = response.download(arguments)
    except Exception as e:
        return await cat.edit(f"Error: \n`{e}`")
    lst = paths[0][query]
    await bot.send_file(
        await bot.get_input_entity(event.chat_id), lst, reply_to=reply_to_id
    )
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await cat.delete()


CMD_HELP.update(
    {
        "images": "**Plugin :**`images`\
\n\n**Syntax :** `.img <limit> <Name>` or `.img <limit> (replied message)`\
    \n**Usage : **do google image search and sends 3 images. default if you havent mentioned limit"
    }
)

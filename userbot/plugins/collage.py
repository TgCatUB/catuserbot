# collage plugin for catuserbot by @sandy1709

# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.import os

import os

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import _catutils, reply_id
from . import make_gif

plugin_category = "utils"


@catub.cat_cmd(
    pattern="collage(?:\s|$)([\s\S]*)",
    command=("collage", plugin_category),
    info={
        "header": "To create collage from still images extracted from video/gif.",
        "description": "Shows you the grid image of images extracted from video/gif. you can customize the Grid size by giving integer between 1 to 9 to cmd by default it is 3",
        "usage": "{tr}collage <1-9>",
    },
)
async def collage(event):
    "To create collage from still images extracted from video/gif."
    catinput = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    catid = await reply_id(event)
    event = await edit_or_reply(
        event, "```collaging this may take several minutes too..... 😁```"
    )
    if not (reply and (reply.media)):
        await event.edit("`Media not found...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith((".mp4", ".mkv", ".tgs")):
        os.remove(catsticker)
        await event.edit("`Media format is not supported...`")
        return
    if catinput:
        if not catinput.isdigit():
            os.remove(catsticker)
            await event.edit("`You input is invalid, check help`")
            return
        catinput = int(catinput)
        if not 0 < catinput < 10:
            os.remove(catsticker)
            await event.edit(
                "`Why too big grid you cant see images, use size of grid between 1 to 9`"
            )
            return
    else:
        catinput = 3
    if catsticker.endswith(".tgs"):
        hmm = await make_gif(event, catsticker)
        if hmm.endswith(("@tgstogifbot")):
            os.remove(catsticker)
            return await event.edit(hmm)
        collagefile = hmm
    else:
        collagefile = catsticker
    endfile = "./temp/collage.png"
    catcmd = f"vcsi -g {catinput}x{catinput} '{collagefile}' -o {endfile}"
    stdout, stderr = (await _catutils.runcmd(catcmd))[:2]
    if not os.path.exists(endfile):
        for files in (catsticker, collagefile):
            if files and os.path.exists(files):
                os.remove(files)
        return await edit_delete(
            event, "`media is not supported or try with smaller grid size`", 5
        )

    await event.client.send_file(
        event.chat_id,
        endfile,
        reply_to=catid,
    )
    await event.delete()
    for files in (catsticker, collagefile, endfile):
        if files and os.path.exists(files):
            os.remove(files)

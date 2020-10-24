# collage plugin for catuserbot by @sandy1709

# Copyright (C) 2020 Alfiananda P.A
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.

import os

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP, make_gif, runcmd


@bot.on(admin_cmd(pattern="collage(?: |$)(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="collage(?: |$)(.*)", allow_sudo=True))
async def collage(cat):
    catinput = cat.pattern_match.group(1)
    reply = await cat.get_reply_message()
    catid = cat.reply_to_msg_id
    cat = await edit_or_reply(
        cat, "```collaging this may take several minutes too..... 😁```"
    )
    if not (reply and (reply.media)):
        await cat.edit("`Media not found...`")
        return
    if not os.path.isdir("./temp/"):
        os.mkdir("./temp/")
    catsticker = await reply.download_media(file="./temp/")
    if not catsticker.endswith((".mp4", ".mkv", ".tgs")):
        os.remove(catsticker)
        await cat.edit("`Media format is not supported...`")
        return
    if catinput:
        if not catinput.isdigit():
            os.remove(catsticker)
            await cat.edit("`You input is invalid, check help`")
            return
        catinput = int(catinput)
        if not 0 < catinput < 10:
            os.remove(catsticker)
            await cat.edit(
                "`Why too big grid you cant see images, use size of grid between 1 to 9`"
            )
            return
    else:
        catinput = 3
    if catsticker.endswith(".tgs"):
        hmm = await make_gif(cat, catsticker)
        if hmm.endswith(("@tgstogifbot")):
            os.remove(catsticker)
            return await cat.edit(hmm)
        collagefile = hmm
    else:
        collagefile = catsticker
    endfile = "./temp/collage.png"
    catcmd = f"vcsi -g {catinput}x{catinput} {collagefile} -o {endfile}"
    stdout, stderr = (await runcmd(catcmd))[:2]
    if not os.path.exists(endfile):
        for files in (catsticker, collagefile):
            if files and os.path.exists(files):
                os.remove(files)
        return await edit_delete(
            cat, f"`media is not supported or try with smaller grid size`", 5
        )
    await cat.client.send_file(
        cat.chat_id,
        endfile,
        reply_to=catid,
    )
    await cat.delete()
    for files in (catsticker, collagefile, endfile):
        if files and os.path.exists(files):
            os.remove(files)


CMD_HELP.update(
    {
        "collage": "**Plugin : **`collage`\
        \n\n**Syntax : **`.collage <grid size>`\
        \n**Function : **__Shows you the grid image of images extracted from video \n Grid size must be between 1 to 9 by default it is 3__"
    }
)

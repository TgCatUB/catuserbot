# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.info(?: |$)(.*)")
async def info(event):
    """ For .info command,"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Please specify a valid plugin name.")
    else:
        await event.edit("Please specify which plugin do you want help for !!\
            \nUsage: .info <plugin name>")
        string = ""
        for i in CMD_HELP:
            string += "`" + str(i)
            string += "`\n"
        await event.reply(string)

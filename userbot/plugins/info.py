from userbot import CMD_HELP
from userbot.utils import admin_cmd

@borg.on(admin_cmd(outgoing=True, pattern="info(?: |$)(.*)"))
async def info(event):
    """ For .info command,"""
    args = event.pattern_match.group(1).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Please specify a valid plugin name.")
    else:
        string = "**Please specify which plugin do you want help for !!**\
            \n**Usage:** `.info` <plugin name>\n\n"
        for i in sorted(CMD_HELP):
            string += "◆`" + str(i)
            string += "`   "
        await event.edit(string)
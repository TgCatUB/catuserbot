from userbot import CMD_LIST, SUDO_LIST
from userbot import ALIVE_NAME
from userbot.utils import admin_cmd, sudo_cmd
from platform import uname
import sys
from telethon import events, functions, __version__

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"

@borg.on(admin_cmd(pattern="help ?(.*)"))
async def cmd_list(event):
        tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
        input_str = event.pattern_match.group(1)
        if tgbotusername is None or input_str == "text":
            string = ""
            for i in CMD_LIST:
                string += "⚚" + i + "\n"
                for iter_list in CMD_LIST[i]:
                    string += "    `" + str(iter_list) + "`"
                    string += "\n"
                string += "\n"
            if len(string) > 4095:
                await borg.send_message(event.chat_id, "Do .help cmd")
                await asyncio.sleep(5)
            else:
                await event.edit(string)
        elif input_str:
            if input_str in CMD_LIST:
                string = "Commands found in {}:\n".format(input_str)
                for i in CMD_LIST[input_str]:
                    string += "    " + i
                    string += "\n"
                await event.edit(string)
            else:
                await event.edit(input_str + " is not a valid plugin!")
        else:
            help_string = f"""Userbot Helper.. Provided by {DEFAULTUSER} \n
Userbot Helper to reveal all the commands\n__Do `.help` plugin_name for commands, in case popup doesn't appear.__\nDo `.info` plugin_name for usage"""
            results = await bot.inline_query(  # pylint:disable=E0602
                tgbotusername,
                help_string
            )
            await results[0].click(
                event.chat_id,
                reply_to=event.reply_to_msg_id,
                hide_via=True
            )
            await event.delete()

@borg.on(admin_cmd(pattern="dc"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetNearestDcRequest())  # pylint:disable=E0602
    await event.edit(result.stringify())



@borg.on(sudo_cmd(allow_sudo=True, pattern="help(?: |$)(.*)"))
async def info(event):
    if event.fwd_from:
        return
    """ For .info command,"""
    args = event.pattern_match.group(1).lower()
    input_str = event.pattern_match.group(1)
    if args:
        if args in SUDO_LIST:
            if input_str in SUDO_LIST:
                string = "Commands found in {}:\n".format(input_str)
                for i in SUDO_LIST[input_str]:
                    string += "    " + i
                    string += "\n"
                await event.reply(string)
        else:
                await event.reply(args + " is not a valid plugin!")
    else:
        await event.reply("Please specify which plugin do you want help for !!\
            \nUsage: .help <plugin name>")
        string = ""
        for i in SUDO_LIST:
            string += "`" + str(i)
            string += "`\n"
        await event.reply(string)

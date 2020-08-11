from userbot import CMD_LIST, SUDO_LIST
from userbot import ALIVE_NAME
from userbot.utils import admin_cmd, sudo_cmd
from platform import uname
import sys
import requests
from telethon import events, functions, __version__

DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"

@borg.on(admin_cmd(pattern="help ?(.*)"))
async def cmd_list(event):
    input_str = event.pattern_match.group(1)
    tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
    if input_str == "text":
        string = ""
        for i in sorted(CMD_LIST):
            string += "⚚" + i + "\n"
            for iter_list in CMD_LIST[i]:
                string += "    " + str(iter_list)
                string += "\n"
            string += "\n"
        if len(string) > 4095:
            data = string
            key = requests.post('https://nekobin.com/api/documents', json={"content": data}).json().get('result').get('key')
            url = f'https://nekobin.com/{key}'
            reply_text = f'All commands of the catuserbot are [here]({url})'
            await event.edit(reply_text)
            return
        await event.edit(string)
        return
    if Config.HELP_INLINETYPE is None:
        if input_str:
            if input_str in CMD_LIST:
                string = "Commands found in {}:\n".format(input_str)
                for i in CMD_LIST[input_str]:
                    string += "    " + i
                    string += "\n"
                await event.edit(string)
            else:
                await event.edit(input_str + " is not a valid plugin!")
        else:
            help_string = f"Userbot Helper.. Provided by {DEFAULTUSER}\
                          \nUserbot Helper to reveal all the plugin names\
                          \n__Do__ `.help` __plugin_name for commands, in case popup doesn't appear.__\
                          \nDo `.info` plugin_name for usage"
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
    else:
        if input_str:
            if input_str in CMD_LIST:
                string = "Commands found in {}:\n".format(input_str)
                for i in CMD_LIST[input_str]:
                    string += "    " + i
                    string += "\n"
                await event.edit(string)
            else:
                await event.edit(input_str + " is not a valid plugin!")
        else:
            string = f"**Userbot Helper.. Provided by {DEFAULTUSER}\nUserbot Helper to reveal all the plugin names\n\n**Do `.help` plugin_name for commands\nDo `.info` plugin_name for usage\n\n"
            for i in sorted(CMD_LIST):
                string += "◆`" + str(i)
                string += "`   "
            await event.edit(string)            
        

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
        string = "**Please specify which plugin do you want help for !!**\
            \n**Usage:** `.info` <plugin name>\n\n"
        for i in sorted(SUDO_LIST):
            string += "◆`" + str(i)
            string += "`   "
        await event.reply(string)

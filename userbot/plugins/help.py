# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from telethon import functions

from userbot import catub

from ..Config import Config
from ..core import CMD_INFO, PLG_INFO
from ..core.cmdinfo import cmdinfo, cmdlist, grpinfo, plugininfo
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id

cmdprefix = Config.COMMAND_HAND_LER


plugin_category = "tools"


@catub.cat_cmd(
    pattern="help ?(-c|-p|-t)? ?([\s\S]*)?",
    command=("help", plugin_category),
    info={
        "header": "To get guide for catuserbot.",
        "description": "To get information or guide for the command or plugin",
        "note": "if command name and plugin name is same then you get guide for plugin. So by using this flag you get command guide",
        "flags": {
            "c": "To get info of command.",
            "p": "To get info of plugin.",
            "t": "To get all plugins in text format.",
        },
        "usage": [
            "{tr}help (plugin/command name)",
            "{tr}help -c (command name)",
        ],
        "examples": ["{tr}help help", "{tr}help -c help"],
    },
)
async def _(event):
    "To get guide for catuserbot."
    flag = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    if flag and flag == "-c" and input_str:
        outstr = await cmdinfo(input_str, event)
        if outstr is None:
            return
    elif input_str:
        outstr = await plugininfo(input_str, event, flag)
        if outstr is None:
            return
    elif flag == "-t":
        outstr = await grpinfo()
    else:
        results = await event.client.inline_query(Config.TG_BOT_USERNAME, "help")
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
        await event.delete()
        return
    await edit_or_reply(event, outstr)


@catub.cat_cmd(
    pattern="cmds(?:\s|$)([\s\S]*)",
    command=("cmds", plugin_category),
    info={
        "header": "To show list of cmds.",
        "description": "if no input is given then will show list of all commands.",
        "usage": [
            "{tr}cmds for all cmds",
            "{tr}cmds <plugin name> for paticular plugin",
        ],
    },
)
async def _(event):
    "To get list of commands."
    if input_str := event.pattern_match.group(1):
        try:
            cmds = PLG_INFO[input_str]
        except KeyError:
            return await edit_delete(event, "__Invalid plugin name recheck it.__")
        except Exception as e:
            return await edit_delete(event, f"**Error**\n`{e}`")
        outstr = f"• **{input_str.title()} has {len(cmds)} commands**\n"
        for cmd in cmds:
            outstr += f"  - `{cmdprefix}{cmd}`\n"
        outstr += f"**👩‍💻 Usage : ** `{cmdprefix}help -c <command name>`"
    else:
        outstr = await cmdlist()
    await edit_or_reply(
        event, outstr, aslink=True, linktext="Total Commands of Catuserbot are :"
    )


@catub.cat_cmd(
    pattern="s ([\s\S]*)",
    command=("s", plugin_category),
    info={
        "header": "To search commands.",
        "examples": "{tr}s song",
    },
)
async def _(event):
    "To search commands."
    cmd = event.pattern_match.group(1)
    if found := [i for i in sorted(list(CMD_INFO)) if cmd in i]:
        out_str = "".join(f"`{i}`    " for i in found)
        out = f"**I found {len(found)} command(s) for: **`{cmd}`\n\n{out_str}"
        out += f"\n\n__For more info check {cmdprefix}help -c <command>__"
    else:
        out = f"I can't find any such command `{cmd}` in CatUserbot"
    await edit_or_reply(event, out)


@catub.cat_cmd(
    pattern="dc$",
    command=("dc", plugin_category),
    info={
        "header": "To show dc of your account.",
        "description": "Dc of your account and list of dc's will be showed",
        "usage": "{tr}dc",
    },
)
async def _(event):
    "To get dc of your bot"
    result = await event.client(functions.help.GetNearestDcRequest())
    result = f"**Dc details of your account:**\
              \n**Country :** {result.country}\
              \n**Current Dc :** {result.this_dc}\
              \n**Nearest Dc :** {result.nearest_dc}\
              \n\n**List Of Telegram Data Centres:**\
              \n**DC1 : **Miami FL, USA\
              \n**DC2 :** Amsterdam, NL\
              \n**DC3 :** Miami FL, USA\
              \n**DC4 :** Amsterdam, NL\
              \n**DC5 : **Singapore, SG\
                "
    await edit_or_reply(event, result)

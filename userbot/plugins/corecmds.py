# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import contextlib
import os
from pathlib import Path

from ..Config import Config
from ..core import CMD_INFO, PLG_INFO
from ..helpers.google_tools import chromeDriver
from ..utils import load_module, remove_plugin
from . import CMD_HELP, CMD_LIST, SUDO_LIST, catub, edit_delete, edit_or_reply, reply_id

plugin_category = "tools"

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


def plug_checker(plugin):
    plug_path = f"./userbot/plugins/{plugin}.py"
    if not os.path.exists(plug_path):
        plug_path = f"./xtraplugins/{plugin}.py"
    if not os.path.exists(plug_path):
        plug_path = f"./badcatext/{plugin}.py"
    if not os.path.exists(plug_path):
        plug_path = f"./catvc/{plugin}.py"
    return plug_path


@catub.cat_cmd(
    pattern="install(?:\s|$)([\s\S]*)",
    command=("install", plugin_category),
    info={
        "header": "To install an external plugin.",
        "description": "Reply to any external plugin(supported by cat) to install it in your bot.",
        "usage": "{tr}install",
    },
)
async def install(event):
    "To install an external plugin."
    install_path = event.pattern_match.group(1) or "userbot/plugins"
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                f"{install_path}/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""), plugin_path=install_path)
                await edit_delete(
                    event,
                    f"Installed Plugin `{os.path.basename(downloaded_file_name)}`",
                    10,
                )
            else:
                os.remove(downloaded_file_name)
                await edit_delete(
                    event, "Errors! This plugin is already installed/pre-installed.", 10
                )
        except Exception as e:
            await edit_delete(event, f"**Error:**\n`{e}`", 10)
            os.remove(downloaded_file_name)


@catub.cat_cmd(
    pattern="load(?:\s|$)([\s\S]*)",
    command=("load", plugin_category),
    info={
        "header": "To load a plugin again. if you have unloaded it",
        "description": "To load a plugin again which you unloaded by {tr}unload",
        "usage": "{tr}load <plugin name>",
        "examples": "{tr}load markdown",
    },
)
async def load(event):
    "To load a plugin again. if you have unloaded it"
    shortname = event.pattern_match.group(1)
    try:
        with contextlib.suppress(BaseException):
            remove_plugin(shortname)
        load_module(shortname)
        await edit_delete(event, f"`Successfully loaded {shortname}`", 10)
    except Exception as e:
        await edit_or_reply(
            event, f"Could not load {shortname} because of the following error.\n{e}"
        )


@catub.cat_cmd(
    pattern="send(?:\s|$)([\s\S]*)",
    command=("send", plugin_category),
    info={
        "header": "To upload a plugin file to telegram chat",
        "usage": "{tr}send <plugin name>",
        "examples": "{tr}send markdown",
    },
)
async def send(event):
    "To uplaod a plugin file to telegram chat"
    reply_to_id = await reply_id(event)
    thumb = thumb_image_path if os.path.exists(thumb_image_path) else None
    input_str = event.pattern_match.group(1)
    the_plugin_file = plug_checker(input_str)
    if os.path.exists(the_plugin_file):
        await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            thumb=thumb,
            caption=f"**➥ Plugin Name:-** `{input_str}`",
        )
        await event.delete()
    else:
        await edit_or_reply(event, "404: File Not Found")


@catub.cat_cmd(
    pattern="unload(?:\s|$)([\s\S]*)",
    command=("unload", plugin_category),
    info={
        "header": "To unload a plugin temporarily.",
        "description": "You can load this unloaded plugin by restarting or using {tr}load cmd. Useful for cases like seting notes in rose bot({tr}unload markdown).",
        "usage": "{tr}unload <plugin name>",
        "examples": "{tr}unload markdown",
    },
)
async def unload(event):
    "To unload a plugin temporarily."
    shortname = event.pattern_match.group(1)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"Unloaded {shortname} successfully")
    except Exception as e:
        await edit_or_reply(event, f"Successfully unload {shortname}\n{e}")


@catub.cat_cmd(
    pattern="uninstall(?:\s|$)([\s\S]*)",
    command=("uninstall", plugin_category),
    info={
        "header": "To uninstall a plugin temporarily.",
        "description": "To stop functioning of that plugin and remove that plugin from bot.",
        "note": "To unload a plugin permanently from bot set NO_LOAD var in heroku with that plugin name, give space between plugin names if more than 1.",
        "usage": "{tr}uninstall <plugin name>",
        "examples": "{tr}uninstall markdown",
    },
)
async def unload(event):
    "To uninstall a plugin."
    shortname = event.pattern_match.group(1)
    path = plug_checker(shortname)
    if not os.path.exists(path):
        return await edit_delete(
            event, f"There is no plugin with path {path} to uninstall it"
        )
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"{shortname} is Uninstalled successfully")
    except Exception as e:
        await edit_or_reply(event, f"Successfully uninstalled {shortname}\n{e}")
    if shortname in PLG_INFO:
        for cmd in PLG_INFO[shortname]:
            CMD_INFO.pop(cmd)
        PLG_INFO.pop(shortname)


@catub.cat_cmd(
    pattern="logs(?:\s|$)([\s\S]*)",
    command=("logs", plugin_category),
    info={
        "header": "To send the log of catub",
        "description": "Send the log by paste or text file or rayso image. If no flag is used then it will paste last 100 lines of log.",
        "flags": {
            "f": "will fetch the whole log",
            "r": "Will send the log using ray.so",
            "t": "Will send the log as text file",
        },
        "usage": [
            "{tr}logs -{flag}",
            "{tr}logs -{flag}{flag}",
        ],
        "examples": [
            "{tr}logs",
            "{tr}logs -f",
            "{tr}logs -r",
            "{tr}logs -t",
            "{tr}logs -ft",
            "{tr}logs -fr",
        ],
    },
)
async def app_log(event):
    "To get log of the Catuserbot"
    flag = event.pattern_match.group(1)
    flag = [*flag]
    if flag and (flag[0] != "-" or any(i not in ["-", "f", "r", "t"] for i in flag)):
        return await edit_delete(event, "**Invalid flag...**")

    with open("catub.log", "r") as file:
        if "f" in flag:
            log = file.read()
            linktext = "**Full logs: **"
        else:
            lines = file.readlines()[-100:]
            log = "".join(lines)
            linktext = "**Recent 100 lines of logs: **"
    if "t" in flag:
        return await edit_or_reply(event, log, file_name="logs.text", caption=linktext)
    elif "r" in flag:
        outfile, error = chromeDriver.get_rayso(log, file_name="logs.png")
        if outfile:
            await catub.send_file(
                event.chat_id, outfile, caption=linktext, force_document=True
            )
            return os.remove(outfile)
    return await edit_or_reply(event, log, deflink=True, linktext=linktext)

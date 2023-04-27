# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import glob
import os
import re

from validators.url import url

from userbot import BOTLOG_CHATID, catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import config_helper as dBcof
from ..helpers.utils import _catutils

plugin_category = "tools"


# ============================@ Constants @===============================
config = "./config.py"
var_checker = [
    "APP_ID",
    "PM_LOGGER_GROUP_ID",
    "PRIVATE_CHANNEL_BOT_API_ID",
    "PRIVATE_GROUP_BOT_API_ID",
    "PLUGIN_CHANNEL",
]

default = [
    "./README.md",
    "./config.py",
    "./requirements.txt",
    "./CatTgbot.session",
    "./sample_config.py",
    "./stringsetup.py",
    "./exampleconfig.py",
]

cmds = [
    "rm -rf downloads",
    "mkdir downloads",
]
# ========================================================================


async def reload_codebase():
    with open(config, "r") as f:
        configs = f.read()
    BRANCH = "master"
    REPO = "https://github.com/TgCatUB/catuserbot"
    for match in re.finditer(
        r"(?:(UPSTREAM_REPO|UPSTREAM_REPO_BRANCH)(?:[ = \"\']+(.*[^\"\'\n])))",
        configs,
    ):
        BRANCH = match.group(2) if match.group(1) == "UPSTREAM_REPO_BRANCH" else BRANCH
        REPO = match.group(2) if match.group(1) == "UPSTREAM_REPO" else REPO
    if REPO:
        await _catutils.runcmd(f"git clone -b {BRANCH} {REPO} TempCat")
        file_list = os.listdir("TempCat")
        for file in file_list:
            await _catutils.runcmd(f"rm -rf {file}")
            await _catutils.runcmd(f"mv ./TempCat/{file} ./")
        await _catutils.runcmd("pip3 install --no-cache-dir -r requirements.txt")
        await _catutils.runcmd("rm -rf TempCat")
    if os.path.exists("catub.log"):
        os.remove("catub.log")
    if os.path.exists("badcatext"):
        await _catutils.runcmd("rm -rf badcatext")
    if os.path.exists("xtraplugins"):
        await _catutils.runcmd("rm -rf xtraplugins")
    if os.path.exists("catvc"):
        await _catutils.runcmd("rm -rf catvc")


@catub.cat_cmd(
    pattern="(set|get|del|info) var(?:\s|$)([\s\S]*)",
    command=("var", plugin_category),
    info={
        "header": "To manage config vars.",
        "flags": {
            "set": "To set new var in vps or modify the old var",
            "get": "To show the already existing var value.",
            "del": "To delete the existing value",
            "info": "To get info about current available vars",
        },
        "usage": [
            "{tr}set var <var name> <var value>",
            "{tr}get var <var name>",
            "{tr}del var <var name>",
            "{tr}info var",
        ],
        "examples": [
            "{tr}get var ALIVE_NAME",
        ],
    },
)
async def variable(event):
    "Manage most of ConfigVars setting, set new var, get current var, or delete var..."
    if not os.path.exists(config):
        return await edit_delete(
            event, "`There no Config file , You can't use this plugin.`"
        )
    cmd = event.pattern_match.group(1)
    if cmd == "info":
        return await edit_delete(event, dBcof.vars_info(), 60)
    value = None
    variable = event.pattern_match.group(2)
    if " " in variable:
        variable, value = variable.split(" ", 1)
    if not variable:
        return await edit_or_reply(event, "`What to do without Config Var??`")
    if variable in dBcof.var_list:
        cat = await edit_or_reply(event, "`Processing...`")
        data = await dBcof.setup_vars(event, cmd, variable, value)
        return await edit_delete(cat, data)
    string = ""
    match = None
    with open(config, "r") as f:
        configs = f.readlines()

    if cmd == "get":
        cat = await edit_or_reply(event, "`Getting information...`")
        for i in configs:
            if variable in i:
                _, val = i.split("= ")
                return await edit_or_reply(
                    cat, "**ConfigVars**:" f"\n\n`{variable}` = `{val}`"
                )
        await edit_or_reply(
            cat, "**ConfigVars**:" f"\n\n__Error:\n-> __`{variable}`__ doesn't exists__"
        )

    elif cmd == "set":
        cat = await edit_or_reply(event, "`Setting information...`")
        if not value:
            return await edit_or_reply(cat, "`.set var <ConfigVars-name> <value>`")
        if variable not in var_checker:
            if variable == "EXTERNAL_REPO":
                if bool(value and (value.lower() != "false")) and not url(value):
                    value = "https://github.com/TgCatUB/CatPlugins"
                else:
                    return await edit_or_reply(
                        cat,
                        f"**There no point in setting `{variable}` with `{value}`\nUse `.del var` to delete instead.**",
                    )
            value = f'"{value}"'
        for i in configs:
            if variable in i:
                string += f"    {variable} = {value}\n"
                match = True
            else:
                string += i
        if match:
            await edit_or_reply(
                cat, f"`{variable}` **successfully changed to  ->  **`{value}`"
            )
            logtext = f"#UPDATED\n\n`{variable}` = `{value}`"
        else:
            string += f"    {variable} = {value}\n"
            await edit_or_reply(
                cat, f"`{variable}`**  successfully added with value  ->  **`{value}`"
            )
            logtext = f"#ADDED\n\n`{variable}` = `{value}`"

    elif cmd == "del":
        cat = await edit_or_reply(event, "`Deleting information...`")
        for i in configs:
            if variable in i:
                match = True
            else:
                string += i
        if not match:
            return await edit_or_reply(
                cat,
                "**ConfigVars**:" f"\n\n__Error:\n-> __`{variable}`__ doesn't exists__",
            )
        await edit_or_reply(cat, f"`{variable}` **successfully deleted.**")
        logtext = f"#DELETED\n\n`{variable}`"

    if cmd != "get":
        with open(config, "w") as f1:
            f1.write(string)
            f1.close()
        await event.client.send_message(
            BOTLOG_CHATID, f"#VAR #CONFIG_VAR {logtext}", silent=True
        )
        await reload_codebase()
        await event.client.reload(cat)


@catub.cat_cmd(
    pattern="(re|clean)load$",
    command=("reload", plugin_category),
    info={
        "header": "To reload your bot in vps/ similar to restart",
        "flags": {
            "re": "restart your bot without deleting junk files",
            "clean": "delete all junk files & restart",
        },
        "usage": [
            "{tr}reload",
            "{tr}cleanload",
        ],
    },
)
async def reload(event):
    "To reload Your bot"
    cmd = event.pattern_match.group(1)
    cat = await edit_or_reply(event, "`Wait 2-3 min, reloading...`")
    if cmd == "clean":
        all_files = glob.glob("./*.*")
        removing = [file for file in all_files if file not in default]
        for i in removing:
            os.remove(i)
        for i in cmds:
            await _catutils.runcmd(i)
    await reload_codebase()
    await event.client.reload(cat)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Special Credit : Adek Maulana.

import math
import os

import heroku3
import requests
import urllib3

from userbot import BOTLOG_CHATID, catub

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import config_helper as dBcof

plugin_category = "tools"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# =================

heroku_api = "https://api.heroku.com"


def heroku_app():
    if (Config.HEROKU_APP_NAME is None) or (Config.HEROKU_API_KEY is None):
        return (
            None,
            "Set the required vars in heroku to function this normally `HEROKU_API_KEY` and `HEROKU_APP_NAME`.",
        )
    try:
        Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
        app = Heroku.app(Config.HEROKU_APP_NAME)
        return app, Heroku
    except BaseException:
        return (
            None,
            "Please make sure your Heroku API Key, Your App name are configured correctly in the heroku",
        )


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
    "Manage most of ConfigVars setting, set new var, get current var, or delete event..."
    app, Heroku = heroku_app()
    value = None
    if not app:
        return await edit_delete(event, Heroku)
    cmd = event.pattern_match.group(1)
    if cmd == "info":
        return await edit_delete(event, dBcof.vars_info(), 60)
    variable = event.pattern_match.group(2)
    if " " in variable:
        variable, value = variable.split(" ", 1)
    if not variable:
        return await edit_delete(event, "`What to do without Config Var??`")
    if variable in dBcof.var_list:
        cat = await edit_or_reply(event, "`Processing...`")
        data = await dBcof.setup_vars(event, cmd, variable, value)
        return await edit_delete(cat, data)

    heroku_var = app.config()
    if cmd == "get":
        cat = await edit_or_reply(event, "`Getting information...`")
        try:
            if variable in heroku_var:
                return await edit_or_reply(
                    cat,
                    "**ConfigVars**:" f"\n\n`{variable}` = `{heroku_var[variable]}`\n",
                )
            await edit_or_reply(
                cat,
                "**ConfigVars**:" f"\n\n__Error:\n-> __`{variable}`__ don't exists__",
            )
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                await edit_or_reply(
                    cat,
                    "`[HEROKU]` ConfigVars:\n\n"
                    "================================"
                    f"\n```{result}```\n"
                    "================================",
                )
            os.remove("configs.json")
    elif cmd == "set":
        cat = await edit_or_reply(event, "`Setting information...`")
        if not value:
            return await edit_or_reply(cat, "`.set var <ConfigVars-name> <value>`")
        if variable in heroku_var:
            await edit_or_reply(
                cat, f"`{variable}` **successfully changed to  ->  **`{value}`"
            )
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#CONFIG_VAR  #UPDATED\n\n`{variable}` = `{value}`",
                silent=True,
            )
        else:
            await edit_or_reply(
                cat, f"`{variable}`**  successfully added with value`  ->  **{value}`"
            )
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#CONFIG_VAR  #ADDED\n\n`{variable}` = `{value}`",
                silent=True,
            )
        heroku_var[variable] = value
    elif cmd == "del":
        cat = await edit_or_reply(
            event, "`Getting information to deleting variable...`"
        )
        if variable not in heroku_var:
            return await edit_or_reply(cat, f"`{variable}`**  does not exist**")
        await edit_or_reply(cat, f"`{variable}`  **successfully deleted**")
        await event.client.send_message(
            BOTLOG_CHATID, f"#CONFIG_VAR  #DELETED\n\n`{variable}`", silent=True
        )
        del heroku_var[variable]


@catub.cat_cmd(
    pattern="usage$",
    command=("usage", plugin_category),
    info={
        "header": "To Check dyno usage of userbot and also to know how much left.",
        "usage": "{tr}usage",
    },
)
async def dyno_usage(dyno):
    "Get your account Dyno Usage"
    app, Heroku = heroku_app()
    if not app:
        return await edit_delete(dyno, Heroku)
    dyno = await edit_or_reply(dyno, "`Processing...`")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = f"/accounts/{user_id}/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit(
            "`Error: something bad happened`\n\n" f">.`{r.reason}`\n"
        )
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    # - Used -
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    # - Current -
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    return await dyno.edit(
        "**Dyno Usage**:\n\n"
        f" -> `Dyno usage for`  **{Config.HEROKU_APP_NAME}**:\n"
        f"     •  `{AppHours}`**h**  `{AppMinutes}`**m**  "
        f"**|**  [`{AppPercentage}`**%**]"
        "\n\n"
        " -> `Dyno hours quota remaining this month`:\n"
        f"     •  `{hours}`**h**  `{minutes}`**m**  "
        f"**|**  [`{percentage}`**%**]"
    )


@catub.cat_cmd(
    pattern="herokulogs$",
    command=("herokulogs", plugin_category),
    info={
        "header": "To get recent 100 lines logs from heroku.",
        "usage": ["{tr}herokulogs", "{tr}logs"],
    },
)
async def herokulogs(event):
    "To get recent 100 lines logs from heroku"
    app, Heroku = heroku_app()
    if not app:
        return await edit_delete(event, Heroku)
    data = app.get_log()
    await edit_or_reply(
        event, data, deflink=True, linktext="**Recent 100 lines of heroku logs: **"
    )


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""
    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)


@catub.cat_cmd(
    pattern="(|add|del)buildpack(?:\s|$)([\s\S]*)",
    command=("buildpack", plugin_category),
    info={
        "header": "To manage heroku buildpacks.",
        "flags": {
            "add": "To set new buildpack",
            "del": "To delete the existing buildpack",
        },
        "usage": [
            "{tr}buildpack",
            "{tr}addbuildpack (url of the buildpack)",
            "{tr}delbuildpack (url of the buildpack)",
        ],
        "examples": [
            "{tr}buildpack",
            "{tr}addbuildpack https://github.com/amivin/aria2-heroku.git",
        ],
    },
)
async def buildpack(event):
    "Manange heroku buildpacks with heroku api"
    app, Heroku = heroku_app()
    if not app:
        return await edit_delete(event, Heroku)
    cmd = event.pattern_match.group(1).lower()
    link = event.pattern_match.group(2)
    buidpacks = [item.buildpack.url for item in app.buildpacks()]
    if cmd and not link:
        return await edit_delete(event, "**Error::** `Give buildpack link..`")
    elif cmd == "add":
        if link in buidpacks:
            return await edit_delete(
                event, "**Error::** __Buildpack is already connected to this app..__"
            )
        buidpacks.append(link)
        app.update_buildpacks(buidpacks)
        return await edit_delete(
            event,
            "**Success:** __Buildpack connected.\nDo `.update deploy` to complete updating__",
        )
    elif cmd == "del":
        if link not in buidpacks:
            return await edit_delete(
                event,
                "**Error::** __Unable to delete, buildpack is not connected to this app...__",
            )
        buidpacks.remove(link)
        app.update_buildpacks(buidpacks)
        return await edit_delete(
            event,
            "**Success:** __Buildpack removed.\nDo `.update deploy` to complete updating__",
        )
    string = (
        f"__**Currently available buildpacks for {Config.HEROKU_APP_NAME}:-**__\n\n"
    )
    for i, url in enumerate(buidpacks, start=1):
        string += f"**{i}.**   `{url}`\n\n"
    await edit_or_reply(event, string)

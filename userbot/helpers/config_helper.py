# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from telegraph import upload_file
from telethon.tl.functions.users import GetFullUserRequest
from validators.url import url

from userbot import BOTLOG_CHATID

from ..Config import Config
from ..sql_helper.globals import addgvar, delgvar, gvarstatus

plugin_category = "tools"

cmdhd = Config.COMMAND_HAND_LER

var_list = [
    "ALIVE_PIC",
    "ALIVE_EMOJI",
    "ALIVE_TEMPLATE",
    "ALIVE_TEXT",
    "ALLOW_NSFW",
    "BOT_START_PIC",
    "CHANGE_TIME",
    "CUSTOM_STICKER_PACKNAME",
    "DEFAULT_BIO",
    "DEFAULT_NAME",
    "DEFAULT_PIC",
    "DEFAULT_USER",
    "DIGITAL_PIC",
    "HELP_EMOJI",
    "HELP_TEXT",
    "IALIVE_PIC",
    "MAX_FLOOD_IN_PMS",
    "NO_OF_ROWS_IN_HELP",
    "NO_OF_COLUMNS_IN_HELP",
    "PING_PIC",
    "PING_TEMPLATE",
    "PM_PIC",
    "PM_TEXT",
    "PM_BLOCK",
    "SPOILER_MEDIA",
    "START_TEXT",
]


def vars_info():
    vnlist = "".join(f"{i}. `{each}`\n" for i, each in enumerate(var_list, start=1))
    return f"**➜ Vars Info:\n     • Config:\n     • Database:**\n\n**📑 Available dBVars :\n\n**{vnlist}"


async def default_user(event):
    USERINFO = await event.client.get_entity(event.client.uid)
    FULL_USERINFO = (await event.client(GetFullUserRequest(event.client.uid))).full_user
    addgvar("FIRST_NAME", USERINFO.first_name)
    addgvar("DEFAULT_NAME", USERINFO.first_name)
    if USERINFO.last_name:
        addgvar(
            "DEFAULT_NAME",
            f"{USERINFO.first_name}  {USERINFO.first_name}",
        )
        addgvar("LAST_NAME", USERINFO.last_name)
    elif gvarstatus("LAST_NAME"):
        delgvar("LAST_NAME")
    if FULL_USERINFO.about:
        addgvar("DEFAULT_BIO", FULL_USERINFO.about)
    elif gvarstatus("DEFAULT_BIO"):
        delgvar("DEFAULT_BIO")
    try:
        photos = await event.client.get_profile_photos(event.client.uid)
        myphoto = await event.client.download_media(photos[0])
        myphoto_urls = upload_file(myphoto)
        addgvar("DEFAULT_PIC", f"https://graph.org{myphoto_urls[0]}")
    except IndexError:
        if gvarstatus("DEFAULT_PIC"):
            delgvar("DEFAULT_PIC")
    usrln = gvarstatus("LAST_NAME") or None
    usrbio = gvarstatus("DEFAULT_BIO") or None
    usrphoto = gvarstatus("DEFAULT_PIC") or None

    return (
        f'**Name:** `{gvarstatus("DEFAULT_NAME")}`\n**First Name:** `{gvarstatus("FIRST_NAME")}`\n**Last Name:** `{usrln}`\n**Bio:** `{usrbio}`\n**Photo:** `{usrphoto}`',
        None,
    )


async def setup_vars(event, cmd, vname, vinfo):
    reply = await event.get_reply_message()
    if not vinfo and reply:
        vinfo = reply.text
    if cmd == "get":
        response = await get_var(vname)
    elif cmd == "set":
        response = await set_var(event, vname, vinfo)
    elif cmd == "del":
        response = await del_var(event, vname)
    return response


async def set_var(event, vname, vinfo):
    if vname == "DEFAULT_USER":
        vinfo, error = await default_user(event)
        if error:
            return error
    else:
        if not vinfo:
            if vname in ["ALIVE_TEMPLATE", "PING_TEMPLATE"]:
                return "Check @cat_alive"
            return f"Give some values which you want to save for **{vname}**"
        check = vinfo.split(" ")
        for i in check:
            if ("PIC" in vname) and not url(i):
                return "**Give me a correct link...**"
            elif vname in [
                "DIGITAL_PIC",
                "DEFAULT_PIC",
                "BOT_START_PIC",
            ] and url(i):
                vinfo = i
                break
            elif "PIC" not in vname:
                break
        if vname == "DEFAULT_BIO" and len(vinfo) > 70:
            return f"No of characters in your bio must not exceed 70 so compress it and set again\n`{vinfo}`"
        addgvar(vname, vinfo)
    await event.client.send_message(
        BOTLOG_CHATID, f"#DATABASE_VAR  #UPDATED\n\n`{vname}` = `{vinfo}`", silent=True
    )
    return f"📑 Value of **{vname}** is changed to :- `{vinfo}`"


async def get_var(vname):
    var_data = gvarstatus(vname)
    return f"📑 Value of **{vname}** is  ```{var_data}```"


async def del_var(event, vname):
    if vname == "DEFAULT_USER":
        delgvar("FIRST_NAME")
        delgvar("DEFAULT_NAME")
        if gvarstatus("LAST_NAME"):
            delgvar("LAST_NAME")
        if gvarstatus("DEFAULT_BIO"):
            delgvar("DEFAULT_BIO")
        if gvarstatus("DEFAULT_PIC"):
            delgvar("DEFAULT_PIC")
    delgvar(vname)
    await event.client.send_message(
        BOTLOG_CHATID, f"#DATABASE_VAR  #DELETED\n\n`{vname}`", silent=True
    )
    return f"📑 Value of **{vname}** is now deleted & set to default."

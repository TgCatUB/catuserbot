# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import re

from telethon import Button

from ..Config import Config
from ..helpers.functions.functions import make_inline
from . import catub, edit_delete, reply_id

plugin_category = "tools"
# regex obtained from:
# https://github.com/PaulSonOfLars/tgbot/blob/master/tg_bot/modules/helper_funcs/string_handling.py#L23
MEDIA_PATH_REGEX = re.compile(r"(:?\<\bmedia:(:?(?:.*?)+)\>)")
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")


def build_inline_keyboard(buttons):
    keyboard = []
    for btn in buttons:
        if btn[2] and keyboard:
            keyboard[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyboard.append([Button.url(btn[0], btn[1])])
    return keyboard


def inline_button_aricle(method):
    markdown_note = method[14:]
    prev = 0
    note_data = ""
    media = None
    buttons_list = []
    if catmedia := MEDIA_PATH_REGEX.search(markdown_note):
        media = catmedia.group(2)
        markdown_note = markdown_note.replace(catmedia.group(0), "")
    for match in BTN_URL_REGEX.finditer(markdown_note):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1
        if n_escapes % 2 == 0:
            buttons_list.append((match.group(2), match.group(3), bool(match.group(4))))
            note_data += markdown_note[prev : match.start(1)]
            prev = match.end(1)
        elif n_escapes % 2 == 1:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
        else:
            break
    else:
        note_data += markdown_note[prev:]
    text = note_data.strip()
    buttons = build_inline_keyboard(buttons_list)
    return (text, buttons, media)


@catub.cat_cmd(
    pattern="ibutton(?:\s|$)([\s\S]*)",
    command=("ibutton", plugin_category),
    info={
        "header": "To create button posts via inline",
        "note": "Markdown is Default to html",
        "options": "If you button to be in same row as other button then follow this <buttonurl:link:same> in 2nd button.",
        "usage": [
            "{tr}ibutton <text> [Name on button]<buttonurl:link you want to open>",
            "{tr}ibutton <text> <media:media_path> [Name on button]<buttonurl:link you want to open>",
        ],
        "examples": "{tr}ibutton test <media:downloads/thumb_image.jpg> [google]<buttonurl:https://www.google.com> [catuserbot]<buttonurl:https://t.me/catuserbot17:same> [support]<buttonurl:https://t.me/catuserbot_support>",
    },
)
async def _(event):
    "To create button posts via inline"
    reply_to_id = await reply_id(event)
    reply_message = await event.get_reply_message()
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = "".join(event.text.split(maxsplit=1)[1:])
    if not markdown_note:
        return await edit_delete(event, "`What text should i use in button post`")
    await make_inline(markdown_note, event.client, event.chat_id, reply_to_id)
    await event.delete()


@catub.cat_cmd(
    pattern="cbutton(?:\s|$)([\s\S]*)",
    command=("cbutton", plugin_category),
    info={
        "header": "To create button posts",
        "note": f"For working of this you need your bot ({Config.TG_BOT_USERNAME}) in the group/channel \
        where you are using and Markdown is Default to html",
        "options": "If you button to be in same row as other button then follow this <buttonurl:link:same> in 2nd button.",
        "usage": [
            "{tr}cbutton <text> [Name on button]<buttonurl:link you want to open>",
        ],
        "examples": "{tr}cbutton test [google]<buttonurl:https://www.google.com> [catuserbot]<buttonurl:https://t.me/catuserbot17:same> [support]<buttonurl:https://t.me/catuserbot_support>",
    },
)
async def _(event):
    "To create button posts."
    reply_message = await event.get_reply_message()
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = "".join(event.text.split(maxsplit=1)[1:])
    if not markdown_note:
        return await edit_delete(event, "`what text should i use in button post`")
    prev = 0
    note_data = ""
    buttons = []
    for match in BTN_URL_REGEX.finditer(markdown_note):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1
        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            # create a thruple with button label, url, and newline status
            buttons.append((match.group(2), match.group(3), bool(match.group(4))))
            note_data += markdown_note[prev : match.start(1)]
            prev = match.end(1)
        # if odd, escaped -> move along
        elif n_escapes % 2 == 1:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
        else:
            break
    else:
        note_data += markdown_note[prev:]
    message_text = note_data.strip() or None
    tl_ib_buttons = build_inline_keyboard(buttons)
    tgbot_reply_message = None
    if reply_message and reply_message.media:
        tgbot_reply_message = await event.client.download_media(reply_message.media)
    if tl_ib_buttons == []:
        tl_ib_buttons = None
    await event.client.tgbot.send_message(
        entity=event.chat_id,
        message=message_text,
        parse_mode="html",
        file=tgbot_reply_message,
        link_preview=False,
        buttons=tl_ib_buttons,
    )
    await event.delete()
    if tgbot_reply_message:
        os.remove(tgbot_reply_message)

"""
Created by @Jisan7509
modified by  @mrconfused
Userbot plugin for CatUserbot
"""

from . import catub, edit_or_reply
from . import fonts as emojify

plugin_category = "fun"


@catub.cat_cmd(
    pattern="emoji(?: |$)(.*)",
    command=("emoji", plugin_category),
    info={
        "header": "Converts your text to big emoji text, with some default emojis.",
        "usage": "{tr}emoji <text>",
        "examples": ["{tr}emoji catuserbot"],
    },
)
async def itachi(event):
    "To get emoji art text."
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(
            event, "`What am I Supposed to do with this idiot, Give me a text. `"
        )
        return
    result = ""
    for a in args:
        a = a.lower()
        if a in emojify.kakashitext:
            char = emojify.kakashiemoji[emojify.kakashitext.index(a)]
            result += char
        else:
            result += a
    await edit_or_reply(event, result)


@catub.cat_cmd(
    pattern="cmoji(?: |$)(.*)",
    command=("cmoji", plugin_category),
    info={
        "header": "Converts your text to big emoji text, with your custom emoji.",
        "usage": "{tr}cmoji <emoji> <text>",
        "examples": ["{tr}cmoji 😺 catuserbot"],
    },
)
async def itachi(event):
    "To get custom emoji art text."
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        return await edit_or_reply(
            event, "`What am I Supposed to do with this idiot, Give me a text. `"
        )
    try:
        emoji, arg = args.split(" ", 1)
    except Exception:
        arg = args
        emoji = "😺"
    result = ""
    for a in arg:
        a = a.lower()
        if a in emojify.kakashitext:
            char = emojify.itachiemoji[emojify.kakashitext.index(a)].format(cj=emoji)
            result += char
        else:
            result += a
    await edit_or_reply(event, result)

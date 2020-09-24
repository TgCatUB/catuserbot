"""
Created by @Jisan7509
Peru helper @mrconfused
Userbot plugin for CatUserbot
"""
import emoji

from userbot import CMD_HELP
from userbot.utils import admin_cmd, edit_or_reply, sudo_cmd

from . import *


@borg.on(admin_cmd(pattern="emoji(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="emoji(?: |$)(.*)", allow_sudo=True))
async def itachi(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(
            event, "`What am I Supposed to do with this nibba/nibbi, Give me a text. `"
        )
        return
    string = "  ".join(args).lower()
    for chutiya in string:
        if chutiya in emojify.kakashitext:
            bsdk = emojify.kakashiemoji[emojify.kakashitext.index(chutiya)]
            string = string.replace(chutiya, bsdk)
    await edit_or_reply(event, string)


@borg.on(admin_cmd(pattern="cmoji(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="cmoji(?: |$)(.*)", allow_sudo=True))
async def itachi(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(
            event, "`What am I Supposed to do with this nibba/nibbi, Give me a text. `"
        )
        return
    try:
        emoji, arg = args.split(" ", 1)
    except:
        arg = args
        emoji = "😺"
    if not char_is_emoji(emoji):
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


def char_is_emoji(character):
    return character in emoji.UNICODE_EMOJI


CMD_HELP.update(
    {
        "emojify": "__**PLUGIN NAME :** Emojify__\
      \n\n📌** CMD ➥** `.emoji` <text>\
      \n**USAGE   ➥  **Converts your text to big emoji text, with default emoji. \
      \n\n📌** CMD ➥** `.cmoji` <emoji> <text>\
      \n**USAGE   ➥  **Converts your text to big emoji text, with your custom emoji.\
      \n\n**☞ NOTE :** For giving sapce between two words use **@** symbol.\
      \n**EXAMPLE :**  `.emoji Bad@cat`\
      \n                    `.cmoji 😋 Good@cat`"
    }
)

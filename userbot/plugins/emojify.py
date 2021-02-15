"""
Created by @Jisan7509
modified by  @mrconfused
Userbot plugin for CatUserbot
"""
import emoji

from . import fonts as emojify


@bot.on(admin_cmd(pattern="emoji(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="emoji(?: |$)(.*)", allow_sudo=True))
async def itachi(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(
            event, "`What am I Supposed to do with this stupid, Give me a text. `"
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


@bot.on(admin_cmd(pattern="cmoji(?: |$)(.*)"))
@bot.on(sudo_cmd(pattern="cmoji(?: |$)(.*)", allow_sudo=True))
async def itachi(event):
    args = event.pattern_match.group(1)
    if not args:
        get = await event.get_reply_message()
        args = get.text
    if not args:
        await edit_or_reply(
            event, "`What am I Supposed to do with this stupid, Give me a text. `"
        )
        return
    try:
        emoji, arg = args.split(" ", 1)
    except Exception:
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
    return character in emoji.UNICODE_EMOJI["en"]


CMD_HELP.update(
    {
        "emojify": "**Plugin :** `emojify`\
      \n\n**Syntax :** `.emoji` <text>\
      \n****Usage : **Converts your text to big emoji text, with default emoji. \
      \n\n**Syntax :** `.cmoji` <emoji> <text>\
      \n****Usage : **Converts your text to big emoji text, with your custom emoji.\
      "
    }
)

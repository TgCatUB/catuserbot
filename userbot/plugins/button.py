#    Copyright (C) 2020  sandeep.n(π.$)
# button post makker for catuserbot thanks to uniborg for the base
# by @sandy1709 (@mrconfused)
import os
import re

from telethon import Button

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, sudo_cmd

# regex obtained from:
# https://github.com/PaulSonOfLars/tgbot/blob/master/tg_bot/modules/helper_funcs/string_handling.py#L23
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")


@borg.on(admin_cmd(pattern=r"cbutton(?: |$)(.*)", outgoing=True))
@borg.on(sudo_cmd(pattern=r"cbutton(?: |$)(.*)", allow_sudo=True))
async def _(event):
    chat = event.chat_id
    reply_message = await event.get_reply_message()
    if reply_message:
        markdown_note = reply_message.text
    else:
        markdown_note = event.pattern_match.group(1)
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
        else:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += markdown_note[prev:]
    message_text = note_data.strip()
    tl_ib_buttons = build_keyboard(buttons)
    tgbot_reply_message = None
    if reply_message and reply_message.media:
        tgbot_reply_message = await borg.download_media(reply_message.media)
    await tgbot.send_message(
        entity=chat,
        message=message_text,
        parse_mode="html",
        file=tgbot_reply_message,
        link_preview=False,
        buttons=tl_ib_buttons,
        silent=True,
    )
    await event.delete()
    if tgbot_reply_message:
        os.remove(tgbot_reply_message)


# Helpers


@borg.on(admin_cmd(pattern=r"ibutton( (.*)|$)", outgoing=True))
@borg.on(sudo_cmd(pattern=r"ibutton( (.*)|$)", allow_sudo=True))
async def _(event):
    reply_to_id = None
    catinput = "".join(event.text.split(maxsplit=1)[1:])
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.get_reply_message()
    # soon will try to add media support
    if not catinput:
        catinput = (await event.get_reply_message()).text
    if not catinput:
        await edit_or_reply(event, "`Give me some thing to write in bot inline`")
        return
    catinput = "Inline buttons " + catinput
    tgbotusername = Var.TG_BOT_USER_NAME_BF_HER
    results = await bot.inline_query(tgbotusername, catinput)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


def build_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb


CMD_HELP.update(
    {
        "button": "**Plugin : **`button`\
    \n\n**SYNTAX : **`.cbutton`\
    \n**USAGE :** Buttons must be in th format as [name on button]<buttonurl:link you want to open> and markdown is Default to html\
    \n**EXAMPLE :** `.cbutton test [google]<buttonurl:https://www.google.com> [catuserbot]<buttonurl:https://t.me/catuserbot17:same> [support]<buttonurl:https://t.me/catuserbot_support>`\
    \n\n**SYNTAX : **`.ibutton`\
    \n**USAGE :** Buttons must be in th format as [name on button]<buttonurl:link you want to open>\
    \n**EXAMPLE :** `.ibutton test [google]<buttonurl:https://www.google.com> [catuserbot]<buttonurl:https://t.me/catuserbot17:same> [support]<buttonurl:https://t.me/catuserbot_support>`\
    "
    }
)

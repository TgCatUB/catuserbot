"""Create Button Posts
"""

import re
from telethon import custom
from userbot.utils import admin_cmd

from telethon import events
from userbot.uniborgConfig import Config

# regex obtained from: https://github.com/PaulSonOfLars/tgbot/blob/master/tg_bot/modules/helper_funcs/string_handling.py#L23
BTN_URL_REGEX = re.compile(r"(\{([^\[]+?)\}\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")


@borg.on(events.NewMessage(pattern=r"\.cbutton(.*)", outgoing=True))
async def _(event):
    if Config.TG_BOT_USER_NAME_BF_HER is None or tgbot is None:
        await event.edit("need to set up a @BotFather bot for this module to work")
        return

    if Config.PRIVATE_CHANNEL_BOT_API_ID is None:
        await event.edit("need to have a `PRIVATE_CHANNEL_BOT_API_ID` for this module to work")
        return

    reply_message = await event.get_reply_message()
    if reply_message is None:
        await event.edit("reply to a message that I need to parse the magic on")
        return

    markdown_note = reply_message.text
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
            note_data += markdown_note[prev:match.start(1)]
            prev = match.end(1)

        # if odd, escaped -> move along
        else:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += markdown_note[prev:]

    message_text = note_data.strip()
    tl_ib_buttons = build_keyboard(buttons)

    # logger.info(message_text)
    # logger.info(tl_ib_buttons)

    tgbot_reply_message = None
    if reply_message.media is not None:
        message_id_in_channel = reply_message.id
        tgbot_reply_message = await tgbot.get_messages(
            entity=Config.PRIVATE_CHANNEL_BOT_API_ID,
            ids=message_id_in_channel
        )
        tgbot_reply_message = tgbot_reply_message.media

    await tgbot.send_message(
        entity=Config.PRIVATE_CHANNEL_BOT_API_ID,
        message=message_text,
        parse_mode="html",
        file=tgbot_reply_message,
        link_preview=False,
        buttons=tl_ib_buttons,
        silent=True
    )


# Helpers

def build_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(custom.Button.url(btn[0], btn[1]))
        else:
            keyb.append([custom.Button.url(btn[0], btn[1])])
    return keyb

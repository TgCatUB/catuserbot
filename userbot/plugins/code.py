"""COMMAND : .code |;|"""

from telethon import events

import asyncio

import requests





@borg.on(events.NewMessage(pattern=r"\.code (.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    input_str = event.pattern_match.group(1)

    DELIMITER = "|;|"

    if DELIMITER not in input_str:

        await event.edit("Invalid Syntax")

        return False

    lang, code = input_str.split(DELIMITER)

    url = "http://www.suka.ml/api/v0/sakty/karbon"

    a = requests.get(url, params={

        "code": code,

        "lang": lang,

        "line": True

    }).json()

    img_url = a["hasil"]["karbon"]

    reply_message_id = event.message.id

    if event.reply_to_msg_id:

        reply_message_id = event.reply_to_msg_id

    try:

        await borg.send_file(

            event.chat_id,

            img_url,

            caption=code,

            force_document=True,

            allow_cache=False,

            reply_to=reply_message_id

        )

        await event.delete()

    except Exception as e:

        await event.edit(str(e))

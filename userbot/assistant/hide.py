# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import json
import os
import re

from telethon.events import CallbackQuery

from userbot import catub


@catub.tgbot.on(CallbackQuery(data=re.compile(b"hide_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./userbot/hide.txt"):
        jsondata = json.load(open("./userbot/hide.txt"))
        try:
            reply_pop_up_alert = jsondata[f"{timestamp}"]["text"]
        except KeyError:
            reply_pop_up_alert = "This message no longer exists in catub server"
    else:
        reply_pop_up_alert = "This message no longer exists "
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

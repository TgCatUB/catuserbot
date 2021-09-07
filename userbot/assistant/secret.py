import json
import os
import re

from telethon.events import CallbackQuery

from userbot import catub


@catub.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./userbot/secrets.txt"):
        jsondata = json.load(open("./userbot/secrets.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = [userid, catub.uid]
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
            else:
                reply_pop_up_alert = "Why were you trying to open and read this top-secret message? Go away kid and do your own work, idiot"
        except KeyError:
            reply_pop_up_alert = "This top-secret message has been destroyed..."
    else:
        reply_pop_up_alert = "This top-secret message has been destroyed..."
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

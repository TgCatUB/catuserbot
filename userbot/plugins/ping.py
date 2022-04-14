import asyncio
import random
import time
from datetime import datetime

import requests
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import get_readable_time
from ..sql_helper.globals import gvarstatus
from . import StartTime, catub, mention

plugin_category = "tools"


temp_ = "Pong!"
temp = "Pong!\n`{ping} ms`"
if Config.BADCAT:
    temp_ = "__**☞ Pong**__"
    temp = "__**☞ Pong**__\n➥ `{ping}` **ms**\n➥ __**Bot of **__{mention}"


@catub.cat_cmd(
    pattern="ping( -a|$)",
    command=("ping", plugin_category),
    info={
        "header": "check how long it takes to ping your userbot",
        "flags": {"-a": "average ping"},
        "usage": ["{tr}ping", "{tr}ping -a"],
    },
)
async def _(event):
    "To check ping"
    flag = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    if flag == " -a":
        catevent = await edit_or_reply(event, "`!....`")
        await asyncio.sleep(0.3)
        await edit_or_reply(catevent, "`..!..`")
        await asyncio.sleep(0.3)
        await edit_or_reply(catevent, "`....!`")
        end = datetime.now()
        tms = (end - start).microseconds / 1000
        ms = round((tms - 0.6) / 3, 3)
        await edit_or_reply(catevent, f"Average Ping!\n`{ms} ms`")
    else:
        catevent = await edit_or_reply(event, temp_)
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        ANIME = None
        ping_temp = gvarstatus("PING_TEMPLATE") or temp
        PING_PIC = gvarstatus("PING_PIC")
        if "ANIME" in ping_temp:
            data = requests.get("https://animechan.vercel.app/api/random").json()
            ANIME = f"**“{data['quote']}” - {data['character']} ({data['anime']})**"
        caption = ping_temp.format(
            ANIME=ANIME,
            mention=mention,
            uptime=uptime,
            ping=ms,
        )
        if PING_PIC:
            CAT = list(PING_PIC.split())
            PIC = random.choice(CAT)
            try:
                await event.client.send_file(
                    event.chat_id, PIC, caption=caption, reply_to=reply_to_id
                )
                await catevent.delete()
            except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
                return await edit_or_reply(
                    catevent,
                    f"**Media Value Error!!**\n__Change the link by __`.setdv`\n\n**__Can't get media from this link :-**__ `{PIC}`",
                )
        else:
            await edit_or_reply(
                catevent,
                caption,
            )

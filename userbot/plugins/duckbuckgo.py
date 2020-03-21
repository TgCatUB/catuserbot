from telethon import events
import os
import requests
import json
from userbot.utils import admin_cmd


@borg.on(admin_cmd("ddg (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://duckduckgo.com/?q={}".format(input_str.replace(" ","+"))
    if sample_url:
        link = sample_url.rstrip()
        await event.edit("Let me 🦆 DuckDuckGo that for you:\n🔎 [{}]({})".format(input_str, link))
    else:
        await event.edit("something is wrong. please try again later.")

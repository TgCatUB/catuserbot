# inspired from uniborg Quotes plugin
import random

import requests

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import catmemes

plugin_category = "extra"


@catub.cat_cmd(
    pattern="quote(?: |$)(.*)",
    command=("quote", plugin_category),
    info={
        "header": "To get random quotes on given topic.",
        "description": "An api that Fetchs random Quote from `goodreads.com`",
        "usage": "{tr}quote <topic>",
        "examples": "{tr}quote love",
    },
)
async def quote_search(event):
    "shows random quotes on given topic."
    catevent = await edit_or_reply(event, "`Processing...`")
    input_str = event.pattern_match.group(1)
    if not input_str:
        api_url = "https://quotes.cwprojects.live/random"
        try:
            response = requests.get(api_url).json()
        except Exception:
            response = None
    else:
        api_url = f"https://quotes.cwprojects.live/search/query={input_str}"
        try:
            response = random.choice(requests.get(api_url).json())
        except Exception:
            response = None
    if response is not None:
        await catevent.edit(f"`{response['text']}`")
    else:
        await edit_delete(catevent, "`Sorry Zero results found`", 5)


@catub.cat_cmd(
    pattern="pquote$",
    command=("pquote", plugin_category),
    info={
        "header": "To get random quotes on programming.",
        "usage": "{tr}pquote",
    },
)
async def _(event):
    "Shows random programming quotes"
    txt = random.choice(catmemes.PROGQUOTES)
    await edit_or_reply(event, txt)

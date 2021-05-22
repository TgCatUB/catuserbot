"""Get a Image Post from Reddit"""
# 👍 https://github.com/D3vd for his awesome API
#
# Copyright (C) 2020 BY - GitHub.com/code-rgb [TG - @DeletedUser420]
# All rights reserved.


import requests
from telethon import Button

from userbot import catub
from ..core.logger import logging
from ..helpers.functions import age_verification
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import unsavegif

LOGS = logging.getLogger(__name__)
API = "https://meme-api.herokuapp.com/gimme"

plugin_category = "misc"


@catub.cat_cmd(
    pattern="reddit(?: |$)(.*)",
    command=("reddit", plugin_category),
    info={
        "header": "get a random reddit post.",
        "description": "An api that Fetchs random Quote from `goodreads.com`",
        "usage": "{tr}reddit <subreddit>",
        "examples": "{tr}reddit dankmemes",
    },
)
async def reddit_fetch(event):
    """Random reddit post"""
    reply_id = await reply_id(event)
    sub_r = event.pattern_match.group(1)
    subreddit_api = f"{API}/{sub_r}" if sub_r else API
    try:
        cn = requests.get(subreddit_api)
        r = cn.json()
    except ValueError:
        return await edit_delete(event, "Value error!.")
    if "code" in r:
        if BOTLOG:
            code = r["code"]
            code_message = r["message"]
            await event.client.send_message(BOTLOG_CHATID,f"*Error Code: {code}*\n`{code_message}`")
    else:
        if "url" not in r:
            return await edit_delete(event,
                "Coudn't Find a post with Image, Please Try Again",
            )
        postlink = r["postLink"]
        subreddit = r["subreddit"]
        title = r["title"]
        media_url = r["url"]
        author = r["author"]
        upvote = r["ups"]
        captionx = f"<b>{title}</b>\n"
        captionx += f"`Posted by u/{author}`\n"
        captionx += f"↕️ <code>{upvote}</code>\n"
        if r["spoiler"]:
            captionx += "⚠️ Post marked as SPOILER\n"
        if r["nsfw"]:
            captionx += "🔞 Post marked Adult \n"

            if await age_verification(event):
                return

        await event.delete()
        captionx += f"Source: [r/{subreddit}]({postlink})"
        sandy = await event.client.send_message(
            event.chat_id, media_url,caption=captionx,reply_to=reply_id
        )
        if media_url.endswith(".gif"):
            await unsavegif(event, sandy)

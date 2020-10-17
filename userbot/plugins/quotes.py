import random

import requests

from ..utils import admin_cmd, edit_or_reply, sudo_cmd


@borg.on(admin_cmd(pattern="quote ?(.*)"))
@bot.on(sudo_cmd(pattern="quote ?(.*)", allow_sudo=True))
async def quote_search(event):
    if event.fwd_from:
        return
    catevent = await edit_or_reply(event, "Processing...")
    search_string = event.pattern_match.group(1)
    input_url = "https://bots.shrimadhavuk.me/Telegram/GoodReadsQuotesBot/?q={}".format(
        search_string
    )
    headers = {"USER-AGENT": "UniBorg"}
    try:
        response = requests.get(input_url, headers=headers).json()
    except BaseException:
        response = None
    if response is not None:
        result = (
            random.choice(response).get("input_message_content").get("message_text")
        )
    else:
        result = None
    if result:
        await catevent.edit(result.replace("<code>", "`").replace("</code>", "`"))
    else:
        await catevent.edit("Zero results found")

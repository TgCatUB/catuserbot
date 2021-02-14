# inspired from uniborg Quotes plugin
import random

import requests


@bot.on(admin_cmd(pattern="quote ?(.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="quote ?(.*)", allow_sudo=True))
async def quote_search(event):
    if event.fwd_from:
        return
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


CMD_HELP.update(
    {
        "quotes": "**Plugin : **`quotes`\
    \n\n**Syntax : **`.quote <category>`\
    \n**Function : **__An api that Fetchs random Quote from `goodreads.com`__\
    "
    }
)

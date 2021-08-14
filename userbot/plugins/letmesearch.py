from asyncio import sleep

import requests

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"


@catub.cat_cmd(
    pattern="lmg ([\s\S]*)",
    command=("lmg", plugin_category),
    info={
        "header": "Searches the given query in Google and shows you the link of that query.",
        "usage": "{tr}lmg <Query>",
    },
)
async def _(event):
    "Searches the given query in Google and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = (
        f"https://da.gd/s?url=http://google.com/search?q={input_str.replace(' ', '+')}"
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **Google** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@catub.cat_cmd(
    pattern="lmy ([\s\S]*)",
    command=("lmy", plugin_category),
    info={
        "header": "Searches the given query in youtube and shows you the link of that query.",
        "usage": "{tr}lmy <Query>",
    },
)
async def _(event):
    "Searches the given query in youtube and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://www.youtube.com/results?search_query={input_str.replace(' ', '+')}"
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **youtube** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@catub.cat_cmd(
    pattern="ddg ([\s\S]*)",
    command=("ddg", plugin_category),
    info={
        "header": "Searches the given query in Duck buck go and shows you the link of that query.",
        "usage": "{tr}ddg <Query>",
    },
)
async def _(event):
    "Searches the given query in Duck buck go and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://duckduckgo.com/?q={input_str.replace(' ', '+')}&t=h_&ia=about"
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **duckduckgo** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@catub.cat_cmd(
    pattern="lmalt ([\s\S]*)",
    command=("lmalt", plugin_category),
    info={
        "header": "Searches the given query in altnews and shows you the link of that query.",
        "usage": "{tr}lmalt <Query>",
    },
)
async def _(event):
    "Searches the given query in altnews and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = (
        f"https://da.gd/s?url=https://www.altnews.in/?s={input_str.replace(' ', '+')}"
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **altnews** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@catub.cat_cmd(
    pattern="lmvar ([\s\S]*)",
    command=("lmvar", plugin_category),
    info={
        "header": "Searches the given app name in heroku and show that app vars page link .",
        "usage": "{tr}lmvar <app name>",
    },
)
async def _(event):
    "Searches the given app name in heroku and show that app vars page link ."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://dashboard.heroku.com/apps/{input_str.replace(' ', '+')}/settings"
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **var** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@catub.cat_cmd(
    pattern="lmlog ([\s\S]*)",
    command=("lmlog", plugin_category),
    info={
        "header": "Searches the given app name in heroku and shows you logs page link of that app.",
        "usage": "{tr}lmlog <app name>",
    },
)
async def _(event):
    "Searches the given app name in heroku and shows you logs page link of that app."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://dashboard.heroku.com/apps/{input_str.replace(' ', '+')}/logs"
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **log** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@catub.cat_cmd(
    pattern="dyno ([\s\S]*)",
    command=("dyno", plugin_category),
    info={
        "header": "Searches the given app name in heroku and shows you dyno page link of that app.",
        "usage": "{tr}dyno <Query>",
    },
)
async def _(event):
    "Searches the given app name in heroku and shows you dyno page link of that app."
    input_str = event.pattern_match.group(1)
    billings_url = "https://da.gd/s?url=https://dashboard.heroku.com/account/billing"
    sample_url = (
        f"https://da.gd/s?url=https://dashboard.heroku.com/apps/{input_str}/resources"
    )
    response_api = requests.get(sample_url).text
    respons_api = requests.get(billings_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **dyno** that for you:\
                \n👉 [{input_str}]({response_api.rstrip()})\
                \n👉 [Billings]({respons_api.rstrip()})\
                \n`Thank me later 😉`"
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@catub.cat_cmd(
    pattern="lmkp ([\s\S]*)",
    command=("lmkp", plugin_category),
    info={
        "header": "Searches the given query in indian kanoon and shows you the link of that query.",
        "usage": "{tr}lmkp <Query>",
    },
)
async def _(event):
    "Searches the given query in indian kanoon and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://indiankanoon.org/search/?formInput={input_str.replace(' ', '+')}+sortby%3Amostrecent"
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **Indiankanoon.com : Place** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@catub.cat_cmd(
    pattern="gem ([\s\S]*)",
    command=("gem", plugin_category),
    info={
        "header": "Searches the given query in Government e marketplace and shows you the link of that query.",
        "usage": "{tr}gem <Query>",
    },
)
async def _(event):
    "Searches the given query in Government e marketplace and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://mkp.gem.gov.in/search?q={input_str.replace(' ', '+')}&sort_type=created_at_desc&_xhr=1"
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me **gem.gov.in** that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@catub.cat_cmd(
    pattern="archive ([\s\S]*)",
    command=("archive", plugin_category),
    info={
        "header": "Searches the given query in web archive and shows you the link of that query.",
        "usage": "{tr}archive <Query>",
    },
)
async def _(event):
    "Searches the given query in web archive and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url=https://web.archive.org/web/*/{input_str.replace(' ', '+')}"
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            f"Let me run your link on wayback machine that for you:\n👉 [{input_str}]({response_api.rstrip()})\n`Thank me later 😉` "
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)

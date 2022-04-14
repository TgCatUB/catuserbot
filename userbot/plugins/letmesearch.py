from asyncio import sleep

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"


@catub.cat_cmd(
    pattern="lmg(?: |$)([\s\S]*)",
    command=("lmg", plugin_category),
    info={
        "header": "Searches the given query in Google and shows you the link of that query.",
        "usage": "{tr}lmg <Query>",
    },
)
async def googal(event):
    "Searches the given query in Google and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(event, "**ಠ∀ಠ Give me text to search..**")
    sample_url = f"http://google.com/search?q={input_str.replace(' ','+')}"
    await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me **Google** that for you:\n👉 [{input_str}]({sample_url})\n`Thank me later 😉` ",
    )


@catub.cat_cmd(
    pattern="lmy(?: |$)([\s\S]*)",
    command=("lmy", plugin_category),
    info={
        "header": "Searches the given query in youtube and shows you the link of that query.",
        "usage": "{tr}lmy <Query>",
    },
)
async def uthoob(event):
    "Searches the given query in youtube and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(event, "**ಠ∀ಠ Give me text to search..**")
    sample_url = (
        f"https://www.youtube.com/results?search_query={input_str.replace(' ', '+')}"
    )
    await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me **youtube** that for you:\n👉 [{input_str}]({sample_url})\n`Thank me later 😉` ",
    )


@catub.cat_cmd(
    pattern="ddg(?: |$)([\s\S]*)",
    command=("ddg", plugin_category),
    info={
        "header": "Searches the given query in Duck buck go and shows you the link of that query.",
        "usage": "{tr}ddg <Query>",
    },
)
async def dukdukgo(event):
    "Searches the given query in Duck buck go and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(event, "**ಠ∀ಠ Give me text to search..**")
    sample_url = (
        f"https://duckduckgo.com/?q={input_str.replace(' ', '+')}&t=h_&ia=about"
    )
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me **duckduckgo** that for you:\n👉 [{input_str}]({sample_url})\n`Thank me later 😉` ",
    )


@catub.cat_cmd(
    pattern="lmalt(?: |$)([\s\S]*)",
    command=("lmalt", plugin_category),
    info={
        "header": "Searches the given query in altnews and shows you the link of that query.",
        "usage": "{tr}lmalt <Query>",
    },
)
async def news(event):
    "Searches the given query in altnews and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(event, "**ಠ∀ಠ Give me text to search..**")
    sample_url = f"https://www.altnews.in/?s={input_str.replace(' ', '+')}"
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me **altnews** that for you:\n👉 [{input_str}]({sample_url})\n`Thank me later 😉` ",
    )


@catub.cat_cmd(
    pattern="lmvar ([\s\S]*)",
    command=("lmvar", plugin_category),
    info={
        "header": "Searches the given app name in heroku and show that app vars page link .",
        "usage": "{tr}lmvar <app name>",
    },
)
async def var(event):
    "Searches the given app name in heroku and show that app vars page link ."
    input_str = event.pattern_match.group(1)
    sample_url = (
        f"https://dashboard.heroku.com/apps/{input_str.replace(' ', '+')}/settings"
    )
    await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me **var** that for you:\n👉 [{input_str}]({sample_url})\n`Thank me later 😉` ",
    )


@catub.cat_cmd(
    pattern="lmlog ([\s\S]*)",
    command=("lmlog", plugin_category),
    info={
        "header": "Searches the given app name in heroku and shows you logs page link of that app.",
        "usage": "{tr}lmlog <app name>",
    },
)
async def log(event):
    "Searches the given app name in heroku and shows you logs page link of that app."
    input_str = event.pattern_match.group(1)
    sample_url = f"https://dashboard.heroku.com/apps/{input_str.replace(' ', '+')}/logs"
    await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me **log** that for you:\n👉 [{input_str}]({sample_url})\n`Thank me later 😉` ",
    )


@catub.cat_cmd(
    pattern="dyno ([\s\S]*)",
    command=("dyno", plugin_category),
    info={
        "header": "Searches the given app name in heroku and shows you dyno page link of that app.",
        "usage": "{tr}dyno <Query>",
    },
)
async def dyno(event):
    "Searches the given app name in heroku and shows you dyno page link of that app."
    input_str = event.pattern_match.group(1)
    billings_url = "https://da.gd/s?url=https://dashboard.heroku.com/account/billing"
    sample_url = (
        f"https://da.gd/s?url=https://dashboard.heroku.com/apps/{input_str}/resources"
    )
    await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me **dyno** that for you:\
            \n👉 [{input_str}]({sample_url})\
            \n👉 [Billings]({billings_url})\
            \n`Thank me later 😉`",
    )


@catub.cat_cmd(
    pattern="lmkp(?: |$)([\s\S]*)",
    command=("lmkp", plugin_category),
    info={
        "header": "Searches the given query in indian kanoon and shows you the link of that query.",
        "usage": "{tr}lmkp <Query>",
    },
)
async def kanun(event):
    "Searches the given query in indian kanoon and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(event, "**ಠ∀ಠ Give me text to search..**")
    sample_url = f"https://indiankanoon.org/search/?formInput={input_str.replace(' ', '+')}+sortby%3Amostrecent"
    await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me **Indiankanoon.com : Place** that for you:\n👉 [{input_str}]({sample_url})\n`Thank me later 😉` ",
    )


@catub.cat_cmd(
    pattern="gem(?: |$)([\s\S]*)",
    command=("gem", plugin_category),
    info={
        "header": "Searches the given query in Government e marketplace and shows you the link of that query.",
        "usage": "{tr}gem <Query>",
    },
)
async def gem(event):
    "Searches the given query in Government e marketplace and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(event, "**ಠ∀ಠ Give me text to search..**")
    sample_url = f"https://mkp.gem.gov.in/search?q={input_str.replace(' ', '+')}&sort_type=created_at_desc&_xhr=1"
    await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me **gem.gov.in** that for you:\n👉 [{input_str}]({sample_url})\n`Thank me later 😉` ",
    )


@catub.cat_cmd(
    pattern="archive(?: |$)([\s\S]*)",
    command=("archive", plugin_category),
    info={
        "header": "Searches the given query in web archive and shows you the link of that query.",
        "usage": "{tr}archive <Query>",
    },
)
async def archive(event):
    "Searches the given query in web archive and shows you the link of that query."
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str and reply:
        input_str = reply.text
    if not input_str:
        return await edit_delete(event, "**ಠ∀ಠ Give me text to search..**")
    sample_url = f"https://da.gd/s?url=https://web.archive.org/web/*/{input_str.replace(' ', '+')}"
    await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    await edit_or_reply(
        event,
        f"Let me run your link on wayback machine that for you:\n👉 [{input_str}]({sample_url})\n`Thank me later 😉` ",
    )

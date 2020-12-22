from asyncio import sleep

import requests


@bot.on(admin_cmd(pattern="lmg (.*)"))
@bot.on(sudo_cmd(pattern="lmg (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=http://google.com/search?q={}".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me **Google** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@bot.on(admin_cmd(pattern="lmy (.*)"))
@bot.on(sudo_cmd(pattern="lmy (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = (
        "https://da.gd/s?url=https://www.youtube.com/results?search_query={}".format(
            input_str.replace(" ", "+")
        )
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me **youtube** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@bot.on(admin_cmd(pattern="ddg (.*)"))
@bot.on(sudo_cmd(pattern="ddg (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = (
        "https://da.gd/s?url=https://duckduckgo.com/?q={}&t=h_&ia=about".format(
            input_str.replace(" ", "+")
        )
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me **duckduckgo** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@bot.on(admin_cmd(pattern="lmalt (.*)"))
@bot.on(sudo_cmd(pattern="lmalt (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://www.altnews.in/?s={}".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me **altnews** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@bot.on(admin_cmd(pattern="lmvar (.*)"))
@bot.on(sudo_cmd(pattern="lmvar (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = (
        "https://da.gd/s?url=https://dashboard.heroku.com/apps/{}/settings".format(
            input_str.replace(" ", "+")
        )
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me **var** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@bot.on(admin_cmd(pattern="lmlog (.*)"))
@bot.on(sudo_cmd(pattern="lmlog (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://dashboard.heroku.com/apps/{}/logs".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me **log** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@bot.on(admin_cmd(pattern="dyno (.*)"))
@bot.on(sudo_cmd(pattern="dyno (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://dashboard.heroku.com/account/{}".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me **dyno** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@bot.on(admin_cmd(pattern="lmkp (.*)"))
@bot.on(sudo_cmd(pattern="lmkp (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://indiankanoon.org/search/?formInput={}+sortby%3Amostrecent".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me **Indiankanoon.com : Place** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@bot.on(admin_cmd(pattern="gem (.*)"))
@bot.on(sudo_cmd(pattern="gem (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://mkp.gem.gov.in/search?q={}&sort_type=created_at_desc&_xhr=1".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me **gem.gov.in** that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


@bot.on(admin_cmd(pattern="archive (.*)"))
@bot.on(sudo_cmd(pattern="archive (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = "https://da.gd/s?url=https://web.archive.org/web/*/{}".format(
        input_str.replace(" ", "+")
    )
    response_api = requests.get(sample_url).text
    event = await edit_or_reply(event, "`Searching.....`")
    await sleep(2)
    if response_api:
        await event.edit(
            "Let me run your link on wayback machine that for you:\n👉 [{}]({})\n`Thank me later 😉` ".format(
                input_str, response_api.rstrip()
            )
        )
    else:
        await edit_delete(event, "`Something went wrong. Please try again later.`", 5)


CMD_HELP.update(
    {
        "letmesearch": """**Plugin : **`letmesearch`

**Syntax : **
  •  `.lmg query`
  •  `.lmy query`
  •  `.ddg query`
  •  `.lmalt query`
  •  `.lmvar heroku app name`
  •  `.lmlog heroku app name`
  •  `.dyno heroku app name`
  •  `.lmkp query`
  •  `.gem query`
  •  `.archive query`

**Functions : **__searches the given query and shows you the link of that query . here are there sites \
let me google(lmg),let me youtube(lmy),Duck buck go (ddg) , let me altnews(lmalt), \
let me var(lmvar) var from heroku ,let me log(lmlog) logs link for heroku , heroku dyno link (dyno) \
indian kanoon (lmkp) , Government e marketplace(gem) , web archive (archive)__\
"""
    }
)

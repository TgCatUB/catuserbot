import asyncio
import calendar
import random

import bs4
import requests
from telethon import functions
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from . import mention

plugin_category = "utils"

chr = Config.COMMAND_HAND_LER
GBOT = "@HowGayBot"
FBOT = "@FsInChatBot"

# t.me/Lal_Bakthan
@catub.cat_cmd(
    pattern="countdown(?:\s|$)([\s\S]*)",
    command=("countdown", plugin_category),
    info={
        "header": "countdown",
        "description": "countdown till 0 from given seconds. use at your own risk.",
        "usage": "{tr}countdown <seconds>",
    },
)
async def _(event):
    "countdown till 0 from given seconds. use at your own risk."
    if event.fwd_from:
        return
    try:
        total = event.pattern_match.group(1)
        if not total:
            await edit_delete(event, f"**Usage:** `{chr}countdown <seconds>`", 10)
            return
        t = int(total)
        pluto = await edit_or_reply(event, f"Counter Starting for {total} seconds.")
        while t >= 0:
            mins, secs = divmod(t, 60)
            timer = "{:02d}:{:02d}".format(mins, secs)
            await pluto.edit(str(timer))
            await asyncio.sleep(1)
            t -= 1
        await event.reply(f"Countdown for {total} seconds completed.")
    except Exception as e:
        await edit_delete(event, f"`{e}`", 7)


# t.me/realnub
@catub.cat_cmd(
    pattern="gey(?:\s|$)([\s\S]*)",
    command=("gey", plugin_category),
    info={
        "header": "try yourself.",
        "description": "try yourself.",
        "usage": "{tr}gey <name>.",
    },
)
async def app_search(event):
    "try yourself"
    name = event.pattern_match.group(1)
    if not name:
        name = " "
    event = await edit_or_reply(event, "`Calculating!..`")
    id = await reply_id(event)
    try:
        score = await event.client.inline_query(GBOT, name)
        await score[0].click(event.chat_id, reply_to=id, hide_via=True)
        await event.delete()
    except Exception as err:
        await event.edit(str(err))


# t.me/realnub
@catub.cat_cmd(
    pattern="fr(?:\s|$)([\s\S]*)",
    command=("fr", plugin_category),
    info={
        "header": "Pay Respect.",
        "description": "Press F to Pay Respect.",
        "usage": "{tr}fr <text>.",
    },
)
async def app_search(event):
    "Press F to Pay Respect."
    czy = event.pattern_match.group(1)
    if not czy:
        czy = " "
    event = await edit_or_reply(event, "`Processing!..`")
    id = await reply_id(event)
    try:
        if not czy:
            czy = " "
        pluto = await event.client.inline_query(FBOT, czy)
        await pluto[0].click(event.chat_id, reply_to=id, hide_via=True)
        await event.delete()
    except Exception as err:
        await event.edit(str(err))


# t.me/realnub & t.me/amnd33p
@catub.cat_cmd(
    pattern="iapp(?:\s|$)([\s\S]*)",
    command=("iapp", plugin_category),
    info={
        "header": "To search any app in playstore via inline.",
        "description": "Searches the app in the playstore and provides the link to the app in playstore and fetches app details via inline.",
        "usage": "{tr}iapp <name>",
    },
)
async def app_search(event):
    "To search any app in playstore via inline."
    app_name = event.pattern_match.group(1)
    if not app_name:
        await edit_delete(event, f"**Usage:** `{chr}iapp <name>`", 10)
        return
    reply_to_id = await reply_id(event)
    event = await edit_or_reply(event, "`Searching!..`")
    try:
        remove_space = app_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            "https://play.google.com/store/search?q=" + final_name + "&c=apps"
        )
        str(page.status_code)
        soup = bs4.BeautifulSoup(page.content, "lxml", from_encoding="utf-8")
        results = soup.findAll("div", "ZmHEEd")
        app_name = (
            results[0].findNext("div", "Vpfmgd").findNext("div", "WsMG1c nnK0zc").text
        )
        app_dev = results[0].findNext("div", "Vpfmgd").findNext("div", "KoLSrc").text
        app_dev_link = (
            "https://play.google.com"
            + results[0].findNext("div", "Vpfmgd").findNext("a", "mnKHRc")["href"]
        )
        app_rating = (
            results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "pf5lIe")
            .find("div")["aria-label"]
        )
        app_link = (
            "https://play.google.com"
            + results[0]
            .findNext("div", "Vpfmgd")
            .findNext("div", "vU6FJ p63iDd")
            .a["href"]
        )

        app_details = "**App Name:** " + app_name + "\n**Developer:** "
        app_details += f"[{app_dev}]({app_dev_link})" + "\n**Rating:**"
        app_details += (
            app_rating.replace("Rated ", " ")
            .replace(" out of ", "/")
            .replace(" stars", "", 1)
            .replace(" stars", " ⭐ ")
            .replace("five", "5")
        )
        catinput = "Inline buttons " + app_details
        catinput += f" [DOWNLOAD]<buttonurl:{app_link}>"
        results = await event.client.inline_query(Config.TG_BOT_USERNAME, catinput)
        await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
        await event.delete()

    except IndexError:
        await event.edit("No result found in search. Please enter **Valid app name**")
    except Exception as err:
        await event.edit("Exception Occured:- " + str(err))


# t.me/realnub
@catub.cat_cmd(
    pattern="cid(?:\s|$)([\s\S]*)",
    command=("cid", plugin_category),
    info={
        "header": "To search a phone number in Truecaller",
        "description": "Searches the given number in the truecaller and provides the details.",
        "usage": "{tr}cid <phone>",
    },
)
async def _(event):
    "To search a phone number in Truecaller"
    args = event.pattern_match.group(1)
    if not args:
        await edit_or_reply(event, f"**Usage:** `{chr}cid <number>`")
        return
    pluto = await edit_or_reply(event, "**__Fetching details...__**")
    chat = "@RespawnRobot"
    await reply_id(event)
    async with event.client.conversation(chat) as conv:
        try:
            await conv.send_message("/start")
            await conv.get_response()
            await conv.send_message("🏙 Theme")
            await conv.get_response()
            await conv.send_message("Box")
            await conv.get_response()
            await conv.send_message(args)
            check = await conv.get_response()
            replace = check.text
            info = replace.replace(
                "════━(@RespawnRobot)━════", f"════━({mention})━════"
            )
            await event.client.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await event.client(functions.contacts.UnblockRequest(chat))
            await edit_delete(
                pluto,
                f"__**An error occurred. Please try again!\n☞**__ `{chr}cid {args}`",
                10,
            )
            return
        await pluto.edit(info)
    await event.client.delete_dialog(chat)

@catub.cat_cmd(
    pattern="mcq ?(.*)",
    command=("mcq", plugin_category),
    info={
        "header": "Chooses a random item in the given options, give a comma ',' to add multiple option",
        "usage": [
            "{tr}mcq <options>",
            "{tr}mcq a,b,c,d",
            "{tr}mcq cat,dog,life,death"
        ],
    },
)
async def Gay(event):
    "Chooses a random item in the given options, give a comma ',' to add multiple option"
    osho = event.pattern_match.group(1)
    if not inp:
        return await edit_delete(event, "`What to choose from`", 10)
    options = osho.split(',')
    await event.edit(f"**Input :** `{inp}`\n**Result :** `{random.choice(options)}`")


@catub.cat_cmd(
    pattern="ycal(?:\s|$)([\s\S]*)",
    command=("ycal", plugin_category),
    info={
        "header": "To get calendar of the given year.",
        "usage": "{tr}ycal year",
        "examples": "{tr}ycal 2021\n\nNote: please view this calendar from a pc",
    },
)
async def _(event):
    "To get the calendar of the given year."
    pluto = event.pattern_match.group(1)
    year = pluto
    if not year:
        await edit_delete(event, f"**Usage:** `{chr}ycal <year>`", 10)
        return
    try:
        cal = calendar.calendar(int(year))
        await edit_or_reply(event, f"`{cal}`")
    except Exception as e:
        await edit_delete(event, f"`{e}`", 7)


# t.me/realnub

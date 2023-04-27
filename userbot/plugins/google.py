""" Reverse search image and Google search """

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import os
import re
from datetime import datetime

from search_engine_parser import BingSearch, GoogleSearch, YahooSearch
from search_engine_parser.core.exceptions import NoResultsOrTrafficError

from userbot import BOTLOG, BOTLOG_CHATID, Convert, catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import deEmojify, unsavegif
from ..helpers.google_tools import GooglePic, chromeDriver
from ..helpers.utils import reply_id

plugin_category = "tools"


@catub.cat_cmd(
    pattern="gs ([\s\S]*)",
    command=("gs", plugin_category),
    info={
        "header": "Google search command.",
        "flags": {
            "-l": "for number of search results.",
            "-p": "for choosing which page results should be showed.",
        },
        "usage": [
            "{tr}gs <flags> <query>",
            "{tr}gs <query>",
        ],
        "examples": [
            "{tr}gs catuserbot",
            "{tr}gs -l6 catuserbot",
            "{tr}gs -p2 catuserbot",
            "{tr}gs -p2 -l7 catuserbot",
        ],
    },
)
async def gsearch(q_event):
    "Google search command."
    catevent = await edit_or_reply(q_event, "`searching........`")
    match = q_event.pattern_match.group(1)
    page = re.findall(r"-p\d+", match)
    lim = re.findall(r"-l\d+", match)
    try:
        page = page[0]
        page = page.replace("-p", "")
        match = match.replace(f"-p{page}", "")
    except IndexError:
        page = 1
    try:
        lim = lim[0]
        lim = lim.replace("-l", "")
        match = match.replace(f"-l{lim}", "")
        lim = int(lim)
        if lim <= 0:
            lim = 5
    except IndexError:
        lim = 5
    #     smatch = urllib.parse.quote_plus(match)
    smatch = match.replace(" ", "+")
    search_args = str(smatch), page
    gsearch = GoogleSearch()
    bsearch = BingSearch()
    ysearch = YahooSearch()
    try:
        gresults = await gsearch.async_search(*search_args)
    except NoResultsOrTrafficError:
        try:
            gresults = await bsearch.async_search(*search_args)
        except NoResultsOrTrafficError:
            try:
                gresults = await ysearch.async_search(*search_args)
            except Exception as e:
                return await edit_delete(catevent, f"**Error:**\n`{e}`", time=10)
    msg = ""
    for i in range(lim):
        if i > len(gresults["links"]):
            break
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"👉[{title}]({link})\n`{desc}`\n\n"
        except IndexError:
            break
    await edit_or_reply(
        catevent,
        "**Search Query:**\n`" + match + "`\n\n**Results:**\n" + msg,
        link_preview=False,
        aslink=True,
        linktext=f"**The search results for the query **__{match}__ **are** :",
    )
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            f"Google Search query `{match}` was executed successfully",
        )


@catub.cat_cmd(
    pattern="gis ([\s\S]*)",
    command=("gis", plugin_category),
    info={
        "header": "Google search in image format",
        "usage": "{tr}gis <query>",
        "examples": "{tr}gis cat",
    },
)
async def gis(event):
    "To search in google and send result in picture."


@catub.cat_cmd(
    pattern="grs$",
    command=("grs", plugin_category),
    info={
        "header": "Google reverse search command.",
        "description": "Reverse search replied media in google and shows results.",
        "usage": "{tr}grs",
    },
)
async def grs(event):
    "Google Reverse Search"


@catub.cat_cmd(
    pattern="(grs|reverse)(?:\s|$)([\s\S]*)",
    command=("reverse", plugin_category),
    info={
        "header": "Google reverse search command.",
        "description": "Reverse search replied media in google and shows results. If count is not used then it send 3 image by default.",
        "usage": "{tr}reverse < 1 - 10 >",
    },
)
async def reverse(event):
    "Google Reverse Search"
    start = datetime.now()
    reply_to = await reply_id(event)
    cmd = event.pattern_match.group(1)
    message = await event.get_reply_message()
    limit = event.pattern_match.group(2) or "3"
    # limit checker for .reverse
    if int(limit) < 1 or int(limit) > 10:
        return await edit_or_reply(event, "`Give a limit between 1-10`")
    if not message and not message.media:
        return await edit_or_reply(event, "`Reply to media...`")
    # convert media file into image to search in google
    photo = await Convert.to_image(
        event, message, dirct="./temp", file="reverse.png", noedits=True
    )
    if photo[1] is None:
        return await edit_delete(
            event, "`Unable to extract image from the replied message..`"
        )
    catevent = await edit_or_reply(event, "`Processing...`")
    # get data accoding to cmd
    flag = cmd != "grs"
    data = GooglePic.reverse_data(photo[1], flag)
    if data["error"]:
        return await edit_delete(catevent, data["error"])
    if data["lens"] is None:
        return await edit_delete(catevent, "`Couldn't find any reverse data..`")
    outfile = "./temp/reverse.png"
    imagelist, captionlist, gifstring = [], [], ""
    if cmd == "grs":
        # save screenshot from lens url
        pic, _ = await chromeDriver.get_screenshot(data["lens"])
        if pic:
            with open(outfile, "wb") as file:
                file.write(pic)
    else:
        for checker, item in enumerate(data["image_set"], 1):
            url = (
                item.image
                if item.image.endswith((".jpg", ".jpeg", ".png", ".gif"))
                else item.site
            )
            # scamming telethon to send media as album
            # gif file can't album so doing single
            try:
                image = await catub.send_file(BOTLOG_CHATID, url, silent=True)
                if url.endswith(".gif"):
                    await unsavegif(event, image)
                    giflink = await catub.get_msg_link(image)
                    gifstring += f'<b><a href="{giflink}">Gif{checker}</a></b>  '
                elif not url.endswith(".gif"):
                    imagelist.append(image.media)
                    captionlist.append("")
                    await image.delete()
                await edit_or_reply(catevent, f"**📥 Downloaded : {checker}/{limit}**")
                if checker >= int(limit):
                    break
            except Exception:
                pass

    end = datetime.now()
    ms = (end - start).seconds
    caption = f'<b>➥ Google Reverse Search:</b>  <code>{data["title"]}</code>\n<b>➥ View Source: <a href="{data["google"]}">Google Image</a></b>\n<b>➥ View Similar: <a href="{data["lens"]}">Google Lens</a> </b>(Desktop)\n<b>➥ Time Taken:</b>  <code>{ms} seconds</code>'
    # if no similar image found save the replied image to respond
    if not imagelist:
        imagelist.append(outfile)
        captionlist.append("")
    if gifstring:
        caption = caption + "\n\n<b>➥ Found Gif:</b>  " + gifstring
    captionlist[-1] = caption
    await catevent.delete()
    await catub.send_file(
        event.chat_id,
        imagelist,
        caption=captionlist,
        parse_mode="html",
        reply_to=reply_to,
    )
    if os.path.exists(outfile):
        os.remove(outfile)


@catub.cat_cmd(
    pattern="google(?:\s|$)([\s\S]*)",
    command=("google", plugin_category),
    info={
        "header": "To get link for google search",
        "description": "Will show google search link as button instead of google search results try {tr}gs for google search results.",
        "usage": [
            "{tr}google query",
        ],
    },
)
async def google_search(event):
    "Will show you google search link of the given query."
    input_str = event.pattern_match.group(1)
    reply_to_id = await reply_id(event)
    if not input_str:
        return await edit_delete(
            event, "__What should i search? Give search query plox.__"
        )
    input_str = deEmojify(input_str).strip()
    if len(input_str) > 195 or len(input_str) < 1:
        return await edit_delete(
            event,
            "__Plox your search query exceeds 200 characters or you search query is empty.__",
        )
    query = f"#12{input_str}"
    results = await event.client.inline_query("@StickerizerBot", query)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()

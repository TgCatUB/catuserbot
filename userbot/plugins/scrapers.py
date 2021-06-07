# Userbot module containing various scrapers.
# Copyright (C) 2019 The Raphielscape Company LLC.(some are ported from there)
# Copyright (c) JeepBot | 2019(for imdb)
# # kanged from Blank-x ;---;

import re

import bs4
import requests
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.utils.format import paste_text
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"


@catub.cat_cmd(
    pattern="wiki (.*)",
    command=("wiki", plugin_category),
    info={
        "header": "To get wikipedia data about query.",
        "usage": "{tr}wiki <query>",
    },
)
async def wiki(event):
    """To fetch content from Wikipedia."""
    match = event.pattern_match.group(1)
    result = None
    try:
        result = summary(match, auto_suggest=False)
    except DisambiguationError as error:
        error = str(error).split("\n")
        result = "".join(
            f"`{i}`\n" if lineno > 1 else f"**{i}**\n"
            for lineno, i in enumerate(error, start=1)
        )
        return await edit_or_reply(event, f"**Disambiguated page found.**\n\n{result}")
    except PageError:
        pass
    if not result:
        try:
            result = summary(match, auto_suggest=True)
        except DisambiguationError as error:
            error = str(error).split("\n")
            result = "".join(
                f"`{i}`\n" if lineno > 1 else f"**{i}**\n"
                for lineno, i in enumerate(error, start=1)
            )
            return await edit_or_reply(
                event, f"**Disambiguated page found.**\n\n{result}"
            )
        except PageError:
            return await edit_or_delete(
                event, f"**Sorry i Can't find any results for **`{match}`"
            )
    await edit_or_reply(
        event, "**Search:**\n`" + match + "`\n\n**Result:**\n" + f"__{result}__"
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"Wiki query `{match}` was executed successfully"
        )


@catub.cat_cmd(
    pattern="imdb (.*)",
    command=("imdb", plugin_category),
    info={
        "header": "To fetch imdb data about the given movie or series.",
        "usage": "{tr}imdb <movie/series name>",
    },
)
async def imdb(event):  # sourcery no-metrics
    """To fetch imdb data about the given movie or series."""
    catevent = await edit_or_reply(event, "`searching........`")
    try:
        movie_name = event.pattern_match.group(1)
        remove_space = movie_name.split(" ")
        final_name = "+".join(remove_space)
        page = requests.get(
            "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name + "&s=all"
        )
        soup = bs4.BeautifulSoup(page.content, "lxml")
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext("td").findNext("td").text
        mov_link = (
            "http://www.imdb.com/" + odds[0].findNext("td").findNext("td").a["href"]
        )
        page1 = requests.get(mov_link)
        soup = bs4.BeautifulSoup(page1.content, "lxml")
        print(paste_text(str(soup)))
        if soup.find("div", "poster"):
            poster = soup.find("div", "poster").img["src"]
        else:
            poster = ""
        if soup.find("div", "title_wrapper"):
            pg = soup.find("div", "title_wrapper").findNext("div").text
            mov_details = re.sub(r"\s+", " ", pg)
        else:
            mov_details = ""
        moviecredits = soup.findAll("div", "credit_summary_item")
        director = moviecredits[0].a.text
        if len(moviecredits) == 1:
            writer = "Not available"
            stars = "Not available"
        elif len(moviecredits) > 2:
            writer = moviecredits[1].a.text
            actors = [x.text for x in moviecredits[2].findAll("a")]
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        else:
            writer = "Not available"
            actors = [x.text for x in moviecredits[1].findAll("a")]
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        if soup.find("div", "inline canwrap"):
            story_line = soup.find("div", "inline canwrap").findAll("p")[0].text
        else:
            story_line = "Not available"
        info = soup.findAll("div", "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll("a")
                for i in a:
                    if "country_of_origin" in i["href"]:
                        mov_country.append(i.text)
                    elif "primary_language" in i["href"]:
                        mov_language.append(i.text)
        if soup.findAll("div", "ratingValue"):
            for r in soup.findAll("div", "ratingValue"):
                mov_rating = r.strong["title"]
        else:
            mov_rating = "Not available"
        await catevent.edit(
            "<a href=" + poster + ">&#8203;</a>"
            "<b>Title : </b><code>"
            + mov_title
            + "</code>\n<code>"
            + mov_details
            + "</code>\n<b>Rating : </b><code>"
            + mov_rating
            + "</code>\n<b>Country : </b><code>"
            + mov_country[0]
            + "</code>\n<b>Language : </b><code>"
            + mov_language[0]
            + "</code>\n<b>Director : </b><code>"
            + director
            + "</code>\n<b>Writer : </b><code>"
            + writer
            + "</code>\n<b>Stars : </b><code>"
            + stars
            + "</code>\n<b>IMDB Url : </b>"
            + mov_link
            + "\n<b>Story Line : </b>"
            + story_line,
            link_preview=True,
            parse_mode="HTML",
        )
    except IndexError:
        await catevent.edit("Plox enter **Valid movie name** kthx")

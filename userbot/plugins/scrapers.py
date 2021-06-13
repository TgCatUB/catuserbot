import os

import bs4
import requests
from pySmartDL import SmartDL
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"
moviepath = os.path.join(os.getcwd(), "temp", "moviethumb.jpg")


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
    reply_to = await reply_id(event)
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
        mov_details = ""
        info_details = soup.find("ul", attrs={"class": "ipc-inline-list"})
        if info_details and [
            "titleblockmetadata" in a.lower() for a in info_details.attrs["class"]
        ]:
            for movdetails in info_details.findAll("li"):
                if movdetails.span:
                    mov_details += (
                        " | " + movdetails.span.text.strip()
                        if mov_details != ""
                        else movdetails.span.text.strip()
                    )
                else:
                    mov_details += (
                        " | " + movdetails.text.strip()
                        if mov_details != ""
                        else movdetails.text.strip()
                    )
        else:
            mov_details = "Not Found!"
        mov_geners = ""
        movgeners = soup.find("div", attrs={"class": "ipc-chip-list"})
        if movgeners:
            for gener in movgeners.findAll("a"):
                mov_geners += (
                    " | " + gener.text.strip()
                    if mov_geners != ""
                    else gener.text.strip()
                )
        else:
            mov_geners = "Not Found!"
        movrating = soup.find(
            "div", attrs={"data-testid": "hero-title-block__aggregate-rating__score"}
        )
        if movrating:
            rating = [rate.text for rate in movrating]
            voted_users = movrating.findNext("div").findNext("div").text
            mov_rating = f"{rating[0]}{rating[1]} based on {voted_users} users ratings."
        else:
            mov_rating = "Not available"
        mov_country = ""
        mov_language = ""
        mov_location = soup.find("div", attrs={"data-testid": "title-details-section"})
        if mov_location:
            for li in mov_location.findNext("ul"):
                detail_header = li.span.text if li.span else None
                if detail_header == "Country of origin":
                    for ct in li.findAll(
                        "a",
                        attrs={"class": "ipc-metadata-list-item__list-content-item"},
                    ):
                        mov_country += (
                            ", " + ct.text.strip()
                            if mov_country != ""
                            else ct.text.strip()
                        )
                elif detail_header == "Languages":
                    for lg in li.findAll(
                        "a",
                        attrs={"class": "ipc-metadata-list-item__list-content-item"},
                    ):
                        mov_language += (
                            ", " + lg.text.strip()
                            if mov_language != ""
                            else lg.text.strip()
                        )
        if mov_country == "":
            mov_country = "Not Found!"
        if mov_language == "":
            mov_language = "Not Found!"
        directors = ""
        writers = ""
        stars = ""
        mov_credit = soup.find("ul", attrs={"class": "ipc-metadata-list"})
        if mov_credit:
            for data in mov_credit:
                credit_name = data.span.text if data.span else data.a.text
                for credit in data.findAll(
                    "a", {"class": "ipc-metadata-list-item__list-content-item"}
                ):
                    if credit_name == "Director":
                        directors += (
                            ", " + credit.text.strip()
                            if directors != ""
                            else credit.text.strip()
                        )
                    if credit_name == "Writers":
                        writers += (
                            ", " + credit.text.strip()
                            if writers != ""
                            else credit.text.strip()
                        )
                    if credit_name == "Stars":
                        stars += (
                            ", " + credit.text.strip()
                            if stars != ""
                            else credit.text.strip()
                        )
        if directors == "":
            directors = "Not Found!"
        if writers == "":
            writers = "Not Found!"
        if stars == "":
            stars = "Not Found!"
        story = soup.find(
            "div", attrs={"class": "ipc-html-content ipc-html-content--base"}
        )
        story_line = story.findAll("div")[0].text if story else "Not available"
        imageurl = None
        image_link = soup.find("a", attrs={"class": "ipc-lockup-overlay ipc-focusable"})
        if image_link:
            image_content = requests.get(
                "https://imdb.com"
                + image_link.get("href").replace("/?ref_=tt_ov_i", "")
            )
            soup = bs4.BeautifulSoup(image_content.content, "lxml")
            for i in soup.findAll("img"):
                if "portraitimage" in i.attrs["class"][0].lower():
                    imageurl = i.get("src")
        resulttext = f"""<b>Title : </b><code>{mov_title}</code>
<b>Info : </b><code>{mov_details}</code>
<b>Genres : </b><code>{mov_geners}</code>
<b>Rating : </b><code>{mov_rating}</code>
<b>Country : </b><code>{mov_country}</code>
<b>Language : </b><code>{mov_language}</code>
<b>Director : </b><code>{directors}</code>
<b>Writer : </b><code>{writers}</code>
<b>Stars : </b><code>{stars}</code>
<b>IMDB Url : </b>{mov_link}

<b>Story Line : </b><i>{story_line}</i>"""
        if imageurl:
            downloader = SmartDL(imageurl, moviepath, progress_bar=False)
            downloader.start(blocking=False)
            while not downloader.isFinished():
                pass
        if os.path.exists(moviepath):
            await event.client.send_file(
                event.chat_id,
                moviepath,
                caption=resulttext,
                reply_to=reply_to,
                parse_mode="HTML",
            )
            os.remove(moviepath)
            return await catevent.delete()
        await catevent.edit(
            resulttext,
            link_preview=False,
            parse_mode="HTML",
        )
    except IndexError:
        await catevent.edit("Plox enter **Valid movie name** kthx")

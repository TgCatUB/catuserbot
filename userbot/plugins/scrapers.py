import os

from bs4 import BeautifulSoup
from pySmartDL import SmartDL
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

from userbot import catub

from ..core.managers import edit_or_reply
from ..helpers.functions import get_cast, get_moviecollections, imdb, mov_titles
from ..helpers.utils import reply_id
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"
moviepath = os.path.join(os.getcwd(), "temp", "moviethumb.jpg")


@catub.cat_cmd(
    pattern="wiki ([\s\S]*)",
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
    pattern="imdb ([\s\S]*)",
    command=("imdb", plugin_category),
    info={
        "header": "To fetch imdb data about the given movie or series.",
        "usage": "{tr}imdb <movie/series name>",
    },
)
async def imdb_query(event):  # sourcery no-metrics
    """To fetch imdb data about the given movie or series."""
    catevent = await edit_or_reply(event, "`searching........`")
    reply_to = await reply_id(event)
    try:
        movie_name = event.pattern_match.group(1)
        movies = imdb.search_movie(movie_name)
        movieid = movies[0].movieID
        movie = imdb.get_movie(movieid)
        moviekeys = list(movie.keys())
        for i in mov_titles:
            if i in moviekeys:
                mov_title = movie[i]
                break
        for j in reversed(mov_titles):
            if j in moviekeys:
                mov_ltitle = movie[j]
                break
        mov_runtime = movie["runtimes"][0] + " min" if "runtimes" in movie else ""
        if "original air date" in moviekeys:
            mov_airdate = movie["original air date"]
        elif "year" in moviekeys:
            mov_airdate = movie["year"]
        else:
            mov_airdate = ""
        mov_genres = ", ".join(movie["genres"]) if "genres" in moviekeys else "Not Data"
        mov_rating = str(movie["rating"]) if "rating" in moviekeys else "Not Data"
        mov_rating += (
            " (by " + str(movie["votes"]) + ")"
            if "votes" in moviekeys and "rating" in moviekeys
            else ""
        )
        mov_countries = (
            ", ".join(movie["countries"]) if "countries" in moviekeys else "Not Data"
        )
        mov_languages = (
            ", ".join(movie["languages"]) if "languages" in moviekeys else "Not Data"
        )
        mov_plot = (
            str(movie["plot outline"]) if "plot outline" in moviekeys else "Not Data"
        )
        mov_director = await get_cast("director", movie)
        mov_composers = await get_cast("composers", movie)
        mov_writer = await get_cast("writer", movie)
        mov_cast = await get_cast("cast", movie)
        mov_box = await get_moviecollections(movie)
        resulttext = f"""
<b>Title : </b><code>{mov_title}</code>
<b>Imdb Url : </b><a href='https://www.imdb.com/title/tt{movieid}'>{mov_ltitle}</a>
<b>Info : </b><code>{mov_runtime} | {mov_airdate}</code>
<b>Genres : </b><code>{mov_genres}</code>
<b>Rating : </b><code>{mov_rating}</code>
<b>Country : </b><code>{mov_countries}</code>
<b>Language : </b><code>{mov_languages}</code>
<b>Director : </b><code>{mov_director}</code>
<b>Music Director : </b><code>{mov_composers}</code>
<b>Writer : </b><code>{mov_writer}</code>
<b>Stars : </b><code>{mov_cast}</code>
<b>Box Office : </b>{mov_box}
<b>Story Outline : </b><i>{mov_plot}</i>"""
        if "full-size cover url" in moviekeys:
            imageurl = movie["full-size cover url"]
        else:
            imageurl = None
        soup = BeautifulSoup(resulttext, features="html.parser")
        rtext = soup.get_text()
        if len(rtext) > 1024:
            extralimit = len(rtext) - 1024
            climit = len(resulttext) - extralimit - 20
            resulttext = resulttext[:climit] + "...........</i>"
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
        await catevent.edit(f"__No movie found with name {movie_name}.__")
    except Exception as e:
        await catevent.edit(f"**Error:**\n__{e}__")

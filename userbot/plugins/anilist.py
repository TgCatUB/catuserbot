import contextlib
import html
import os
import re
import textwrap
from datetime import datetime
from urllib.parse import quote_plus

import aiohttp
import bs4
import requests
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from pySmartDL import SmartDL
from telegraph import exceptions, upload_file

from userbot import Convert, catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, readable_time, reply_id, time_formatter
from ..helpers.functions import (
    airing_query,
    anilist_user,
    anime_json_synomsis,
    callAPI,
    character_query,
    formatJSON,
    get_anime_manga,
    get_anime_schedule,
    get_filler_episodes,
    getBannerLink,
    memory_file,
    post_to_telegraph,
    search_in_animefiller,
    searchanilist,
    weekdays,
)

jikan = Jikan()

anilistapiurl = "https://graphql.anilist.co"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
}

ppath = os.path.join(os.getcwd(), "temp", "anilistuser.jpg")
anime_path = os.path.join(os.getcwd(), "temp", "animeresult.jpg")

plugin_category = "extra"


@catub.cat_cmd(
    pattern="aq$",
    command=("aq", plugin_category),
    info={
        "header": "Get random Anime quotes.",
        "usage": "{tr}aq",
        "examples": "{tr}aq",
    },
)
async def anime_quote(event):
    data = requests.get("https://animechan.vercel.app/api/random").json()
    anime = data["anime"]
    character = data["character"]
    quote = data["quote"]
    await edit_or_reply(
        event,
        f"• <b>Anime</b> (アニメ) <b>:</b>\n ➥ <i>{anime}</i>\n\n• <b>Character:</b> (キャラクター) <b>:</b>\n ➥ <i>{character}</i>\n\n• <b>Quote:</b> (言っている) <b>:</b>\n ➥ <i>{quote}</i>",
        parse_mode="html",
    )


@catub.cat_cmd(
    pattern="aluser(?:\s|$)([\s\S]*)",
    command=("aluser", plugin_category),
    info={
        "header": "Search User profiles in anilist.",
        "usage": "{tr}aluser <username>",
        "examples": "{tr}aluser Infinity20998",
    },
)
async def anilist_usersearch(event):
    "Search user profiles of Anilist."
    search_query = event.pattern_match.group(1)
    reply_to = await reply_id(event)
    reply = await event.get_reply_message()
    if not search_query:
        if reply and reply.text:
            search_query = reply.text
        else:
            return await edit_delete(event, "__Whom should i search.__")
    catevent = await edit_or_reply(event, "`Searching user profile in anilist...`")
    searchresult = await anilist_user(search_query)
    if len(searchresult) == 1:
        return await edit_or_reply(
            catevent, f"**Error while searching user profile:**\n{searchresult[0]}"
        )
    downloader = SmartDL(searchresult[1], ppath, progress_bar=False)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        pass
    await event.client.send_file(
        event.chat_id,
        ppath,
        caption=searchresult[0],
        reply_to=reply_to,
    )
    os.remove(ppath)
    await catevent.delete()


@catub.cat_cmd(
    pattern="mal(?:\s|$)([\s\S]*)",
    command=("mal", plugin_category),
    info={
        "header": "Search profiles of MAL.",
        "usage": "{tr}mal <username>",
        "examples": "{tr}mal Infinity20998",
    },
)
async def user(event):
    "Search profiles of MAL."
    search_query = event.pattern_match.group(1)
    replyto = await reply_id(event)
    reply = await event.get_reply_message()
    if not search_query:
        if reply and reply.text:
            search_query = reply.text
        else:
            return await edit_delete(event, "__Whom should i search.__")
    try:
        user = jikan.user(search_query)
    except APIException:
        return await edit_delete(event, "__No User found with given username__", 5)
    date_format = "%Y-%m-%d"
    img = user["image_url"] or "https://telegra.ph//file/9b4205e1b1cc68a4ffd5e.jpg"
    try:
        user_birthday = datetime.fromisoformat(user["birthday"])
        user_birthday_formatted = user_birthday.strftime(date_format)
    except BaseException:
        user_birthday_formatted = "Unknown"
    user_joined_date = datetime.fromisoformat(user["joined"])
    user_joined_date_formatted = user_joined_date.strftime(date_format)
    user_last_online = datetime.fromisoformat(user["last_online"])
    user_last_online_formatted = user_last_online.strftime(date_format)
    for entity in user:
        if user[entity] is None:
            user[entity] = "Unknown"
    about = user["about"].split(" ", 60)
    with contextlib.suppress(IndexError):
        about.pop(60)
    about_string = " ".join(about)
    about_string = about_string.replace("<br>", "").strip().replace("\r\n", "\n")
    caption = ""
    caption += textwrap.dedent(
        f"""
    **Username:** [{user['username']}]({user['url']})
    **Gender:** `{user['gender']}`
    **MAL ID:** `{user['user_id']}`
    **Birthday:** `{user_birthday_formatted}`
    **Joined:** `{user_joined_date_formatted}`
    **Last Online:** `{user_last_online_formatted}`
    
    **Days wasted watching Anime:** `{user['anime_stats']['days_watched']}`
    **No of completed Animes:** `{user['anime_stats']['completed']}`
    **Total No of episodes Watched:** `{user['anime_stats']['episodes_watched']}`
    **Days wasted reading Manga:** `{user['manga_stats']['days_read']}`
    """
    )

    caption += f"**About:** __{about_string}__"
    await event.client.send_file(
        event.chat_id, file=img, caption=caption, reply_to=replyto
    )
    await event.delete()


@catub.cat_cmd(
    pattern="airing(?:\s|$)([\s\S]*)",
    command=("airing", plugin_category),
    info={
        "header": "Shows you the time left for the new episode of current running anime show.",
        "usage": "{tr}airing",
        "examples": "{tr}airing one piece",
    },
)
async def anilist(event):
    "Get airing date & time of any anime"
    search = event.pattern_match.group(1)
    if not search:
        return await edit_delete(event, "__which anime results should i fetch__")
    variables = {"search": search}
    response = requests.post(
        anilistapiurl, json={"query": airing_query, "variables": variables}
    ).json()["data"]["Media"]
    if response is None:
        return await edit_delete(event, "__Unable to find the anime.__")
    ms_g = f"**Name**: **{response['title']['romaji']}**(`{response['title']['native']}`)\n**ID**: `{response['id']}`"
    if response["nextAiringEpisode"]:
        airing_time = response["nextAiringEpisode"]["timeUntilAiring"]
        airing_time_final = time_formatter(airing_time)
        airing_at = response["nextAiringEpisode"]["airingAt"]
        ms_g += f"\n**Episode**: `{response['nextAiringEpisode']['episode']}`\n**Airing In**: `{airing_time_final}`\n**Time: **`{datetime.fromtimestamp(airing_at)}`"
    else:
        ms_g += f"\n**Episode**:{response['episodes']}\n**Status**: `N/A`"
    await edit_or_reply(event, ms_g)


@catub.cat_cmd(
    pattern="anime(?:\s|$)([\s\S]*)",
    command=("anime", plugin_category),
    info={
        "header": "search anime.",
        "description": "Fetches anime information from anilist",
        "flags": {
            "d": "shows you anime details (another format)",
            "s": "anime search list (shows only anime name and link to anilist)",
            "n": "get details of specific anime number from search list",
        },
        "note": "for flag n you need to use number attached to flag",
        "usage": "{tr}anime <flags> <name of anime>",
        "examples": [
            "{tr}anime fairy tail",
            "{tr}anime -d fairy tail",
            "{tr}anime -s fairy tail",
            "{tr}anime -n3 fairy tail",
        ],
    },
)
async def anilist(event):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    "Get info on any anime."
    reply_to = await reply_id(event)
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str:
        if reply:
            input_str = reply.text
        else:
            return await edit_delete(
                event, "__What should i search ? Gib me Something to Search__"
            )
    match = input_str
    animeno = re.findall(r"-n\d+", match)
    listview = re.findall(r"-s", match)
    myanime = re.findall(r"-d", match)
    specific = bool(animeno)
    try:
        animeno = animeno[0]
        animeno = animeno.replace("-n", "")
        match = match.replace(f"-n{animeno}", "")
        animeno = int(animeno)
    except IndexError:
        animeno = 1
    if animeno < 1 or animeno > 10:
        return await edit_or_reply(
            event,
            "`anime number must be in between 1 to 10 use -l flag to query results`",
        )
    catevent = await edit_or_reply(event, "`Searching Anime..`")
    match = match.replace("-s", "")
    listview = bool(listview)
    match = match.replace("-d", "")
    myanime = bool(myanime)
    query = match.strip()
    result, respone = await searchanilist(query)
    if not respone:
        return await edit_delete(catevent, result)
    if len(result) == 0:
        return await edit_or_reply(
            catevent, f"**Search query:** `{query}`\n**Result:** `No results found`"
        )
    input_str = result[0]["title"]["english"] or result[0]["title"]["romaji"]
    if myanime:
        result = await callAPI(input_str)
        msg = await formatJSON(result)
        await catevent.edit(msg, link_preview=True)
        return
    if listview:
        msg = f"<b>Search Query: </b> <code>{query}</code>\n\n<b>Results:</b>\n"
        i = 1
        ani_data = result
        for result in ani_data:
            if i > 10:
                break
            input_str = result["title"]["english"] or result["title"]["romaji"]
            if result["title"]["english"]:
                msg += f'<b>{i}.</b> <code>{result["title"]["english"]}</code> - <a href="{result["siteUrl"]}">{result["title"]["romaji"]}</a>\n'
            else:
                msg += f'<b>{i}.</b> <code>{result["title"]["romaji"]}</code> - <a href="{result["siteUrl"]}">{result["title"]["native"]}</a>\n'
            i += 1
        await catevent.edit(msg, parse_mode="html")
        return
    input_str = result[animeno - 1]["title"]["romaji"] if specific else query
    caption, image = await get_anime_manga(input_str, "anime_anime", event.chat_id)
    if image is None:
        await edit_or_reply(catevent, caption, parse_mode="html")
        return
    try:
        downloader = SmartDL(image, anime_path, progress_bar=False)
        downloader.start(blocking=False)
        while not downloader.isFinished():
            pass
        await event.client.send_file(
            event.chat_id,
            file=anime_path,
            caption=caption,
            parse_mode="html",
            reply_to=reply_to,
        )
        await catevent.delete()
        os.remove(anime_path)
    except BaseException:
        image = getBannerLink(first_mal_id, True)
        await event.client.send_file(
            event.chat_id,
            file=image,
            caption=caption,
            parse_mode="html",
            reply_to=reply_to,
        )
        await catevent.delete()


@catub.cat_cmd(
    pattern="manga(?:\s|$)([\s\S]*)",
    command=("manga", plugin_category),
    info={
        "header": "search manga.",
        "description": "Fetches manga information from anilist",
        "flags": {
            "d": "shows you manga details (another format)",
            "s": "manga search list (shows only manga name and link to anilist)",
            "n": "get details of specific manga number from search list",
        },
        "note": "for flag n you need to use number attached to flag",
        "usage": "{tr}manga <flags> <name of manga>",
        "examples": [
            "{tr}manga wind breaker",
            "{tr}manga -d wind breaker",
            "{tr}manga -s wind breaker",
            "{tr}manga -n2 wind breaker",
        ],
    },
)
async def anilist(event):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    "Get info on any manga."
    reply_to = await reply_id(event)
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str:
        if reply:
            input_str = reply.text
        else:
            return await edit_delete(
                event, "__What should i search ? Gib me Something to Search__"
            )
    match = input_str
    animeno = re.findall(r"-n\d+", match)
    listview = re.findall(r"-s", match)
    myanime = re.findall(r"-d", match)
    specific = bool(animeno)
    try:
        animeno = animeno[0]
        animeno = animeno.replace("-n", "")
        match = match.replace(f"-n{animeno}", "")
        animeno = int(animeno)
    except IndexError:
        animeno = 1
    if animeno < 1 or animeno > 10:
        return await edit_or_reply(
            event,
            "`manga number must be in between 1 to 10 use -l flag to query results`",
        )
    catevent = await edit_or_reply(event, "`Searching manga..`")
    match = match.replace("-s", "")
    listview = bool(listview)
    match = match.replace("-d", "")
    myanime = bool(myanime)
    query = match.strip()
    result, respone = await searchanilist(query, manga=True)
    if not respone:
        return await edit_delete(catevent, result)
    if len(result) == 0:
        return await edit_or_reply(
            catevent, f"**Search query:** `{query}`\n**Result:** `No results found`"
        )
    input_str = result[0]["title"]["english"] or result[0]["title"]["romaji"]
    if myanime:
        result = await callAPI(input_str)
        msg = await formatJSON(result)
        await catevent.edit(msg, link_preview=True)
        return
    if listview:
        msg = f"<b>Search Query: </b> <code>{query}</code>\n\n<b>Results:</b>\n"
        i = 1
        ani_data = result
        for result in ani_data:
            if i > 10:
                break
            input_str = result["title"]["english"] or result["title"]["romaji"]
            if result["title"]["english"]:
                msg += f'<b>{i}.</b> <code>{result["title"]["english"]}</code> - <a href="{result["siteUrl"]}">{result["title"]["romaji"]}</a>\n'
            else:
                msg += f'<b>{i}.</b> <code>{result["title"]["romaji"]}</code> - <a href="{result["siteUrl"]}">{result["title"]["native"]}</a>\n'
            i += 1
        await catevent.edit(msg, parse_mode="html")
        return
    input_str = result[animeno - 1]["title"]["romaji"] if specific else query
    caption, image = await get_anime_manga(input_str, "anime_manga", event.chat_id)
    if image is None:
        await edit_or_reply(catevent, caption, parse_mode="html")
        return
    try:
        downloader = SmartDL(image, anime_path, progress_bar=False)
        downloader.start(blocking=False)
        while not downloader.isFinished():
            pass
        await event.client.send_file(
            event.chat_id,
            file=anime_path,
            caption=caption,
            parse_mode="html",
            reply_to=reply_to,
        )
        await catevent.delete()
        os.remove(anime_path)
    except BaseException:
        image = getBannerLink(first_mal_id, True)
        await event.client.send_file(
            event.chat_id,
            file=image,
            caption=caption,
            parse_mode="html",
            reply_to=reply_to,
        )
        await catevent.delete()


@catub.cat_cmd(
    pattern="fillers(?:\s|$)([\s\S]*)",
    command=("fillers", plugin_category),
    info={
        "header": "To get list of filler episodes.",
        "flags": {
            "-n": "If more than one name have same common word then to select required anime"
        },
        "usage": ["{tr}fillers <anime name>", "{tr}fillers -n<number> <anime name>"],
        "examples": [
            "{tr}fillers one piece",
            "{tr}fillers -n5 naruto",
        ],
    },
)
async def get_anime(event):
    "to get list of filler episodes."
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str:
        if reply:
            input_str = reply.text
        else:
            return await edit_delete(
                event, "__What should i search ? Gib me Something to Search__"
            )
    anime = re.findall(r"-n\d+", input_str)
    try:
        anime = anime[0]
        anime = anime.replace("-n", "")
        input_str = input_str.replace(f"-n{anime}", "")
        anime = int(anime)
    except IndexError:
        anime = 0
    input_str = input_str.strip()
    result = await search_in_animefiller(input_str)
    if result == {}:
        return await edit_or_reply(
            event, f"**No filler episodes for the given anime**` {input_str}`"
        )
    if len(result) == 1:
        response = await get_filler_episodes(result[list(result.keys())[0]])
        msg = ""
        msg += f"**Fillers for anime** `{list(result.keys())[0]}`**"
        msg += "\n\n• Manga Canon episodes:**`\n"
        msg += str(response.get("total_ep"))
        msg += "\n\n`**• Mixed/Canon fillers:**`\n"
        msg += str(response.get("mixed_ep"))
        msg += "\n\n`**• Fillers:**\n`"
        msg += str(response.get("filler_episodes"))
        if response.get("anime_canon_episodes") is not None:
            msg += "\n\n`**• Anime Canon episodes:**\n`"
            msg += str(response.get("anime_canon_episodes"))
        msg += "`"
        return await edit_or_reply(event, msg)
    if anime == 0:
        msg = f"**More than 1 result found for {input_str}. so try as** `{Config.COMMAND_HAND_LER}fillers -n<number> {input_str}`\n\n"
        for i, an in enumerate(list(result.keys()), start=1):
            msg += f"{i}. {an}\n"
        return await edit_or_reply(event, msg)
    try:
        response = await get_filler_episodes(result[list(result.keys())[anime - 1]])
    except IndexError:
        msg = f"**Given index for {input_str} is wrong check again for correct index and then try** `{Config.COMMAND_HAND_LER}fillers -n<index> {input_str}`\n\n"
        for i, an in enumerate(list(result.keys()), start=1):
            msg += f"{i}. {an}\n"
        return await edit_or_reply(event, msg)
    msg = ""
    msg += f"**Fillers for anime** `{list(result.keys())[anime-1]}`**"
    msg += "\n\n• Manga Canon episodes:**`\n"
    msg += str(response.get("total_ep"))
    msg += "\n\n`**• Mixed/Canon fillers:**`\n"
    msg += str(response.get("mixed_ep"))
    msg += "\n\n`**• Fillers:**\n`"
    msg += str(response.get("filler_episodes"))
    if response.get("anime_canon_episodes") is not None:
        msg += "\n\n`**• Anime Canon episodes:**\n`"
        msg += str(response.get("anime_canon_episodes"))
    msg += "`"
    await edit_or_reply(event, msg)


@catub.cat_cmd(
    pattern="char(?:\s|$)([\s\S]*)",
    command=("char", plugin_category),
    info={
        "header": "search character.",
        "description": "Fetches character information from anilist",
        "flags": {
            "s": "character search list (shows only character name and link to anilist)",
            "n": "get details of specific character number from search list",
        },
        "note": "for flag n you need to use number attached to flag",
        "usage": "{tr}character <flags> <name of character>",
        "examples": [
            "{tr}character erza scarlet",
            "{tr}character -s erza scarlet",
            "{tr}character -n2 erza scarlet",
        ],
    },
)
async def anilist(event):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    "Get info on any character."
    reply_to = await reply_id(event)
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str:
        if reply:
            input_str = reply.text
        else:
            return await edit_delete(
                event, "__What should i search ? Gib me Something to Search__"
            )
    match = input_str
    animeno = re.findall(r"-n\d+", match)
    listview = re.findall(r"-s", match)
    specific = bool(animeno)
    try:
        animeno = animeno[0]
        animeno = animeno.replace("-n", "")
        match = match.replace(f"-n{animeno}", "")
        animeno = int(animeno)
    except IndexError:
        animeno = 1
    if animeno < 1 or animeno > 10:
        return await edit_or_reply(
            event,
            "`character number must be in between 1 to 10 use -l flag to query results`",
        )
    catevent = await edit_or_reply(event, "`Searching character..`")
    match = match.replace("-s", "")
    listview = bool(listview)
    query = match.strip()
    search_query = {"page": 1, "perPage": 10, "query": query}
    result = await anime_json_synomsis(character_query, search_query)
    result = result["data"]["Page"]["characters"]
    if len(result) == 0:
        return await edit_or_reply(
            catevent, f"**Search query:** `{query}`\n**Result:** `No results found`"
        )
    if listview:
        msg = f"<b>Search Query: </b> <code>{query}</code>\n\n<b>Results:</b>\n"
        i = 1
        ani_data = result
        for result in ani_data:
            if i > 10:
                break
            msg += f'<b>{i}.</b> <code>{result["name"]["full"]}</code> - <a href="{result["siteUrl"]}">{result["name"]["first"]}</a>\n'
            i += 1
        await catevent.edit(msg, parse_mode="html")
        return
    result = result[animeno - 1] if specific else result[0]
    for entity in result:
        if result[entity] is None:
            result[entity] = "Unknown"
    dateofbirth = []
    if result["dateOfBirth"]["year"]:
        dateofbirth.append(str(result["dateOfBirth"]["year"]))
    if result["dateOfBirth"]["month"]:
        dateofbirth.append(str(result["dateOfBirth"]["month"]))
    if result["dateOfBirth"]["day"]:
        dateofbirth.append(str(result["dateOfBirth"]["day"]))
    dob = "-".join(dateofbirth) if dateofbirth else "Unknown"
    caption = textwrap.dedent(
        f"""
        🆎 <b> Name</b>: <i>{result['name']['full']}</i>
        🆔 <b>AL ID</b>: <i>{result['id']}</i>
        👫 <b>Gender</b>: <i>{result['gender'].lower()}</i>
        🔢 <b>Age</b>: <i>{result['age']}</i>
        🎂 <b>Date of Birth</b>: {dob}
        📃 <b>Blood Type</b>: <i>{result['bloodType']}</i>
        📊 <b>Liked By</b>: <i>{result['favourites']}</i>
        """
    )
    html_ = f"""<a href="{result['siteUrl']}">"""
    html_ += f"""<img src="{result['image']['large']}"/></a>"""
    html_ += "<br>"
    html_ += f"<h3>{result['name']['full']}</h3>"
    html_ += f"<em>{result['name']['native']}</em><br>"
    html_ += f"<b>Character ID</b>: {result['id']}<br>"
    html_ += f"<h4>About Character and Role:</h4>{result['description'] or 'N/A'}"
    html_ += "<br><br>"
    html_ += f"<a href='{result['siteUrl']}'> View on anilist</a>"

    synopsis_link = await post_to_telegraph(
        result["name"]["full"], f"<code>{caption}</code>\n<br>{html_}"
    )

    await event.client.send_file(
        event.chat_id,
        file=result["image"]["large"],
        caption=caption
        + f"📖 <a href='{synopsis_link}'><b>Description</b></a> <b>&</b> <a href='{result['siteUrl']}'><b>Read More</b></a>",
        parse_mode="html",
        reply_to=reply_to,
    )


@catub.cat_cmd(
    pattern="a(kaizoku|kayo|indi)(?: |$)([\S\s]*)",
    command=("akaizoku", plugin_category),
    info={
        "header": "Shows you anime download link.",
        "usage": [
            "{tr}akaizoku <anime name>",
            "{tr}akayo <anime name>",
            "{tr}aindi <anime name>",
        ],
        "examples": [
            "{tr}akaizoku one piece",
            "{tr}akayo tokyo revengers",
            "{tr}aindi Spirited Away",
        ],
    },
)
async def anime_download(event):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    "Anime download links."
    search_query = event.pattern_match.group(2)
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not search_query and reply:
        search_query = reply.text
    elif not search_query:
        return await edit_delete(
            event, "__What should i search ? Gib me Something to Search__"
        )
    catevent = await edit_or_reply(event, "`Searching anime...`")
    search_query = search_query.replace(" ", "+")
    if input_str == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url, headers=headers).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        if search_result := soup.find_all("h2", {"class": "post-title"}):
            result = f"<a href={search_url}>Click Here For More Results</a> <b>of</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n\n"
            for entry in search_result:
                post_link = "https://animekaizoku.com/" + entry.a["href"]
                post_name = html.escape(entry.text)
                result += f"• <a href={post_link}>{post_name}</a>\n"
        else:
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"
    elif input_str == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url, headers=headers).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})
        result = f"<a href={search_url}>Click Here For More Results</a> <b>of</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n\n"
        if search_result:
            for entry in search_result:
                if entry.text.strip() == "Nothing Found":
                    result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                    break
                post_link = entry.a["href"]
                post_name = html.escape(entry.text.strip())
                result += f"• <a href={post_link}>{post_name}</a>\n"
        else:
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
    elif input_str == "indi":
        search_url = f"https://indianime.com/?s={search_query}"
        html_text = requests.get(search_url, headers=headers).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h1", {"class": "elementor-post__title"})
        result = f"<a href={search_url}>Click Here For More Results</a> <b>of</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>indianime</code>: \n\n"
        if search_result:
            for entry in search_result:
                if entry.text.strip() == "Nothing Found":
                    result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>Indianime</code>.\n<b>You can request anime <a href='https://indianime.com/request-anime'>here</a></b>"
                    break
                post_link = entry.a["href"]
                post_name = html.escape(entry.text.strip())
                result += f"• <a href={post_link}>{post_name}</a>\n"
        else:
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>IndiAnime</code>"
    await catevent.edit(result, parse_mode="html")


@catub.cat_cmd(
    pattern="upcoming$",
    command=("upcoming", plugin_category),
    info={
        "header": "Shows you upcoming anime's.",
        "usage": "{tr}upcoming",
    },
)
async def upcoming(event):
    "Shows you Upcoming anime's."
    rep = "<b>Upcoming anime</b>\n"
    later = jikan.season_later()
    anime = later.get("anime")
    for new in anime:
        name = new.get("title")
        a_url = new.get("url")
        rep += f"• <a href='{a_url}'>{name}</a>\n"
        if len(rep) > 1000:
            break
    await edit_or_reply(event, rep, parse_mode="html")


@catub.cat_cmd(
    pattern="aschedule(?: |$)([\S\s]*)",
    command=("aschedule", plugin_category),
    info={
        "header": "Shows you animes to be aired on that day.",
        "description": "To get list of animes to be aired on that day use can also use 0 for monday , 1 for tuesday.... 6 for sunday.",
        "usage": "{tr}aschedule <weekdays/[0-6]>",
        "example": ["{tr}aschedule sunday", "{tr}aschedule 5"],
    },
)
async def aschedule_fetch(event):
    "To get list of animes scheduled on that day"
    input_str = event.pattern_match.group(1) or datetime.now().weekday()
    if input_str in weekdays:
        input_str = weekdays[input_str]
    try:
        input_str = int(input_str)
    except ValueError:
        return await edit_delete(event, "`You have given and invalid weekday`", 7)
    if input_str not in [0, 1, 2, 3, 4, 5, 6]:
        return await edit_delete(event, "`You have given and invalid weekday`", 7)
    result = await get_anime_schedule(input_str)
    await edit_or_reply(event, result[0])


@catub.cat_cmd(
    pattern="w(hat)?anime$",
    command=("whatanime", plugin_category),
    info={
        "header": "Reverse search of anime.",
        "usage": [
            "{tr}whatanime reply to photo/gif/video",
            "{tr}wanime reply to photo/gif/video",
        ],
    },
)
async def whatanime(event):
    "Reverse search of anime."
    reply = await event.get_reply_message()
    if not reply:
        return await edit_delete(
            event, "__reply to media to reverse search that anime__."
        )
    mediatype = await media_type(reply)
    if mediatype not in ["Photo", "Video", "Gif", "Sticker", "Document"]:
        return await edit_delete(
            event,
            f"__Reply to proper media that is expecting photo/video/gif/sticker. not {mediatype}__.",
        )
    output = await Convert.to_image(
        event,
        reply,
        dirct="./temp",
        file="wanime.png",
    )
    if output[1] is None:
        return await edit_delete(
            output[0], "__Unable to extract image from the replied message.__"
        )
    file = memory_file("anime.jpg", output[1])
    try:
        response = upload_file(file)
    except exceptions.TelegraphException as exc:
        try:
            response = upload_file(output[1])
        except exceptions.TelegraphException as exc:
            return await edit_delete(output[0], f"**Error :**\n__{exc}__")
    cat = f"https://telegra.ph{response[0]}"
    await output[0].edit("`Searching for result..`")
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"https://api.trace.moe/search?anilistInfo&url={quote_plus(cat)}"
        ) as raw_resp0:
            resp0 = await raw_resp0.json()
        framecount = resp0["frameCount"]
        error = resp0["error"]
        if error != "":
            return await edit_delete(output[0], f"**Error:**\n__{error}__")
        js0 = resp0["result"]
        if not js0:
            return await output[0].edit("`No results found.`")
        js0 = js0[0]
        text = (
            f'**Titile Romaji : **`{html.escape(js0["anilist"]["title"]["romaji"])}`\n'
        )
        text += (
            f'**Titile Native :** `{html.escape(js0["anilist"]["title"]["native"])}`\n'
        )
        text += (
            f'**Titile English :** `{html.escape(js0["anilist"]["title"]["english"])}`\n'
            if js0["anilist"]["title"]["english"] is not None
            else ""
        )
        text += f'**Is Adult :** __{js0["anilist"]["isAdult"]}__\n'
        #         text += f'**File name :** __{js0["filename"]}__\n'
        text += f'**Episode :** __{html.escape(str(js0["episode"]))}__\n'
        text += f'**From :** __{readable_time(js0["from"])}__\n'
        text += f'**To :** __{readable_time(js0["to"])}__\n'
        percent = round(js0["similarity"] * 100, 2)
        text += f"**Similarity :** __{percent}%__\n"
        result = (
            f"**Searched {framecount} frames and found this as best result :**\n\n"
            + text
        )
        msg = await output[0].edit(result)
        try:
            await msg.reply(
                f'{readable_time(js0["from"])} - {readable_time(js0["to"])}',
                file=js0["video"],
            )
        except Exception:
            await msg.reply(
                f'{readable_time(js0["from"])} - {readable_time(js0["to"])}',
                file=js0["image"],
            )

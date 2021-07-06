import html
from urllib.parse import quote_plus

import aiohttp
import bs4
import jikanpy
import requests
from jikanpy import Jikan
from jikanpy.exceptions import APIException
from telegraph import exceptions, upload_file

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type, readable_time, time_formatter
from ..helpers.functions import (
    airing_query,
    callAPI,
    formatJSON,
    get_anime_manga,
    getBannerLink,
    memory_file,
    replace_text,
)
from ..helpers.utils import _cattools, reply_id

jikan = Jikan()
url = "https://graphql.anilist.co"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
}
plugin_category = "extra"


@catub.cat_cmd(
    pattern="airing ([\s\S]*)",
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
    variables = {"search": search}
    response = requests.post(
        url, json={"query": airing_query, "variables": variables}
    ).json()["data"]["Media"]
    ms_g = f"**Name**: **{response['title']['romaji']}**(`{response['title']['native']}`)\n**ID**: `{response['id']}`"
    if response["nextAiringEpisode"]:
        airing_time = response["nextAiringEpisode"]["timeUntilAiring"]
        airing_time_final = time_formatter(airing_time)
        ms_g += f"\n**Episode**: `{response['nextAiringEpisode']['episode']}`\n**Airing In**: `{airing_time_final}`"
    else:
        ms_g += f"\n**Episode**:{response['episodes']}\n**Status**: `N/A`"
    await edit_or_reply(event, ms_g)


@catub.cat_cmd(
    pattern="anime(?:\s|$)([\s\S]*)",
    command=("anime", plugin_category),
    info={
        "header": "Shows you the details of the anime.",
        "description": "Fectchs anime information from anilist",
        "usage": "{tr}anime <name of anime>",
        "examples": "{tr}anime fairy tail",
    },
)
async def anilist(event):
    "Get info on any anime."
    input_str = event.pattern_match.group(1)
    if not input_str:
        return await edit_delete(
            event, "__What should i search ? Gib me Something to Search__"
        )
    event = await edit_or_reply(event, "`Searching...`")
    result = await callAPI(input_str)
    msg = await formatJSON(result)
    await event.edit(msg, link_preview=True)


@catub.cat_cmd(
    pattern="manga(?:\s|$)([\s\S]*)",
    command=("manga", plugin_category),
    info={
        "header": "Searches for manga.",
        "usage": "{tr}manga <manga name",
        "examples": "{tr}manga fairy tail",
    },
)
async def get_manga(event):
    "searches for manga."
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
    catevent = await edit_or_reply(event, "`Searching Manga..`")
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("manga", input_str)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(first_mal_id, "anime_manga", event.chat_id)
    await catevent.delete()
    await event.client.send_file(
        event.chat_id, file=image, caption=caption, parse_mode="html", reply_to=reply_to
    )


@catub.cat_cmd(
    pattern="sanime(?:\s|$)([\s\S]*)",
    command=("sanime", plugin_category),
    info={
        "header": "Searches for anime.",
        "usage": "{tr}sanime <anime name",
        "examples": "{tr}sanime black clover",
    },
)
async def get_manga(event):
    "searches for anime."
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
    catevent = await edit_or_reply(event, "`Searching Anime..`")
    jikan = jikanpy.jikan.Jikan()
    search_result = jikan.search("anime", input_str)
    first_mal_id = search_result["results"][0]["mal_id"]
    caption, image = get_anime_manga(first_mal_id, "anime_anime", event.chat_id)
    try:
        await catevent.delete()
        await event.client.send_file(
            event.chat_id,
            file=image,
            caption=caption,
            parse_mode="html",
            reply_to=reply_to,
        )
    except BaseException:
        image = getBannerLink(first_mal_id, False)
        await event.client.send_file(
            event.chat_id,
            file=image,
            caption=caption,
            parse_mode="html",
            reply_to=reply_to,
        )


@catub.cat_cmd(
    pattern="char(?:\s|$)([\s\S]*)",
    command=("char", plugin_category),
    info={
        "header": "Shows you character infomation.",
        "usage": "{tr}char <char name>",
        "examples": "{tr}char erza scarlet",
    },
)
async def character(event):
    "Character information."
    reply_to = await reply_id(event)
    search_query = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not search_query:
        if reply:
            search_query = reply.text
        else:
            return await edit_delete(
                event, "__What should i search ? Gib me Something to Search__"
            )
    catevent = await edit_or_reply(event, "`Searching Character...`")
    try:
        search_result = jikan.search("character", search_query)
    except APIException:
        return await edit_delete(catevent, "`Character not found.`")
    first_mal_id = search_result["results"][0]["mal_id"]
    character = jikan.character(first_mal_id)
    caption = f"[{character['name']}]({character['url']})"
    if character["name_kanji"] != "Japanese":
        caption += f" ({character['name_kanji']})\n"
    else:
        caption += "\n"
    if character["nicknames"]:
        nicknames_string = ", ".join(character["nicknames"])
        caption += f"\n**Nicknames** : `{nicknames_string}`"
    about = character["about"].split(" ", 60)
    try:
        about.pop(60)
    except IndexError:
        pass
    about_string = " ".join(about)
    mal_url = search_result["results"][0]["url"]
    for entity in character:
        if character[entity] is None:
            character[entity] = "Unknown"
    caption += f"\n🔰**Extracted Character Data**🔰\n\n{about_string}"
    caption += f" [Read More]({mal_url})..."
    await catevent.delete()
    await event.client.send_file(
        event.chat_id,
        file=character["image_url"],
        caption=replace_text(caption),
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
        search_result = soup.find_all("h2", {"class": "post-title"})
        if search_result:
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
        url = new.get("url")
        rep += f"• <a href='{url}'>{name}</a>\n"
        if len(rep) > 1000:
            break
    await edit_or_reply(event, rep, parse_mode="html")


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
    mediatype = media_type(reply)
    if mediatype not in ["Photo", "Video", "Gif", "Sticker"]:
        return await edit_delete(
            event,
            f"__Reply to proper media that is expecting photo/video/gif/sticker. not {mediatype}__.",
        )
    output = await _cattools.media_to_pic(event, reply)
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
            return await edit_delete(output[0], f"**Error :**\n__{str(exc)}__")
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

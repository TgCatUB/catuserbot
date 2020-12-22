"""
Anilist Search Plugin for Userbot
Usage : .anilist animeName
By :- @Zero_cool7870
ported char, airing and manga by @sandy1709 and @mrconfused
"""

import json
import re

import requests

from ..utils import time_formatter as t


def shorten(description, info="anilist.co"):
    msg = ""
    if len(description) > 700:
        description = description[0:200] + "....."
        msg += f"\n**Description**:\n{description} [Read More]({info})"
    else:
        msg += f"\n**Description**: \n   {description}"
    return (
        msg.replace("<br>", "")
        .replace("</br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
        .replace("__", "**")
    )


character_query = """
    query ($query: String) {
        Character (search: $query) {
               id
               name {
                     first
                     last
                     full
               }
               siteUrl
               image {
                        large
               }
               description
        }
    }
"""

airing_query = """
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        episodes
        title {
          romaji
          english
          native
        }
        nextAiringEpisode {
           airingAt
           timeUntilAiring
           episode
        }
      }
    }
    """

anime_query = """
   query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
"""

manga_query = """
query ($id: Int,$search: String) {
      Media (id: $id, type: MANGA,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""


async def callAPI(search_str):
    query = """
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        title {
          romaji
          english
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          chapters
          volumes
          season
          type
          format
          status
          duration
          averageScore
          genres
          bannerImage
      }
    }
    """
    variables = {"search": search_str}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})
    return response.text


async def formatJSON(outData):
    msg = ""
    jsonData = json.loads(outData)
    res = list(jsonData.keys())
    if "errors" in res:
        msg += f"**Error** : `{jsonData['errors'][0]['message']}`"
        return msg
    jsonData = jsonData["data"]["Media"]
    if "bannerImage" in jsonData.keys():
        msg += f"[〽️]({jsonData['bannerImage']})"
    else:
        msg += "〽️"
    title = jsonData["title"]["romaji"]
    link = f"https://anilist.co/anime/{jsonData['id']}"
    msg += f"[{title}]({link})"
    msg += f"\n\n**Type** : {jsonData['format']}"
    msg += f"\n**Genres** : "
    for g in jsonData["genres"]:
        msg += g + " "
    msg += f"\n**Status** : {jsonData['status']}"
    msg += f"\n**Episode** : {jsonData['episodes']}"
    msg += f"\n**Year** : {jsonData['startDate']['year']}"
    msg += f"\n**Score** : {jsonData['averageScore']}"
    msg += f"\n**Duration** : {jsonData['duration']} min\n\n"
    # https://t.me/catuserbot_support/19496
    cat = f"{jsonData['description']}"
    msg += " __" + re.sub("<br>", "\n", cat) + "__"
    return msg


url = "https://graphql.anilist.co"


@bot.on(admin_cmd(pattern="char (.*)"))
@bot.on(sudo_cmd(pattern="char (.*)", allow_sudo=True))
async def anilist(event):
    if event.fwd_from:
        return
    search = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    variables = {"query": search}
    json = (
        requests.post(url, json={"query": character_query, "variables": variables})
        .json()["data"]
        .get("Character", None)
    )
    if json:
        msg = f"**{json.get('name').get('full')}**\n"
        description = f"{json['description']}"
        site_url = json.get("siteUrl")
        msg += shorten(description, site_url)
        image = json.get("image", None)
        if image:
            image = image.get("large")
            await event.delete()
            await event.client.send_file(
                event.chat_id, image, caption=msg, parse_mode="md", reply_to=reply_to_id
            )
        else:
            await edit_or_reply(event, msg)
    else:
        await edit_or_reply(event, "Sorry, No such results")


@bot.on(admin_cmd(pattern="airing (.*)"))
@bot.on(sudo_cmd(pattern="airing (.*)", allow_sudo=True))
async def anilist(event):
    if event.fwd_from:
        return
    search = event.pattern_match.group(1)
    variables = {"search": search}
    response = requests.post(
        url, json={"query": airing_query, "variables": variables}
    ).json()["data"]["Media"]
    ms_g = f"**Name**: **{response['title']['romaji']}**(`{response['title']['native']}`)\n**ID**: `{response['id']}`"
    if response["nextAiringEpisode"]:
        airing_time = response["nextAiringEpisode"]["timeUntilAiring"] * 1000
        airing_time_final = t(airing_time)
        ms_g += f"\n**Episode**: `{response['nextAiringEpisode']['episode']}`\n**Airing In**: `{airing_time_final}`"
    else:
        ms_g += f"\n**Episode**:{response['episodes']}\n**Status**: `N/A`"
    await edit_or_reply(event, ms_g)


@bot.on(admin_cmd(pattern="manga (.*)"))
@bot.on(sudo_cmd(pattern="manga (.*)", allow_sudo=True))
async def anilist(event):
    if event.fwd_from:
        return
    search = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    variables = {"search": search}
    json = (
        requests.post(url, json={"query": manga_query, "variables": variables})
        .json()["data"]
        .get("Media", None)
    )
    ms_g = ""
    if json:
        title, title_native = json["title"].get("romaji", False), json["title"].get(
            "native", False
        )
        start_date, status, score = (
            json["startDate"].get("year", False),
            json.get("status", False),
            json.get("averageScore", False),
        )
        if title:
            ms_g += f"**{title}**"
            if title_native:
                ms_g += f"(`{title_native}`)"
        if start_date:
            ms_g += f"\n**Start Date** - `{start_date}`"
        if status:
            ms_g += f"\n**Status** - `{status}`"
        if score:
            ms_g += f"\n**Score** - `{score}`"
        ms_g += "\n**Genres** - "
        for x in json.get("genres", []):
            ms_g += f"{x}, "
        ms_g = ms_g[:-2]
        image = json.get("bannerImage", False)
        ms_g += f"_{json.get('description', None)}_"
        ms_g = (
            ms_g.replace("<br>", "")
            .replace("</br>", "")
            .replace("<i>", "")
            .replace("</i>", "")
        )
        if image:
            try:
                await event.client.send_file(
                    event.chat_id,
                    image,
                    caption=ms_ms_g,
                    parse_mode="md",
                    reply_to=reply_to_id,
                )
                await event.delete()
            except BaseException:
                ms_g += f" [〽️]({image})"
                await edit_or_reply(event, ms_g)
        else:
            await edit_or_reply(event, ms_g)


@bot.on(admin_cmd(pattern="anilist (.*)"))
@bot.on(sudo_cmd(pattern="anilist (.*)", allow_sudo=True))
async def anilist(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    event = await edit_or_reply(event, "Searching...")
    result = await callAPI(input_str)
    msg = await formatJSON(result)
    await event.edit(msg, link_preview=True)


CMD_HELP.update(
    {
        "anilist": "**Plugin : **`anilist`\
    \n\n**Syntax : **`.anilist <anime name >`\
    \n**Usage : **Shows you the details of the anime.\
    \n\n**Syntax : **`.char <character name >`\
    \n**Usage : **Shows you the details of that character in anime with pic.\
    \n\n**Syntax : **`.manga <anime name >`\
    \n**Usage : **Shows you the details of the manga.\
    \n\n**Syntax : **`.airing <anime name >`\
    \n**Usage : **Shows you the time for that current running anime show.\
    "
    }
)

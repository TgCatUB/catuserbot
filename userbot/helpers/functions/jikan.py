import json
import re
import textwrap
import time
from io import BytesIO, StringIO

import bs4
import jikanpy
import requests
from aiohttp import ClientSession
from jikanpy import Jikan
from telethon.tl.types import DocumentAttributeAnimated
from telethon.utils import is_video

from ..progress import readable_time
from ..tools import post_to_telegraph

jikan = Jikan()

anilisturl = "https://graphql.anilist.co"
animnefillerurl = "https://www.animefillerlist.com/shows/"
# Anime Helper

weekdays = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def get_weekday(dayid):
    for key, value in weekdays.items():
        if value == dayid:
            return key


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


anime_query = """
query ($id: Int, $idMal:Int, $search: String, $type: MediaType, $asHtml: Boolean) {
  Media (id: $id, idMal: $idMal, search: $search, type: $type) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    type 
    description (asHtml: $asHtml)
    startDate {
      year
      month
      day
    }
    season
    episodes
    duration
    countryOfOrigin
    source (version: 2)
    trailer {
      id
      site
      thumbnail
    }
    coverImage {
      extraLarge
    }
    bannerImage
    genres
    averageScore
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    isAdult
    characters (role: MAIN, page: 1, perPage: 10) {
      nodes {
        id
        name {
          full
          native
        }
        image {
          large
        }
        description (asHtml: $asHtml)
        siteUrl
      }
    }
    studios (isMain: true) {
      nodes {
        name
        siteUrl
      }
    }
    siteUrl
  }
}
"""

user_query = """
query ($search: String) {
  User (name: $search) {
    id
    name
    siteUrl
    statistics {
      anime {
        count
        minutesWatched
        episodesWatched
        meanScore
      }
      manga {
        count
        chaptersRead
        volumesRead
        meanScore
      }
    }
  }
}
"""


async def get_anime_schedule(weekid):
    "get anime schedule"
    dayname = get_weekday(weekid)
    result = f"✙ **Scheduled animes for {dayname.title()} are : **\n\n"
    async with jikanpy.AioJikan() as animesession:
        scheduled_list = (await animesession.schedule(day=dayname)).get(dayname)
        for a_name in scheduled_list:
            result += f"• [{a_name['title']}]({a_name['url']})\n"
    return result, dayname


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
    msg += "\n**Genres** : "
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
    msg = re.sub("<b>", "__**", msg)
    msg = re.sub("</b>", "**__", msg)
    return msg


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


async def anilist_user(input_str):
    "Fetch user details from anilist"
    username = {"search": input_str}
    result = requests.post(
        anilisturl, json={"query": user_query, "variables": username}
    ).json()
    error = result.get("errors")
    if error:
        error_sts = error[0].get("message")
        return [f"{error_sts}"]
    user_data = result["data"]["User"]
    stats = textwrap.dedent(
        f"""
**User name :** [{user_data['name']}]({user_data['siteUrl']})
**Anilist ID :** `{user_data['id']}` 

**✙  Anime Stats**
• **Total Anime Watched :** `{user_data["statistics"]["anime"]['count']}`
• **Total Episode Watched : **`{user_data["statistics"]["anime"]['episodesWatched']}`
• **Total Time Spent : **`{readable_time(user_data["statistics"]["anime"]['minutesWatched']*60)}`
• **Average Score :** `{user_data["statistics"]["anime"]['meanScore']}`

**✙  Manga Stats**
• **Total Manga Read :** `{user_data["statistics"]["manga"]['count']}`
• **Total Chapters Read :** `{user_data["statistics"]["manga"]['chaptersRead']}`
• **Total Volumes Read : **`{user_data["statistics"]["manga"]['volumesRead']}`
• **Average Score : **`{user_data["statistics"]["manga"]['meanScore']}`
"""
    )
    return stats, f'https://img.anili.st/user/{user_data["id"]}?a={time.time()}'


async def anime_json_synomsis(query, vars_):
    """Makes a Post to https://graphql.anilist.co."""
    async with ClientSession() as session:
        async with session.post(
            anilisturl, json={"query": query, "variables": vars_}
        ) as post_con:
            json_data = await post_con.json()
    return json_data


def getPosterLink(mal):
    # grab poster from kitsu
    kitsu = getKitsu(mal)
    image = requests.get(f"https://kitsu.io/api/edge/anime/{kitsu}").json()
    return image["data"]["attributes"]["posterImage"]["original"]


def getKitsu(mal):
    # get kitsu id from mal id
    link = f"https://kitsu.io/api/edge/mappings?filter[external_site]=myanimelist/anime&filter[external_id]={mal}"
    result = requests.get(link).json()["data"][0]["id"]
    link = f"https://kitsu.io/api/edge/mappings/{result}/item?fields[anime]=slug"
    return requests.get(link).json()["data"]["id"]


def getBannerLink(mal, kitsu_search=True, anilistid=0):
    # try getting kitsu backdrop
    if kitsu_search:
        kitsu = getKitsu(mal)
        image = f"http://media.kitsu.io/anime/cover_images/{kitsu}/original.jpg"
        response = requests.get(image)
        if response.status_code == 200:
            return image
    if anilistid != 0:
        return f"https://img.anili.st/media/{anilistid}"
    # try getting anilist banner
    query = """
    query ($idMal: Int){
        Media(idMal: $idMal){
            bannerImage
        }
    }
    """
    data = {"query": query, "variables": {"idMal": int(mal)}}
    image = requests.post("https://graphql.anilist.co", json=data).json()["data"][
        "Media"
    ]["bannerImage"]
    if image:
        return image
    return getPosterLink(mal)


async def get_anime_manga(mal_id, search_type, _user_id):  # sourcery no-metrics
    jikan = jikanpy.jikan.Jikan()
    if search_type == "anime_anime":
        result = jikan.anime(mal_id)
        trailer = result["trailer_url"]
        if trailer:
            TRAILER = f"<a href='{trailer}'>🎬 Trailer</a>"
        else:
            TRAILER = "🎬 <i>No Trailer Available</i>"
        studio_string = ", ".join(
            studio_info["name"] for studio_info in result["studios"]
        )
        producer_string = ", ".join(
            producer_info["name"] for producer_info in result["producers"]
        )
    elif search_type == "anime_manga":
        result = jikan.manga(mal_id)
        image = result["image_url"]
    caption = f"📺 <a href='{result['url']}'>{result['title']}</a>"
    if result["title_japanese"]:
        caption += f" ({result['title_japanese']})\n"
    else:
        caption += "\n"
    alternative_names = []
    if result["title_english"] is not None:
        alternative_names.append(result["title_english"])
    alternative_names.extend(result["title_synonyms"])
    if alternative_names:
        alternative_names_string = ", ".join(alternative_names)
        caption += f"\n<b>Also known as</b>: <i>{alternative_names_string}</i>"
    genre_string = ", ".join(genre_info["name"] for genre_info in result["genres"])
    if result["synopsis"] is not None:
        synopsis = result["synopsis"].split(" ", 60)
        try:
            synopsis.pop(60)
        except IndexError:
            pass
        synopsis_string = " ".join(synopsis) + "..."
    else:
        synopsis_string = "Unknown"
    for entity in result:
        if result[entity] is None:
            result[entity] = "Unknown"
    if search_type == "anime_anime":
        anime_malid = result["mal_id"]
        anime_result = await anime_json_synomsis(
            anime_query, {"idMal": anime_malid, "asHtml": True, "type": "ANIME"}
        )
        anime_data = anime_result["data"]["Media"]
        html_char = ""
        for character in anime_data["characters"]["nodes"]:
            html_ = ""
            html_ += "<br>"
            html_ += f"""<a href="{character['siteUrl']}">"""
            html_ += f"""<img src="{character['image']['large']}"/></a>"""
            html_ += "<br>"
            html_ += f"<h3>{character['name']['full']}</h3>"
            html_ += f"<em>{character['name']['native']}</em><br>"
            html_ += f"<b>Character ID</b>: {character['id']}<br>"
            html_ += f"<h4>About Character and Role:</h4>{character.get('description', 'N/A')}"
            html_char += f"{html_}<br><br>"
        studios = "".join(
            "<a href='{}'>• {}</a> ".format(studio["siteUrl"], studio["name"])
            for studio in anime_data["studios"]["nodes"]
        )
        coverImg = anime_data.get("coverImage")["extraLarge"]
        bannerImg = anime_data.get("bannerImage")
        anilist_animelink = anime_data.get("siteUrl")
        title_img = coverImg or bannerImg
        romaji = anime_data["title"]["romaji"]
        native = anime_data["title"]["native"]
        english = anime_data["title"]["english"]
        image = getBannerLink(mal_id, False, anime_data.get("id"))
        # Telegraph Post mejik
        html_pc = ""
        html_pc += f"<h1>{native}</h1>"
        html_pc += "<h3>Synopsis:</h3>"
        html_pc += result["synopsis"] or "Unknown"
        html_pc += "<br>"
        if html_char:
            html_pc += "<h2>Main Characters:</h2>"
            html_pc += html_char
            html_pc += "<br><br>"
        html_pc += "<h3>More Info:</h3>"
        html_pc += f"<br><b>Studios:</b> {studios}<br>"
        html_pc += (
            f"<a href='https://myanimelist.net/anime/{anime_malid}'>View on MAL</a>"
        )
        html_pc += f"<a href='{anilist_animelink}'> View on anilist.co</a>"
        html_pc += f"<img src='{bannerImg}'/>"
        title_h = english or romaji
    if search_type == "anime_anime":
        caption += textwrap.dedent(
            f"""
        🆎 <b>Type</b>: <i>{result['type']}</i>
        🆔 <b>MAL ID</b>: <i>{result['mal_id']}</i>
        📡 <b>Status</b>: <i>{result['status']}</i>
        🎙️ <b>Aired</b>: <i>{result['aired']['string']}</i>
        🔢 <b>Episodes</b>: <i>{result['episodes']}</i>
        🔞 <b>Rating</b>: <i>{result['rating']}</i>
        💯 <b>Score</b>: <i>{result['score']}</i>
        🌐 <b>Premiered</b>: <i>{result['premiered']}</i>
        ⌛ <b>Duration</b>: <i>{result['duration']}</i>
        🎭 <b>Genres</b>: <i>{genre_string}</i>
        🎙️ <b>Studios</b>: <i>{studio_string}</i>
        💸 <b>Producers</b>: <i>{producer_string}</i>
        """
        )
        synopsis_link = await post_to_telegraph(
            title_h,
            f"<img src='{title_img}' title={romaji}/>\n"
            + f"<code>{caption}</code>\n"
            + f"{TRAILER}\n"
            + html_pc,
        )
        caption += f"<b>{TRAILER}</b>\n📖 <a href='{synopsis_link}'><b>Synopsis</b></a> <b>&</b> <a href='{result['url']}'><b>Read More</b></a>"
    elif search_type == "anime_manga":
        caption += textwrap.dedent(
            f"""
        🆎 <b>Type</b>: <i>{result['type']}</i>
        📡 <b>Status</b>: <i>{result['status']}</i>
        🔢 <b>Volumes</b>: <i>{result['volumes']}</i>
        📃 <b>Chapters</b>: <i>{result['chapters']}</i>
        📊 <b>Rank</b>: <i>{result['rank']}</i>
        💯 <b>Score</b>: <i>{result['score']}</i>
        🎭 <b>Genres</b>: <i>{genre_string}</i>
        📖 <b>Synopsis</b>: <i>{synopsis_string}</i>
        """
        )
    return caption, image


def get_poster(query):
    url_enc_name = query.replace(" ", "+")
    # Searching for query list in imdb
    page = requests.get(
        f"https://www.imdb.com/find?ref_=nv_sr_fn&q={url_enc_name}&s=all"
    )
    soup = bs4.BeautifulSoup(page.content, "lxml")
    odds = soup.findAll("tr", "odd")
    # Fetching the first post from search
    page_link = "http://www.imdb.com/" + odds[0].findNext("td").findNext("td").a["href"]
    page1 = requests.get(page_link)
    soup = bs4.BeautifulSoup(page1.content, "lxml")
    # Poster Link
    image = soup.find("link", attrs={"rel": "image_src"}).get("href", None)
    if image is not None:
        # img_path = wget.download(image, os.path.join(Config.DOWNLOAD_LOCATION, 'imdb_poster.jpg'))
        return image


def replace_text(text):
    return text.replace('"', "").replace("\\r", "").replace("\\n", "").replace("\\", "")


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
    response = requests.post(anilisturl, json={"query": query, "variables": variables})
    return response.text


def memory_file(name=None, contents=None, *, temp_bytes=True):
    if isinstance(contents, str) and temp_bytes:
        contents = contents.encode()
    file = BytesIO() if temp_bytes else StringIO()
    if name:
        file.name = name
    if contents:
        file.write(contents)
        file.seek(0)
    return file


def is_gif(file):
    # ngl this should be fixed, telethon.utils.is_gif but working
    # lazy to go to github and make an issue kek
    if not is_video(file):
        return False
    return DocumentAttributeAnimated() in getattr(file, "document", file).attributes


async def search_in_animefiller(query):
    "To search anime name and get its id"
    html = requests.get(animnefillerurl).text
    soup = bs4.BeautifulSoup(html, "html.parser")
    div = soup.findAll("div", attrs={"class": "Group"})
    index = {}
    for i in div:
        li = i.findAll("li")
        for jk in li:
            yum = jk.a["href"].split("/")[-1]
            cum = jk.text
            index[cum] = yum
    keys = list(index.keys())
    return {
        keys[i]: index[keys[i]]
        for i in range(len(keys))
        if query.lower() in keys[i].lower()
    }


async def get_filler_episodes(filler_id):  # sourcery no-metrics
    "to get eppisode numbers"
    html = requests.get(animnefillerurl + filler_id).text
    soup = bs4.BeautifulSoup(html, "html.parser")
    div = soup.find("div", attrs={"id": "Condensed"})
    complete_anime = div.find_all("span", attrs={"class": "Episodes"})
    if len(complete_anime) == 1:
        total_episodes = complete_anime[0].findAll("a")
        mixed_episodes = None
        filler_episodes = None
        anime_canon_episodes = None
        total_ep = ", ".join(total_no.text for total_no in total_episodes)
    elif len(complete_anime) == 2:
        total_episodes = complete_anime[0].findAll("a")
        filler_ep = complete_anime[1].findAll("a")
        mixed_episodes = None
        anime_canon_episodes = None
        total_ep = ", ".join(total_no.text for total_no in total_episodes)
        filler_episodes = ", ".join(filler_no.text for filler_no in filler_ep)
    elif len(complete_anime) == 3:
        total_episodes = complete_anime[0].findAll("a")
        mixed_ep = complete_anime[1].findAll("a")
        filler_ep = complete_anime[2].findAll("a")
        anime_canon_episodes = None
        total_ep = ", ".join(total_no.text for total_no in total_episodes)
        filler_episodes = ", ".join(filler_no.text for filler_no in filler_ep)
        mixed_episodes = ", ".join(miixed_no.text for miixed_no in mixed_ep)
    elif len(complete_anime) == 4:
        total_episodes = complete_anime[0].findAll("a")
        mixed_ep = complete_anime[1].findAll("a")
        filler_ep = complete_anime[2].findAll("a")
        animecanon_ep = complete_anime[3].findAll("a")
        total_ep = ", ".join(total_no.text for total_no in total_episodes)
        filler_episodes = ", ".join(filler_no.text for filler_no in filler_ep)
        mixed_episodes = ", ".join(miixed_no.text for miixed_no in mixed_ep)
        anime_canon_episodes = ", ".join(
            animecanon_no.text for animecanon_no in animecanon_ep
        )
    return {
        "filler_id": filler_id,
        "total_ep": total_ep,
        "mixed_ep": mixed_episodes,
        "filler_episodes": filler_episodes,
        "anime_canon_episodes": anime_canon_episodes,
    }

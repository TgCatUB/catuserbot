# credits to @mrconfused (@sandy1709)

import re

import lyricsgenius

from userbot import catub

from ..Config import Config
from ..core.managers import edit_or_reply

plugin_category = "extra"

GENIUS = Config.GENIUS_API_TOKEN


@catub.cat_cmd(
    pattern="lyrics(?:\s|$)([\s\S]*)",
    command=("lyrics", plugin_category),
    info={
        "header": "Song lyrics searcher using genius api.",
        "description": "if you want to provide artist name with song name then use this format {tr}lyrics <artist name> - <song name> . if you use this format in your query then flags won't work. by default it will show first query.",
        "flags": {
            "-l": "to get list of search lists.",
            "-g": "To get paticular song lyrics.",
        },
        "note": "For functioning of this command set the GENIUS_API_TOKEN in heroku. Get value from  https://genius.com/developers.",
        "usage": [
            "{tr}lyrics <artist name> - <song name>",
            "{tr}lyrics -l <song name>",
            "{tr}lyrics -n<song number> <song name>",
        ],
        "examples": [
            "{tr}lyrics Armaan Malik - butta bomma",
            "{tr}lyrics -l butta bomma",
            "{tr}lyrics -n2 butta bomma",
        ],
    },
)
async def lyrics(event):  # sourcery no-metrics
    "To fetch song lyrics"
    if GENIUS is None:
        return await edit_or_reply(
            event,
            "`Set genius access token in heroku vars for functioning of this command`",
        )
    match = event.pattern_match.group(1)
    songno = re.findall(r"-n\d+", match)
    listview = re.findall(r"-l", match)
    try:
        songno = songno[0]
        songno = songno.replace("-n", "")
        match = match.replace("-n" + songno, "")
        songno = int(songno)
    except IndexError:
        songno = 1
    if songno < 1 or songno > 10:
        return await edit_or_reply(
            event,
            "`song number must be in between 1 to 10 use -l flag to query results`",
        )
    match = match.replace("-l", "")
    listview = bool(listview)
    query = match.strip()
    genius = lyricsgenius.Genius(GENIUS)
    if "-" in query:
        args = query.split("-", 1)
        artist = args[0].strip(" ")
        song = args[1].strip(" ")
        catevent = await edit_or_reply(
            event, f"`Searching lyrics for {artist} - {song}...`"
        )
        try:
            songs = genius.search_song(song, artist)
        except TypeError:
            songs = None
        if songs is None:
            return await catevent.edit(f"Song **{artist} - {song}** not found!")
        result = f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```"
    else:
        catevent = await edit_or_reply(event, f"`Searching lyrics for {query}...`")
        response = genius.search_songs(query)
        msg = f"**The songs found for the given query:** `{query}`\n\n"
        if len(response["hits"]) == 0:
            return await edit_or_reply(
                catevent, f"**I can't find lyrics for the given query: **`{query}`"
            )
        for i, an in enumerate(response["hits"], start=1):
            msg += f"{i}. `{an['result']['title']}`\n"
        if listview:
            result = msg
        else:
            result = f"**The song found for the given query:** `{query}`\n\n"
            if songno > len(response["hits"]):
                return await edit_or_reply(
                    catevent,
                    f"**Invalid song selection for the query select proper number**\n{msg}",
                )
            songtitle = response["hits"][songno - 1]["result"]["title"]
            result += f"`{genius.search_song(songtitle).lyrics}`"
    await edit_or_reply(catevent, result)

# \\ Created by-@mrconfused -- Github.com/sandy1709 //
# \\ Modified by-@Jisan7509 -- Github.com/Jisan09 //
#  \\    https://github.com/TgCatUB/catuserbot   //
#   \\        Plugin for @catuserbot            //
#    ````````````````````````````````````````````


import re

from ..Config import Config
from ..core.managers import edit_or_reply
from . import LyricsGen, catub

GENIUS = Config.GENIUS_API_TOKEN

plugin_category = "extra"


@catub.cat_cmd(
    pattern="lyrics(?:\s|$)([\s\S]*)",
    command=("lyrics", plugin_category),
    info={
        "header": "Song lyrics searcher using genius api.",
        "description": "if you want to provide artist name with song name then use this format {tr}lyrics <artist name> - <song name> . if you use this format in your query then flags won't work. by default it will show first query.",
        "flags": {
            "-l": "to get list of search lists.",
            "-n": "To get paticular song lyrics.",
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
            "<i>Set <code>GENIUS_API_TOKEN</code> in heroku vars for functioning of this command.\n\nCheck out this <b><a href = https://graph.org/How-to-get-Genius-API-Token-04-26>Tutorial</a></b></i>",
            parse_mode="html",
        )
    match = event.pattern_match.group(1)
    songno = re.findall(r"-n\d+", match)
    listview = re.findall(r"-l", match)
    try:
        songno = songno[0]
        songno = songno.replace("-n", "")
        match = match.replace(f"-n{songno}", "")
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
    song = songinfo = query
    artist = None
    if "-" in query:
        args = query.split("-", 1)
        artist = args[0].strip(" ")
        song = args[1].strip(" ")
        songinfo = f"{artist} - {song}"
        catevent = await edit_or_reply(event, f"`Searching lyrics for {songinfo}...`")
        lyrics = await LyricsGen.lyrics(event, song, artist)
        if lyrics is None:
            return await catevent.edit(f"Song **{songinfo}** not found!")
        result = f"**Search query**: \n`{songinfo}`\n\n```{lyrics}```"
    else:
        catevent = await edit_or_reply(event, f"`Searching lyrics for {query}...`")
        response = LyricsGen.songs(song)
        msg = f"**The songs found for the given query:** `{query}`\n\n"
        for i, an in enumerate(response, start=1):
            msg += f"{i}. `{an['result']['title']}`\n"
        if listview:
            result = msg
        else:
            result = f"**The song found for the given query:** `{query}`\n\n"
            if songno > len(response):
                return await edit_or_reply(
                    catevent,
                    f"**Invalid song selection for the query select proper number**\n{msg}",
                )
            songtitle = response[songno - 1]["result"]["title"]
            result += f"`{await LyricsGen.lyrics(event, songtitle)}`"
    await edit_or_reply(catevent, result)

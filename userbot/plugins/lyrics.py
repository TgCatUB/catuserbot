# \\ Created by-@mrconfused -- Github.com/sandy1709 //
# \\ Modified by-@Jisan7509 -- Github.com/Jisan09 //
#  \\    https://github.com/TgCatUB/catuserbot   //
#   \\        Plugin for @catuserbot            //
#    ````````````````````````````````````````````


import os
import re

import lyricsgenius
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock

from userbot import catub

from ..Config import Config
from ..core.managers import edit_or_reply

plugin_category = "extra"

GENIUS = Config.GENIUS_API_TOKEN
ENV = bool(os.environ.get("ENV", False))


class LyricGenius:
    def __init__(self):
        if GENIUS:
            self.genius = lyricsgenius.Genius(GENIUS)

    def songs(self, title):
        songs = self.genius.search_songs(title)["hits"]
        return songs

    def song(self, title, artist=None):
        song_info = None
        try:
            if not artist:
                song_info = self.songs(title)[0]["result"]
            else:
                for song in self.songs(title):
                    if artist in song["result"]["primary_artist"]["name"]:
                        song_info = song["result"]
                        break
                if not song_info:
                    for song in self.songs(f"{title} by {artist}"):
                        if artist in song["result"]["primary_artist"]["name"]:
                            song_info = song["result"]
                            break
        except (AttributeError, IndexError):
            pass
        return song_info

    async def lyrics(self, title, artist=None, mode="lyrics"):
        try:
            if ENV:
                if not artist:
                    song_info = self.song(title)["title"]
                    song = self.genius.search_song(song_info)
                    lyrics = song.lyrics
                    link = song.song_art_image_url
                else:
                    song = self.genius.search_song(title, artist)
                    lyrics = song.lyrics
                    link = song.song_art_image_url
            else:
                msg = f"{artist}-{title}" if artist else title
                chat = "@lyrics69bot"
                async with catub.conversation(chat) as conv:
                    try:
                        flag = await conv.send_message("/start")
                    except YouBlockedUserError:
                        await catub(unblock("lyrics69bot"))
                        flag = await conv.send_message("/start")
                    await conv.get_response()
                    await catub.send_read_acknowledge(conv.chat_id)
                    await conv.send_message(f"/{mode} {msg}")
                    if mode == "devloper":
                        link = (await conv.get_response()).text
                        await catub.send_read_acknowledge(conv.chat_id)
                    lyrics = (await conv.get_response()).text
                    await catub.send_read_acknowledge(conv.chat_id)
                    await delete_conv(catub, chat, flag)
        except (TypeError, KeyError):
            lyrics = link = None
        if mode == "devloper":
            return link, lyrics
        return lyrics


LyricsGen = LyricGenius()


async def delete_conv(client, chat, from_message):
    itermsg = client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await client.delete_messages(chat, msgs)
    await client.send_read_acknowledge(chat)


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
        return await edit_or_reply(event,"<i>Set <code>GENIUS_API_TOKEN</code> in heroku vars for functioning of this command.\n\nCheck out this <b><a href = https://telegra.ph/How-to-get-Genius-API-Token-04-26>Tutorial</a></b></i>",parse_mode="html")
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
        lyrics = await LyricsGen.lyrics(song, artist)
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
            result += f"`{await LyricsGen.lyrics(songtitle)}`"
    await edit_or_reply(catevent, result)

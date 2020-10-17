# credits to @mrconfused (@sandy1709)
import io
import os

import lyricsgenius
from tswift import Song

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP

GENIUS = os.environ.get("GENIUS_API_TOKEN", None)


@bot.on(admin_cmd(outgoing=True, pattern="lyrics ?(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="lyrics ?(.*)"))
async def _(event):
    catevent = await edit_or_reply(event, "wi8..! I am searching your lyrics....`")
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    reply = await event.get_reply_message()
    if event.pattern_match.group(1):
        query = event.pattern_match.group(1)
    elif reply.text:
        query = reply.message
    else:
        await catevent.edit("`What I am Supposed to find `")
        return
    song = ""
    song = Song.find_song(query)
    if song:
        if song.lyrics:
            reply = song.format()
        else:
            reply = "Couldn't find any lyrics for that song! try with artist name along with song if still doesnt work try `.glyrics`"
    else:
        reply = "lyrics not found! try with artist name along with song if still doesnt work try `.glyrics`"
    if len(reply) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(reply)) as out_file:
            out_file.name = "lyrics.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=query,
                reply_to=reply_to_id,
            )
            await catevent.delete()
    else:
        await catevent.edit(reply)


@bot.on(admin_cmd(outgoing=True, pattern="glyrics ?(.*)"))
@bot.on(sudo_cmd(allow_sudo=True, pattern="glyrics ?(.*)"))
async def lyrics(lyric):
    if lyric.pattern_match.group(1):
        query = lyric.pattern_match.group(1)
    else:
        await edit_or_reply(
            lyric,
            "Error: please use '-' as divider for <artist> and <song> \neg: `.glyrics Nicki Minaj - Super Bass`",
        )
        return
    if r"-" not in query:
        await edit_or_reply(
            lyric,
            "Error: please use '-' as divider for <artist> and <song> \neg: `.glyrics Nicki Minaj - Super Bass`",
        )
        return
    if GENIUS is None:
        await edit_or_reply(
            lyric,
            "`Provide genius access token to config.py or Heroku Var first kthxbye!`",
        )
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = query.split("-", 1)
            artist = args[0].strip(" ")
            song = args[1].strip(" ")
        except Exception as e:
            await edit_or_reply(lyric, f"Error:\n`{e}`")
            return
    if len(args) < 1:
        await edit_or_reply(lyric, "`Please provide artist and song names`")
        return
    catevent = await edit_or_reply(
        lyric, f"`Searching lyrics for {artist} - {song}...`"
    )
    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None
    if songs is None:
        await catevent.edit(f"Song **{artist} - {song}** not found!")
        return
    if len(songs.lyrics) > 4096:
        await catevent.edit("`Lyrics is too big, view the file to see it.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Search query: \n{artist} - {song}\n\n{songs.lyrics}")
        await lyric.client.send_file(
            lyric.chat_id,
            "lyrics.txt",
            reply_to=lyric.id,
        )
        os.remove("lyrics.txt")
    else:
        await catevent.edit(
            f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```"
        )
    return


CMD_HELP.update(
    {
        "lyrics": "**Plugin : **`lyrics`\
        \n\n**Syntax : **`.lyrics <aritst name - song nane>` __or__ `.lyrics <song_name>`\
        \n**Function : ** __searches a song lyrics and sends you if song name doesnt work try along with artisyt name__\
        \n\n**Syntax : ** .`glyrics <artist name> - <song name>`\
        \n**Function : **__genius lyrics finder for songs__\
        \n__note__: **-** is neccessary when searching the lyrics to divided artist and song\
        \nget this value from `https://genius.com/developers` \
        \nAdd:-  `GENIUS_API_TOKEN` and token value in heroku app settings for funtion of glyrics \
    "
    }
)

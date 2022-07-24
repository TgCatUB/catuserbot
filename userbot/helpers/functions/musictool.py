import contextlib
import os
from pathlib import Path

import lyricsgenius
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock

from ...Config import Config
from ...core.managers import edit_or_reply
from ..utils.utils import runcmd
from .functions import delete_conv
from .utube import name_dl, song_dl, video_dl

GENIUS = Config.GENIUS_API_TOKEN
ENV = bool(os.environ.get("ENV", False))


class LyricGenius:
    def __init__(self):
        if GENIUS:
            self.genius = lyricsgenius.Genius(GENIUS)

    def songs(self, title):
        return self.genius.search_songs(title)["hits"]

    def song(self, title, artist=None):
        song_info = None
        with contextlib.suppress(AttributeError, IndexError):
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
        return song_info

    async def lyrics(self, event, title, artist=None, mode="lyrics"):
        lyrics = link = None
        if ENV:
            if not artist:
                song_info = self.song(title)["title"]
                song = self.genius.search_song(song_info)
            else:
                song = self.genius.search_song(title, artist)
            if song:
                lyrics = song.lyrics
                link = song.song_art_image_url
        else:
            msg = f"{artist}-{title}" if artist else title
            chat = "@CatMusicRobot"
            async with event.client.conversation(chat) as conv:
                try:
                    flag = await conv.send_message("/start")
                except YouBlockedUserError:
                    await event.client(unblock("CatMusicRobot"))
                    flag = await conv.send_message("/start")
                await conv.get_response()
                await event.client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(f"/{mode} {msg}")
                if mode == "devloper":
                    link = (await conv.get_response()).text
                    await event.client.send_read_acknowledge(conv.chat_id)
                lyrics = (await conv.get_response()).text
                await event.client.send_read_acknowledge(conv.chat_id)
                await delete_conv(event, chat, flag)
        if mode == "devloper":
            return link, lyrics
        return lyrics


LyricsGen = LyricGenius()


async def song_download(url, event, quality="128k", video=False, title=True):
    media_type = "Audio"
    media_ext = ["mp3", "mp4a"]
    media_cmd = song_dl.format(QUALITY=quality, video_link=url)
    name_cmd = name_dl.format(video_link=url)
    if video:
        media_type = "Video"
        media_ext = ["mp4", "mkv"]
        media_cmd = video_dl.format(video_link=url)

    with contextlib.suppress(Exception):
        stderr = (await runcmd(media_cmd))[1]
        media_name, stderr = (await runcmd(name_cmd))[:2]
        if stderr:
            return await edit_or_reply(event, f"**Error ::** `{stderr}`")
        media_name = os.path.splitext(media_name)[0]
        media_file = Path(f"{media_name}.{media_ext[0]}")
    if not os.path.exists(media_file):
        media_file = Path(f"{media_name}.{media_ext[1]}")
    elif not os.path.exists(media_file):
        return await edit_or_reply(
            event, f"__Sorry!.. I'm unable to find your requested {media_type}.__"
        )
    await edit_or_reply(event, f"__Uploading requested {media_type}...__")
    media_thumb = Path(f"{media_name}.jpg")
    if not os.path.exists(media_thumb):
        media_thumb = Path(f"{media_name}.webp")
    elif not os.path.exists(media_thumb):
        media_thumb = None
    if title:
        media_title = media_name.replace("./temp/", "").replace("_", "|")
        return media_file, media_thumb, media_title
    return media_file, media_thumb

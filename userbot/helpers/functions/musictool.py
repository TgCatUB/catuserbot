# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import contextlib
import os
from pathlib import Path

import lyricsgenius
import requests
from bs4 import BeautifulSoup

from ...Config import Config
from ...core.managers import edit_or_reply
from ...helpers.google_tools import chromeDriver
from ..utils.utils import runcmd
from .utube import name_dl, song_dl, video_dl

GENIUS = Config.GENIUS_API_TOKEN


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

    def lyrics(self, title, artist=None):
        lyrics = ""
        song_info = self.song(title, artist)
        title = song_info["title"]
        link = song_info["song_art_image_url"] or None
        if not artist:
            artist = song_info["primary_artist"]["name"]
        try:
            song = self.genius.search_song(title, artist)
            lyrics = song.lyrics.split(f"{title} Lyrics")
            if len(lyrics) > 1:
                lyrics = (
                    lyrics[1]
                    .replace("[", "\n\n[")
                    .replace("\n\n\n[", "\n\n[")
                    .replace("\n\n\n", "\n\n")
                )
        except Exception:
            # try to scrap 1st
            url = f"https://www.musixmatch.com/lyrics/{artist.replace(' ', '-')}/{title.replace(' ', '-')}"
            soup, _ = chromeDriver.get_html(url)
            soup = BeautifulSoup(soup, "html.parser")
            lyrics_containers = soup.find_all(class_="lyrics__content__ok")
            for container in lyrics_containers:
                lyrics += container.get_text().strip()

            # if private data then show 30%
            if not lyrics:
                base_url = "https://api.musixmatch.com/ws/1.1/"
                endpoint = (
                    base_url
                    + f"matcher.lyrics.get?format=json&q_track={title}&q_artist={artist}&apikey=bf9bfaeccae52f5a4366bcdb2a6b0c4e"
                )
                response = requests.get(endpoint)
                data = response.json()
                lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]
        return link, lyrics


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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K


from telethon import events
import asyncio
from bs4 import BeautifulSoup
import requests

from userbot.utils import admin_cmd

@borg.on(admin_cmd(pattern=f"yify recents", allow_sudo=True))
@borg.on(events.NewMessage(pattern=r"\.yify recents", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    uploadbot = await borg.get_entity("@uploadbot")
    BASE_URL = "https://yts.pm"
    tg_feed_link = BASE_URL + "/browse-movies"
    main_page_response = requests.get(tg_feed_link)
    main_soup = BeautifulSoup(main_page_response.text, "html.parser")
    movies_in_page = main_soup.find_all("div", class_="browse-movie-wrap")
    for movie in movies_in_page:
        movie_bottom = movie.div
        name = movie_bottom.a.string
        year = movie_bottom.div.string
        movie_links = movie.div.find_all("a")
        movie_links = movie_links[1:]
        for torrent_link in movie_links:
            href_link = BASE_URL + torrent_link.get("href")
            magnetic_link_response = requests.get(href_link, allow_redirects=False)
            magnetic_link = magnetic_link_response.headers.get("Location")
            await borg.send_message(
                uploadbot,
                magnetic_link
            )
            # return False
            await asyncio.sleep(120)



import os
import re
import time
import urllib.request
import zipfile
from datetime import datetime
from random import choice

import PIL.ImageOps
import requests
from emoji import get_emoji_regexp
from PIL import Image, ImageDraw, ImageFont
from telethon.tl.types import Channel, PollAnswer
from validators.url import url
from youtubesearchpython import VideosSearch

from ..resources.states import states

song_dl = "youtube-dl --force-ipv4 --write-thumbnail -o './temp/%(title)s.%(ext)s' --extract-audio --audio-format mp3 --audio-quality {QUALITY} {video_link}"
thumb_dl = "youtube-dl --force-ipv4 -o './temp/%(title)s.%(ext)s' --write-thumbnail --skip-download {video_link}"
video_dl = "youtube-dl --force-ipv4 --write-thumbnail  -o './temp/%(title)s.%(ext)s' -f '[filesize<20M]' {video_link}"
name_dl = (
    "youtube-dl --force-ipv4 --get-filename -o './temp/%(title)s.%(ext)s' {video_link}"
)


async def ytsearch(query, limit):
    result = ""
    videolinks = VideosSearch(query.lower(), limit=limit)
    for v in videolinks.result()["result"]:
        textresult = f"[{v['title']}](https://www.youtube.com/watch?v={v['id']})\n"
        try:
            textresult += f"**Description : **`{v['descriptionSnippet'][-1]['text']}`\n"
        except Exception:
            textresult += "**Description : **`None`\n"
        textresult += f"**Duration : **__{v['duration']}__  **Views : **__{v['viewCount']['short']}__\n"
        result += f"☞ {textresult}\n"
    return result

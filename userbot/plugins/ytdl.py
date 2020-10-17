# Thanks to @AvinashReddy3108 for this plugin

import asyncio
import os
import time
from html import unescape
from pathlib import Path

from googleapiclient.discovery import build
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from .. import CMD_HELP
from ..utils import admin_cmd, edit_or_reply, progress, sudo_cmd


@bot.on(admin_cmd(pattern="yt(a|v) (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="yt(a|v) (.*)", allow_sudo=True))
async def download_video(v_url):
    """ For .ytdl command, download media from YouTube and many other sites. """
    url = v_url.pattern_match.group(2)
    ytype = v_url.pattern_match.group(1).lower()
    v_url = await edit_or_reply(v_url, "`Preparing to download...`")
    if ytype == "a":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        video = False
        song = True
    elif ytype == "v":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        await v_url.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await v_url.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await v_url.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    catthumb = Path(f"{ytdl_data['id']}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{ytdl_data['id']}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None
    if song:
        await v_url.edit(
            f"`Preparing to upload song:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await borg.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            thumb=catthumb,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(ytdl_data["duration"]),
                    title=str(ytdl_data["title"]),
                    performer=str(ytdl_data["uploader"]),
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, v_url, c_time, "Uploading..", f"{ytdl_data['title']}.mp3"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp3")
        if catthumb:
            os.remove(catthumb)
        await v_url.delete()
    elif video:
        await v_url.edit(
            f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*"
        )
        await borg.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data["title"],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(
                    d, t, v_url, c_time, "Uploading..", f"{ytdl_data['title']}.mp4"
                )
            ),
        )
        os.remove(f"{ytdl_data['id']}.mp4")
        if catthumb:
            os.remove(catthumb)
        await v_url.delete()


@bot.on(admin_cmd(pattern="yts (.*)"))
@bot.on(sudo_cmd(pattern="yts (.*)", allow_sudo=True))
async def yt_search(video_q):
    """ For .yts command, do a YouTube search from Telegram. """
    query = video_q.pattern_match.group(1)
    result = ""
    if not Config.YOUTUBE_API_KEY:
        await edit_or_reply(
            video_q,
            "`Error: YouTube API key missing! Add it to reveal config vars in heroku or userbot/uniborgConfig.py in github fork.`",
        )
        return
    video_q = await edit_or_reply(video_q, "```Processing...```")
    full_response = await youtube_search(query)
    videos_json = full_response[1]
    for video in videos_json:
        title = f"{unescape(video['snippet']['title'])}"
        link = f"https://youtu.be/{video['id']['videoId']}"
        result += f"{title}\n{link}\n\n"
    reply_text = f"**Search Query:**\n`{query}`\n\n**Results:**\n\n{result}"
    await video_q.edit(reply_text)


async def youtube_search(
    query, order="relevance", token=None, location=None, location_radius=None
):
    """ Do a YouTube search. """
    youtube = build(
        "youtube", "v3", developerKey=Config.YOUTUBE_API_KEY, cache_discovery=False
    )
    search_response = (
        youtube.search()
        .list(
            q=query,
            type="video",
            pageToken=token,
            order=order,
            part="id,snippet",
            maxResults=10,
            location=location,
            locationRadius=location_radius,
        )
        .execute()
    )
    videos = [
        search_result
        for search_result in search_response.get("items", [])
        if search_result["id"]["kind"] == "youtube#video"
    ]

    try:
        nexttok = search_response["nextPageToken"]
        return (nexttok, videos)
    except HttpError:
        nexttok = "last_page"
        return (nexttok, videos)
    except KeyError:
        nexttok = "KeyError, try again."
        return (nexttok, videos)


CMD_HELP.update(
    {
        "ytdl": "**Plugin :** `ytdl`\
    \n\n**Syntax :** `.yta link`\
    \n**Usage : **downloads th audio from the given link(Suports the all sites which support youtube-dl)\
    \n\n**Syntax : **`.ytv link`\
    \n**Usage : **downloads th video from the given link(Suports the all sites which support youtube-dl)\
    \n\n**Syntax : ** `.yts query`\
    \n**Usage : **Fetches youtube results you need api token for this\
    "
    }
)

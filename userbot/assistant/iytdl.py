""" Download Youtube Video / Audio in a User friendly interface """
# --------------------------- #
#   Modded ytdl by code-rgb   #
# --------------------------- #

import glob
import os
import io
import asyncio
from collections import defaultdict
from pathlib import Path
import re
from time import time
from telethon.utils import get_attributes
from ..core.managers import edit_delete, edit_or_reply
import ujson
import youtube_dl
from telethon import Button,types
from telethon.events import CallbackQuery, InlineQuery
from wget import download
from youtube_dl.utils import DownloadError, ExtractorError, GeoRestrictedError
from youtubesearchpython import VideosSearch
from ..Config import Config
from ..core import pool, check_owner
from userbot import catub
from ..core.logger import logging
from ..helpers import AioHttp, humanbytes,post_to_telegraph,rand_key,sublists,progress


LOGS = logging.getLogger(__name__)
BASE_YT_URL = "https://www.youtube.com/watch?v="
YOUTUBE_REGEX = re.compile(
    r"(?:youtube\.com|youtu\.be)/(?:[\w-]+\?v=|embed/|v/|shorts/)?([\w-]{11})"
)
PATH = "./userbot/cache/ytsearch.json"


class YT_Search_X:
    def __init__(self):
        if not os.path.exists(PATH):
            with open(PATH, "w") as f_x:
                ujson.dump({}, f_x)
        with open(PATH) as yt_db:
            self.db = ujson.load(yt_db)

    def store_(self, rnd_id: str, results: dict):
        self.db[rnd_id] = results
        self.save()

    def save(self):
        with open(PATH, "w") as outfile:
            ujson.dump(self.db, outfile, indent=4)


ytsearch_data = YT_Search_X()


async def get_ytthumb(videoid: str):
    thumb_quality = [
        "maxresdefault.jpg",  # Best quality
        "hqdefault.jpg",
        "sddefault.jpg",
        "mqdefault.jpg",
        "default.jpg",  # Worst quality
    ]
    thumb_link = "https://i.imgur.com/4LwPLai.png"
    for qualiy in thumb_quality:
        link = f"https://i.ytimg.com/vi/{videoid}/{qualiy}"
        if await AioHttp().status(link) == 200:
            thumb_link = link
            break
    return thumb_link

@catub.cat_cmd(
    pattern="iytdl(?: |$)(.*)",
    command=("iytdl", plugin_category),
    info={
        "header": "ytdl with inline buttons.",
        "description": "An api that Fetchs random Quote from `goodreads.com`",
        "usage": "{tr}iytdl [URL / Text] or [Reply to URL / Text]",
    },
)
async def iytdl_inline(event):
    "ytdl with inline buttons."
    reply = await event.get_reply_message()
    reply_to_id = await reply_id(event)
    input_str =event.pattern_match.group(1)
    input_url = None
    if input_str:
        input_url = (input_str).strip()
    elif reply and reply.text:
        input_url = (reply.text).strip()
    if not input_url:
        return await edit_delete(event,"Give input or reply to a valid youtube URL")
    catevent = await edit_or_reply(event,f"🔎 Searching Youtube for: `'{input_url}'`")
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, f"ytdl {input_url}")
    await catevent.delete()
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)



@catub.tgbot.on(CallbackQuery(data=re.compile(r"^ytdl_download_(.*)_([\d]+|mkv|mp4|mp3)(?:_(a|v))?")))
@check_owner
async def ytdl_download_callback(c_q: CallbackQuery):
        yt_code = c_q.matches[0].group(1)
        choice_id = c_q.matches[0].group(2)
        downtype = c_q.matches[0].group(3)
        if str(choice_id).isdigit():
            choice_id = int(choice_id)
            if choice_id == 0:
                await c_q.answer("🔄  Processing...", show_alert=False)
                await c_q.edit(
                    buttons=(await download_button(yt_code))
                )
                return
        startTime = time()
        choice_str, disp_str = get_choice_by_id(choice_id, downtype)
        media_type = "Video" if downtype == "v" else "Audio"
        callback_continue = f"Downloading {media_type} Please Wait..."
        callback_continue += f"\n\nFormat Code : {disp_str}"
        await c_q.answer(callback_continue, show_alert=True)
        upload_msg = await c_q.client.send_message(BOTLOG_CHATID, "Uploading...")
        yt_url = BASE_YT_URL + yt_code
        await c_q.edit(
            f"**⬇️ Downloading {media_type} ...**\n\n🔗  [<b>Link</b>]({yt_url})\n🆔  <b>Format Code</b> : {disp_str}"
        )
        if downtype == "v":
            retcode = await _tubeDl(url=yt_url, starttime=startTime, uid=choice_str)
        else:
            retcode = await _mp3Dl(url=yt_url, starttime=startTime, uid=choice_str)
        if retcode != 0:
            return await upload_msg.edit(str(retcode))
        _fpath = ""
        thumb_pic = None
        for _path in glob.glob(os.path.join(Config.TEMP_DIR , str(startTime), "*")):
            if _path.lower().endswith((".jpg", ".png", ".webp")):
                thumb_pic = _path
            else:
                _fpath = _path
        if not _fpath:
            await edit_delete(upload_msg,"nothing found !")
            return
        if not thumb_pic and downtype == "v":
            thumb_pic = str(
                await pool.run_in_thread(download)(await get_ytthumb(yt_code))
            )
        attributes, mime_type = get_attributes(str(_fpath))
        ul = io.open(Path(_fpath), "rb")
        uploaded = await event.client.fast_upload_file(
            file=ul,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, startTime, "trying to upload", file_name=os.path.basename(Path(_path)))
            ),
        )
        ul.close()
        media = types.InputMediaUploadedDocument(
            file=uploaded,
            mime_type=mime_type,
            attributes=attributes,
            force_file=False,
            thumb=await event.client.upload_file(thumb_pic) if thumb_pic else None,
        )
        uploaded_media = await event.client.send_file(
            BOTLOG_CHATID,
            file=media,
            caption=f"**File Name : **`{os.path.basename(Path(_path))}`",
        )
        await c_q.edit(
                text=f"📹  **[{uploaded_media.caption}]({yt_url})**",
                file=uploaded_media.media
            )

    
@catub.tgbot.on(CallbackQuery(data=re.compile(r"^ytdl_(listall|back|next|detail)_([a-z0-9]+)_(.*)")))
@check_owner
async def ytdl_callback(c_q: CallbackQuery):
        choosen_btn = c_q.matches[0].group(1)
        data_key = c_q.matches[0].group(2)
        page = c_q.matches[0].group(3)
        if not os.path.exists(PATH):
            return await c_q.answer(
                "Search data doesn't exists anymore, please perform search again ...",
                show_alert=True,
            )
        with open(PATH) as f:
            view_data = ujson.load(f)
        search_data = view_data.get(data_key)
        total = len(search_data)
        if choosen_btn == "back":
            index = int(page) - 1
            del_back = index == 1
            await c_q.answer()
            back_vid = search_data.get(str(index))
            await c_q.edit(
                text=back_vid.get("message"),
                file=back_vid.get("thumb"),
                reply_markup=yt_search_btns(
                    del_back=del_back,
                    data_key=data_key,
                    page=index,
                    vid=back_vid.get("video_id"),
                    total=total,
                ),
            )
        elif choosen_btn == "next":
            index = int(page) + 1
            if index > total:
                return await c_q.answer("That's All Folks !", show_alert=True)
            await c_q.answer()
            front_vid = search_data.get(str(index))
            await c_q.edit(
                text=back_vid.get("message"),
                file=back_vid.get("thumb"),
                reply_markup=yt_search_btns(
                    data_key=data_key,
                    page=index,
                    vid=front_vid.get("video_id"),
                    total=total,
                ),
            )
        elif choosen_btn == "listall":
            await c_q.answer("View Changed to:  📜  List", show_alert=False)
            list_res = "".join(
                search_data.get(vid_s).get("list_view") for vid_s in search_data
            )

            telegraph = post_to_telegraph(
                a_title=f"Showing {total} youtube video results for the given query ...",
                content=list_res,
            )
            await c_q.edit(
                file=search_data.get("1").get("thumb"),
                reply_markup=[
                        (
                            Button.url(
                                "↗️  Click To Open",
                                url=telegraph,
                            )
                        ),
                        (
                            Button.inline(
                                "📰  Detailed View",
                                data=f"ytdl_detail_{data_key}_{page}",
                            )
                        ),
                    ]
                )
        else:  # Detailed
            index = 1
            await c_q.answer("View Changed to:  📰  Detailed", show_alert=False)
            first = search_data.get(str(index))
            await c_q.edit(
                        text=first.get("message"),
                        file=first.get("thumb"),
                        reply_markup=yt_search_btns(
                            del_back=True,
                            data_key=data_key,
                            page=index,
                            vid=first.get("video_id"),
                            total=total,
                        ),
            )


@pool.run_in_thread
def _tubeDl(url: str, starttime, uid: str):
    ydl_opts = {
        "addmetadata": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "outtmpl": os.path.join(
            Config.TEMP_DIR , str(starttime), "%(title)s-%(format)s.%(ext)s"
        ),
        "logger": LOGS,
        "format": uid,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "postprocessors": [
            {"key": "FFmpegMetadata"}
            # ERROR R15: Memory quota vastly exceeded
            # {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
        ],
        "quiet": True,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            x = ydl.download([url])
    except DownloadError as e:
        LOGS.error(e)
    except GeoRestrictedError:
        LOGS.error(
            "ERROR: The uploader has not made this video available in your country"
        )
    else:
        return x


@pool.run_in_thread
def _mp3Dl(url: str, starttime, uid: str):
    _opts = {
        "outtmpl": os.path.join(Config.TEMP_DIR , str(starttime), "%(title)s.%(ext)s"),
        "logger": LOGS,
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "format": "bestaudio/best",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": uid,
            },
            {"key": "EmbedThumbnail"},  # ERROR: Conversion failed!
            {"key": "FFmpegMetadata"},
        ],
        "quiet": True,
    }
    try:
        with youtube_dl.YoutubeDL(_opts) as ytdl:
            dloader = ytdl.download([url])
    except Exception as y_e:
        LOGS.exception(y_e)
        return y_e
    else:
        return dloader


def get_yt_video_id(url: str):
    # https://regex101.com/r/c06cbV/1
    match = YOUTUBE_REGEX.search(url)
    if match:
        return match.group(1)


# Based on https://gist.github.com/AgentOak/34d47c65b1d28829bb17c24c04a0096f
def get_choice_by_id(choice_id, media_type: str):
    if choice_id == "mkv":
        # default format selection
        choice_str = "bestvideo+bestaudio/best"
        disp_str = "best(video+audio)"
    elif choice_id == "mp4":
        # Download best Webm / Mp4 format available or any other best if no mp4
        # available
        choice_str = "bestvideo[ext=webm]+251/bestvideo[ext=mp4]+(258/256/140/bestaudio[ext=m4a])/bestvideo[ext=webm]+(250/249)/best"
        disp_str = "best(video+audio)[webm/mp4]"
    elif choice_id == "mp3":
        choice_str = "320"
        disp_str = "320 Kbps"
    else:
        disp_str = str(choice_id)
        if media_type == "v":
            # mp4 video quality + best compatible audio
            choice_str = disp_str + "+(258/256/140/bestaudio[ext=m4a])/best"
        else:  # Audio
            choice_str = disp_str
    return choice_str, disp_str


async def result_formatter(results: list):
    output = {}
    for index, r in enumerate(results, start=1):
        thumb = (r.get("thumbnails").pop()).get("url")
        upld = r.get("channel")
        title = f'<a href={r.get("link")}><b>{r.get("title")}</b></a>\n'
        out = title
        if r.get("descriptionSnippet"):
            out += "<code>{}</code>\n\n".format(
                "".join(x.get("text") for x in r.get("descriptionSnippet"))
            )
        out += f'<b>❯  Duration:</b> {r.get("accessibility").get("duration")}\n'
        views = f'<b>❯  Views:</b> {r.get("viewCount").get("short")}\n'
        out += views
        out += f'<b>❯  Upload date:</b> {r.get("publishedTime")}\n'
        if upld:
            out += "<b>❯  Uploader:</b> "
            out += f'<a href={upld.get("link")}>{upld.get("name")}</a>'
        v_deo_id = r.get("id")
        output[index] = dict(
            message=out,
            thumb=thumb,
            video_id=v_deo_id,
            list_view=f'<img src={thumb}><b><a href={r.get("link")}>{index}. {r.get("accessibility").get("title")}</a></b><br>',
        )

    return output


def yt_search_btns(
    data_key: str, page: int, vid: str, total: int, del_back: bool = False
):
    buttons = [
        (
            Button.inline(
                text="⬅️  Back",
                data=f"ytdl_back_{data_key}_{page}",
            ),
            Button.inline(
                text=f"{page} / {total}",
                data=f"ytdl_next_{data_key}_{page}",
            ),
        ),
        (
            Button.inline(
                text="📜  List all",
                data=f"ytdl_listall_{data_key}_{page}",
            ),
            Button.inline(
                text="⬇️  Download",
                data=f"ytdl_download_{vid}_0",
            ),
        ),
    ]
    if del_back:
        buttons[0].pop(0)
    return buttons


@pool.run_in_thread
def download_button(vid: str, body: bool = False):  # sourcery no-metrics
    try:
        vid_data = youtube_dl.YoutubeDL({"no-playlist": True}).extract_info(
            BASE_YT_URL + vid, download=False
        )
    except ExtractorError:
        vid_data = {"formats": []}
    buttons = [
        (
            Button.inline(
                "⭐️ BEST - 📹 MKV", data=f"ytdl_download_{vid}_mkv_v"
            ),
            Button.inline(
                "⭐️ BEST - 📹 WebM/MP4",
                data=f"ytdl_download_{vid}_mp4_v",
            ),
        )
    ]
    # ------------------------------------------------ #
    qual_dict = defaultdict(lambda: defaultdict(int))
    qual_list = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p"]
    audio_dict = {}
    # ------------------------------------------------ #
    for video in vid_data["formats"]:

        fr_note = video.get("format_note")
        fr_id = int(video.get("format_id"))
        fr_size = video.get("filesize")
        if video.get("ext") == "mp4":
            for frmt_ in qual_list:
                if fr_note in (frmt_, frmt_ + "60"):
                    qual_dict[frmt_][fr_id] = fr_size
        if video.get("acodec") != "none":
            bitrrate = int(video.get("abr", 0))
            if bitrrate != 0:
                audio_dict[
                    bitrrate
                ] = f"🎵 {bitrrate}Kbps ({humanbytes(fr_size) or 'N/A'})"

    video_btns = []
    for frmt in qual_list:
        frmt_dict = qual_dict[frmt]
        if len(frmt_dict) != 0:
            frmt_id = sorted(list(frmt_dict))[-1]
            frmt_size = humanbytes(frmt_dict.get(frmt_id)) or "N/A"
            video_btns.append(
                Button.inline(
                    f"📹 {frmt} ({frmt_size})",
                    data=f"ytdl_download_{vid}_{frmt_id}_v",
                )
            )
    buttons += sublists(video_btns, width=2)
    buttons += [
        (
            Button.inline(
                "⭐️ BEST - 🎵 320Kbps - MP3", data=f"ytdl_download_{vid}_mp3_a"
            )
        )
    ]
    buttons += sublists(
        [
            Button.inline(
                audio_dict.get(key_), data=f"ytdl_download_{vid}_{key_}_a"
            )
            for key_ in sorted(audio_dict.keys())
        ],
        width=2,
    )
    if body:
        vid_body = f"<b>[{vid_data.get('title')}]({vid_data.get('webpage_url')})</b>"
        return vid_body, buttons
    return buttons

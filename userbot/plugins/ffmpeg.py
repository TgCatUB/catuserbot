# ported from uniborg by @spechide
import asyncio
import contextlib
import io
import math
import os
import re
import time
import pathlib
from datetime import datetime

from userbot import catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import (
    _catutils,
    fileinfo,
    humanbytes,
    media_type,
    progress,
    readable_time,
    reply_id,
    take_screen_shot,
    time_formatter,
)

plugin_category = "utils"


thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
NAME = "untitled"
MERGER_DIR = pathlib.Path(os.path.join(os.getcwd(), "merger"))
FF_MPEG_DOWN_LOAD_MEDIA_PATH = os.path.join(
    Config.TMP_DOWNLOAD_DIRECTORY, "catuserbot.media.ffmpeg"
)
FINISHED_PROGRESS_STR = Config.FINISHED_PROGRESS_STR
UN_FINISHED_PROGRESS_STR = Config.UNFINISHED_PROGRESS_STR
LOGGER = logging.getLogger(__name__)


async def convert_video(video_file, output_directory, crf, total_time, bot, message):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = f"{output_directory}/{str(round(time.time()))}.mp4"
    progress = f"{output_directory}/progress.txt"
    with open(progress, "w") as f:
        pass
    COMPRESSION_START_TIME = time.time()
    process = await asyncio.create_subprocess_shell(
        f'ffmpeg -hide_banner -loglevel quiet -progress {progress} -i """{video_file}""" -preset ultrafast -vcodec libx265 -crf {crf} -c:a copy """{out_put_file_name}"""',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    LOGGER.info(f"ffmpeg_process: {str(process.pid)}")
    while process.returncode != 0:
        await asyncio.sleep(3)
        with open("./temp/progress.txt", "r+") as file:
            text = file.read()
            frame = re.findall("frame=(\d+)", text)
            time_in_us = re.findall("out_time_ms=(\d+)", text)
            progress = re.findall("progress=(\w+)", text)
            speed = re.findall("speed=(\d+\.?\d*)", text)
            frame = int(frame[-1]) if len(frame) else 1
            speed = speed[-1] if len(speed) else 1
            time_in_us = time_in_us[-1] if len(time_in_us) else 1
            if len(progress) and progress[-1] == "end":
                LOGGER.info(progress[-1])
                break
            time_formatter((time.time() - COMPRESSION_START_TIME))
            elapsed_time = int(time_in_us) / 1000000
            difference = math.floor((total_time - elapsed_time) / float(speed))
            ETA = "-"
            if difference > 0:
                ETA = time_formatter(difference)
            percentage = math.floor(elapsed_time * 100 / total_time)
            progress_str = "📊 **Progress :** {0}%\n[{1}{2}]".format(
                round(percentage, 2),
                "".join(
                    [FINISHED_PROGRESS_STR for _ in range(math.floor(percentage / 10))]
                ),
                "".join(
                    [
                        UN_FINISHED_PROGRESS_STR
                        for _ in range(10 - math.floor(percentage / 10))
                    ]
                ),
            )

            stats = (
                f"📦️ **Compressing CRF-{crf}**\n\n"
                f"⏰️ **ETA :** {ETA}\n\n"
                f"{progress_str}\n"
            )
            with contextlib.suppress(Exception):
                await message.edit(text=stats)
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    return out_put_file_name if os.path.lexists(out_put_file_name) else None


async def cult_small_video(
    video_file, output_directory, start_time, end_time, out_put_file_name=None
):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = out_put_file_name or os.path.join(
        output_directory, f"{round(time.time())}.mp4"
    )
    process = await asyncio.create_subprocess_shell(
        # stdout must a pipe to be accessible as process.stdout
        f'ffmpeg -i """{video_file}""" -ss {start_time} -to {end_time} -async 1 -strict -2 """{out_put_file_name}"""',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    await process.communicate()
    return out_put_file_name if os.path.lexists(out_put_file_name) else None

async def tg_dl(mone, reply):
    "To download the replied telegram file"
    name = NAME
    path = None
    if not os.path.isdir(Config.TEMP_DIR):
        os.makedirs(Config.TEMP_DIR)
    start = datetime.now()
    for attr in getattr(reply.document, "attributes", []):
        if isinstance(attr, types.DocumentAttributeFilename):
            name = attr.file_name
    path = pathlib.Path(os.path.join(MERGER_DIR, name))
    ext = get_extension(reply.document)
    if path and not path.suffix and ext:
        path = path.with_suffix(ext)
    if name == NAME:
        name += "_" + str(getattr(reply.document, "id", reply.id)) + ext
    if path and path.exists():
        if path.is_file():
            newname = f"{str(path.stem)}_OLD"
            path.rename(path.with_name(newname).with_suffix(path.suffix))
            file_name = path
        else:
            file_name = path / name
    elif path and not path.suffix and ext:
        file_name = MERGER_DIR / path.with_suffix(ext)
    elif path:
        file_name = path
    else:
        file_name = MERGER_DIR / name
    file_name.parent.mkdir(parents=True, exist_ok=True)
    c_time = time.time()
    progress_callback = lambda d, t: asyncio.get_event_loop().create_task(
        progress(d, t, mone, c_time, "trying to download")
    )
    if (
        not reply.document
        and reply.photo
        and file_name
        and file_name.suffix
        or not reply.document
        and not reply.photo
    ):
        await reply.download_media(
            file=file_name.absolute(), progress_callback=progress_callback
        )
    elif not reply.document:
        file_name = await reply.download_media(
            file=MERGER_DIR, progress_callback=progress_callback
        )
    else:
        dl = io.FileIO(file_name.absolute(), "a")
        await catub.fast_download_file(
            location=reply.document,
            out=dl,
            progress_callback=progress_callback,
        )
        dl.close()
    end = datetime.now()
    ms = (end - start).seconds
    await mone.edit(
        f"**•  Downloaded in {ms} seconds.**\n**•  Downloaded to :- **  `{os.path.relpath(file_name,os.getcwd())}`\n"
    )

    return [os.path.relpath(file_name, os.getcwd()), file_name]


async def merger(output_name=f"{MERGER_DIR}/MineisZarox.mp4"):
    process = await asyncio.create_subprocess_shell(
        f'ffmpeg -f concat -safe 0 -i {MERGER_DIR}/join.txt -c copy {output_name}',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.communicate()
    return output_name if os.path.lexists(output_name) else None


@catub.cat_cmd(
    pattern="(|f)compress(?:\s|$)([\s\S]*)",
    command=("compress", plugin_category),
    info={
        "header": "Compress the video file.",
        "description": "Will compress the replied video, if not replied to video it will check any video saved by .ffmpegsave or not.",
        "flags": {
            "f": "To Force file the compressed video.",
        },
        "note": "For quality of compress choose CRF value [ 0 - 51 ]\nHigher crf value = less video size = low on quality.\nIf no crf given it will use default value 23.",
        "usage": [
            "{tr}compress < 0 - 51 >",
            "{tr}fcompress < 0 - 51 >",
        ],
        "examples": [
            "{tr}compress",
            "{tr}fcompress",
            "{tr}compress 35",
            "{tr}fcompress 35",
        ],
    },
)
async def ffmpeg_compress(event):  # sourcery skip: low-code-quality
    "Compress the video file."
    crf = event.pattern_match.group(2)
    reply_to_id = await reply_id(event)
    cmd = event.pattern_match.group(1).lower()
    reply_message = await event.get_reply_message()
    start = datetime.now()
    if not crf:
        crf = "23"
    dlpath = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "cat.media.ffmpeg")
    if reply_message and reply_message.media:
        media = await media_type(reply_message)
        if (
            reply_message.media.document.mime_type.split("/")[0] != "video"
            or media == "Sticker"
        ):
            return await edit_delete(event, "`Only Video files are supported`")
        catevent = await edit_or_reply(event, "`Saving the file...`")
        try:
            c_time = time.time()
            dl = io.FileIO(dlpath, "a")
            await event.client.fast_download_file(
                location=reply_message.document,
                out=dl,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "Trying to download")
                ),
            )
            dl.close()
        except Exception as e:
            await edit_or_reply(catevent, f"**Error:**\n`{e}`")
        else:
            await edit_or_reply(catevent, "`Processing...`")
            delete = True
    elif os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        media = (await fileinfo(FF_MPEG_DOWN_LOAD_MEDIA_PATH))["type"]
        if media not in ["Video"]:
            return await edit_delete(event, "`Only Video files are supported`")
        dlpath = FF_MPEG_DOWN_LOAD_MEDIA_PATH
        catevent = await edit_or_reply(event, "`Processing...`")
        delete = False
    else:
        await edit_delete(event, "`Reply to Video file or save video by .ffmpegsave`")
    old = await fileinfo(dlpath)
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")
    cstart = datetime.now()
    compress = await convert_video(
        dlpath, "./temp", crf, old["duration"], catub, catevent
    )
    cend = datetime.now()
    cms = (cend - cstart).seconds
    if delete:
        os.remove(dlpath)
    if not compress:
        return await edit_delete(catevent, "**ERROR :: Unalble to Compress**")
    new = await fileinfo(compress)
    osize = old["size"]
    nsize = new["size"]
    cap = f"**Old Size:** `{humanbytes(osize)}`\n**New Size:** `{humanbytes(nsize)}`\n**Compressed:** `{int(100-(nsize/osize*100))}%`\n\n**Time Taken:-**\n**Compression : **`{time_formatter(cms)}`"
    if cmd == "f":
        try:
            c_time = time.time()
            catt = await event.client.send_file(
                event.chat_id,
                compress,
                thumb=thumb_image_path,
                caption=cap,
                force_document=True,
                supports_streaming=True,
                allow_cache=False,
                reply_to=reply_to_id,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "Trying to upload")
                ),
            )
            os.remove(compress)
        except Exception as e:
            return await edit_delete(catevent, f"**Error : **`{e}`")
    else:
        thumb = await take_screen_shot(compress, "00:01")
        try:
            c_time = time.time()
            catt = await event.client.send_file(
                event.chat_id,
                compress,
                caption=cap,
                thumb=thumb,
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=reply_to_id,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "Trying to upload")
                ),
            )
            os.remove(compress)
        except Exception as e:
            return await edit_delete(catevent, f"**Error : **`{e}`")
    await catevent.delete()
    end = datetime.now()
    ms = (end - start).seconds
    cap += f"\n**Total :** `{time_formatter(ms)}`"
    await edit_or_reply(catt, cap)


@catub.cat_cmd(
    pattern="ffmpegsave(?:\s|$)([\s\S]*)",
    command=("ffmpegsave", plugin_category),
    info={
        "header": "Saves the media file in bot to trim mutliple times",
        "description": "Will download the replied media into the bot so that you an trim it as your needs.",
        "usage": "{tr}ffmpegsave <reply>",
    },
)
async def ff_mpeg_trim_cmd(event):
    "Saves the media file in bot to trim mutliple times"
    mpath = event.pattern_match.group(1)
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        if mpath and os.path.exists(mpath):
            media = (await fileinfo(mpath))["type"]
            if media not in ["Video", "Audio"]:
                return await edit_delete(event, "`Only media files are supported`", 5)
            await _catutils.runcmd(f"cp -r {mpath} {FF_MPEG_DOWN_LOAD_MEDIA_PATH}")
            return await edit_or_reply(
                event, f"Saved file to `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`"
            )
        reply_message = await event.get_reply_message()
        if reply_message:
            if not reply_message.media:
                return await edit_delete(event, "`Reply to a media file...`")
            start = datetime.now()
            media = await media_type(reply_message)
            if (
                reply_message.media.document.mime_type.split("/")[0]
                not in ["video", "audio"]
                or media == "Sticker"
            ):
                return await edit_delete(
                    event, "`Only Video/Audio files are supported`", 5
                )
            catevent = await edit_or_reply(event, "`Saving the file...`")
            try:
                c_time = time.time()
                dl = io.FileIO(FF_MPEG_DOWN_LOAD_MEDIA_PATH, "a")
                await event.client.fast_download_file(
                    location=reply_message.document,
                    out=dl,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, catevent, c_time, "trying to download")
                    ),
                )
                dl.close()
            except Exception as e:
                await edit_or_reply(catevent, f"**Error:**\n`{e}`")
            else:
                end = datetime.now()
                ms = (end - start).seconds
                await edit_or_reply(
                    catevent,
                    f"Saved file to `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}` in `{ms}` seconds.",
                )
        else:
            await edit_delete(event, "`Reply to a any media file`")
    else:
        await edit_delete(
            event,
            "A media file already exists in path. Please remove the media and try again!\n`.ffmpegclear`",
        )


@catub.cat_cmd(
    pattern="vtrim(?:\s|$)([\s\S]*)",
    command=("vtrim", plugin_category),
    info={
        "header": "Trims the saved media with specific given time internval and outputs as video if it is video",
        "description": "Will trim the saved media with given time interval.",
        "note": "if you haven't mentioned time interval and just time then will send screenshot at that location.",
        "usage": "{tr}vtrim <time interval>",
        "examples": "{tr}vtrim 00:00 00:10",
    },
)
async def ff_mpeg_trim_cmd(event):
    "Trims the saved media with specific given time internval and outputs as video if it is video"
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        return await edit_delete(
            event,
            f"a media file needs to be download, and save to the following path: `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`",
        )
    reply_to_id = await reply_id(event)
    catevent = await edit_or_reply(event, "`Triming the media......`")
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    start = datetime.now()
    if len(cmt) == 3:
        # output should be video
        cmd, start_time, end_time = cmt
        o = await cult_small_video(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time,
        )
        if o is None:
            return await edit_delete(
                catevent, "**Error : **`Can't complete the process`"
            )
        try:
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=False,
                supports_streaming=True,
                allow_cache=False,
                reply_to=reply_to_id,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "trying to upload")
                ),
            )
            os.remove(o)
        except Exception as e:
            return await edit_delete(catevent, f"**Error : **`{e}`")
    elif len(cmt) == 2:
        # output should be image
        cmd, start_time = cmt
        o = await take_screen_shot(FF_MPEG_DOWN_LOAD_MEDIA_PATH, start_time)
        if o is None:
            return await edit_delete(
                catevent, "**Error : **`Can't complete the process`"
            )
        try:
            c_time = time.time()
            await event.client.send_file(
                event.chat_id,
                o,
                caption=" ".join(cmt[1:]),
                force_document=True,
                supports_streaming=True,
                allow_cache=False,
                reply_to=event.message.id,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, catevent, c_time, "trying to upload")
                ),
            )
            os.remove(o)
        except Exception as e:
            return await edit_delete(catevent, f"**Error : **`{e}`")
    else:
        await edit_delete(catevent, "RTFM")
        return
    end = datetime.now()
    ms = (end - start).seconds
    await edit_delete(catevent, f"`Completed Process in {ms} seconds`", 3)


@catub.cat_cmd(
    pattern="atrim(?:\s|$)([\s\S]*)",
    command=("atrim", plugin_category),
    info={
        "header": "Trims the saved media with specific given time internval and outputs as audio",
        "description": "Will trim the saved media with given time interval. and output only audio part, if no interval given it will trim whole audio",
        "usage": [
            "{tr}atrim",
            "{tr}atrim <time interval>",
        ],
        "examples": "{tr}atrim 00:00 00:10",
    },
)
async def ff_mpeg_trim_cmd(event):
    "Trims the saved media with specific given time internval and outputs as audio"
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        return await edit_delete(
            event,
            f"a media file needs to be download, and save to the following path: `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`",
        )
    reply_to_id = await reply_id(event)
    catevent = await edit_or_reply(event, "`Triming the media...........`")
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    start = datetime.now()
    out_put_file_name = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY, f"{round(time.time())}.mp3"
    )
    if len(cmt) == 3:
        cmd, start_time, end_time = cmt
    else:
        start_time = "00:00"
        duration = (await fileinfo(FF_MPEG_DOWN_LOAD_MEDIA_PATH))["duration"]
        end_time = readable_time(duration)
    o = await cult_small_video(
        FF_MPEG_DOWN_LOAD_MEDIA_PATH,
        Config.TMP_DOWNLOAD_DIRECTORY,
        start_time,
        end_time,
        out_put_file_name,
    )
    if o is None:
        return await edit_delete(catevent, "**Error : **`Can't complete the process`")
    try:
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            o,
            caption=" ".join(cmt[1:]),
            force_document=False,
            supports_streaming=True,
            allow_cache=False,
            reply_to=reply_to_id,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, catevent, c_time, "trying to upload")
            ),
        )
        os.remove(o)
    except Exception as e:
        return await edit_delete(catevent, f"**Error : **`{e}`")
    end = datetime.now()
    ms = (end - start).seconds
    await edit_delete(catevent, f"`Completed Process in {ms} seconds`", 3)


@catub.cat_cmd(
    pattern="ffmpegclear$",
    command=("ffmpegclear", plugin_category),
    info={
        "header": "Deletes the saved media so you can save new one",
        "description": "Only after deleting the old saved file you can add new file",
        "usage": "{tr}ffmpegclear",
    },
)
async def ff_mpeg_trim_cmd(event):
    "Deletes the saved media so you can save new one"
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await edit_delete(event, "`There is no media saved in bot for triming`")
    else:
        os.remove(FF_MPEG_DOWN_LOAD_MEDIA_PATH)
        await edit_delete(
            event,
            "`The media saved in bot for triming is deleted now . you can save now new one `",
        )

# VIDEO MERGER
@catub.cat_cmd(
    pattern="merge$",
    command=("merge", plugin_category),
    info={
        "header": "Merge the videos together",
        "description": "Will download the replied video into the bot.",
        "usage": "{tr}merge <reply>",
        "Note": "Videos will be merged in a sequence you download them."
    },
)
async def merge_save(event):
    "Merge provided videos together"
    reply = await event.get_reply_message()
    catevent = await edit_or_reply(event, "`Downloading....`")
    count = 0
    async for messages in event.client.iter_messages(event.chat_id, from_user=reply.sender_id, min_id=reply.id-1, max_id=event.id, reverse=True):
        if not messages.video:
            continue
        file_ = await tg_dl(catevent, reply)
        video_file, file_name = file_
        ffprobe_cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', video_file]
        output = subprocess.check_output(ffprobe_cmd)
        metadata = json.loads(output)
        if metadata['streams'][0]['codec_name'] != 'h264':
            await edit_or_reply(catevent, "Converting...  __This might take a while__")
            ffmpeg_cmd = ['ffmpeg', '-i', video_file, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'copy', f"/temp/{file_name}", "-y"]
            subprocess.call(ffmpeg_cmd)
            process = await asyncio.create_subprocess_shell(
                " ".join(ffmpeg_cmd),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await process.communicate()
            await _catutils.runcmd(f"mv /temp/{file_name}, {MERGER_DIR}")
            await edit_or_reply(catevent, "Downloaded and converted")
        with open(f"{MERGER_DIR}/join.txt", "a+") as join_file:
            join_file.write(f"file {file_name}\n")
        count += 1
    if count == 0 :
        await edit_delete(catevent, "`Found Zero videos to merge. Aborting...`")
    elif count == 1:
        await edit_delete(catevent, "`Found Single video. Aborting...`")
    else:
        await edit_or_reply(catevent, f"Merging {count} downloaded videos.")
        output = await merger()
        if not output:
            return await edit_delete(catevent, "Failed to merge given videos")
        await edit_or_reply(catevent, "Uploading...")
        await event.client.send_file(event.chat_id, file=output)
        await catevent.delete()
    await _catutils.runcmd(f"rm -rf {MERGER_DIR")

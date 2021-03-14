# ported from uniborg by @spechide

import asyncio
import os
import time
from datetime import datetime

from . import media_type, progress, reply_id

FF_MPEG_DOWN_LOAD_MEDIA_PATH = "./downloads/catuserbot.media.ffmpeg"


@bot.on(admin_cmd(pattern="ffmpegsave$"))
@bot.on(sudo_cmd(pattern="ffmpegsave$", allow_sudo=True))
async def ff_mpeg_trim_cmd(event):
    if event.fwd_from:
        return
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        reply_message = await event.get_reply_message()
        if reply_message:
            start = datetime.now()
            media = media_type(reply_message)
            if media not in ["Video", "Audio", "Voice", "Round Video", "Gif"]:
                return await edit_delete(event, "`Only media files are supported`", 5)
            catevent = await edit_or_reply(event, "`Saving the file...`")
            try:
                c_time = time.time()
                downloaded_file_name = await event.client.download_media(
                    reply_message,
                    FF_MPEG_DOWN_LOAD_MEDIA_PATH,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, catevent, c_time, "trying to download")
                    ),
                )
            except Exception as e:
                await catevent.edit(str(e))
            else:
                end = datetime.now()
                ms = (end - start).seconds
                await catevent.edit(
                    f"Saved file to `{downloaded_file_name}` in `{ms}` seconds."
                )
        else:
            await edit_delete(event, "`Reply to a any media file`")
    else:
        await edit_delete(
            event,
            f"A media file already exists in path. Please remove the media and try again!\n`.ffmpegclear`",
        )


@bot.on(admin_cmd(pattern="vtrim"))
@bot.on(sudo_cmd(pattern="vtrim", allow_sudo=True))
async def ff_mpeg_trim_cmd(event):
    if event.fwd_from:
        return
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await edit_delete(
            event,
            f"a media file needs to be download, and save to the following path: `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`",
        )
        return
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
                catevent, f"**Error : **`Can't complete the process`"
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
        o = await _cattools.take_screen_shot(FF_MPEG_DOWN_LOAD_MEDIA_PATH, start_time)
        if o is None:
            return await edit_delete(
                catevent, f"**Error : **`Can't complete the process`"
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


@bot.on(admin_cmd(pattern="atrim"))
@bot.on(sudo_cmd(pattern="atrim", allow_sudo=True))
async def ff_mpeg_trim_cmd(event):
    if event.fwd_from:
        return
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await edit_delete(
            event,
            f"a media file needs to be download, and save to the following path: `{FF_MPEG_DOWN_LOAD_MEDIA_PATH}`",
        )
        return
    reply_to_id = await reply_id(event)
    catevent = await edit_or_reply(event, "`Triming the media...........`")
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    start = datetime.now()
    out_put_file_name = os.path.join(
        Config.TMP_DOWNLOAD_DIRECTORY, f"{str(round(time.time()))}.mp3"
    )
    if len(cmt) == 3:
        # output should be audio
        cmd, start_time, end_time = cmt
        o = await cult_small_video(
            FF_MPEG_DOWN_LOAD_MEDIA_PATH,
            Config.TMP_DOWNLOAD_DIRECTORY,
            start_time,
            end_time,
            out_put_file_name,
        )
        if o is None:
            return await edit_delete(
                catevent, f"**Error : **`Can't complete the process`"
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
    else:
        await edit_delete(catevent, "RTFM")
        return
    end = datetime.now()
    ms = (end - start).seconds
    await edit_delete(catevent, f"`Completed Process in {ms} seconds`", 3)


@bot.on(admin_cmd(pattern="ffmpegclear$"))
@bot.on(sudo_cmd(pattern="ffmpegclear$", allow_sudo=True))
async def ff_mpeg_trim_cmd(event):
    if event.fwd_from:
        return
    if not os.path.exists(FF_MPEG_DOWN_LOAD_MEDIA_PATH):
        await edit_delete(event, "`There is no media saved in bot for triming`")
    else:
        os.remove(FF_MPEG_DOWN_LOAD_MEDIA_PATH)
        await edit_delete(
            event,
            "`The media saved in bot for triming is deleted now . you can save now new one `",
        )


# https://github.com/Nekmo/telegram-upload/blob/master/telegram_upload/video.py#L26


async def cult_small_video(
    video_file, output_directory, start_time, end_time, out_put_file_name=None
):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = out_put_file_name or os.path.join(
        output_directory, f"{str(round(time.time()))}.mp4"
    )
    file_genertor_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name,
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    await process.communicate()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    return None


CMD_HELP.update(
    {
        "ffmpeg": "**Plugin : **`ffmpeg`\
    \n\n  •  **Syntax : **`.ffmpegsave`\
    \n  •  **Function : **__Saves the media file in bot to trim mutliple times__\
    \n\n  •  **Syntax : **`.vtrim time`\
    \n  •  **Function : **__Sends you the screenshot of the video at the given specific time__\
    \n\n  •  **Syntax : **`.vtrim starttime endtime`\
    \n  •  **Function : **__Trims the saved media with specific given time internval and outputs as video__\
    \n\n  •  **Syntax : **`.atrim starttime endtime`\
    \n  •  **Function : **__Trims the saved media with specific given time internval and outputs as audio__\
    \n\n  •  **Syntax : **`.ffmpegclear`\
    \n  •  **Function : **__Deletes the saved media so you can save new one__\
    "
    }
)

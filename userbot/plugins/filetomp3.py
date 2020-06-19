"""File Converter
.nfc """

import asyncio
import os
import time
from datetime import datetime
from telethon import events
from userbot.utils import admin_cmd, progress
from userbot import CMD_HELP

@borg.on(admin_cmd(pattern="nfc ?(.*)"))
async def _(event):
    if event.fwd_from:
        return 
    if not event.reply_to_msg_id:
       await event.edit("```Reply to any media file.```")
       return
    reply_message = await event.get_reply_message() 
    if not reply_message.media:
       await event.edit("reply to media file")
       return
    input_str = event.pattern_match.group(1)
    if  input_str is None:
        await event.edit("try `.nfc voice` or`.nfc mp3`")
        return
    elif input_str == "mp3":
        await event.edit("converting...")
    elif input_str == "voice":
        await event.edit("converting...")
    else:
        await event.edit("try `.nfc voice` or`.nfc mp3`")
        return
        
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await borg.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            )
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        force_document = False
        voice_note = False
        supports_streaming = False
        if input_str == "voice":
            new_required_file_caption = "AUDIO_" + str(round(time.time())) + ".opus"
            new_required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "mp3":
            new_required_file_caption = "MP3_" + str(round(time.time())) + ".mp3"
            new_required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("not supported")
            os.remove(downloaded_file_name)
            return
        logger.info(command_to_run)
        # TODO: re-write create_subprocess_exec 😉
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            end_two = datetime.now()
            await borg.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                )
            )
            ms_two = (end_two - end).seconds
            os.remove(new_required_file_name)
            await event.delete()

            
CMD_HELP.update({"filetomp3": "`.nfc voice` or `.nfc mp3` reply to required media to extract voice/mp3 :\
      \n**USAGE:**Converts the required media file to voice or mp3 file. "
})

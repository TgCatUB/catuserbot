"""File Converter
.nfc """

import asyncio
import os
import time
from datetime import datetime
from uniborg.util import admin_cmd, progress


@borg.on(admin_cmd(pattern="nfc (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if reply_message is None:
        await event.edit("reply to a media to use the `nfc` operation.\nInspired by @FileConverterBot")
        return
    await event.edit("trying to download media file, to my local")
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
            new_required_file_caption = "NLFC_" + str(round(time.time())) + ".opus"
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
            new_required_file_caption = "NLFC_" + str(round(time.time())) + ".mp3"
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
                caption=new_required_file_caption,
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
            await event.edit(f"converted in {ms_two} seconds")


# credits: SNAPDRAGON (@s_n_a_p_s)
from telethon import events
import subprocess
import os
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import asyncio
import time


@command(pattern="^.webupload ?(.+?|) (?:--)(anonfiles|transfer|filebin|anonymousfiles|megaupload|bayfiles)")
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    PROCESS_RUN_TIME = 100
    input_str = event.pattern_match.group(1)
    selected_transfer = event.pattern_match.group(2)
    if input_str:
        file_name = input_str
    else:
        reply = await event.get_reply_message()
        file_name = await bot.download_media(reply.media, Var.TEMP_DOWNLOAD_DIRECTORY)
    reply_to_id = event.message.id
    CMD_WEB = {"anonfiles": "curl -F \"file=@{}\" https://anonfiles.com/api/upload", "transfer": "curl --upload-file \"{}\" https://transfer.sh/{os.path.basename(file_name)}", "filebin": "curl -X POST --data-binary \"@test.png\" -H \"filename: {}\" \"https://filebin.net\"", "anonymousfiles": "curl -F file=\"@{}\" https://api.anonymousfiles.io/", "megaupload": "curl -F \"file=@{}\" https://megaupload.is/api/upload", "bayfiles": ".exec curl -F \"file=@{}\" https://bayfiles.com/api/upload"}
    try:
        selected_one = CMD_WEB[selected_transfer].format(file_name)
    except KeyError:
        await event.edit("Invalid selected Transfer")
    cmd = selected_one
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    await event.edit(f"{stdout.decode()}")

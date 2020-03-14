import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
import asyncio
import os
import shutil
import subprocess
import time
from pySmartDL import SmartDL
from userbot.uniborgConfig import Config
from telethon import events
from userbot.utils import admin_cmd, humanbytes, progress, time_formatter
import subprocess
import patoolib
from bin.cmrudl import *
from datetime import datetime
import io





@borg.on(admin_cmd(pattern=("cmrdl ?(.*)")))
async def _(event):
    url = event.pattern_match.group(1)
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    start = datetime.now()
    reply_message = await event.get_reply_message()
    c_time = time.time()
    downloaded_file_name = Config.TMP_DOWNLOAD_DIRECTORY
    await event.edit("Finish downloading to my local")
    command_to_exec = f"./bin/cmrudl.py {url} -d ./DOWNLOADS/"
    reply_to_id = event.message.id
    PROCESS_RUN_TIME = 100
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        command_to_exec, 
        stdout=asyncio.subprocess.PIPE, 
        stderr=asyncio.subprocess.PIPE
    )
    logger.info(command_to_exec)
    OUTPUT = f"**Files in DOWNLOADS folder:**\n"
    stdout, stderr = await process.communicate()
    t_response = stdout.decode().strip()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(stdout) as out_file:
            x = stdout.decode().strip()
            output = stdout.decode('utf-8').splitlines()
            file_name = output[1]
            file_name = file_name.split()
            full_file_name = file_name[2]
            out_file_name = "./DOWNLOADS/" + full_file_name
            logger.info(file_name)
            await event.edit("Uploading, please wait!!")
            await borg.send_file(
                event.chat_id,
                out_file_name,
                force_document=True,
                allow_cache=False,
                caption=f"`{full_file_name}`",
                reply_to=reply_to_id
            )


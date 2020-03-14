import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
import asyncio
import os
import shutil
import subprocess
import time
from pySmartDL import SmartDL
from sample_config import Config
from telethon import events
from userbot.utils import admin_cmd, humanbytes, progress, time_formatter
import subprocess
import patoolib
from bin.cmrudl import *
from datetime import datetime
import io




@borg.on(admin_cmd(pattern=("mailru ?(.*)")))
async def _(event):
    url = event.pattern_match.group(1)
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    start = datetime.now()
    reply_message = await event.get_reply_message()
    try:
        c_time = time.time()
        downloaded_file_name = Config.TMP_DOWNLOAD_DIRECTORY
        await event.edit("Finish downloading to my local")
        command_to_exec = [
                "./bin/cmrudl.py",
                url,
                "-d",
                "./DOWNLOADS/"
                ]
        process = await asyncio.create_subprocess_shell(
        command_to_exec, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        OUTPUT = f"**Files in DOWNLOADS folder:**\n"
        stdout, stderr = await process.communicate()

        if stdout.decode():
            std = stdout.decode()
            stds = std.split("\n")
            std1 = stds[1]
            std2 = stds[2]
            std3 = stds[3]
            out = str(std1)+"\n"+str(std2)+"\n"+str(std3)
            await event.edit(f"**{out}**")
        if stderr.decode():
            await event.edit(f"**{stderr.decode()}**")
            return
    except Exception as e:
        print(e)

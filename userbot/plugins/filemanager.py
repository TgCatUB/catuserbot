"""Execute GNU/Linux commands inside Telegram
Syntax: .lsroot , .lslocal"""
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from telethon import events
import subprocess
from telethon.errors import MessageEmptyError, MessageTooLongError, MessageNotModifiedError
import io
import asyncio
import time
import os
from userbot.utils import admin_cmd

if not os.path.isdir("./SAVED"):
     os.makedirs("./SAVED")
if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
     os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)

#@borg.on(events.NewMessage(pattern=r"\.lslocal", outgoing=True))
@borg.on(admin_cmd(pattern="lslocal", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
#    dirname = event.pattern_match.group(1)
#    tempdir = "localdir"
    cmd = "ls -lh ./DOWNLOADS/"
#    if dirname == tempdir:
	
    eply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in [cat's](tg://need_update_for_some_feature/) DOWNLOADS Folder:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id
            )
            await event.delete()
    if stderr.decode():
        await event.edit(f"**{stderr.decode()}**")
        return
    await event.edit(f"{OUTPUT}`{stdout.decode()}`")
#    else:
#        await event.edit("Unknown Command")



#@borg.on(events.NewMessage(pattern=r"\.lsroot", outgoing=True))
@borg.on(admin_cmd(pattern="lsroot", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = "ls -lh"
	
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in root directory:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id
            )
            await event.delete()
    if stderr.decode():
        await event.edit(f"**{stderr.decode()}**")
        return
    await event.edit(f"{OUTPUT}`{stdout.decode()}`")
	
#@borg.on(events.NewMessage(pattern=r"\.lssaved", outgoing=True))
@borg.on(admin_cmd(pattern="lssaved", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    cmd = "ls ./SAVED/"
	
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in SAVED directory:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id
            )
            await event.delete()
    if stderr.decode():
        await event.edit(f"**{stderr.decode()}**")
        return
    await event.edit(f"{OUTPUT}`{stdout.decode()}`")
    
    
#@borg.on(events.NewMessage(pattern=r"\.rnsaved ?(.*)", outgoing=True))
@borg.on(admin_cmd(pattern="rnsaved ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        src, dst = input_str.split("|")
        src = src.strip()
        dst = dst.strip()
    cmd = f"mv ./SAVED/{src} ./SAVED/{dst}"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in root directory:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id
            )
            await event.delete()
    if stderr.decode():
        await event.edit(f"**{stderr.decode()}**")
        return
    await event.edit(f"File renamed `{src}` to `{dst}`")
	
#@borg.on(events.NewMessage(pattern=r"\.rnlocal ?(.*)", outgoing=True))
@borg.on(admin_cmd(pattern="rnlocal ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    DELAY_BETWEEN_EDITS = 0.3
    PROCESS_RUN_TIME = 100
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        src, dst = input_str.split("|")
        src = src.strip()
        dst = dst.strip()
    cmd = f"mv ./DOWNLOADS/{src} ./DOWNLOADS/{dst}"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    OUTPUT = f"**Files in root directory:**\n"
    stdout, stderr = await process.communicate()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(stdout)) as out_file:
            out_file.name = "exec.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id
            )
            await event.delete()
    if stderr.decode():
        await event.edit(f"**{stderr.decode()}**")
        return
    await event.edit(f"File renamed `{src}` to `{dst}`")
        
#@borg.on(events.NewMessage(pattern=r"\.delsave (.*)", outgoing=True))
@borg.on(admin_cmd(pattern="delsave (.*)", outgoing=True))
async def handler(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    pathtofile = f"./SAVED/{input_str}"

	
    if os.path.isfile(pathtofile):
     os.remove(pathtofile)
     await event.edit("✅ File Deleted 🗑")
	 
    else:
         await event.edit("⛔️File Not Found. The goods are out of hand😬")
        
#@borg.on(events.NewMessage(pattern=r"\.delocal (.*)", outgoing=True))
@borg.on(admin_cmd(pattern="delocal (.*)", outgoing=True))
async def handler(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    pathtofile = f"./DOWNLOADS/{input_str}"

	
    if os.path.isfile(pathtofile):
     os.remove(pathtofile)
     await event.edit("✅ File Deleted 🗑")
	 
    else:
         await event.edit("⛔️File Not Found .The goods are out of hand😬")

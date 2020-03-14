"""
usage: reply with file : .rar , .7z  create archived file

unzip usage: reply with zipped file .unzipper

Coded by @furki

"""



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


extracted = Config.TMP_DOWNLOAD_DIRECTORY + "extracted/"
thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"





@borg.on(admin_cmd(pattern=("rar ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
            directory_name = downloaded_file_name
            await event.edit("creating rar archive, please wait..")
            # patoolib.create_archive(directory_name + '.7z',directory_name)
            patoolib.create_archive(directory_name + ".rar",(directory_name,Config.TMP_DOWNLOAD_DIRECTORY))
            # patoolib.create_archive("/content/21.yy Avrupa (1).pdf.zip",("/content/21.yy Avrupa (1).pdf","/content/"))
            await borg.send_file(
                event.chat_id,
                directory_name + ".rar",
                caption="rarred By @By_Azade",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(directory_name + ".rar")
                os.remove(directory_name)
            except:
                    pass
            await event.edit("Task Completed")
            await asyncio.sleep(3)
            await event.delete()
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str
        
        await event.edit("Local file compressed to `{}`".format(directory_name + ".rar"))




@borg.on(admin_cmd(pattern=("7z ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
            directory_name = downloaded_file_name
            await event.edit("creating 7z archive, please wait..")
            # patoolib.create_archive(directory_name + '.7z',directory_name)
            patoolib.create_archive(directory_name + ".7z",(directory_name,Config.TMP_DOWNLOAD_DIRECTORY))
            # patoolib.create_archive("/content/21.yy Avrupa (1).pdf.zip",("/content/21.yy Avrupa (1).pdf","/content/"))
            await borg.send_file(
                event.chat_id,
                directory_name + ".7z",
                caption="7z archived By @By_Azade",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(directory_name + ".7z")
                os.remove(directory_name)
            except:
                    pass
            await event.edit("Task Completed")
            await asyncio.sleep(3)
            await event.delete()
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str
        
        await event.edit("Local file compressed to `{}`".format(directory_name + ".7z"))


@borg.on(admin_cmd(pattern=("unzipper ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
            directory_name = downloaded_file_name
            await event.edit("Finish downloading to my local")
            command_to_exec = [
                    "7z",
                    "e",
                    "-o" + extracted,
                    directory_name]
            sp = subprocess.Popen(command_to_exec, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            await borg.send_file(
                event.chat_id,
                directory_name + ".zip",
                caption="Zipped By @By_Azade",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(directory_name + ".zip")
                os.remove(directory_name)
            except:
                    pass
            await event.edit("Task Completed")
            await asyncio.sleep(3)
            await event.delete()
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str
        
        await event.edit("Local file compressed to `{}`".format(directory_name + ".zip"))

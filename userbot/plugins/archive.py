# by @mrconfused and some part by @furki

import asyncio
import os
import shutil
import tarfile
import time
import zipfile
from datetime import datetime
from pathlib import Path

import patoolib
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo

from . import progress

thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@bot.on(admin_cmd(pattern=("zip ?(.*)")))
@bot.on(sudo_cmd(pattern="zip ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await edit_or_reply(event, "Zipping in progress....")
    if event.reply_to_msg_id:
        if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
            directory_name = downloaded_file_name
            await mone.edit("Finish downloading to my local")
            zipfile.ZipFile(directory_name + ".zip", "w", zipfile.ZIP_DEFLATED).write(
                directory_name
            )
            os.remove(directory_name)
            cat = directory_name + ".zip"
            await mone.edit(f"compressed successfully into `{cat}`")
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        if not os.path.exists(input_str):
            await mone.edit(
                f"There is no such directory or file with the name `{input_str}` check again"
            )
            return
        filePaths = zipdir(input_str)
        zip_file = zipfile.ZipFile(input_str + ".zip", "w")
        with zip_file:
            for file in filePaths:
                zip_file.write(file)
        await mone.edit("Local file compressed to `{}`".format(input_str + ".zip"))


@bot.on(admin_cmd(pattern="unzip ?(.*)"))
@bot.on(sudo_cmd(pattern="unzip ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await edit_or_reply(event, "Processing ...")
    if input_str:
        path = Path(input_str)
        if os.path.exists(path):
            start = datetime.now()
            if not zipfile.is_zipfile(path):
                await mone.edit(
                    f"`the given file {str(path)} is not zip file to unzip`"
                )
            destination = os.path.join(
                Config.TMP_DOWNLOAD_DIRECTORY,
                os.path.splitext(os.path.basename(path))[0],
            )
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(destination)
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                f"unzipped and stored to `{destination}` \n**Time Taken :** `{ms} seconds`"
            )
        else:
            await mone.edit(f"I can't find that path `{input_str}`")
    else:
        if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
            os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
        if event.reply_to_msg_id:
            start = datetime.now()
            reply_message = await event.get_reply_message()
            try:
                c_time = time.time()
                path = await event.client.download_media(
                    reply_message,
                    Config.TMP_DOWNLOAD_DIRECTORY,
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, mone, c_time, "trying to download")
                    ),
                )
            except Exception as e:
                await mone.edit(str(e))
            await mone.edit("Unzipping now")
            if not zipfile.is_zipfile(path):
                await mone.edit(
                    f"`the given file {str(path)} is not zip file to unzip`"
                )
            destination = os.path.join(
                Config.TMP_DOWNLOAD_DIRECTORY,
                os.path.splitext(os.path.basename(path))[0],
            )
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(destination)
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                f"unzipped and stored to `{destination}` \n**Time Taken :** `{ms} seconds`"
            )
            os.remove(path)


def zipdir(dirName):
    filePaths = []
    for root, directories, files in os.walk(dirName):
        for filename in files:
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
    return filePaths


@bot.on(admin_cmd(pattern=("rar ?(.*)")))
@bot.on(sudo_cmd(pattern="rar ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await edit_or_reply(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
            directory_name = downloaded_file_name
            await mone.edit("creating rar archive, please wait..")
            patoolib.create_archive(
                directory_name + ".rar", (directory_name, Config.TMP_DOWNLOAD_DIRECTORY)
            )
            await event.client.send_file(
                event.chat_id,
                directory_name + ".rar",
                caption="rarred By cat",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(directory_name + ".rar")
                os.remove(directory_name)
            except BaseException:
                pass
            await mone.edit("Task Completed")
            await asyncio.sleep(3)
            await mone.delete()
        except Exception as e:
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str
        await mone.edit("Local file compressed to `{}`".format(directory_name + ".rar"))


@bot.on(admin_cmd(pattern=("tar ?(.*)")))
@bot.on(sudo_cmd(pattern="tar ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await edit_or_reply(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
            directory_name = downloaded_file_name
            await mone.edit("Finish downloading to my local")
            to_upload_file = directory_name
            output = await create_archive(to_upload_file)
            is_zip = False
            if is_zip:
                check_if_file = await create_archive(to_upload_file)
                if check_if_file is not None:
                    to_upload_file = check_if_file
            await event.client.send_file(
                event.chat_id,
                output,
                caption="TAR By cat",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(output)
                os.remove(output)
            except BaseException:
                pass
            await mone.edit("Task Completed")
            await asyncio.sleep(3)
            await mone.delete()
        except Exception as e:
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str
        await mone.edit("Local file compressed to `{}`".format(output))


async def create_archive(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        compressed_file_name = f"{base_dir_name}.tar.gz"
        compressed_file_name += ".tar.gz"
        file_genertor_command = [
            "tar",
            "-zcvf",
            compressed_file_name,
            f"{input_directory}",
        ]
        process = await asyncio.create_subprocess_exec(
            *file_genertor_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        if os.path.exists(compressed_file_name):
            try:
                shutil.rmtree(input_directory)
            except BaseException:
                pass
            return_name = compressed_file_name
    return return_name


@bot.on(admin_cmd(pattern="unrar"))
@bot.on(sudo_cmd(pattern="unrar", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await edit_or_reply(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
        except Exception as e:
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                "Stored the rar to `{}` in {} seconds.".format(downloaded_file_name, ms)
            )
        patoolib.extract_archive(downloaded_file_name, outdir=extracted)
        filename = sorted(get_lst_of_files(extracted, []))
        await mone.edit("Unraring now")
        for single_file in filename:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                force_document = True
                supports_streaming = False
                document_attributes = []
                if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ]
                try:
                    await event.client.send_file(
                        event.chat_id,
                        single_file,
                        caption=f"UnRarred `{caption_rts}`",
                        force_document=force_document,
                        supports_streaming=supports_streaming,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=document_attributes,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, event, c_time, "trying to upload")
                        ),
                    )
                except Exception as e:
                    await event.client.send_message(
                        event.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id,
                    )
                    # some media were having some issues
                    continue
                os.remove(single_file)
        os.remove(downloaded_file_name)
        await mone.edit("DONE!!!")
        await asyncio.sleep(5)
        await mone.delete()


@bot.on(admin_cmd(pattern="untar"))
@bot.on(sudo_cmd(pattern="untar", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await edit_or_reply(event, "Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    extracted = Config.TMP_DOWNLOAD_DIRECTORY + "extracted/"
    if not os.path.isdir(extracted):
        os.makedirs(extracted)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                ),
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit(
                "Stored the tar to `{}` in {} seconds.".format(downloaded_file_name, ms)
            )
        with tarfile.TarFile.open(downloaded_file_name, "r") as tar_file:
            tar_file.extractall()
        await mone.edit(f"unzipped and stored to `{downloaded_file_name[:-4]}`")
        os.remove(downloaded_file_name)


def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


CMD_HELP.update(
    {
        "archive": "**Plugin : **`archive`\
    \n\n  •  **Syntax : **`.zip (reply/path)`\
    \n  •  **Usage : **it will zip that file which you replied or will zip the folder/file in the given path\
    \n\n  •  **Syntax : **`.unzip (reply to zip file/path`\
    \n  •  **Usage : **it will unzip that zip file or the zip file in the given path\
    \n\n  •  **Syntax : **`.rar reply to a file/media`\
    \n  •  **Usage : **it will rar that file/media\
    \n\n  •  **Syntax : **`.tar reply to a file/media`\
    \n  •  **Usage : **it will tar that file/media\
    \n\n  •  **Syntax : **`.unrar reply to a .rar file`\
    \n  •  **Usage : **it will unrar that .rar file\
    \n\n  •  **Syntax : **`.untar reply to a .tar`\
    \n  •  **Usage : **it will untar that .tar file\
"
    }
)

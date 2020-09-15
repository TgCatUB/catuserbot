import asyncio
import json
import os
import subprocess
import time
from datetime import datetime

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon.tl.types import DocumentAttributeVideo

from .. import ALIVE_NAME, CMD_HELP, LOGS
from ..utils import admin_cmd, edit_or_reply, progress, sudo_cmd

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else "cat"
USERNAME = str(Config.LIVE_USERNAME) if Config.LIVE_USERNAME else "@Jisan7509"


async def catlst_of_files(path):
    files = []
    for dirname, dirnames, filenames in os.walk(path):
        # print path to all filenames.
        for filename in filenames:
            files.append(os.path.join(dirname, filename))
    return files


@borg.on(admin_cmd(pattern="uploadir (.*)", outgoing=True))
@borg.on(sudo_cmd(pattern="uploadir (.*)", allow_sudo=True))
async def uploadir(event):
    input_str = event.pattern_match.group(1)
    hmm = event.message.id
    udir_event = await edit_or_reply(event, "Uploading....")
    if os.path.exists(input_str):
        await udir_event.edit(f"Gathering file details in directory `{input_str}`")
        lst_of_files = []
        lst_of_files = await catlst_of_files(input_str)
        uploaded = 0
        await udir_event.edit(
            "Found {} files. Uploading will start soon. Please wait!".format(
                len(lst_of_files)
            )
        )
        for single_file in lst_of_files:
            if os.path.exists(single_file):
                # https://stackoverflow.com/a/678242/4723940
                caption_rts = os.path.basename(single_file)
                c_time = time.time()
                if not caption_rts.lower().endswith(".mp4"):
                    await borg.send_file(
                        udir_event.chat_id,
                        single_file,
                        caption=caption_rts,
                        force_document=False,
                        allow_cache=False,
                        reply_to=hmm,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, event, c_time, "Uploading...", single_file)
                        ),
                    )
                else:
                    thumb_image = os.path.join(input_str, "thumb.jpg")
                    c_time = time.time()
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    width = 0
                    height = 0
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    await borg.send_file(
                        event.chat_id,
                        single_file,
                        caption=caption_rts,
                        thumb=thumb_image,
                        force_document=False,
                        allow_cache=False,
                        reply_to=hmm,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True,
                            )
                        ],
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(
                                d, t, udir_event, c_time, "Uploading...", single_file
                            )
                        ),
                    )
                uploaded = uploaded + 1
        await udir_event.edit("Uploaded {} files successfully !!".format(uploaded))
    else:
        await udir_event.edit("404: Directory Not Found")


@borg.on(admin_cmd(pattern="upload (.*)", outgoing=True))
@borg.on(sudo_cmd(pattern="upload (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await edit_or_reply(event, "Processing ...")
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    if os.path.exists(input_str):
        start = datetime.now()
        c_time = time.time()
        caat = await bot.send_file(
            event.chat_id,
            input_str,
            force_document=True,
            supports_streaming=True,
            allow_cache=False,
            reply_to=event.message.id,
            thumb=thumb,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to upload")
            ),
        )
        end = datetime.now()
        ms = (end - start).seconds
        await mone.delete()
        await caat.edit(
            f"__**➥ Uploaded in {ms} seconds.**__\n__**➥ Uploaded by :-**__ [{DEFAULTUSER}]({USERNAME})"
        )
    else:
        await mone.edit("404: File Not Found")


def get_video_thumb(file, output=None, width=320):
    output = file + ".jpg"
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            file,
            "-ss",
            str(
                int((0, metadata.get("duration").seconds)[metadata.has("duration")] / 2)
            ),
            # '-filter:v', 'scale={}:-1'.format(width),
            "-vframes",
            "1",
            output,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    p.communicate()
    if not p.returncode and os.path.lexists(file):
        return output


def extract_w_h(file):
    """ Get width and height of media """
    command_to_run = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file,
    ]
    # https://stackoverflow.com/a/11236144/4723940
    try:
        t_response = subprocess.check_output(command_to_run, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        LOGS.warning(exc)
    else:
        x_reponse = t_response.decode("UTF-8")
        response_json = json.loads(x_reponse)
        width = int(response_json["streams"][0]["width"])
        height = int(response_json["streams"][0]["height"])
        return width, height


@borg.on(admin_cmd(pattern="uploadas(stream|vn|all) (.*)", outgoing=True))
@borg.on(sudo_cmd(pattern="uploadas(stream|vn|all) (.*) ", allow_sudo=True))
async def uploadas(event):
    # For .uploadas command, allows you to specify some arguments for upload.
    type_of_upload = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    uas_event = await edit_or_reply(event, "uploading.....")
    supports_streaming = False
    round_message = False
    spam_big_messages = False
    if type_of_upload == "stream":
        supports_streaming = True
    if type_of_upload == "vn":
        round_message = True
    if type_of_upload == "all":
        spam_big_messages = True
    thumb = None
    file_name = None
    if "|" in input_str:
        file_name, thumb = input_str.split("|")
        file_name = file_name.strip()
        thumb = thumb.strip()
    else:
        file_name = input_str
        thumb = vthumb = get_video_thumb(file_name)
    if not thumb:
        if os.path.exists(thumb_image_path):
            thumb = thumb_image_path
    if os.path.exists(file_name):
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get("duration").seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        try:
            if supports_streaming:
                c_time = time.time()
                await borg.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    caption=input_str,
                    force_document=False,
                    allow_cache=False,
                    reply_to=event.message.id,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, uas_event, c_time, "Uploading...", file_name)
                    ),
                )
            elif round_message:
                c_time = time.time()
                await borg.send_file(
                    uas_event.chat_id,
                    file_name,
                    thumb=thumb,
                    allow_cache=False,
                    reply_to=event.message.id,
                    video_note=True,
                    attributes=[
                        DocumentAttributeVideo(
                            duration=60,
                            w=1,
                            h=1,
                            round_message=True,
                            supports_streaming=True,
                        )
                    ],
                    progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        progress(d, t, uas_event, c_time, "Uploading...", file_name)
                    ),
                )
            elif spam_big_messages:
                await uas_event.edit("TBD: Not (yet) Implemented")
                return
            try:
                os.remove(vthumb)
            except BaseException:
                pass
            await uas_event.edit("Uploaded successfully !!")
        except FileNotFoundError as err:
            await uas_event.edit(str(err))
    else:
        await uas_event.edit("404: File Not Found")


CMD_HELP.update(
    {
        "upload": "__**PLUGIN NAME :** Upload__\
    \n\n📌** CMD ➥** `.upload` path of file\
    \n**USAGE   ➥  **Uploads the file from the server\
    \n\n📌** CMD ➥** `.uploadasstream` path of video/audio\
    \n**USAGE   ➥  **Uploads video/audio as streamable from the server\
    \n\n📌** CMD ➥** `.uploadasvn path of video`\
    \n**USAGE   ➥  **Uploads video/audio as round video from the server **Present supports few videos need to work onit takes some time to develop it **\
    "
    }
)

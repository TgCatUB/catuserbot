# originally created by
# https://github.com/Total-Noob-69/X-tra-Telegram/blob/master/userbot/plugins/webupload.py

import asyncio
import json
import os
import subprocess
import time

import requests

from userbot import CMD_HELP
from userbot.utils import admin_cmd


@borg.on(admin_cmd(pattern="labstack ?(.*)"))
async def labstack(event):
    if event.fwd_from:
        return
    await event.edit("Processing...")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if input_str:
        filebase = input_str
    elif reply:
        filebase = await event.client.download_media(
            reply.media, Var.TEMP_DOWNLOAD_DIRECTORY
        )
    else:
        await event.edit(
            "Reply to a media file or provide a directory to upload the file to labstack"
        )
        return
    filesize = os.path.getsize(filebase)
    filename = os.path.basename(filebase)
    headers2 = {"Up-User-ID": "IZfFbjUcgoo3Ao3m"}
    files2 = {
        "ttl": 604800,
        "files": [{"name": filename, "type": "", "size": filesize}],
    }
    r2 = requests.post(
        "https://up.labstack.com/api/v1/links", json=files2, headers=headers2
    )
    r2json = json.loads(r2.text)

    url = "https://up.labstack.com/api/v1/links/{}/send".format(r2json["code"])
    max_days = 7
    command_to_exec = [
        "curl",
        "-F",
        "files=@" + filebase,
        "-H",
        "Transfer-Encoding: chunked",
        "-H",
        "Up-User-ID: IZfFbjUcgoo3Ao3m",
        url,
    ]
    try:
        logger.info(command_to_exec)
        t_response = subprocess.check_output(command_to_exec, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        logger.info("Status : FAIL", exc.returncode, exc.output)
        await event.edit(exc.output.decode("UTF-8"))
        return
    else:
        logger.info(t_response)
        t_response_arry = "https://up.labstack.com/api/v1/links/{}/receive".format(
            r2json["code"]
        )
    await event.edit(
        t_response_arry + "\nMax Days:" + str(max_days), link_preview=False
    )


@borg.on(
    admin_cmd(
        pattern="webupload ?(.+?|) (?:--)(anonfiles|transfer|filebin|anonymousfiles|megaupload|bayfiles)"
    )
)
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
    event.message.id
    CMD_WEB = {
        "anonfiles": 'curl -F "file=@{}" https://anonfiles.com/api/upload',
        "transfer": 'curl --upload-file "{}" https://transfer.sh/{os.path.basename(file_name)}',
        "filebin": 'curl -X POST --data-binary "@test.png" -H "filename: {}" "https://filebin.net"',
        "anonymousfiles": 'curl -F file="@{}" https://api.anonymousfiles.io/',
        "megaupload": 'curl -F "file=@{}" https://megaupload.is/api/upload',
        "bayfiles": '.exec curl -F "file=@{}" https://bayfiles.com/api/upload',
    }
    try:
        selected_one = CMD_WEB[selected_transfer].format(file_name)
    except KeyError:
        await event.edit("Invalid selected Transfer")
    cmd = selected_one
    time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    await event.edit(f"{stdout.decode()}")


CMD_HELP.update(
    {
        "webupload": ".webupload ?(.+?|) (?:--)(anonfiles|transfer|filebin|anonymousfiles|megaupload|bayfiles\
    \nexample: `.webupload --anonfiles` tag this to a file\
"
    }
)

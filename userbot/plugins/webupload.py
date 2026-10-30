import asyncio
import json
import os
import re

import httpx

from userbot import catub
from userbot.core.logger import logging
from userbot.helpers.functions import upload_to_temp_web

from ..Config import Config
from ..core.managers import edit_or_reply

plugin_category = "misc"
LOGS = logging.getLogger(__name__)


link_regex = re.compile(r"((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)", re.DOTALL)


@catub.cat_cmd(
    pattern=r"tgu(?:\s|$)([\s\S]*)",
    command=("tgu", plugin_category),
    info={
        "header": "To upload telegram media to temporary 0x0.st",
        "description": "Will upload media to 0x0.st and shares you link so that you can share with friends.",
        "usage": "{tr}tgu <reply to media or provide path of media>",
    },
)
async def upload_oxo(event):
    "to upload media to 0x0.st"
    editor = await edit_or_reply(event, "Processing...")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if input_str:
        filepath = input_str
    elif reply:
        filepath = await event.client.download_media(reply.media, Config.TMP_DOWNLOAD_DIRECTORY)
    else:
        return await editor.edit("Reply to a media file or provide a directory to upload the file to 0x0.st")

    link = await upload_to_temp_web(file_path=filepath)
    if link:
        await editor.edit(link, link_preview=False)
    else:
        await editor.edit("Failed to upload file.")


@catub.cat_cmd(
    pattern=r"labstack(?:\s|$)([\s\S]*)",
    command=("labstack", plugin_category),
    info={
        "header": "To upload media to labstack.",
        "description": "Will upload media to labstack and shares you link so that you can share with friends and it expires automatically after 7 days",
        "usage": "{tr}labstack <reply to media or provide path of media>",
    },
)
async def labstack(event):
    "to upload media to labstack"
    editor = await edit_or_reply(event, "Processing...")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if input_str:
        filebase = input_str
    elif reply:
        filebase = await event.client.download_media(reply.media, Config.TMP_DOWNLOAD_DIRECTORY)
    else:
        return await editor.edit("Reply to a media file or provide a directory to upload the file to labstack")
    filesize = os.path.getsize(filebase)
    filename = os.path.basename(filebase)
    headers2 = {"Up-User-ID": "IZfFbjUcgoo3Ao3m"}
    files2 = {
        "ttl": 604800,
        "files": [{"name": filename, "type": "", "size": filesize}],
    }
    async with httpx.AsyncClient(follow_redirects=True, timeout=60) as client:
        r2 = await client.post("https://up.labstack.com/api/v1/links", json=files2, headers=headers2)
    r2json = json.loads(r2.text)
    url = f"https://up.labstack.com/api/v1/links/{r2json['code']}/send"
    max_days = 7
    command_to_exec = [
        "curl",
        "-F",
        f"files=@{filebase}",
        "-H",
        "Transfer-Encoding: chunked",
        "-H",
        "Up-User-ID: IZfFbjUcgoo3Ao3m",
        url,
    ]

    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    t_response, _ = await process.communicate()
    if process.returncode != 0:
        LOGS.info("Status : FAIL %s %s", process.returncode, t_response)
        return await editor.edit(t_response.decode("UTF-8"))
    LOGS.info(t_response)
    t_response_arry = f"https://up.labstack.com/api/v1/links/{r2json['code']}/receive"
    await editor.edit(t_response_arry + "\nMax Days:" + str(max_days), link_preview=False)


@catub.cat_cmd(
    pattern=r"webupload ?(.+?|) --(fileio|anonfiles|transfer|filebin|anonymousfiles|bayfiles)",
    command=("webupload", plugin_category),
    info={
        "header": "To upload media to some online media sharing platforms.",
        "description": "you can upload media to any of the sites mentioned. so you can share link to others.",
        "options": {
            "fileio": "to file.io site",
            "anonfiles": "to anonfiles site",
            "transfer": "to transfer.sh site",
            "filebin": "to file bin site",
            "anonymousfiles": "to anonymousfiles site",
            "bayfiles": "to bayfiles site",
        },
        "usage": [
            "{tr}webupload --option",
            "{tr}webupload path --option",
        ],
        "examples": "{tr}webupload --fileio reply this to media file.",
    },
)
async def _(event):
    "To upload media to some online media sharing platforms"
    editor = await edit_or_reply(event, "processing ...")
    input_str = event.pattern_match.group(1)
    selected_transfer = event.pattern_match.group(2)
    catcheck = None
    if input_str:
        file_name = input_str
    else:
        reply = await event.get_reply_message()
        file_name = await event.client.download_media(reply.media, Config.TMP_DOWNLOAD_DIRECTORY)
        catcheck = True
    # a dictionary containing the shell commands
    CMD_WEB = {
        "fileio": 'curl -F "file=@{full_file_path}" https://file.io',
        "oload": 'curl -F "file=@{full_file_path}" https://api.openload.cc/upload',
        "anonfiles": 'curl -F "file=@{full_file_path}" https://api.anonfiles.com/upload',
        "transfer": 'curl --upload-file "{full_file_path}" https://transfer.sh/' + os.path.basename(file_name),
        "filebin": 'curl -X POST --data-binary "@{full_file_path}" -H "filename: {bare_local_name}" "https://filebin.net"',
        "anonymousfiles": 'curl -F "file=@{full_file_path}" https://api.anonymousfiles.io/',
        "vshare": 'curl -F "file=@{full_file_path}" https://api.vshare.is/upload',
        "bayfiles": 'curl -F "file=@{full_file_path}" https://bayfiles.com/api/upload',
    }
    filename = os.path.basename(file_name)
    try:
        selected_one = CMD_WEB[selected_transfer].format(full_file_path=file_name, bare_local_name=filename)
    except KeyError:
        return await editor.edit("Invalid selected Transfer")
    cmd = selected_one
    # start the subprocess $SHELL
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    error = stderr.decode().strip()
    if t_response := stdout.decode().strip():
        try:
            t_response = json.dumps(json.loads(t_response), sort_keys=True, indent=4)
        except Exception as e:
            # some sites don't return valid JSONs
            LOGS.info(str(e))
        urls = re.findall(link_regex, t_response)
        result = ""
        for i in urls:
            if not result:
                result = "**Uploaded File link/links :**"
            result += f"\n{i[0]}"
        await editor.edit(result)
    else:
        await editor.edit(error)
    if catcheck:
        os.remove(file_name)

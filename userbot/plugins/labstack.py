#   Copyright 2019 - 2020 DarkPrinc3

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from datetime import datetime
import os
import requests
import subprocess
import time
import json
import sys

@command(pattern="^.labstack ?(.*)")
async def labstack(event):
    if event.fwd_from:
        return
    await event.edit("Processing...")
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if input_str:
        filebase = input_str
    elif reply:
        filebase = await event.client.download_media(reply.media, Var.TEMP_DOWNLOAD_DIRECTORY)
    else:
        await event.edit("Reply to a media file or provide a directory to upload the file to labstack")
        return
    filesize = os.path.getsize(filebase)
    filename = os.path.basename(filebase)
    headers2 = {'Up-User-ID': 'IZfFbjUcgoo3Ao3m'}
    files2 = {"ttl":604800,"files":[{"name": filename, "type": "", "size": filesize}]}
    r2 = requests.post("https://up.labstack.com/api/v1/links", json=files2, headers=headers2)
    r2json = json.loads(r2.text)

    url = "https://up.labstack.com/api/v1/links/{}/send".format(r2json['code'])
    max_days = 7
    command_to_exec = [
        "curl",
        "-F", "files=@" + filebase,
        "-H","Transfer-Encoding: chunked",
        "-H","Up-User-ID: IZfFbjUcgoo3Ao3m",
        url
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
        t_response_arry = "https://up.labstack.com/api/v1/links/{}/receive".format(r2json['code'])
    await event.edit(t_response_arry + "\nMax Days:" + str(max_days), link_preview=False)
    

"""Upload local Files to Mirrors
Syntax:
.verystream"""

import aiohttp
import aiofiles
import asyncio
import hashlib
import json
import magic
import os
import requests
import time
from datetime import datetime
from uniborg.util import admin_cmd, progress


@borg.on(admin_cmd(pattern="verystream ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    if Config.VERY_STREAM_LOGIN is None or Config.VERY_STREAM_KEY is None:
        await mone.edit("This module requires API key from https://verystream.com. Aborting!")
        return False
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    required_file_name = None
    start = datetime.now()
    if event.reply_to_msg_id and not input_str:
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
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
            return False
        else:
            end = datetime.now()
            ms = (end - start).seconds
            required_file_name = downloaded_file_name
            await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    elif input_str:
        input_str = input_str.strip()
        if os.path.exists(input_str):
            end = datetime.now()
            ms = (end - start).seconds
            required_file_name = input_str
            await mone.edit("Found `{}` in {} seconds.".format(input_str, ms))
        else:
            await mone.edit("File Not found in local server. Give me a file path :((")
            return False
    # logger.info(required_file_name)
    if required_file_name:
        # required_file_name will have the full path
        file_name = os.path.basename(required_file_name)
        if "." in file_name:
            file_name = file_name.rsplit(".", maxsplit=1)[0]
        file_name = file_name + str(time.time())
        file_size = os.stat(required_file_name).st_size
        # https://stackoverflow.com/a/22058673/4723940
        sha_one_file_hash = get_sha_one_hash(required_file_name, 65536)
        # /* STEP 1: get upload_key */
        login = Config.VERY_STREAM_LOGIN
        key = Config.VERY_STREAM_KEY
        sha1 = sha_one_file_hash
        mime = magic.Magic(mime=True)
        step_zero_url = f"https://api.verystream.com/file/createfolder?login={login}&key={key}&name={file_name}"
        async with aiohttp.ClientSession() as session:
            resp_zero = await session.get(step_zero_url)
            step_zero_response_text = json.loads(await resp_zero.text())
            # logger.info(step_zero_response_text)
            if step_zero_response_text["status"] == 200:
                folder_id_e = step_zero_response_text["result"]["folderid"]
                await mone.edit(f"Created Folder with ID: {folder_id_e}")
                step_one_url = f"https://api.verystream.com/file/ul?login={login}&key={key}&sha1={sha1}&folder={folder_id_e}"
                resp = await session.get(step_one_url)
                # logger.info(resp.status)
                step_one_response_text = json.loads(await resp.text())
                # logger.info(step_one_response_text)
                if step_one_response_text["status"] == 200:
                    url = step_one_response_text["result"]["url"]
                    await mone.edit(f"Start Uploading to {url}")
                    start = datetime.now()
                    files = {"file1": (file_name, open(required_file_name, "rb"))}
                    resp = requests.post(url, files=files)
                    step_two_response_text = resp.json()
                    # logger.info(step_two_response_text)
                    if step_two_response_text["status"] == 200:
                        output_str = json.dumps(step_two_response_text["result"], sort_keys=True, indent=4)
                        stream_url = step_two_response_text["result"]["url"]
                        end = datetime.now()
                        ms = (end - start).seconds
                        await mone.edit(f"Obtained {stream_url} in {ms} seconds.\n{output_str}")
                        # cleanup
                        await event.delete()
                        try:
                            os.remove(required_file_name)
                        except:
                            pass
                    else:
                        await mone.edit(f"VeryStream returned {step_two_response_text['status']} => {step_two_response_text['msg']}, after STEP ONE")
                else:
                    await mone.edit(f"VeryStream returned {step_one_response_text['status']} => {step_one_response_text['msg']}, after STEP ONE")
            else:
                await mone.edit(f"VeryStream returned {step_zero_response_text['status']} => {step_zero_response_text['msg']}, after STEP INIT")
    else:
        await mone.edit("File Not found in local server. Give me a file path :((")


def get_sha_one_hash(input_file, chunk_size):
    sha1 = hashlib.sha1()
    with open(input_file, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

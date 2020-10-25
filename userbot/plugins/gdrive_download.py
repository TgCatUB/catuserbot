"""
G-Drive File Downloader Plugin For Userbot.
usage: .gdl File-Link
By: @Zero_cool7870
"""
import requests

from ..utils import admin_cmd, edit_or_reply, sudo_cmd
from . import CMD_HELP


async def download_file_from_google_drive(gid):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={"id": gid}, stream=True)
    token = await get_confirm_token(response)
    if token:
        params = {"id": gid, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    headers = response.headers
    content = headers["Content-Disposition"]
    destination = await get_file_name(content)

    file_name = await save_response_content(response, destination)
    return file_name


async def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


async def save_response_content(response, destination):
    with open(destination, "wb") as f:
        CHUNK_SIZE = 32768
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return destination


async def get_id(link):  # Extract File Id from G-Drive Link
    file_id = ""
    c_append = False
    if link[1:33] == "https://drive.google.com/file/d/":
        link = link[33:]
        fid = ""
        for c in link:
            if c == "/":
                break
            fid += c
        return fid
    for c in link:
        if c == "=":
            c_append = True
        if c == "&":
            break
        if c_append:
            file_id += c
    file_id = file_id[1:]
    return file_id


async def get_file_name(content):
    file_name = ""
    c_append = False
    for c in str(content):
        if c == ";":
            c_append = False
        elif c == '"':
            c_append = True
        if c_append:
            file_name += c
    file_name = file_name.replace('"', "")
    print("File Name: " + str(file_name))
    return file_name


@bot.on(admin_cmd(pattern=f"gdl (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern=f"gdl (.*)", allow_sudo=True))
async def g_download(event):
    if event.fwd_from:
        return
    drive_link = event.text[4:]
    file_id = await get_id(drive_link)
    event = await edit_or_reply(event, "Downloading Requested File from G-Drive...")
    file_name = await download_file_from_google_drive(file_id)
    await event.edit("File Downloaded.\n**Name : **`" + str(file_name) + "`")


CMD_HELP.update(
    {
        "gdrive_download": "**Plugin : **`gdrive_download`\
        \n\n**Syntax : **`.gdl <gdrive File-Link>`\
        \n**Function : **G-Drive File Downloader Plugin For Userbot. only gdrive files are supported now"
    }
)

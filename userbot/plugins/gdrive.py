# Catuserbot Google Drive managers  ported from Projectbish and added extra things by @mrconfused

import asyncio
import base64
import io
import json
import logging
import math
import os
import pickle
import re
import time
from datetime import datetime
from mimetypes import guess_type
from os.path import getctime, isdir, isfile, join
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from telethon import events

from . import (
    BOTLOG,
    BOTLOG_CHATID,
    G_DRIVE_CLIENT_ID,
    G_DRIVE_CLIENT_SECRET,
    G_DRIVE_DATA,
    G_DRIVE_FOLDER_ID,
    LOGS,
    TMP_DOWNLOAD_DIRECTORY,
    CancelProcess,
    humanbytes,
    progress,
    time_formatter,
)
from .sql_helper import google_drive_sql as helper

# =========================================================== #
#                          STATIC                             #
# =========================================================== #
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.metadata",
]
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
# =========================================================== #
#      STATIC CASE FOR G_DRIVE_FOLDER_ID IF VALUE IS URL      #
# =========================================================== #
__ = G_DRIVE_FOLDER_ID
if __ is not None:
    if "uc?id=" in G_DRIVE_FOLDER_ID:
        LOGS.info("G_DRIVE_FOLDER_ID is not a valid folderURL...")
        G_DRIVE_FOLDER_ID = None
    try:
        G_DRIVE_FOLDER_ID = __.split("folders/")[1]
    except IndexError:
        try:
            G_DRIVE_FOLDER_ID = __.split("open?id=")[1]
        except IndexError:
            if "/view" in __:
                G_DRIVE_FOLDER_ID = __.split("/")[-2]
            else:
                try:
                    G_DRIVE_FOLDER_ID = __.split("folderview?id=")[1]
                except IndexError:
                    if "http://" not in __ or "https://" not in __:
                        _1 = any(map(str.isdigit, __))
                        _2 = "-" in __ or "_" in __
                        if True not in [_1 or _2]:
                            LOGS.info("G_DRIVE_FOLDER_ID " "not a valid ID...")
                            G_DRIVE_FOLDER_ID = None
                    else:
                        LOGS.info("G_DRIVE_FOLDER_ID " "not a valid URL...")
                        G_DRIVE_FOLDER_ID = None
# =========================================================== #
#                           LOG                               #
# =========================================================== #
logger = logging.getLogger("googleapiclient.discovery")
logger.setLevel(logging.ERROR)

thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "/thumb_image.jpg")
# =========================================================== #
#                                                             #
# =========================================================== #
GDRIVE_ID = re.compile(
    r"https://drive.google.com/[\w\?\./&=]+([-\w]{33}|(?<=[/=])0(?:A[-\w]{17}|B[-\w]{26}))"
)


@bot.on(admin_cmd(pattern="gauth$", command="gauth", outgoing=True))
@bot.on(sudo_cmd(pattern="gauth$", command="gauth", allow_sudo=True))
async def generate_credentials(gdrive):
    """ - Only generate once for long run - """
    if not BOTLOG:
        await edit_delete(
            gdrive,
            "for authencation you need to set PRIVATE_GROUP_BOT_API_ID in heroku",
            time=10,
        )
    hmm = gdrive.client.uid
    if helper.get_credentials(str(hmm)) is not None:
        await edit_or_reply(gdrive, "`You already authorized token...`")
        await asyncio.sleep(1.5)
        await gdrive.delete()
        return False
    """ - Generate credentials - """
    if G_DRIVE_DATA is not None:
        try:
            configs = json.loads(G_DRIVE_DATA)
        except json.JSONDecodeError:
            await edit_or_reply(
                gdrive,
                "**AUTHENTICATE - ERROR**\n\n"
                "**Status : **`BAD`\n"
                "**Reason : **`G_DRIVE_DATA entity is not valid!`",
            )
            return False
    else:
        """ - Only for old user - """
        if G_DRIVE_CLIENT_ID is None and G_DRIVE_CLIENT_SECRET is None:
            await edit_or_reply(
                gdrive,
                "**AUTHENTICATE - ERROR**\n\n"
                "**Status : **`BAD`\n"
                "**Reason : **`please get your G_DRIVE_DATA`",
            )
            return False
        configs = {
            "installed": {
                "client_id": G_DRIVE_CLIENT_ID,
                "client_secret": G_DRIVE_CLIENT_SECRET,
                "auth_uri": GOOGLE_AUTH_URI,
                "token_uri": GOOGLE_TOKEN_URI,
            }
        }
    gdrive = await edit_or_reply(gdrive, "`Creating credentials...`")
    flow = InstalledAppFlow.from_client_config(
        configs, SCOPES, redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")
    msg = await gdrive.respond(
        "`Go to your Private log group to authenticate token...`"
    )
    async with gdrive.client.conversation(BOTLOG_CHATID) as conv:
        url_msg = await conv.send_message(
            "Please go to this URL:\n" f"{auth_url}\nauthorize then reply the code"
        )
        r = conv.wait_event(events.NewMessage(outgoing=True, chats=BOTLOG_CHATID))
        r = await r
        code = r.message.message.strip()
        flow.fetch_token(code=code)
        creds = flow.credentials
        await asyncio.sleep(3.5)
        await gdrive.client.delete_messages(gdrive.chat_id, msg.id)
        await gdrive.client.delete_messages(BOTLOG_CHATID, [url_msg.id, r.id])
        """ - Unpack credential objects into strings - """
        creds = base64.b64encode(pickle.dumps(creds)).decode()
        await gdrive.edit("`Credentials created...`")
    helper.save_credentials(str(gdrive.sender_id), creds)
    await gdrive.delete()
    return


async def create_app(gdrive):
    """ - Create google drive service app - """
    hmm = bot.uid
    creds = helper.get_credentials(str(hmm))
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if creds is not None:
        """ - Repack credential objects from strings - """
        creds = pickle.loads(base64.b64decode(creds.encode()))
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            await gdrive.edit("`Refreshing credentials...`")
            """ - Refresh credentials - """
            creds.refresh(Request())
            helper.save_credentials(
                str(hmm), base64.b64encode(pickle.dumps(creds)).decode()
            )
        else:
            await gdrive.edit("`Credentials is empty, please generate it...`")
            return False
    try:
        cat = Get(cat)
        await gdrive.client(cat)
    except BaseException:
        pass
    return build("drive", "v3", credentials=creds, cache_discovery=False)


@bot.on(admin_cmd(pattern="greset$", command="greset", outgoing=True))
@bot.on(sudo_cmd(pattern="greset$", command="greset", allow_sudo=True))
async def reset_credentials(gdrive):
    """ - Reset credentials or change account - """
    hmm = bot.uid
    gdrive = await edit_or_reply(gdrive, "`Resetting information...`")
    helper.clear_credentials(str(hmm))
    await gdrive.edit("`Done...`")
    await asyncio.sleep(1)
    await gdrive.delete()
    return


async def get_raw_name(file_path):
    """ - Get file_name from file_path - """
    return file_path.split("/")[-1]


async def get_mimeType(name):
    """ - Check mimeType given file - """
    mimeType = guess_type(name)[0]
    if not mimeType:
        mimeType = "text/plain"
    return mimeType


async def get_file_id(input_str):
    link = input_str
    found = GDRIVE_ID.search(link)
    if found and "folder" in link:
        return found.group(1), "folder"
    elif found:
        return found.group(1), "file"
    else:
        return link, "unknown"


async def download(event, gdrive, service, uri=None):
    start = datetime.now()
    global is_cancelled
    reply = ""
    """ - Download files to local then upload - """
    if not isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        required_file_name = ""
    if uri:
        try:
            from .torrentutils import aria2, check_metadata

            cattorrent = True
        except Exception:
            cattorrent = False
        full_path = os.getcwd() + TMP_DOWNLOAD_DIRECTORY.strip(".")
        if cattorrent:
            LOGS.info("torrentutils exists")
            if isfile(uri) and uri.endswith(".torrent"):
                downloads = aria2.add_torrent(
                    uri, uris=None, options={"dir": full_path}, position=None
                )
            else:
                uri = [uri]
                downloads = aria2.add_uris(
                    uri, options={"dir": full_path}, position=None
                )
        else:
            LOGS.info("No torrentutils")
            await edit_or_reply(
                gdrive,
                "`To use torrent files or download files from link install torrentutils from` @catplugins",
            )
            return "install torrentutils"
        from .torrentutils import aria2, check_metadata

        gid = downloads.gid
        filename = await check_progress_for_dl(gdrive, gid, previous=None)
        file = aria2.get_download(gid)
        if file.followed_by_ids:
            new_gid = await check_metadata(gid)
            filename = await check_progress_for_dl(gdrive, new_gid, previous=None)
        try:
            required_file_name = TMP_DOWNLOAD_DIRECTORY + filenames
        except Exception:
            required_file_name = TMP_DOWNLOAD_DIRECTORY + filename
    else:
        try:
            current_time = time.time()
            is_cancelled = False
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(
                        d,
                        t,
                        gdrive,
                        current_time,
                        "[FILE - DOWNLOAD]",
                        is_cancelled=is_cancelled,
                    )
                ),
            )
        except CancelProcess:
            names = [
                join(TMP_DOWNLOAD_DIRECTORY, name)
                for name in os.listdir(TMP_DOWNLOAD_DIRECTORY)
            ]

            """ asumming newest files are the cancelled one """
            newest = max(names, key=getctime)
            os.remove(newest)
            reply += (
                "**FILE - CANCELLED**\n\n"
                "**Status : **`OK - received signal cancelled.`"
            )
            return reply
        else:
            required_file_name = downloaded_file_name
    try:
        file_name = await get_raw_name(required_file_name)
    except AttributeError:
        reply += "**[ENTRY - ERROR]**\n\n" "**Status : **`BAD`\n"
        return reply
    mimeType = await get_mimeType(required_file_name)
    try:
        status = "[FILE - UPLOAD]"
        if isfile(required_file_name):
            try:
                result = await upload(
                    gdrive, service, required_file_name, file_name, mimeType
                )
            except CancelProcess:
                reply += (
                    "**[FILE - CANCELLED]**\n\n"
                    "**Status : **`OK - received signal cancelled.`"
                )
                return reply
            else:
                end = datetime.now()
                ms = (end - start).seconds
                reply += (
                    f"**File Uploaded in **`{ms} seconds`\n\n"
                    f"**➥ Size : **`{humanbytes(result[0])}`\n"
                    f"**➥ Link :** [{file_name}]({result[1]})\n"
                )
                return reply
        else:
            status = status.replace("[FILE", "[FOLDER")
            global parent_Id
            folder = await create_dir(service, file_name)
            parent_Id = folder.get("id")
            webViewURL = "https://drive.google.com/drive/folders/" + parent_Id
            try:
                await task_directory(gdrive, service, required_file_name)
            except CancelProcess:
                reply += (
                    "**[FOLDER - CANCELLED]**\n\n"
                    "**Status : **`OK - received signal cancelled.`"
                )
                await reset_parentId()
                return reply
            except Exception:
                await reset_parentId()
            else:
                reply += (
                    f"**{status}**\n\n"
                    f"[{file_name}]({webViewURL})\n"
                    "**Status : **`OK - Successfully uploaded.`\n\n"
                )
                await reset_parentId()
                return reply
    except Exception as e:
        status = status.replace("DOWNLOAD]", "ERROR]")
        reply += (
            f"**{status}**\n\n" "**Status : **`failed`\n" f"**Reason : **`{str(e)}`\n\n"
        )
        return reply


async def list_drive_dir(service, file_id):
    query = f"'{file_id}' in parents and (name contains '*')"
    fields = "nextPageToken, files(id, name, mimeType)"
    page_token = None
    page_size = 100
    files = []
    while True:
        response = (
            service.files()
            .list(
                supportsTeamDrives=True,
                includeTeamDriveItems=True,
                q=query,
                spaces="drive",
                fields=fields,
                pageToken=page_token,
                pageSize=page_size,
                corpora="allDrives",
                orderBy="folder, name",
            )
            .execute()
        )
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break
        if self._is_canceled:
            raise ProcessCanceled
    return files


async def copy_file(service, file_id, dir_id):
    body = {}
    if dir_id:
        body["parents"] = [dir_id]
    drive_file = (
        service.files()
        .copy(body=body, fileId=file_id, supportsTeamDrives=True)
        .execute()
    )
    return drive_file["id"]


async def copy_dir(service, file_id, dir_id):
    files = await list_drive_dir(service, file_id)
    if len(files) == 0:
        return dir_id
    new_id = None
    for file in files:
        if file["mimeType"] == "application/vnd.google-apps.folder":
            folder = await create_dir(service, file["name"], dir_id)
            catdir_id = folder.get("id")
            new_id = await copy_dir(service, file["id"], catdir_id)
        else:
            await copy_file(service, file["id"], dir_id)
            await asyncio.sleep(0.5)
            new_id = dir_id
    return new_id


async def gdrive_download(event, gdrive, service, uri):
    reply = ""
    global is_cancelled
    if "&export=download" in uri:
        uri = uri.split("&export=download")[0]
    elif "file/d/" in uri and "/view" in uri:
        uri = uri.split("?usp=drivesdk")[0]
    try:
        file_Id = uri.split("uc?id=")[1]
    except IndexError:
        try:
            file_Id = uri.split("open?id=")[1]
        except IndexError:
            if "/view" in uri:
                file_Id = uri.split("/")[-2]
            else:
                try:
                    file_Id = uri.split("uc?export=download&confirm=")[1].split("id=")[
                        1
                    ]
                except IndexError:
                    file_Id = uri
    try:
        file = await get_information(service, file_Id)
    except HttpError as e:
        if "404" in str(e):
            drive = "https://drive.google.com"
            url = f"{drive}/uc?export=download&id={file_Id}"
            session = requests.session()
            download = session.get(url, stream=True)
            try:
                download.headers["Content-Disposition"]
            except KeyError:
                page = BeautifulSoup(download.content, "lxml")
                try:
                    export = drive + page.find("a", {"id": "uc-download-link"}).get(
                        "href"
                    )
                except AttributeError:
                    try:
                        error = (
                            page.find("p", {"class": "uc-error-caption"}).text
                            + "\n"
                            + page.find("p", {"class": "uc-error-subcaption"}).text
                        )
                    except Exception:
                        reply += (
                            "**[FILE - ERROR]**\n\n"
                            "**Status : **BAD - failed to download.\n"
                            "**Reason : **uncaught err."
                        )
                    else:
                        reply += (
                            "**[FILE - ERROR]**\n\n"
                            "**Status : **BAD - failed to download.\n"
                            f"**Reason : **`{error}`"
                        )
                    return reply, "Error"
                download = session.get(export, stream=True)
                file_size = human_to_bytes(
                    page.find("span", {"class": "uc-name-size"})
                    .text.split()[-1]
                    .strip("()")
                )
            else:
                file_size = int(download.headers["Content-Length"])
            file_name = re.search(
                "filename='(.)'", download.headers["Content-Disposition"]
            ).group(1)
            file_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, file_name)
            with io.FileIO(file_path, "wb") as files:
                CHUNK_SIZE = None
                current_time = time.time()
                display_message = None
                first = True
                is_cancelled = False
                for chunk in download.iter_content(CHUNK_SIZE):
                    if is_cancelled:
                        raise CancelProcess
                    if not chunk:
                        break
                    diff = time.time() - current_time
                    if first:
                        downloaded = len(chunk)
                        first = False
                    else:
                        downloaded += len(chunk)
                    percentage = downloaded / file_size * 100
                    speed = round(downloaded / diff, 2)
                    eta = round((file_size - downloaded) / speed)
                    prog_str = "`[{0}{1}] {2}%`".format(
                        "".join("▰" for i in range(math.floor(percentage / 10))),
                        "".join("▱" for i in range(10 - math.floor(percentage / 10))),
                        round(percentage, 2),
                    )
                    current_message = (
                        "**File downloading**\n\n"
                        f"**Name : **`{file_name}`\n"
                        f"**Status**\n{prog_str}\n"
                        f"`{humanbytes(downloaded)} of {humanbytes(file_size)}`"
                        f" @ {humanbytes(speed)}`\n"
                        f"**ETA :** `{time_formatter(eta)}`"
                    )
                    if display_message != current_message:
                        await gdrive.edit(current_message)
                        display_message = current_message
                    files.write(chunk)
    else:
        file_name = file.get("name")
        mimeType = file.get("mimeType")
        if mimeType == "application/vnd.google-apps.folder":
            return "Aborting, folder download not support...", "Error"
        file_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, file_name)
        request = service.files().get_media(fileId=file_Id, supportsAllDrives=True)
        with io.FileIO(file_path, "wb") as df:
            downloader = MediaIoBaseDownload(df, request)
            complete = False
            is_cancelled = False
            current_time = time.time()
            display_message = None
            while not complete:
                if is_cancelled:
                    raise CancelProcess
                status, complete = downloader.next_chunk()
                if status:
                    file_size = status.total_size
                    diff = time.time() - current_time
                    downloaded = status.resumable_progress
                    percentage = downloaded / file_size * 100
                    speed = round(downloaded / diff, 2)
                    eta = round((file_size - downloaded) / speed)
                    prog_str = "`[{0}{1}] {2}%`".format(
                        "".join("▰" for i in range(math.floor(percentage / 10))),
                        "".join("▱" for i in range(10 - math.floor(percentage / 10))),
                        round(percentage, 2),
                    )
                    current_message = (
                        "**File Downloading**\n\n"
                        f"**Name : **`{file_name}`\n"
                        f"**Status : **\n{prog_str}\n"
                        f"`{humanbytes(downloaded)} of {humanbytes(file_size)}"
                        f" @ {humanbytes(speed)}\n`"
                        f"**ETA :** `{time_formatter(eta)}`"
                    )
                    if display_message != current_message:
                        await gdrive.edit(current_message)
                        display_message = current_message
    await gdrive.edit(
        "**[FILE - DOWNLOAD]**\n\n"
        f"**Name   :** `{file_name}`\n"
        f"**Size   : **`{humanbytes(file_size)}`\n"
        f"**Path   : **`{file_path}`\n"
        "**Status : **OK - Successfully downloaded."
    )
    return file_path, None


async def download_gdrive(gdrive, service, uri):
    reply = ""
    start = datetime.now()
    global is_cancelled
    """ - remove drivesdk and export=download from link - """
    if "&export=download" in uri:
        uri = uri.split("&export=download")[0]
    elif "file/d/" in uri and "/view" in uri:
        uri = uri.split("?usp=drivesdk")[0]
    try:
        file_Id = uri.split("uc?id=")[1]
    except IndexError:
        try:
            file_Id = uri.split("open?id=")[1]
        except IndexError:
            if "/view" in uri:
                file_Id = uri.split("/")[-2]
            else:
                try:
                    file_Id = uri.split("uc?export=download&confirm=")[1].split("id=")[
                        1
                    ]
                except IndexError:
                    """ - if error parse in url, assume given value is Id - """
                    file_Id = uri
    file_Id, _ = await get_file_id(file_Id)
    global parent_Id
    try:
        if parent_Id is not None:
            dir_id = parent_Id
    except NameError:
        dir_id = G_DRIVE_FOLDER_ID if G_DRIVE_FOLDER_ID is not None else []
    try:
        file = (
            service.files()
            .get(fileId=file_Id, fields="name, mimeType", supportsTeamDrives=True)
            .execute()
        )
        if file["mimeType"] == "application/vnd.google-apps.folder":
            folder = await create_dir(service, file["name"])
            dir_id = folder.get("id")
            await copy_dir(service, file_Id, dir_id)
            end = datetime.now()
            ms = (end - start).seconds
            reply = (
                f"**Folder successfully copied in** `{ms} seconds`\n\n"
                f"**Link : **[{file['name']}]({folder['webViewLink']})"
            )
        else:
            ret_id = await copy_file(service, file_Id, dir_id)
            end = datetime.now()
            ms = (end - start).seconds
            reply = (
                f"**File successfully copied in** `{ms} seconds`\n\n"
                f"**Link : **[link](https://drive.google.com/open?id={ret_id})"
            )
    except HttpError as e:
        reply = f"**Error : **`{str(e)}`"
    return reply


async def change_permission(service, Id):
    permission = {"role": "reader", "type": "anyone"}
    try:
        service.permissions().create(fileId=Id, body=permission).execute()
    except HttpError as e:
        """ it's not possible to change permission per file for teamdrive """
        if f'"File not found: {Id}."' in str(e) or (
            '"Sharing folders that are inside a shared drive is not supported."'
            in str(e)
        ):
            return
        else:
            raise e
    return


async def get_information(service, Id):
    return (
        service.files()
        .get(
            fileId=Id,
            fields="name, id, size, mimeType, "
            "webViewLink, webContentLink,"
            "description",
            supportsAllDrives=True,
        )
        .execute()
    )


async def create_dir(service, folder_name, dir_id=None):
    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if not dir_id:
        try:
            if parent_Id is not None:
                pass
        except NameError:
            """ - Fallback to G_DRIVE_FOLDER_ID else root dir - """
            if G_DRIVE_FOLDER_ID is not None:
                metadata["parents"] = [G_DRIVE_FOLDER_ID]
        else:
            """ - Override G_DRIVE_FOLDER_ID because parent_Id not empty - """
            metadata["parents"] = [parent_Id]
    else:
        metadata["parents"] = [dir_id]
    folder = (
        service.files()
        .create(body=metadata, fields="id, webViewLink", supportsAllDrives=True)
        .execute()
    )
    await change_permission(service, folder.get("id"))
    return folder


async def upload(gdrive, service, file_path, file_name, mimeType):
    try:
        await gdrive.edit("`Processing upload...`")
    except Exception as e:
        LOGS.info(str(e))
    body = {
        "name": file_name,
        "description": "Uploaded from Telegram using Catuserbot.",
        "mimeType": mimeType,
    }
    try:
        if parent_Id is not None:
            pass
    except NameError:
        """ - Fallback to G_DRIVE_FOLDER_ID else root dir - """
        if G_DRIVE_FOLDER_ID is not None:
            body["parents"] = [G_DRIVE_FOLDER_ID]
    else:
        """ - Override G_DRIVE_FOLDER_ID because parent_Id not empty - """
        body["parents"] = [parent_Id]
    media_body = MediaFileUpload(file_path, mimetype=mimeType, resumable=True)
    """ - Start upload process - """
    file = service.files().create(
        body=body,
        media_body=media_body,
        fields="id, size, webContentLink",
        supportsAllDrives=True,
    )
    global is_cancelled
    current_time = time.time()
    response = None
    display_message = None
    is_cancelled = False
    while response is None:
        if is_cancelled is True:
            raise CancelProcess
        status, response = file.next_chunk()
        if status:
            file_size = status.total_size
            diff = time.time() - current_time
            uploaded = status.resumable_progress
            percentage = uploaded / file_size * 100
            speed = round(uploaded / diff, 2)
            eta = round((file_size - uploaded) / speed)
            prog_str = "`Uploading :`\n`[{0}{1}] {2}`".format(
                "".join(["▰" for i in range(math.floor(percentage / 10))]),
                "".join(["▱" for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2),
            )
            current_message = (
                "**Uploading **\n\n"
                f"**Name : **`{file_name}`\n"
                f"**Status : **\n{prog_str}\n"
                f"`{humanbytes(uploaded)} of {humanbytes(file_size)} "
                f"@ {humanbytes(speed)}`\n"
                f"**ETA** -> `{time_formatter(eta)}`"
            )
            if display_message != current_message:
                await gdrive.edit(current_message)
                display_message = current_message
    file_id = response.get("id")
    file_size = response.get("size")
    downloadURL = response.get("webContentLink")
    """ - Change permission - """
    await change_permission(service, file_id)
    return int(file_size), downloadURL


async def task_directory(gdrive, service, folder_path):
    global parent_Id
    global is_cancelled
    is_cancelled = False
    lists = os.listdir(folder_path)
    if len(lists) == 0:
        return parent_Id
    root_parent_Id = None
    for f in lists:
        if is_cancelled:
            raise CancelProcess

        current_f_name = join(folder_path, f)
        if isdir(current_f_name):
            folder = await create_dir(service, f)
            parent_Id = folder.get("id")
            root_parent_Id = await task_directory(gdrive, service, current_f_name)
        else:
            file_name = await get_raw_name(current_f_name)
            mimeType = await get_mimeType(current_f_name)
            await upload(gdrive, service, current_f_name, file_name, mimeType)
            root_parent_Id = parent_Id
    return root_parent_Id


async def reset_parentId():
    global parent_Id
    try:
        if parent_Id is not None:
            pass
    except NameError:
        if G_DRIVE_FOLDER_ID is not None:
            parent_Id = G_DRIVE_FOLDER_ID
    else:
        del parent_Id
    return


G_DRIVE_FILE_LINK = "📄 [{}](https://drive.google.com/open?id={}) __({})__"
G_DRIVE_FOLDER_LINK = "📁 [{}](https://drive.google.com/drive/folders/{})"


async def share(service, event, url):
    """ get shareable link """
    await event.edit("`Loading GDrive Share...`")
    file_id, _ = await get_file_id(url)
    try:
        result = await get_output(service, file_id)
    except Exception as e:
        await edit_delete(event, f"str({e})", parse_mode=parse_pre)
        return
    await event.edit(f"**Shareable Links**\n\n{result}")


def get_file_path(service, file_id, file_name):
    tmp_path = [file_name]
    while True:
        response = (
            service.files()
            .get(fileId=file_id, fields="parents", supportsTeamDrives=True)
            .execute()
        )
        if not response:
            break
        file_id = response["parents"][0]
        response = (
            service.files()
            .get(fileId=file_id, fields="name", supportsTeamDrives=True)
            .execute()
        )
        tmp_path.append(response["name"])
    return "/".join(reversed(tmp_path[:-1]))


async def get_output(service, file_id):
    file_ = (
        service.files()
        .get(
            fileId=file_id,
            fields="id, name, size, mimeType",
            supportsTeamDrives=True,
        )
        .execute()
    )
    file_id = file_.get("id")
    file_name = file_.get("name")
    file_size = humanbytes(int(file_.get("size", 0)))
    mime_type = file_.get("mimeType")
    if mime_type == "application/vnd.google-apps.folder":
        out = G_DRIVE_FOLDER_LINK.format(file_name, file_id)
    else:
        out = G_DRIVE_FILE_LINK.format(file_name, file_id, file_size)
    if Config.G_DRIVE_INDEX_LINK:
        link = os.path.join(
            Config.G_DRIVE_INDEX_LINK.rstrip("/"),
            quote(get_file_path(service, file_id, file_name)),
        )
        if mime_type == "application/vnd.google-apps.folder":
            link += "/"
        out += f"\n👥 __[Shareable Link]({link})__"
    return out


async def lists(gdrive):
    checker = gdrive.pattern_match.group(1)
    if checker is not None:
        page_size = int(gdrive.pattern_match.group(1).strip("-l "))
        if page_size > 1000:
            await edit_or_reply(
                gdrive,
                "**GDRIVE - LIST**\n\n"
                "**Status : **`BAD`\n"
                "**Reason : **`can't get list if limit more than 1000.`",
            )
            return
    else:
        page_size = 25  # default page_size is 25
    checker = gdrive.pattern_match.group(2)
    if checker != "":
        if checker.startswith("-p"):
            parents = checker.split(None, 2)[1]
            parents = parents.split("/")[-1]
            try:
                name = checker.split(None, 2)[2]
            except IndexError:
                query = f"'{parents}' in parents and (name contains '*')"
            else:
                query = f"'{parents}' in parents and (name contains '{name}')"
        else:
            if re.search("-p (.*)", checker):
                parents = re.search("-p (.*)", checker).group(1)
                name = checker.split("-p")[0].strip()
                query = f"'{parents}' in parents and (name contains '{name}')"
            else:
                name = checker
                query = f"name contains '{name}'"
    else:
        global parent_Id
        try:
            if parent_Id is not None:
                query = f"'{parent_Id}' in parents and (name contains '*')"
        except NameError:
            if G_DRIVE_FOLDER_ID is not None:
                query = f"'{G_DRIVE_FOLDER_ID}' in parents and (name contains '*')"
            else:
                query = ""
    service = await create_app(gdrive)
    if service is False:
        return False
    message = ""
    fields = "nextPageToken, files(name, id, " "mimeType, webViewLink, webContentLink)"
    page_token = None
    result = []
    while True:
        try:
            response = (
                service.files()
                .list(
                    supportsAllDrives=True,
                    includeTeamDriveItems=True,
                    q=query,
                    spaces="drive",
                    corpora="allDrives",
                    fields=fields,
                    pageSize=page_size,
                    orderBy="modifiedTime desc, folder",
                    pageToken=page_token,
                )
                .execute()
            )
        except HttpError as e:
            await edit_or_reply(
                gdrive,
                "**[GDRIVE - LIST]**\n\n"
                "**Status : **`BAD`\n"
                f"**Reason : **`{str(e)}`",
            )
            return
        for files in response.get("files", []):
            if len(result) >= page_size:
                break

            file_name = files.get("name")
            if files.get("mimeType") == "application/vnd.google-apps.folder":
                link = files.get("webViewLink")
                message += f"📁️ • [{file_name}]({link})\n"
            else:
                link = files.get("webContentLink")
                message += f"📄️ • [{file_name}]({link})\n"
            result.append(files)
        if len(result) >= page_size:
            break

        page_token = response.get("nextPageToken", None)
        if page_token is None:
            break

    del result
    if query == "":
        query = "Not specified"
    await edit_or_reply(
        gdrive, "**Google Drive Query**:\n" f"`{query}`\n\n**Results**\n\n{message}"
    )


@bot.on(
    admin_cmd(
        pattern=r"glist(?: |$)(-l \d+)?(?: |$)?(.*)?(?: |$)",
        command="glist",
        outgoing=True,
    )
)
@bot.on(
    sudo_cmd(
        pattern="glist(?: |$)(-l \d+)?(?: |$)?(.*)?(?: |$)",
        command="glist",
        allow_sudo=True,
    )
)
async def catlists(gdrive):
    await lists(gdrive)


@bot.on(
    admin_cmd(
        pattern="gdf (mkdir|rm|chck) (.*)", command="gdf (mkdir|rm|chck)", outgoing=True
    )
)
@bot.on(
    sudo_cmd(
        pattern="gdf (mkdir|rm|chck) (.*)",
        command="gdf (mkdir|rm|chck)",
        allow_sudo=True,
    )
)
async def google_drive_managers(gdrive):
    """ - Google Drive folder/file management - """
    service = await create_app(gdrive)
    if service is False:
        return None
    """ - Split name if contains spaces by using ; - """
    f_name = gdrive.pattern_match.group(2).split(";")
    exe = gdrive.pattern_match.group(1)
    gdrive = await edit_or_reply(gdrive, "`Sending information...`")
    reply = ""
    for name_or_id in f_name:
        """ - in case given name has a space beetween ; - """

        name_or_id = name_or_id.strip()
        # ported from userge
        found = GDRIVE_ID.search(name_or_id)
        if found and "folder" in name_or_id:
            name_or_id, _ = (found.group(1), "folder")
        elif found:
            name_or_id, _ = (found.group(1), "file")
        else:
            name_or_id, _ = (name_or_id, "unknown")
        metadata = {
            "name": name_or_id,
            "mimeType": "application/vnd.google-apps.folder",
        }
        try:
            if parent_Id is not None:
                pass
        except NameError:
            """ - Fallback to G_DRIVE_FOLDER_ID else to root dir - """
            if G_DRIVE_FOLDER_ID is not None:
                metadata["parents"] = [G_DRIVE_FOLDER_ID]
        else:
            """ - Override G_DRIVE_FOLDER_ID because parent_Id not empty - """
            metadata["parents"] = [parent_Id]
        page_token = None
        result = (
            service.files()
            .list(
                q=f'name="{name_or_id}"',
                spaces="drive",
                fields=(
                    "nextPageToken, files(parents, name, id, size, "
                    "mimeType, webViewLink, webContentLink, description)"
                ),
                supportsAllDrives=True,
                pageToken=page_token,
            )
            .execute()
        )
        if exe == "mkdir":
            """
            - Create a directory, abort if exist when parent not given -
            """
            status = "**FOLDER - EXIST**"
            try:
                folder = result.get("files", [])[0]
            except IndexError:
                folder = await create_dir(service, name_or_id)
                status = status.replace("EXIST", "CREATED")
            folder_id = folder.get("id")
            webViewURL = folder.get("webViewLink")
            if "CREATED" in status:
                """ - Change permission - """
                await change_permission(service, folder_id)
            reply += (
                f"**{status}**\n\n"
                f"**Folder Name : **`{name_or_id}`\n"
                f"**ID  :** `{folder_id}`\n"
                f"**URL :** [Open]({webViewURL})\n\n"
            )
        elif exe == "rm":
            """ - Permanently delete, skipping the trash - """
            try:
                """ - Try if given value is a name not a folderId/fileId - """
                f = result.get("files", [])[0]
                f_id = f.get("id")
            except IndexError:
                """ - If failed assumming value is folderId/fileId - """
                f_id = name_or_id
                try:
                    f = await get_information(service, f_id)
                except Exception as e:
                    reply += (
                        f"**[FILE/FOLDER - ERROR]**\n\n"
                        "**Status : **`BAD`\n"
                        f"**Reason : **`{str(e)}`\n"
                    )
                    continue
            name = f.get("name")
            mimeType = f.get("mimeType")
            if mimeType == "application/vnd.google-apps.folder":
                status = "FOLDER - DELETION"
            else:
                status = "FILE - DELETION"
            try:
                service.files().delete(fileId=f_id, supportsAllDrives=True).execute()
            except HttpError as e:
                status.replace("DELETE", "ERROR")
                reply += (
                    f"**{status}**\n\n"
                    "**Status : **`BAD`\n"
                    f"**Reason : **`{str(e)}`\n\n"
                )
                continue
            else:
                reply += (
                    f"**{status}**\n\n" f"**Name : **`{name}`\n" "**Status : **`OK`\n\n"
                )
        elif exe == "chck":
            """ - Check file/folder if exists - """
            try:
                f = result.get("files", [])[0]
            except IndexError:
                """ - If failed assumming value is folderId/fileId - """
                f_id = name_or_id
                try:
                    f = await get_information(service, f_id)
                except Exception as e:
                    reply += (
                        "**FILE/FOLDER - ERROR**\n\n"
                        "**Status : **`BAD`\n"
                        f"**Reason : **`{str(e)}`\n\n"
                    )
                    continue
            """ - If exists parse file/folder information - """
            name_or_id = f.get("name")  # override input value
            f_id = f.get("id")
            f_size = f.get("size")
            mimeType = f.get("mimeType")
            webViewLink = f.get("webViewLink")
            downloadURL = f.get("webContentLink")
            description = f.get("description")
            if mimeType == "application/vnd.google-apps.folder":
                status = "**FOLDER - EXIST **"
            else:
                status = "**FILE - EXIST **"
            msg = (
                f"**{status}**\n\n"
                f"**Name  : **`{name_or_id}`\n"
                f"**ID    :** `{f_id}`\n"
            )
            if mimeType != "application/vnd.google-apps.folder":
                msg += f"**Size  :** `{humanbytes(f_size)}`\n"
                msg += f"**Link  :** [{name_or_id}]({downloadURL})\n\n"
            else:
                msg += f"**URL   :** [Open]({webViewLink})\n\n"
            if description:
                msg += f"**About :**\n`{description}`\n\n"
            reply += msg
        page_token = result.get("nextPageToken", None)
    await gdrive.edit(reply)


@bot.on(admin_cmd(pattern="gabort$", command="gabort", outgoing=True))
@bot.on(sudo_cmd(pattern="gabort$", command="gabort", allow_sudo=True))
async def cancel_process(gdrive):
    """
    Abort process for download and upload
    """
    global is_cancelled
    gdrive = await edit_or_reply(gdrive, "`Cancelling...`")
    try:
        from .torrentutils import aria2

        downloads = aria2.get_downloads()
        if len(downloads) != 0:
            aria2.remove_all(force=True)
            aria2.autopurge()
    except Exception as e:
        LOGS.info(str(e))
    is_cancelled = True
    await asyncio.sleep(3.5)
    await gdrive.delete()


@bot.on(admin_cmd(pattern="ugd(?: |$)(.*)", command="ugd", outgoing=True))
@bot.on(sudo_cmd(pattern="ugd(?: |$)(.*)", command="ugd", allow_sudo=True))
async def google_drive(gdrive):
    reply = ""
    """ - Parsing all google drive function - """
    start = datetime.now()
    value = gdrive.pattern_match.group(1)
    file_path = None
    uri = None
    if not value and not gdrive.reply_to_msg_id:
        return await edit_or_reply(gdrive, "`What should i Do You idiot`")
    elif value and gdrive.reply_to_msg_id:
        await edit_or_reply(
            gdrive,
            "**[UNKNOWN - ERROR]\n\n"
            "**Status : **`failed`\n"
            "**Reason : **`Confused to upload file or the replied message/media.`",
        )
        return None
    service = await create_app(gdrive)
    event = gdrive
    gdrive = await edit_or_reply(gdrive, "`Uploading...`")
    if service is False:
        return None
    if isfile(value):
        file_path = value
        if file_path.endswith(".torrent"):
            uri = [file_path]
            file_path = None
    elif isdir(value):
        folder_path = value
        global parent_Id
        folder_name = await get_raw_name(folder_path)
        folder = await create_dir(service, folder_name)
        parent_Id = folder.get("id")
        webViewURL = "https://drive.google.com/drive/folders/" + parent_Id
        try:
            await task_directory(gdrive, service, folder_path)
        except CancelProcess:
            await gdrive.edit(
                "**[FOLDER - CANCELLED]**\n\n"
                "**Status : **`OK - received signal cancelled.`"
            )
            await reset_parentId()
            await gdrive.delete()
            return True
        except Exception as e:
            await gdrive.edit(
                "**[FOLDER - UPLOAD]**\n\n"
                f"**Folder Name : **`{folder_name}`\n"
                "**Status : **`BAD`\n"
                f"**Reason : **`{str(e)}`"
            )
            await reset_parentId()
            return False
        else:
            await gdrive.edit(
                "**[FOLDER - UPLOAD]**\n\n"
                f"[{folder_name}]({webViewURL})\n"
                "**Status : **`OK - Successfully uploaded.`\n\n"
            )
            await reset_parentId()
            return True
    elif not value and event.reply_to_msg_id:
        output = await download(event, gdrive, service)
        if output == "install torrentutils":
            return
        reply += output
        await gdrive.edit(reply, link_preview=False)
        return None
    else:
        if re.findall(r"\bhttps?://drive\.google\.com\S+", value):
            """ - Link is google drive fallback to download - """
            value = re.findall(r"\bhttps?://drive\.google\.com\S+", value)
            for uri in value:
                try:
                    reply += await download_gdrive(gdrive, service, uri)
                except CancelProcess:
                    reply += (
                        "**[FILE - CANCELLED]**\n\n"
                        "**Status : **`OK - received signal cancelled.`"
                    )
                    break
                except Exception as e:
                    reply += (
                        "**[FILE - ERROR]**\n\n"
                        "**Status : **`BAD`\n"
                        f"**Reason : **`{str(e)}`\n\n"
                    )
                    continue
            if not reply:
                return None
            await gdrive.edit(reply, link_preview=False)
            return True
        elif re.findall(r"\bhttps?://.*\.\S+", value) or "magnet:?" in value:
            uri = value.split()
        else:
            for fileId in value.split():
                one = any(map(str.isdigit, fileId))
                two = "-" in fileId or "_" in fileId
                if True in [one or two]:
                    try:
                        reply += await download_gdrive(gdrive, service, fileId)
                    except CancelProcess:
                        reply += (
                            "**[FILE - CANCELLED]**\n\n"
                            "**Status : **`OK - received signal cancelled.`"
                        )
                        break
                    except Exception as e:
                        reply += (
                            "**[FILE - ERROR]**\n\n"
                            "**Status : **`BAD`\n"
                            f"**Reason : **`{str(e)}`\n\n"
                        )
                        continue
            if not reply:
                return None
            await gdrive.edit(reply, link_preview=False)
            return True
        if not uri and not event.reply_to_msg_id:
            await gdrive.edit(
                "**[VALUE - ERROR]**\n\n"
                "**Status : **`BAD`\n"
                "**Reason : **given value is not URL nor file/folder path. "
                "If you think this is wrong, maybe you use .gd with multiple "
                "value of files/folders, e.g `.gd <filename1> <filename2>` "
                "for upload from files/folders path this doesn't support it."
            )
            return False
    if uri and not event.reply_to_msg_id:
        for dl in uri:
            try:
                output = await download(event, gdrive, service, dl)
                if output == "install torrentutils":
                    return
                reply += str(output)
            except Exception as e:
                if " not found" in str(e) or "'file'" in str(e):
                    reply += (
                        "**[FILE - CANCELLED]**\n\n"
                        "**Status : **`OK - received signal cancelled.`"
                    )
                    await asyncio.sleep(2.5)
                    break
                else:
                    """ - if something bad happened, continue to next uri - """
                    reply += (
                        "**[UNKNOWN - ERROR]**\n\n"
                        "**Status : **`BAD`\n"
                        f"**Reason : **`{dl}` | `{str(e)}`\n\n"
                    )
                    continue
        await gdrive.edit(reply, link_preview=False)
        return None
    mimeType = await get_mimeType(file_path)
    file_name = await get_raw_name(file_path)
    try:
        result = await upload(gdrive, service, file_path, file_name, mimeType)
    except CancelProcess:
        gdrive.respond(
            "**[FILE - CANCELLED]**\n\n"
            "**Status : **`OK - received signal cancelled.`"
        )
    end = datetime.now()
    ms = (end - start).seconds
    if result:
        await gdrive.edit(
            f"**File Uploaded in **`{ms} seconds`\n\n"
            f"**➥ Size : **`{humanbytes(result[0])}`\n"
            f"**➥ Link :** [{file_name}]({result[1]})\n",
            link_preview=False,
        )
    return


@bot.on(
    admin_cmd(
        pattern="(gdfset|gdfclear)(?: |$)(.*)",
        command="(gdfset|gdfclear)",
        outgoing=True,
    )
)
@bot.on(
    sudo_cmd(
        pattern="(gdfset|gdfclear)(?: |$)(.*)",
        command="(gdfset|gdfclear)",
        allow_sudo=True,
    )
)
async def set_upload_folder(gdrive):
    """ - Set parents dir for upload/check/makedir/remove - """
    global parent_Id
    exe = gdrive.pattern_match.group(1)
    event = gdrive
    gdrive = await edit_or_reply(gdrive, "`Sending information...`")
    if exe == "gdfclear":
        if G_DRIVE_FOLDER_ID is not None:
            parent_Id = G_DRIVE_FOLDER_ID
            await gdrive.edit(
                "**[FOLDER - SET]**\n\n"
                "**Status : **`OK- using G_DRIVE_FOLDER_ID now.`"
            )
            return None
        else:
            try:
                del parent_Id
            except NameError:
                await gdrive.edit(
                    "**[FOLDER - SET]**\n\n" "**Status : **`BAD - No parent_Id is set.`"
                )
                return False
            else:
                await gdrive.edit(
                    "**[FOLDER - SET]**\n\n"
                    "**Status : **`OK`"
                    " - `G_DRIVE_FOLDER_ID empty, will use root.`"
                )
                return None
    inp = event.pattern_match.group(2)
    if not inp:
        await gdrive.edit(">`.gdfset put <folderURL/folderID>`")
        return None
    """ - Value for .gdfset (put|rm) can be folderId or folder link - """
    try:
        ext_id = re.findall(r"\bhttps?://drive\.google\.com\S+", inp)[0]
    except IndexError:
        """ - if given value isn't folderURL assume it's an Id - """
        c1 = any(map(str.isdigit, inp))
        c2 = "-" in inp or "_" in inp
        if True in [c1 or c2]:
            parent_Id = inp
            await gdrive.edit(
                "**[PARENT - FOLDER]**\n\n" "**Status : **`OK - Successfully changed.`"
            )
            return None
        else:
            await gdrive.edit(
                "**[PARENT - FOLDER]**\n\n" "**Status : WARNING** -` forcing use...`"
            )
            parent_Id = inp
    else:
        if "uc?id=" in ext_id:
            await gdrive.edit(
                "**[URL - ERROR]**\n\n" "**Status : **`BAD - Not a valid folderURL.`"
            )
            return None
        try:
            parent_Id = ext_id.split("folders/")[1]
        except IndexError:
            """ - Try catch again if URL open?id= - """
            try:
                parent_Id = ext_id.split("open?id=")[1]
            except IndexError:
                if "/view" in ext_id:
                    parent_Id = ext_id.split("/")[-2]
                else:
                    try:
                        parent_Id = ext_id.split("folderview?id=")[1]
                    except IndexError:
                        await gdrive.edit(
                            "**[URL - ERROR]**\n\n"
                            "**Status : **`BAD - Not a valid folderURL.`"
                        )
                        return None
        await gdrive.edit(
            "**[PARENT - FOLDER]**\n\n" "**Status : **`OK - Successfully changed.`"
        )
    return


async def check_progress_for_dl(event, gid, previous):
    complete = None
    global is_cancelled
    global filenames
    is_cancelled = False
    from .torrentutils import aria2

    while not complete:
        file = aria2.get_download(gid)
        complete = file.is_complete
        if is_cancelled:
            raise CancelProcess
        try:
            if not complete:
                if not file.error_message:
                    percentage = int(file.progress)
                    downloaded = percentage * int(file.total_length) / 100
                    prog_str = "**Downloading : **`[{0}{1}] {2}`".format(
                        "".join("▰" for i in range(math.floor(percentage / 10))),
                        "".join("▱" for i in range(10 - math.floor(percentage / 10))),
                        file.progress_string(),
                    )

                    msg = (
                        "**[URI - DOWNLOAD]**\n\n"
                        f"**Name : **`{file.name}`\n"
                        f"**Status : **`{file.status.capitalize()}`\n"
                        f"{prog_str}\n"
                        f"`{humanbytes(downloaded)} of {file.total_length_string()}"
                        f" @ {file.download_speed_string()}`\n"
                        f"**ETA** -> `{file.eta_string()}`\n"
                    )
                    if msg != previous:
                        await event.edit(msg)
                        msg = previous

                    await asyncio.sleep(3)
                    await check_progress_for_dl(gid, event, previous)
                else:
                    await event.edit("Error : `{}`".format(str(file.error_message)))
                    return
            else:
                await event.edit(
                    f"**Name : **`{file.name}`\n"
                    f"**Size : **`{file.total_length_string()}`\n"
                    f"**Path : **`{TMP_DOWNLOAD_DIRECTORY + file.name}`\n"
                    "**Resp : **`OK - Successfully downloaded...`"
                )
                return file.name
        except Exception as e:
            if " not found" in str(e) or "'file'" in str(e):
                await event.edit("Download Canceled :\n`{}`".format(file.name))
                await asyncio.sleep(2.5)
                return await event.delete()
            elif " depth exceeded" in str(e):
                file.remove(force=True)
                await event.edit(
                    "Download Auto Canceled :\n`{}`\nYour Torrent/Link is Dead.".format(
                        file.name
                    )
                )


@bot.on(
    admin_cmd(pattern="gdown ?(-u)? (.*)", command="(gdown|gdown -u)", outgoing=True)
)
@bot.on(
    sudo_cmd(pattern="gdown ?(-u)? (.*)", command="(gdown|gdown -u)", allow_sudo=True)
)
async def g_download(event):
    if event.fwd_from:
        return
    service = await create_app(event)
    if service is False:
        return None
    thumb = None
    cmd = event.pattern_match.group(1)
    drive_link = event.pattern_match.group(2)
    catevent = await edit_or_reply(
        event, "`Downloading Requested File from G-Drive...`"
    )
    file_name, catprocess = await gdrive_download(event, catevent, service, drive_link)
    if catprocess is not None:
        return await edit_delete(catevent, file_name)
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    if not cmd:
        await catevent.edit("**File Downloaded.\nName : **`" + str(file_name) + "`")
    else:
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            file_name,
            caption=f"**File Name : **`{os.path.basename(file_name)}`",
            thumb=thumb,
            force_document=False,
            supports_streaming=True,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, catevent, c_time, "Uploading...", file_name)
            ),
        )
        os.remove(file_name)
        await edit_delete(
            catevent,
            "**File Downloaded and uploaded.\nName : **`" + str(file_name) + "`",
            5,
        )


@bot.on(admin_cmd(pattern="gshare (.*)", command="gshare"))
@bot.on(sudo_cmd(pattern="gshare (.*)", command="gshare", allow_sudo=True))
async def gshare(event):
    if event.fwd_from:
        return
    service = await create_app(event)
    if service is False:
        return None
    input_str = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "`Creating sharable link...`")
    await asyncio.sleep(2)
    await share(service, catevent, input_str)


CMD_HELP.update(
    {
        "gdrive": "**Plugin :** `gdrive`"
        "\n\n  •  **Syntax : **`.gauth`"
        "\n  •  **Function : **generate token to enable all cmd google drive service."
        "\nThis only need to run once in life time."
        "\n\n  •  **Syntax : **`.greset`"
        "\n  •  **Function : **reset your token if something bad happened or change drive acc."
        "\n\n  •  **Syntax : **`.ugd`"
        "\n  •  **Function : **Upload file from local or uri/url/drivelink into google drive."
        "\nfor drivelink it's upload only if you want to."
        "\n\n  •  **Syntax : **`.gabort`"
        "\n  •  **Function : **Abort process uploading or downloading."
        "\n\n  •  **Syntax : **`.gdf mkdir`"
        "\n  •  **Function : **Create gdrive folder."
        "\n\n  •  **Syntax : **`.gdf chck`"
        "\n  •  **Function : **Check file/folder in gdrive."
        "\n\n  •  **Syntax : **`.gdf rm`"
        "\n  •  **Function : **Delete files/folders in gdrive."
        "\nCan't be undone, this method skipping file trash, so be caution..."
        "\n\n  •  **Syntax : **`.gdfset`"
        "\n  •  **Function : **Change upload directory in gdrive."
        "\ninto **G_DRIVE_FOLDER_ID** and if empty upload will go to root."
        "\n\n  •  **Syntax : **`.gdfclear`"
        "\n  •  **Function : **remove set parentId from cmd\n>`.gfset put` "
        "\n\n  •  **Syntax : **`.gdown <gdrive File-Link>`\
        \n  •  **Function : **G-Drive File Downloader Plugin For Userbot. only gdrive files are supported now"
        "\nUse flag `-u` to directly upload to telegram in `.gdown` command"
        "\n\n  •  **Syntax : **`.glist`"
        "\n  •  **Function : **Get list of folders and files with default size 50."
        "\nUse flags `-l range[1-1000]` for limit output."
        "\nUse flags `-p parents-folder_id` for lists given folder in gdrive."
        "\n\n  •  **NOTE :**"
        "\nfor `.glist` you can combine -l and -p flags with or without name "
        "at the same time, it must be `-l` flags first before use `-p` flags.\n"
        "And by default it lists from latest 'modifiedTime' and then folders."
        "\n\n  •  **Syntax : **`.gshare your gdrive link`"
        "\n  •  **Function : **Get sharable link for team drive files need to set G_DRIVE_INDEX_LINK"
    }
)

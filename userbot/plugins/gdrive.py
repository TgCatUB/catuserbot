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
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from telethon import events

from userbot import catub
from userbot.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import CancelProcess, humanbytes, progress, time_formatter
from ..helpers.utils import _format
from ..sql_helper import google_drive_sql as helper
from . import (
    BOTLOG,
    BOTLOG_CHATID,
    G_DRIVE_CLIENT_ID,
    G_DRIVE_CLIENT_SECRET,
    G_DRIVE_DATA,
    G_DRIVE_FOLDER_ID,
    TMP_DOWNLOAD_DIRECTORY,
)

LOGS = logging.getLogger(__name__)
plugin_category = "misc"

# Catuserbot Google Drive managers  ported from Projectbish and added extra things by @mrconfused


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

thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "/thumb_image.jpg")
# =========================================================== #
#                                                             #
# =========================================================== #
GDRIVE_ID = re.compile(
    r"https://drive.google.com/[\w\?\./&=]+([-\w]{33}|(?<=[/=])0(?:A[-\w]{17}|B[-\w]{26}))"
)


G_DRIVE_FILE_LINK = "📄 [{}](https://drive.google.com/open?id={}) __({})__"
G_DRIVE_FOLDER_LINK = "📁 [{}](https://drive.google.com/drive/folders/{})"


class GDRIVE:
    def __init__(self):
        self.parent_Id = G_DRIVE_FOLDER_ID or ""
        self.is_cancelled = False


GDRIVE_ = GDRIVE()


async def create_app(gdrive):
    """Create google drive service app"""
    hmm = gdrive.client.uid
    creds = helper.get_credentials(str(hmm))
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if creds is not None:
        """Repack credential objects from strings"""
        creds = pickle.loads(base64.b64decode(creds.encode()))
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            await gdrive.edit("`Refreshing credentials...`")
            """Refresh credentials"""
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


async def get_raw_name(file_path):
    """Get file_name from file_path"""
    return file_path.split("/")[-1]


async def get_mimeType(name):
    """Check mimeType given file"""
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


async def download(event, gdrive, service, uri=None):  # sourcery no-metrics
    """Download files to local then upload"""
    start = datetime.now()
    reply = ""
    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)
        required_file_name = ""
    if uri:
        try:
            from .torrentutils import aria2, check_metadata

            cattorrent = True
        except Exception:
            cattorrent = False
        full_path = os.path.join(os.getcwd(), TMP_DOWNLOAD_DIRECTORY)
        if cattorrent:
            LOGS.info("torrentutils exists")
            if os.path.isfile(uri) and uri.endswith(".torrent"):
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
            required_file_name = os.path.join(TMP_DOWNLOAD_DIRECTORY, filenames)
        except Exception:
            required_file_name = os.path.join(TMP_DOWNLOAD_DIRECTORY, filename)
    else:
        try:
            current_time = time.time()
            GDRIVE_.is_cancelled = False
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
                        is_cancelled=GDRIVE_.is_cancelled,
                    )
                ),
            )
        except CancelProcess:
            names = [
                os.path.join(TMP_DOWNLOAD_DIRECTORY, name)
                for name in os.listdir(TMP_DOWNLOAD_DIRECTORY)
            ]

            """ asumming newest files are the cancelled one """
            newest = max(names, key=os.path.getctime)
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
        if os.path.isfile(required_file_name):
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
            folder = await create_dir(service, file_name, GDRIVE_.parent_Id)
            dir_id = folder.get("id")
            webViewURL = "https://drive.google.com/drive/folders/" + dir_id
            try:
                await task_directory(gdrive, service, required_file_name, dir_id)
            except CancelProcess:
                reply += (
                    "**[FOLDER - CANCELLED]**\n\n"
                    "**Status : **`OK - received signal cancelled.`"
                )
                return reply
            except Exception:
                pass
            else:
                reply += (
                    f"**{status}**\n\n"
                    f"[{file_name}]({webViewURL})\n"
                    "**Status : **`OK - Successfully uploaded.`\n\n"
                )
                return reply
    except Exception as e:
        status = status.replace("DOWNLOAD]", "ERROR]")
        reply += f"**{status}**\n\n**Status : **`failed`\n**Reason : **`{e}`\n\n"
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
        if GDRIVE_._is_canceled:
            raise CancelProcess
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


async def create_server_dir(service, current_path, folder_name):
    path = os.path.join(current_path, folder_name)
    if not os.path.exists(path):
        os.mkdir(path)
    LOGS.info("Created Folder => Name: %s", folder_name)
    return path


async def gdrive_download(
    event, gdrive, service, uri, path=os.path.join(os.getcwd(), "gdrive")
):  # sourcery no-metrics
    reply = ""
    if not os.path.exists(path):
        os.mkdir(path)
    try:
        file_Id, _ = await get_file_id(uri)
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
                file_size = humanbytes(
                    page.find("span", {"class": "uc-name-size"})
                    .text.split()[-1]
                    .strip("()")
                )
            else:
                file_size = int(download.headers["Content-Length"])
            file_name = re.search(
                "filename='(.)'", download.headers["Content-Disposition"]
            ).group(1)
            file_path = os.path.join(path, file_name)
            with io.FileIO(file_path, "wb") as files:
                CHUNK_SIZE = None
                current_time = time.time()
                display_message = None
                first = True
                GDRIVE_.is_cancelled = False
                for chunk in download.iter_content(CHUNK_SIZE):
                    if GDRIVE_.is_cancelled:
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
            file_name = file.get("name").replace(" ", "_")
            newpath = await create_server_dir(service, path, file_name)
            filespath_d = await list_drive_dir(service, file_Id)
            newerrors = []
            for nfileid in filespath_d:
                nfile_path, error = await gdrive_download(
                    event, gdrive, service, nfileid["id"], path=newpath
                )
                if error is not None:
                    newerrors.append(error)
            errorstr = "".join(f"{i}\n" for i in newerrors)
            return newpath, errorstr
        file_path = os.path.join(path, file_name)
        request = service.files().get_media(fileId=file_Id, supportsAllDrives=True)
        with io.FileIO(file_path, "wb") as df:
            downloader = MediaIoBaseDownload(df, request)
            complete = False
            GDRIVE_.is_cancelled = False
            current_time = time.time()
            display_message = None
            while not complete:
                if GDRIVE_.is_cancelled:
                    raise CancelProcess
                status, complete = downloader.next_chunk()
                if status:
                    file_size = status.total_size
                    diff = time.time() - current_time
                    downloaded = status.resumable_progress
                    percentage = downloaded / file_size * 100
                    speed = round(downloaded / diff, 2)
                    eta = round((file_size - downloaded) / speed)
                    prog_str = "`{0}` | `[{1}{2}] {3}%`".format(
                        status,
                        "".join(
                            Config.FINISHED_PROGRESS_STR
                            for i in range(math.floor(percentage / 5))
                        ),
                        "".join(
                            Config.UNFINISHED_PROGRESS_STR
                            for i in range(20 - math.floor(percentage / 5))
                        ),
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


async def download_gdrive(gdrive, service, uri, dir_id=GDRIVE_.parent_Id):
    """remove drivesdk and export=download from link"""
    reply = ""
    start = datetime.now()
    file_Id, _ = await get_file_id(uri)
    try:
        file = (
            service.files()
            .get(fileId=file_Id, fields="name, mimeType", supportsTeamDrives=True)
            .execute()
        )
        if file["mimeType"] == "application/vnd.google-apps.folder":
            folder = await create_dir(service, file["name"], dir_id)
            filespath_d = await list_drive_dir(service, file_Id)
            for nfileid in filespath_d:
                await download_gdrive(gdrive, service, nfileid["id"], folder["id"])
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
        reply = f"**Error : **`{e}`"
    return reply


async def change_permission(service, Id):
    permission = {"role": "reader", "type": "anyone"}
    try:
        service.permissions().create(fileId=Id, body=permission).execute()
    except HttpError as e:
        """it's not possible to change permission per file for teamdrive"""
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
            len(GDRIVE_.parent_Id)
        except NameError:
            # Fallback to G_DRIVE_FOLDER_ID else root dir
            if G_DRIVE_FOLDER_ID is not None:
                metadata["parents"] = [G_DRIVE_FOLDER_ID]
        else:
            # Override G_DRIVE_FOLDER_ID because parent_Id not empty
            metadata["parents"] = [GDRIVE_.parent_Id]
    else:
        metadata["parents"] = [dir_id]
    folder = (
        service.files()
        .create(body=metadata, fields="id, webViewLink", supportsAllDrives=True)
        .execute()
    )
    await change_permission(service, folder.get("id"))
    return folder


async def upload(gdrive, service, file_path, file_name, mimeType, dir_id=None):
    try:
        await gdrive.edit("`Processing upload...`")
    except Exception:
        pass
    body = {
        "name": file_name,
        "description": "Uploaded from Telegram using Catuserbot.",
        "mimeType": mimeType,
        "parents": [dir_id] if dir_id is not None else [GDRIVE_.parent_Id],
    }
    media_body = MediaFileUpload(file_path, mimetype=mimeType, resumable=True)
    # Start upload process
    file = service.files().create(
        body=body,
        media_body=media_body,
        fields="id, size, webContentLink",
        supportsAllDrives=True,
    )
    current_time = time.time()
    response = None
    display_message = None
    GDRIVE_.is_cancelled = False
    while response is None:
        if GDRIVE_.is_cancelled:
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
                "".join(
                    Config.FINISHED_PROGRESS_STR
                    for i in range(math.floor(percentage / 10))
                ),
                "".join(
                    Config.UNFINISHED_PROGRESS_STR
                    for i in range(10 - math.floor(percentage / 10))
                ),
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
    # Change permission
    await change_permission(service, file_id)
    return int(file_size), downloadURL


async def task_directory(gdrive, service, folder_path, dir_id=None):
    GDRIVE_.is_cancelled = False
    lists = os.listdir(folder_path)
    dir_id = dir_id or GDRIVE_.parent_Id
    if len(lists) == 0:
        return dir_id
    for f in lists:
        if GDRIVE_.is_cancelled:
            raise CancelProcess
        current_f_name = os.path.join(folder_path, f)
        if os.path.isdir(current_f_name):
            folder = await create_dir(service, f, dir_id)
            await task_directory(gdrive, service, current_f_name, folder.get("id"))
            returnid = folder.get("id")
        else:
            file_name = await get_raw_name(current_f_name)
            mimeType = await get_mimeType(current_f_name)
            await upload(gdrive, service, current_f_name, file_name, mimeType, dir_id)
            returnid = dir_id
    return returnid


async def share(service, event, url):
    """get shareable link"""
    await event.edit("`Loading GDrive Share...`")
    file_id, _ = await get_file_id(url)
    try:
        result = await get_output(service, file_id)
    except Exception as e:
        await edit_delete(event, f"str({e})", parse_mode=_format.parse_pre)
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


async def check_progress_for_dl(event, gid, previous):  # sourcery no-metrics
    complete = None
    global filenames
    GDRIVE_.is_cancelled = False
    from .torrentutils import aria2

    while not complete:
        file = aria2.get_download(gid)
        complete = file.is_complete
        if GDRIVE_.is_cancelled:
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
                    f"**Path : **`{os.path.join(TMP_DOWNLOAD_DIRECTORY , file.name)}`\n"
                    "**Resp : **`OK - Successfully downloaded...`"
                )
                LOGS.info(file.name)
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


async def lists(gdrive, folderlink=None):  # sourcery no-metrics
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
    if checker == "":
        try:
            if GDRIVE_.parent_Id is not None:
                query = f"'{GDRIVE_.parent_Id}' in parents and (name contains '*')"
        except NameError:
            if G_DRIVE_FOLDER_ID is not None:
                query = f"'{G_DRIVE_FOLDER_ID}' in parents and (name contains '*')"
            else:
                query = ""
    elif checker.startswith("-p"):
        parents = checker.split(None, 2)[1]
        parents = parents.split("/")[-1]
        try:
            name = checker.split(None, 2)[2]
        except IndexError:
            query = f"'{parents}' in parents and (name contains '*')"
        else:
            query = f"'{parents}' in parents and (name contains '{name}')"
    elif re.search("-p ([\s\S]*)", checker):
        parents = re.search("-p ([\s\S]*)", checker).group(1)
        name = checker.split("-p")[0].strip()
        query = f"'{parents}' in parents and (name contains '{name}')"
    else:
        name = checker
        query = f"name contains '{name}'"
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
                f"**[GDRIVE - LIST]**\n\n**Status : **`BAD`\n**Reason : **`{e}`",
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


@catub.cat_cmd(
    pattern="gauth$",
    command=("gauth", plugin_category),
    info={
        "header": "To authenciate gdrive credentials.",
        "description": "Generate token to enable all cmd google drive service. This only need to run once in life time.",
        "usage": "{tr}gauth",
    },
)
async def generate_credentials(gdrive):
    """Only generate once for long run"""
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
    """Generate credentials"""
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
        """Only for old user"""
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
        """Unpack credential objects into strings"""
        creds = base64.b64encode(pickle.dumps(creds)).decode()
        await gdrive.edit("`Credentials created...`")
    helper.save_credentials(str(gdrive.sender_id), creds)
    await gdrive.delete()
    return


@catub.cat_cmd(
    pattern="greset",
    command=("greset", plugin_category),
    info={
        "header": "To reset gdrive credentials.",
        "description": "reset your token if something bad happened or change drive acc.",
        "usage": "{tr}greset",
    },
)
async def reset_credentials(gdrive):
    """Reset credentials or change account"""
    hmm = gdrive.client.uid
    gdrive = await edit_or_reply(gdrive, "`Resetting information...`")
    helper.clear_credentials(str(hmm))
    await gdrive.edit("`Done...`")
    await asyncio.sleep(1)
    await gdrive.delete()
    return


@catub.cat_cmd(
    pattern="glist(?: |$)(-l \d+)?(?: |$)?([\s\S]*)?(?: |$)",
    command=("glist", plugin_category),
    info={
        "header": "Get list of folders and files with default size 50",
        "flags": {
            "l": "Use flag `-l range[1-1000]` for limit output",
            "p": "Use flag `-p parents-folder_id` for files/folder in given folder in gdrive.",
        },
        "note": "for `.glist` you can combine -l and -p flags with or without name "
        "at the same time, it must be `-l` flags first before use `-p` flags.\n"
        "And by default it lists from latest 'modifiedTime' and then folders.",
        "usage": [
            "{tr}glist -l <count>",
            "{tr}glist -l <count> -p parent_id",
            "{tr}glist -p <parent_id>",
            "{tr}glist",
        ],
    },
)
async def catlists(gdrive):
    "To get list of files and folers"
    await lists(gdrive)


@catub.cat_cmd(
    pattern="gdf (mkdir|rm|info) ([\s\S]*)",
    command=("gdf", plugin_category),
    info={
        "header": "Google Drive folder/file management",
        "description": "To create or delete or check folders/files in gdrive.",
        "options": {
            "mkdir": "Create gdrive folder",
            "info": "to get file/folder details of our gdrive.",
            "rm": "Delete files/folders in gdrive. Can't be undone, this method skipping file trash, so be caution..",
        },
        "usage": [
            "{tr}gdf mkdir <folder name>",
            "{tr}gdf info <folder/file path>",
            "{tr}gdf rm <folder/file path>",
        ],
    },
)
async def google_drive_managers(gdrive):  # sourcery no-metrics
    """Google Drive folder/file management"""
    service = await create_app(gdrive)
    if service is False:
        return None
    """Split name if contains spaces by using ;"""
    f_name = gdrive.pattern_match.group(2).split(";")
    exe = gdrive.pattern_match.group(1)
    gdrive = await edit_or_reply(gdrive, "`Sending information...`")
    reply = ""
    for name_or_id in f_name:
        """in case given name has a space beetween ;"""

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
            len(GDRIVE_.parent_Id)
        except NameError:
            """Fallback to G_DRIVE_FOLDER_ID else to root dir"""
            if G_DRIVE_FOLDER_ID is not None:
                metadata["parents"] = [G_DRIVE_FOLDER_ID]
        else:
            """Override G_DRIVE_FOLDER_ID because parent_Id not empty"""
            metadata["parents"] = [GDRIVE_.parent_Id]
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
                folder = await create_dir(service, name_or_id, GDRIVE_.parent_Id)
                status = status.replace("EXIST", "CREATED")
            folder_id = folder.get("id")
            webViewURL = folder.get("webViewLink")
            if "CREATED" in status:
                """Change permission"""
                await change_permission(service, folder_id)
            reply += (
                f"**{status}**\n\n"
                f"**Folder Name : **`{name_or_id}`\n"
                f"**ID  :** `{folder_id}`\n"
                f"**URL :** [Open]({webViewURL})\n\n"
            )
        elif exe == "rm":
            """Permanently delete, skipping the trash"""
            try:
                """Try if given value is a name not a folderId/fileId"""
                f = result.get("files", [])[0]
                f_id = f.get("id")
            except IndexError:
                """If failed assumming value is folderId/fileId"""
                f_id = name_or_id
                try:
                    f = await get_information(service, f_id)
                except Exception as e:
                    reply += f"**[FILE/FOLDER - ERROR]**\n\n**Status : **`BAD`\n**Reason : **`{e}`\n"

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
                reply += f"**{status}**\n\n**Status : **`BAD`\n**Reason : **`{e}`\n\n"
                continue
            else:
                reply += (
                    f"**{status}**\n\n" f"**Name : **`{name}`\n" "**Status : **`OK`\n\n"
                )
        elif exe == "info":
            """Check file/folder if exists"""
            try:
                f = result.get("files", [])[0]
            except IndexError:
                """If failed assumming value is folderId/fileId"""
                f_id = name_or_id
                try:
                    f = await get_information(service, f_id)
                except Exception as e:
                    reply += f"**FILE/FOLDER - ERROR**\n\n**Status : **`BAD`\n**Reason : **`{e}`\n\n"

                    continue
            """If exists parse file/folder information"""
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


@catub.cat_cmd(
    pattern="gabort$",
    command=("gabort", plugin_category),
    info={
        "header": "Abort process uploading or downloading process.",
        "usage": "{tr}gabort",
    },
)
async def cancel_process(gdrive):
    "Abort process for download and upload."
    gdrive = await edit_or_reply(gdrive, "`Cancelling...`")
    try:
        from .torrentutils import aria2

        downloads = aria2.get_downloads()
        if len(downloads) != 0:
            aria2.remove_all(force=True)
            aria2.autopurge()
    except Exception as e:
        LOGS.info(str(e))
    GDRIVE_.is_cancelled = True
    await asyncio.sleep(3.5)
    await gdrive.delete()


@catub.cat_cmd(
    pattern="ugd(?:\s|$)([\s\S]*)",
    command=("ugd", plugin_category),
    info={
        "header": "upload files/folders to gdrive.",
        "description": "Upload file from local or uri/url/drivelink into google drive."
        "\nfor drivelink it's upload only if you want to",
        "usage": "{tr}ugd <uri/url/drivelink/local file/folder path>",
    },
)
async def google_drive(gdrive):  # sourcery no-metrics
    "To upload to gdrive."
    reply = ""
    start = datetime.now()
    value = gdrive.pattern_match.group(1)
    file_path = None
    uri = None
    if not value and not gdrive.reply_to_msg_id:
        return await edit_or_reply(gdrive, "`What should i Do You idiot`")
    elif value and gdrive.reply_to_msg_id:
        await edit_or_reply(
            gdrive,
            "**[UNKNOWN - ERROR]**\n\n"
            "**Status : **`failed`\n"
            "**Reason : **`Confused to upload file or the replied message/media.`",
        )
        return None
    service = await create_app(gdrive)
    event = gdrive
    if service is False:
        return None
    gdrive = await edit_or_reply(gdrive, "`Uploading...`")
    if os.path.isfile(value):
        file_path = value
        if file_path.endswith(".torrent"):
            uri = [file_path]
            file_path = None
    elif os.path.isdir(value):
        folder_path = value
        folder_name = await get_raw_name(folder_path)
        folder = await create_dir(service, folder_name, dir_id=GDRIVE_.parent_Id)
        dir_Id = folder.get("id")
        webViewURL = "https://drive.google.com/drive/folders/" + dir_Id
        try:
            await task_directory(gdrive, service, folder_path, dir_id=folder.get("id"))
        except CancelProcess:
            await gdrive.edit(
                "**[FOLDER - CANCELLED]**\n\n"
                "**Status : **`OK - received signal cancelled.`"
            )
            await gdrive.delete()
            return True
        except Exception as e:
            await gdrive.edit(
                f"**[FOLDER - UPLOAD]**\n\n**Folder Name : **`{folder_name}`\n**Status : **`BAD`\n**Reason : **`{e}`"
            )

            return False
        else:
            await gdrive.edit(
                "**[FOLDER - UPLOAD]**\n\n"
                f"[{folder_name}]({webViewURL})\n"
                "**Status : **`OK - Successfully uploaded.`\n\n"
            )
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
            """Link is google drive fallback to download"""
            value = re.findall(r"\bhttps?://drive\.google\.com\S+", value)
            for uri in value:
                try:
                    reply += await download_gdrive(
                        gdrive,
                        service,
                        uri,
                    )
                except CancelProcess:
                    reply += (
                        "**[FILE - CANCELLED]**\n\n"
                        "**Status : **`OK - received signal cancelled.`"
                    )
                    break
                except Exception as e:
                    reply += f"**[FILE - ERROR]**\n\n**Status : **`BAD`\n**Reason : **`{e}`\n\n"
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
                        reply += f"**[FILE - ERROR]**\n\n**Status : **`BAD`\n**Reason : **`{e}`\n\n"
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
                    """if something bad happened, continue to next uri"""
                    reply += f"**[UNKNOWN - ERROR]**\n\n**Status : **`BAD`\n**Reason : **`{dl}` | `{e}`\n\n"

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


@catub.cat_cmd(
    pattern="gclear$",
    command=("gclear", plugin_category),
    info={
        "header": "to clear the temparary upload directory.",
        "description": "that is directory set by command gset . when you used this command it will make your parent directory as G_DRIVE_FOLDER_ID",
        "usage": "{tr}gclear",
    },
)
async def set_upload_folder(gdrive):
    """to clear the temperary upload parent id."""
    gdrive = await edit_or_reply(gdrive, "`Sending information...`")
    if G_DRIVE_FOLDER_ID is not None:
        GDRIVE_.parent_Id = G_DRIVE_FOLDER_ID
        await gdrive.edit(
            "**[FOLDER - SET]**\n\n" "**Status : **`OK- using G_DRIVE_FOLDER_ID now.`"
        )
        return None
    try:
        GDRIVE_.parent_id = ""
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


@catub.cat_cmd(
    pattern="gset(?:\s|$)([\s\S]*)",
    command=("gset", plugin_category),
    info={
        "header": "To set temparary parent id.",
        "description": "Change upload directory in gdrive",
        "usage": "{tr}gset  <folderURL/folderID>",
    },
)
async def set_upload_folder(gdrive):
    """Set parents dir for upload/check/makedir/remve"""
    event = gdrive
    gdrive = await edit_or_reply(gdrive, "`Sending information...`")
    inp = event.pattern_match.group(1)
    if not inp:
        await gdrive.edit(">`.gset <folderURL/folderID>`")
        return None
    """Value for .gset can be folderId or folder link"""
    try:
        ext_id = re.findall(r"\bhttps?://drive\.google\.com\S+", inp)[0]
    except IndexError:
        """if given value isn't folderURL assume it's an Id"""
        c1 = any(map(str.isdigit, inp))
        c2 = "-" in inp or "_" in inp
        if True in [c1 or c2]:
            GDRIVE_.parent_Id = inp
            await gdrive.edit(
                "**[PARENT - FOLDER]**\n\n" "**Status : **`OK - Successfully changed.`"
            )
            return None
        await gdrive.edit(
            "**[PARENT - FOLDER]**\n\n" "**Status : WARNING** -` forcing use...`"
        )
        GDRIVE_.parent_Id = inp
    else:
        GDRIVE_.parent_Id, _ = await get_file_id(ext_id)
        await gdrive.edit(
            "**[PARENT - FOLDER]**\n\n" "**Status : **`OK - Successfully changed.`"
        )


@catub.cat_cmd(
    pattern="gdown ?(-u)? ([\s\S]*)",
    command=("gdown", plugin_category),
    info={
        "header": "To download files form gdrive.",
        "description": "G-Drive File Downloader Plugin For Userbot. only gdrive files are supported now",
        "flags": {
            "u": "to directly upload to telegram",
        },
        "usage": [
            "{tr}gdown <gdrive File-Link>",
            "{tr}gdown -u <gdrive File-Link>",
        ],
    },
)
async def g_download(event):
    "To download from gdrive"
    service = await create_app(event)
    if service is False:
        return None
    cmd = event.pattern_match.group(1)
    drive_link = event.pattern_match.group(2)
    catevent = await edit_or_reply(
        event, "`Downloading Requested File from G-Drive...`"
    )
    file_name, catprocess = await gdrive_download(event, catevent, service, drive_link)
    if catprocess is not None:
        return await edit_delete(catevent, file_name)
    thumb = thumb_image_path if os.path.exists(thumb_image_path) else None
    if not cmd:
        await catevent.edit("**File Downloaded.\nLocation : **`" + str(file_name) + "`")
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


@catub.cat_cmd(
    pattern="gshare ([\s\S]*)",
    command=("gshare", plugin_category),
    info={
        "header": "To share the team drive files.",
        "description": "Get sharable link for team drive files need to set G_DRIVE_INDEX_LINK",
        "usage": "{tr}gshare <folder/file link>",
    },
)
async def gshare(event):
    "To share the team drive files."
    service = await create_app(event)
    if service is False:
        return None
    input_str = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "`Creating sharable link...`")
    await asyncio.sleep(2)
    await share(service, catevent, input_str)

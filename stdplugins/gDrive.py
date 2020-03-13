"""Upload local Files to gDrive
Syntax:
.ugdrive"""

# The entire code given below is verbatim copied from
# https://github.com/cyberboysumanjay/Gdrivedownloader/blob/master/gdrive_upload.py
# there might be some changes made to suit the needs for this repository
# Licensed under MIT License

import asyncio
import json
import math
import os
import time
from datetime import datetime
from telethon import events
from uniborg.util import admin_cmd, progress, humanbytes
#
from mimetypes import guess_type
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient.errors import ResumableUploadError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import file, client, tools
import httplib2


# Path to token json file, it should be in same directory as script
G_DRIVE_TOKEN_FILE = Config.TMP_DOWNLOAD_DIRECTORY + "/auth_token.txt"
# Copy your credentials from the APIs Console
CLIENT_ID = Config.G_DRIVE_CLIENT_ID
CLIENT_SECRET = Config.G_DRIVE_CLIENT_SECRET
# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"
# Redirect URI for installed apps, can be left as is
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
# global variable to set Folder ID to upload to
G_DRIVE_F_PARENT_ID = None
# global variable to indicate mimeType of directories in gDrive
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"


@borg.on(admin_cmd(pattern="ugdrive ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        await mone.edit("This module requires credentials from https://da.gd/so63O. Aborting!")
        return
    if Config.PRIVATE_GROUP_BOT_API_ID is None:
        await event.edit("Please set the required environment variable `PRIVATE_GROUP_BOT_API_ID` for this plugin to work")
        return
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
        #
        if Config.G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(Config.G_DRIVE_AUTH_TOKEN_DATA)
        # Check if token file exists, if not create it by requesting authorization code
        storage = None
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
        http = authorize(G_DRIVE_TOKEN_FILE, storage)
        # Authorize, get file parameters, upload file and print out result URL for download
        # http = authorize(G_DRIVE_TOKEN_FILE, None)
        file_name, mime_type = file_ops(required_file_name)
        # required_file_name will have the full path
        # Sometimes API fails to retrieve starting URI, we wrap it.
        try:
            g_drive_link = await upload_file(http, required_file_name, file_name, mime_type, mone, G_DRIVE_F_PARENT_ID)
            await mone.edit(f"Here is your Google Drive link: {g_drive_link}")
        except Exception as e:
            await mone.edit(f"Exception occurred while uploading to gDrive {e}")
    else:
        await mone.edit("File Not found in local server. Give me a file path :((")


@borg.on(admin_cmd(pattern="gdrivesp https?://drive\.google\.com/drive/u/\d/folders/([-\w]{25,})", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    input_str = event.pattern_match.group(1)
    if input_str:
        G_DRIVE_F_PARENT_ID = input_str
        await mone.edit(f"Custom Folder ID set successfully. The next uploads will upload to {G_DRIVE_F_PARENT_ID} till `.gdriveclear`")
        await event.delete()
    else:
        await mone.edit("Send `.gdrivesp https://drive.google.com/drive/u/X/folders/Y` to set the folder to upload new files to")


@borg.on(admin_cmd(pattern="gdriveclear", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    G_DRIVE_F_PARENT_ID = None
    await mone.edit("Custom Folder ID cleared successfully.")
    await event.delete()


@borg.on(admin_cmd(pattern="gdrivedir ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        await mone.edit("This module requires credentials from https://da.gd/so63O. Aborting!")
        return
    if Config.PRIVATE_GROUP_BOT_API_ID is None:
        await event.edit("Please set the required environment variable `PRIVATE_GROUP_BOT_API_ID` for this plugin to work")
        return
    input_str = event.pattern_match.group(1)
    if os.path.isdir(input_str):
        # TODO: remove redundant code
        #
        if Config.G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(Config.G_DRIVE_AUTH_TOKEN_DATA)
        # Check if token file exists, if not create it by requesting authorization code
        storage = None
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
        http = authorize(G_DRIVE_TOKEN_FILE, storage)
        # Authorize, get file parameters, upload file and print out result URL for download
        # first, create a sub-directory
        dir_id = await create_directory(http, os.path.basename(os.path.abspath(input_str)), G_DRIVE_F_PARENT_ID)
        await DoTeskWithDir(http, input_str, mone, dir_id)
        dir_link = "https://drive.google.com/folderview?id={}".format(dir_id)
        await mone.edit(f"[Here is your Google Drive link]({dir_link})")
    else:
        await mone.edit(f"directory {input_str} does not seem to exist")


@borg.on(admin_cmd(pattern="drive (delete|get) ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        await mone.edit("This module requires credentials from https://da.gd/so63O. Aborting!")
        return
    if Config.PRIVATE_GROUP_BOT_API_ID is None:
        await event.edit("Please set the required environment variable `PRIVATE_GROUP_BOT_API_ID` for this plugin to work")
        return
    t_reqd_comd = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2).strip()
    # TODO: remove redundant code
    #
    if Config.G_DRIVE_AUTH_TOKEN_DATA is not None:
        with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
            t_file.write(Config.G_DRIVE_AUTH_TOKEN_DATA)
    # Check if token file exists, if not create it by requesting authorization code
    storage = None
    if not os.path.isfile(G_DRIVE_TOKEN_FILE):
        storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
    http = authorize(G_DRIVE_TOKEN_FILE, storage)
    # Authorize, get file parameters, upload file and print out result URL for download
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    if t_reqd_comd == "delete":
        response_from_svc = await gdrive_delete(drive_service, input_str)
    elif t_reqd_comd == "get":
        response_from_svc = await gdrive_list_file_md(drive_service, input_str)
    await mone.edit(response_from_svc)


@borg.on(admin_cmd(pattern="drive search ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        await mone.edit("This module requires credentials from https://da.gd/so63O. Aborting!")
        return
    if Config.PRIVATE_GROUP_BOT_API_ID is None:
        await event.edit("Please set the required environment variable `PRIVATE_GROUP_BOT_API_ID` for this plugin to work")
        return
    input_str = event.pattern_match.group(1).strip()
    # TODO: remove redundant code
    #
    if Config.G_DRIVE_AUTH_TOKEN_DATA is not None:
        with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
            t_file.write(Config.G_DRIVE_AUTH_TOKEN_DATA)
    # Check if token file exists, if not create it by requesting authorization code
    storage = None
    if not os.path.isfile(G_DRIVE_TOKEN_FILE):
        storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
    http = authorize(G_DRIVE_TOKEN_FILE, storage)
    # Authorize, get file parameters, upload file and print out result URL for download
    await mone.edit(f"searching for {input_str} in your gDrive ...")
    gsearch_results = await gdrive_search(http, input_str)
    await mone.edit(gsearch_results, link_preview=False, parse_mode="html")


# Get mime type and name of given file
def file_ops(file_path):
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    file_name = file_path.split("/")[-1]
    return file_name, mime_type


async def create_token_file(token_file, event):
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(
        CLIENT_ID,
        CLIENT_SECRET,
        OAUTH_SCOPE,
        redirect_uri=REDIRECT_URI
    )
    authorize_url = flow.step1_get_authorize_url()
    async with event.client.conversation(Config.PRIVATE_GROUP_BOT_API_ID) as conv:
        await conv.send_message(f"Go to the following link in your browser: {authorize_url} and reply the code")
        response = conv.wait_event(events.NewMessage(
            outgoing=True,
            chats=Config.PRIVATE_GROUP_BOT_API_ID
        ))
        response = await response
        code = response.message.message.strip()
        credentials = flow.step2_exchange(code)
        storage = Storage(token_file)
        storage.put(credentials)
        return storage


def authorize(token_file, storage):
    # Get credentials
    if storage is None:
        storage = Storage(token_file)
    credentials = storage.get()
    # Create an httplib2.Http object and authorize it with our credentials
    http = httplib2.Http()
    credentials.refresh(http)
    http = credentials.authorize(http)
    return http


async def upload_file(http, file_path, file_name, mime_type, event, parent_id):
    # Create Google Drive service instance
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    # File body description
    media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    body = {
        "title": file_name,
        "description": "Uploaded using @UniBorg gDrive v2",
        "mimeType": mime_type,
    }
    if parent_id is not None:
        body["parents"] = [{"id": parent_id}]
    # Permissions body description: anyone who has link can upload
    # Other permissions can be found at https://developers.google.com/drive/v2/reference/permissions
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True
    }
    # Insert a file
    file = drive_service.files().insert(body=body, media_body=media_body)
    response = None
    display_message = ""
    while response is None:
        status, response = file.next_chunk()
        await asyncio.sleep(1)
        if status:
            percentage = int(status.progress() * 100)
            progress_str = "[{0}{1}]\nProgress: {2}%\n".format(
                "".join(["█" for i in range(math.floor(percentage / 5))]),
                "".join(["░" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2)
            )
            current_message = f"uploading to gDrive\nFile Name: {file_name}\n{progress_str}"
            if display_message != current_message:
                try:
                    await event.edit(current_message)
                    display_message = current_message
                except Exception as e:
                    logger.info(str(e))
                    pass
    file_id = response.get("id")
    try:
        # Insert new permissions
        drive_service.permissions().insert(fileId=file_id, body=permissions).execute()
    except:
        pass
    # Define file instance and get url for download
    file = drive_service.files().get(fileId=file_id).execute()
    download_url = file.get("webContentLink")
    return download_url


async def create_directory(http, directory_name, parent_id):
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    permissions = {
        "role": "reader",
        "type": "anyone",
        "value": None,
        "withLink": True
    }
    file_metadata = {
        "title": directory_name,
        "mimeType": G_DRIVE_DIR_MIME_TYPE
    }
    if parent_id is not None:
        file_metadata["parents"] = [{"id": parent_id}]
    file = drive_service.files().insert(body=file_metadata).execute()
    file_id = file.get("id")
    try:
        drive_service.permissions().insert(fileId=file_id, body=permissions).execute()
    except:
        pass
    logger.info("Created Gdrive Folder:\nName: {}\nID: {} ".format(file.get("title"), file_id))
    return file_id


async def DoTeskWithDir(http, input_directory, event, parent_id):
    list_dirs = os.listdir(input_directory)
    if len(list_dirs) == 0:
        return parent_id
    r_p_id = None
    for a_c_f_name in list_dirs:
        current_file_name = os.path.join(input_directory, a_c_f_name)
        if os.path.isdir(current_file_name):
            current_dir_id = await create_directory(http, a_c_f_name, parent_id)
            r_p_id = await DoTeskWithDir(http, current_file_name, event, current_dir_id)
        else:
            file_name, mime_type = file_ops(current_file_name)
            # current_file_name will have the full path
            g_drive_link = await upload_file(http, current_file_name, file_name, mime_type, event, parent_id)
            r_p_id = parent_id
    # TODO: there is a #bug here :(
    return r_p_id


async def gdrive_delete(service, file_id):
    try:
        service.files().delete(fileId=file_id).execute()
        return f"successfully deleted {file_id} from my gDrive."
    except Exception as e:
        return str(e)


async def gdrive_list_file_md(service, file_id):
    try:
        file = service.files().get(fileId=file_id).execute()
        # logger.info(file)
        file_meta_data = {}
        file_meta_data["title"] = file["title"]
        mimeType = file["mimeType"]
        file_meta_data["createdDate"] = file["createdDate"]
        if mimeType == G_DRIVE_DIR_MIME_TYPE:
            # is a dir.
            file_meta_data["mimeType"] = "directory"
            file_meta_data["previewURL"] = file["alternateLink"]
        else:
            # is a file.
            file_meta_data["mimeType"] = file["mimeType"]
            file_meta_data["md5Checksum"] = file["md5Checksum"]
            file_meta_data["fileSize"] = str(humanbytes(int(file["fileSize"])))
            file_meta_data["quotaBytesUsed"] = str(humanbytes(int(file["quotaBytesUsed"])))
            file_meta_data["previewURL"] = file["downloadUrl"]
        return json.dumps(file_meta_data, sort_keys=True, indent=4)
    except Exception as e:
        return str(e)


async def gdrive_search(http, search_query):
    if G_DRIVE_F_PARENT_ID is not None:
        query = "'{}' in parents and (title contains '{}')".format(G_DRIVE_F_PARENT_ID, search_query)
    else:
        query = "title contains '{}'".format(search_query)
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    page_token = None
    msg = f"<b>G-Drive Search Query</b>: <code>{search_query}</code>\n\n<b>Results</b>\n"
    while True:
        try:
            response = drive_service.files().list(
                q=query,
                spaces="drive",
                fields="nextPageToken, items(id, title, mimeType)",
                pageToken=page_token
            ).execute()
            for file in response.get("items",[]):
                file_title = file.get("title")
                file_id = file.get("id")
                if file.get("mimeType") == G_DRIVE_DIR_MIME_TYPE:
                    msg += f"🗃️ <a href='https://drive.google.com/drive/folders/{file_id}'>{file_title}</a>"
                    msg += f" <code>{file_id}</code>\n"
                else:
                    msg += f"👉 <a href='https://drive.google.com/uc?id={file_id}&export=download'>{file_title}</a>"
                    msg += f" <code>{file_id}</code>\n"
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
        except Exception as e:
            msg += str(e)
            break
    return msg

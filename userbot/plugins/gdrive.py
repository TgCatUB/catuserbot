# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

import asyncio
import math
import os
import time
from pySmartDL import SmartDL
from telethon import events
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import ResumableUploadError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import file, client, tools
from userbot import (G_DRIVE_CLIENT_ID, G_DRIVE_CLIENT_SECRET,
                     G_DRIVE_AUTH_TOKEN_DATA, GDRIVE_FOLDER_ID, BOTLOG_CHATID,
                     TEMP_DOWNLOAD_DIRECTORY, CMD_HELP, LOGS)
from userbot.events import register
from mimetypes import guess_type
import httplib2
import subprocess
from userbot.utils import progress, humanbytes, time_formatter
from userbot.uniborgConfig import Config

# Path to token json file, it should be in same directory as script
G_DRIVE_TOKEN_FILE = "./auth_token.txt"
# Copy your credentials from the APIs Console
CLIENT_ID = G_DRIVE_CLIENT_ID
CLIENT_SECRET = G_DRIVE_CLIENT_SECRET
# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = "https://www.googleapis.com/auth/drive.file"
# Redirect URI for installed apps, can be left as is
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
# global variable to set Folder ID to upload to
parent_id = GDRIVE_FOLDER_ID
# global variable to indicate mimeType of directories in gDrive
G_DRIVE_DIR_MIME_TYPE = "application/vnd.google-apps.folder"
BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
BOTLOG = True

@register(pattern=r"^\.ugdrive(?: |$)(.*)", outgoing=True)
async def gdrive_upload_function(dryb):
    """ For .gdrive command, upload files to google drive. """
    await dryb.edit("Processing ...")
    input_str = dryb.pattern_match.group(1)
    if CLIENT_ID is None or CLIENT_SECRET is None:
        return
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
        required_file_name = None
    if "|" in input_str:
        url, file_name = input_str.split("|")
        url = url.strip()
        # https://stackoverflow.com/a/761825/4723940
        file_name = file_name.strip()
        head, tail = os.path.split(file_name)
        if head:
            if not os.path.isdir(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head)):
                os.makedirs(os.path.join(TEMP_DOWNLOAD_DIRECTORY, head))
                file_name = os.path.join(head, tail)
        downloaded_file_name = TEMP_DOWNLOAD_DIRECTORY + "" + file_name
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        display_message = None
        while not downloader.isFinished():
            status = downloader.get_status().capitalize()
            total_length = downloader.filesize if downloader.filesize else None
            downloaded = downloader.get_dl_size()
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            elapsed_time = round(diff) * 1000
            progress_str = "[{0}{1}] {2}%".format(
                ''.join(["█" for i in range(math.floor(percentage / 10))]),
                ''.join(["░"
                         for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2))
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"{status}...\
                \nURL: {url}\
                \nFile Name: {file_name}\
                \n{progress_str}\
                \n{humanbytes(downloaded)} of {humanbytes(total_length)}\
                \nETA: {estimated_total_time}"

                if round(diff %
                         10.00) == 0 and current_message != display_message:
                    await dryb.edit(current_message)
                    display_message = current_message
            except Exception as e:
                LOGS.info(str(e))
                pass
        if downloader.isSuccessful():
            await dryb.edit(
                "Downloaded to `{}` successfully !!\nInitiating Upload to Google Drive.."
                .format(downloaded_file_name))
            required_file_name = downloaded_file_name
        else:
            await dryb.edit("Incorrect URL\n{}".format(url))
    elif input_str:
        input_str = input_str.strip()
        if os.path.exists(input_str):
            required_file_name = input_str
            await dryb.edit(
                "Found `{}` in local server, Initiating Upload to Google Drive.."
                .format(input_str))
        else:
            await dryb.edit(
                "File not found in local server. Give me a valid file path !")
            return False
    elif dryb.reply_to_msg_id:
        try:
            c_time = time.time()
            downloaded_file_name = await dryb.client.download_media(
                await dryb.get_reply_message(),
                TEMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop(
                ).create_task(progress(d, t, dryb, c_time, "Downloading...")))
        except Exception as e:
            await dryb.edit(str(e))
        else:
            required_file_name = downloaded_file_name
            await dryb.edit(
                "Downloaded to `{}` Successfully !!\nInitiating Upload to Google Drive.."
                .format(downloaded_file_name))
    if required_file_name:
        if G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(G_DRIVE_AUTH_TOKEN_DATA)
        # Check if token file exists, if not create it by requesting
        # authorization code
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, dryb)
            http = authorize(G_DRIVE_TOKEN_FILE, storage)
        # Authorize, get file parameters, upload file and print out result URL
        # for download
        http = authorize(G_DRIVE_TOKEN_FILE, None)
        file_name, mime_type = file_ops(required_file_name)
        # required_file_name will have the full path
        # Sometimes API fails to retrieve starting URI, we wrap it.
        try:
            g_drive_link = await upload_file(http, required_file_name,
                                             file_name, mime_type, dryb,
                                             parent_id)
            await dryb.edit(
                f"File:`{required_file_name}`\nwas Successfully Uploaded to [Google Drive]({g_drive_link})!"
            )
        except Exception as e:
            await dryb.edit(
                f"Error while Uploading to Google Drive\nError Code:\n`{e}`")


@register(pattern=r"^\.ggd(?: |$)(.*)", outgoing=True)
async def upload_dir_to_gdrive(event):
    await event.edit("Processing ...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        return
    input_str = event.pattern_match.group(1)
    if os.path.isdir(input_str):
        # TODO: remove redundant code
        if G_DRIVE_AUTH_TOKEN_DATA is not None:
            with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
                t_file.write(G_DRIVE_AUTH_TOKEN_DATA)
        # Check if token file exists, if not create it by requesting authorization code
        storage = None
        if not os.path.isfile(G_DRIVE_TOKEN_FILE):
            storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
        http = authorize(G_DRIVE_TOKEN_FILE, storage)
        # Authorize, get file parameters, upload file and print out result URL for download
        # first, create a sub-directory
        dir_id = await create_directory(
            http, os.path.basename(os.path.abspath(input_str)), parent_id)
        await DoTeskWithDir(http, input_str, event, dir_id)
        dir_link = "https://drive.google.com/folderview?id={}".format(dir_id)
        await event.edit(f"Here is your Google Drive [link]({dir_link})")
    else:
        await event.edit(f"Directory {input_str} does not seem to exist")


@register(pattern=r"^\.list(?: |$)(.*)", outgoing=True)
async def gdrive_search_list(event):
    await event.edit("Processing ...")
    if CLIENT_ID is None or CLIENT_SECRET is None:
        return
    input_str = event.pattern_match.group(1).strip()
    # TODO: remove redundant code
    if G_DRIVE_AUTH_TOKEN_DATA is not None:
        with open(G_DRIVE_TOKEN_FILE, "w") as t_file:
            t_file.write(G_DRIVE_AUTH_TOKEN_DATA)
    # Check if token file exists, if not create it by requesting authorization code
    storage = None
    if not os.path.isfile(G_DRIVE_TOKEN_FILE):
        storage = await create_token_file(G_DRIVE_TOKEN_FILE, event)
    http = authorize(G_DRIVE_TOKEN_FILE, storage)
    # Authorize, get file parameters, upload file and print out result URL for download
    await event.edit(f"Searching for {input_str} in your Google Drive ...")
    gsearch_results = await gdrive_search(http, input_str)
    await event.edit(gsearch_results, link_preview=False)


@register(
    pattern=
    r"^\.gsetf https?://drive\.google\.com/drive/u/\d/folders/([-\w]{25,})",
    outgoing=True)
async def download(set):
    """For .gsetf command, allows you to set path"""
    await set.edit("Processing ...")
    input_str = set.pattern_match.group(1)
    if input_str:
        parent_id = input_str
        await set.edit(
            "Custom Folder ID set successfully. The next uploads will upload to {parent_id} till `.gdriveclear`"
        )
        await set.delete()
    else:
        await set.edit(
            "Use `.gdrivesp <link to GDrive Folder>` to set the folder to upload new files to."
        )


@register(pattern="^\.gsetclear$", outgoing=True)
async def download(gclr):
    """For .gsetclear command, allows you clear ur curnt custom path"""
    await gclr.reply("Processing ...")
    parent_id = GDRIVE_FOLDER_ID
    await gclr.edit("Custom Folder ID cleared successfully.")


@register(pattern="^\.gfolder$", outgoing=True)
async def show_current_gdrove_folder(event):
    if parent_id:
        folder_link = f"https://drive.google.com/drive/folders/" + parent_id
        await event.edit(
            f"My userbot is currently uploading files [here]({folder_link})")
    else:
        await event.edit(
            f"My userbot is currently uploading files to the root of my Google Drive storage.\
            \nFind uploaded files [here](https://drive.google.com/drive/my-drive)"
        )


# Get mime type and name of given file
def file_ops(file_path):
    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    file_name = file_path.split("/")[-1]
    return file_name, mime_type


async def create_token_file(token_file, event):
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID,
                               CLIENT_SECRET,
                               OAUTH_SCOPE,
                               redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    async with event.client.conversation(BOTLOG_CHATID) as conv:
        await conv.send_message(
            f"Go to the following link in your browser: {authorize_url} and reply the code"
        )
        response = conv.wait_event(
            events.NewMessage(outgoing=True, chats=BOTLOG_CHATID))
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
        "description": "Uploaded using PaperplaneExtended Userbot",
        "mimeType": mime_type,
    }
    if parent_id:
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
            progress_str = "[{0}{1}] {2}%".format(
                "".join(["█" for i in range(math.floor(percentage / 10))]),
                "".join(["░"
                         for i in range(10 - math.floor(percentage / 10))]),
                round(percentage, 2))
            current_message = f"Uploading to Google Drive\nFile Name: {file_name}\n{progress_str}"
            if display_message != current_message:
                try:
                    await event.edit(current_message)
                    display_message = current_message
                except Exception as e:
                    LOGS.info(str(e))
                    pass
    file_id = response.get("id")
    # Insert new permissions
    drive_service.permissions().insert(fileId=file_id,
                                       body=permissions).execute()
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
    if parent_id:
        file_metadata["parents"] = [{"id": parent_id}]
    file = drive_service.files().insert(body=file_metadata).execute()
    file_id = file.get("id")
    drive_service.permissions().insert(fileId=file_id,
                                       body=permissions).execute()
    LOGS.info("Created Gdrive Folder:\nName: {}\nID: {} ".format(
        file.get("title"), file_id))
    return file_id


async def DoTeskWithDir(http, input_directory, event, parent_id):
    list_dirs = os.listdir(input_directory)
    if len(list_dirs) == 0:
        return parent_id
    r_p_id = None
    for a_c_f_name in list_dirs:
        current_file_name = os.path.join(input_directory, a_c_f_name)
        if os.path.isdir(current_file_name):
            current_dir_id = await create_directory(http, a_c_f_name,
                                                    parent_id)
            r_p_id = await DoTeskWithDir(http, current_file_name, event,
                                         current_dir_id)
        else:
            file_name, mime_type = file_ops(current_file_name)
            # current_file_name will have the full path
            g_drive_link = await upload_file(http, current_file_name,
                                             file_name, mime_type, event,
                                             parent_id)
            r_p_id = parent_id
    # TODO: there is a #bug here :(
    return r_p_id


async def gdrive_list_file_md(service, file_id):
    try:
        file = service.files().get(fileId=file_id).execute()
        # LOGS.info(file)
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
            file_meta_data["quotaBytesUsed"] = str(
                humanbytes(int(file["quotaBytesUsed"])))
            file_meta_data["previewURL"] = file["downloadUrl"]
        return json.dumps(file_meta_data, sort_keys=True, indent=4)
    except Exception as e:
        return str(e)


async def gdrive_search(http, search_query):
    if parent_id:
        query = "'{}' in parents and (title contains '{}')".format(
            parent_id, search_query)
    else:
        query = "title contains '{}'".format(search_query)
    drive_service = build("drive", "v2", http=http, cache_discovery=False)
    page_token = None
    res = ""
    while True:
        try:
            response = drive_service.files().list(
                q=query,
                spaces="drive",
                fields="nextPageToken, items(id, title, mimeType)",
                pageToken=page_token).execute()
            for file in response.get("items", []):
                file_title = file.get("title")
                file_id = file.get("id")
                if file.get("mimeType") == G_DRIVE_DIR_MIME_TYPE:
                    res += f"`[FOLDER] {file_title}`\nhttps://drive.google.com/drive/folders/{file_id}\n\n"
                else:
                    res += f"`{file_title}`\nhttps://drive.google.com/uc?id={file_id}&export=download\n\n"
            page_token = response.get("nextPageToken", None)
            if page_token is None:
                break
        except Exception as e:
            res += str(e)
            break
    msg = f"**Google Drive Query**:\n`{search_query}`\n\n**Results**\n\n{res}"
    return msg


CMD_HELP.update({
    "gdrive":
    ".ugdrive <file_path / reply / URL|file_name>\
    \nUsage: Uploads the file in reply , URL or file path in server to your Google Drive.\
    \n\n.gsetf <GDrive Folder URL>\
    \nUsage: Sets the folder to upload new files to.\
    \n\n.gsetclear\
    \nUsage: Reverts to default upload destination.\
    \n\n.gfolder\
    \nUsage: Shows your current upload destination/folder.\
    \n\n.list <query>\
    \nUsage: Looks for files and folders in your Google Drive.\
    \n\n.ggd <path_to_folder_in_server>\
    \nUsage: Uploads all the files in the directory to a folder in Google Drive."
})

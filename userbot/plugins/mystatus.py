"""

Commands - .offline .online
Offline = Add an offline tag in your name and change profile pic to black.
Online = Remove Offline Tag from your name and change profile pic to vars PROFILE_IMAGE.
Note - If you have a last name remove it unless it automatically removed.
"""


import os , urllib
from telethon import events
from telethon.tl import functions
from uniborg.util import admin_cmd

OFFLINE_TAG = "[OFFLINE]"
ONLINE_TAG = "[ONLINE]"
PROFILE_IMAGE = os.environ.get("PROFILE_IMAGE", "https://telegra.ph/file/9f0638dbfa028162a8682.jpg")

@borg.on(admin_cmd(pattern="offline"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    user_it = "me"
    user = await event.client.get_entity(user_it)
    if user.first_name.startswith(OFFLINE_TAG):
        await event.edit("**Already in Offline Mode.**")
        return
    await event.edit("**Changing Profile to Offline...**")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    urllib.request.urlretrieve("https://telegra.ph/file/249f27d5b52a87babcb3f.jpg","donottouch.jpg")
    photo = "donottouch.jpg"
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await borg(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit("**Changed profile to OffLine.**")
    try:
        os.system("rm -fr donottouch.jpg")
    except Exception as e:  # pylint:disable=C0103,W0703
        logger.warn(str(e))  # pylint:disable=E0602
    last_name = ""
    first_name = OFFLINE_TAG
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            last_name=last_name,
            first_name=first_name
        ))
        result = "**`{} {}`\nI am Offline now.**".format(first_name, last_name)
        await event.edit(result)
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))

@borg.on(admin_cmd(pattern="online"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    user_it = "me"
    user = await event.client.get_entity(user_it)
    if user.first_name.startswith(OFFLINE_TAG):
        await event.edit("**Changing Profile to Online...**")
    else:
      await event.edit("**Already Online.**")
      return
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
    urllib.request.urlretrieve(PROFILE_IMAGE,"donottouch.jpg")
    photo = "donottouch.jpg"
    if photo:
        file = await event.client.upload_file(photo)
        try:
            await borg(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
        else:
            await event.edit("**Changed profile to Online.**")
    try:
        os.system("rm -fr donottouch.jpg")
    except Exception as e:  # pylint:disable=C0103,W0703
        logger.warn(str(e))  # pylint:disable=E0602
    first_name = ONLINE_TAG
    last_name = ""
    try:
        await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
            last_name=last_name,
            first_name=first_name
        ))
        result = "**`{} {}`\nI am Online !**".format(first_name, last_name)
        await event.edit(result)
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))

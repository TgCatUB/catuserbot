# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#

import os

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl import functions
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User

# ====================== CONSTANT ===============================
INVALID_MEDIA = "```The extension of the media entity is invalid.```"
PP_CHANGED = "```Profile picture changed successfully.```"
PP_TOO_SMOL = "```This image is too small, use a bigger image.```"
PP_ERROR = "```Failure occured while processing image.```"
BIO_SUCCESS = "```Successfully edited Bio.```"
NAME_OK = "```Your name was succesfully changed.```"
USERNAME_SUCCESS = "```Your username was succesfully changed.```"
USERNAME_TAKEN = "```This username is already taken.```"
# ===============================================================


@bot.on(admin_cmd(pattern="pbio (.*)"))
async def _(event):
    if event.fwd_from:
        return
    bio = event.pattern_match.group(1)
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await event.edit("Succesfully changed my profile bio")
    except Exception as e:
        await event.edit(str(e))


@bot.on(admin_cmd(pattern="pname ((.|\n)*)"))
async def _(event):
    if event.fwd_from:
        return
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if "|" in names:
        first_name, last_name = names.split("|", 1)
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await event.edit("My name was changed successfully")
    except Exception as e:
        await event.edit(str(e))


@bot.on(admin_cmd(pattern="ppic"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    await event.edit("Downloading Profile Picture to my local ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await event.client.download_media(
            reply_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await event.edit(str(e))
    else:
        if photo:
            await event.edit("now, Uploading to Telegram ...")
            if photo.endswith((".mp4", ".MP4")):
                # https://t.me/tgbetachat/324694
                size = os.stat(photo).st_size
                if size > 2097152:
                    await event.edit("size must be less than 2 mb")
                    os.remove(photo)
                    return
                catpic = None
                catvideo = await event.client.upload_file(photo)
            else:
                catpic = await event.client.upload_file(photo)
                catvideo = None
            try:
                await event.client(
                    functions.photos.UploadProfilePhotoRequest(
                        file=catpic, video=catvideo, video_start_ts=0.01
                    )
                )
            except Exception as e:
                await event.edit(str(e))
            else:
                await event.edit("My profile picture was succesfully changed")
    try:
        os.remove(photo)
    except Exception as e:
        print(str(e))


@bot.on(admin_cmd(outgoing=True, pattern="username (.*)"))
async def update_username(username):
    """For .username command, set a new username in Telegram."""
    newusername = username.pattern_match.group(1)
    try:
        await username.client(UpdateUsernameRequest(newusername))
        await username.edit(USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await username.edit(USERNAME_TAKEN)


@bot.on(admin_cmd(outgoing=True, pattern="count$"))
async def count(event):
    """For .count command, get profile stats."""
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    await event.edit("`Processing..`")
    dialogs = await event.client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            print(d)

    result += f"`Users:`\t**{u}**\n"
    result += f"`Groups:`\t**{g}**\n"
    result += f"`Super Groups:`\t**{c}**\n"
    result += f"`Channels:`\t**{bc}**\n"
    result += f"`Bots:`\t**{b}**"

    await event.edit(result)


@bot.on(admin_cmd(outgoing=True, pattern=r"delpfp"))
async def remove_profilepic(delpfp):
    """For .delpfp command, delete your current profile picture in Telegram."""
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = [
        InputPhoto(
            id=sep.id,
            access_hash=sep.access_hash,
            file_reference=sep.file_reference,
        )
        for sep in pfplist.photos
    ]
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await delpfp.edit(f"`Successfully deleted {len(input_photos)} profile picture(s).`")


@bot.on(admin_cmd(pattern="myusernames$"))
async def _(event):
    if event.fwd_from:
        return
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "".join(
        f"- {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )

    await event.edit(output_str)


CMD_HELP.update(
    {
        "profile": "**Plugin : **`profile`\
        \n\n•  **Syntax : **`.username <new_username>`\
        \n•  **Function : **__ Changes your Telegram username.__\
        \n\n•  **Syntax : **`.pname <name>`\
        \n•  **Function : **__ Changes your Telegram name.(First and last name will get split by the first space)__\
        \n\n•  **Syntax : **`.ppic`\
        \n•  **Function : **__ Reply with .setpfp or .ppic to an image to change your Telegram profie picture.__\
        \n\n•  **Syntax : **`.pbio <new_bio>`\
        \n•  **Function : **__ Changes your Telegram bio.__\
        \n\n•  **Syntax : **`.delpfp or .delpfp <number>/<all>`\
        \n•  **Function : **__ Deletes your Telegram profile picture(s).__\
        \n\n•  **Syntax : **`.myusernames`\
        \n•  **Function : **__ Shows usernames of your created channels and groups __\
        \n\n•  **Syntax : **`.count`\
        \n•  **Function : **__ Counts your groups, chats, bots etc...__"
    }
)

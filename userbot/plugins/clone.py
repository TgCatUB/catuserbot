"""Get Telegram Profile Picture and other information
and set as own profile.
Syntax: .clone @username"""
#Copy That Plugin by @ViperAdnan and @mrconfused
#Give credit if you are going to kang it.

import html
import os
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location
from userbot.utils import admin_cmd
from telethon.tl import functions
from telethon import events
from userbot.utils import admin_cmd
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import (PhotoExtInvalidError,
                                          UsernameOccupiedError)
from telethon.tl.functions.account import (UpdateProfileRequest,
                                           UpdateUsernameRequest)
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import (DeletePhotosRequest,
                                          GetUserPhotosRequest,
                                          UploadProfilePhotoRequest)
from telethon.tl.types import InputPhoto, MessageMediaPhoto, User, Chat, Channel
from userbot import bot, CMD_HELP , AUTONAME , DEFAULT_BIO , ALIVE_NAME

DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = str(DEFAULT_BIO) if DEFAULT_BIO else "sıɥʇ ǝpoɔǝp uǝɥʇ llıʇu∩ ˙ ǝɔɐds ǝʇɐʌıɹd ǝɯos ǝɯ ǝʌı⅁˙"
BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
BOTLOG = True

@borg.on(admin_cmd(pattern="clone ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    replied_user, error_i_a = await get_full_user(event)
    if replied_user is None:
        await event.edit(str(error_i_a))
        return False
    user_id = replied_user.user.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TMP_DOWNLOAD_DIRECTORY)
    # some people have weird HTML in their names
    first_name = html.escape(replied_user.user.first_name)
    # https://stackoverflow.com/a/5072031/4723940
    # some Deleted Accounts do not have first_name
    if first_name is not None:
        # some weird people (like me) have more than 4096 characters in their names
        first_name = first_name.replace("\u2060", "")
    last_name = replied_user.user.last_name
    # last_name is not Manadatory in @Telegram
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
      last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    if user_bio is not None:
        user_bio = replied_user.about
    await borg(functions.account.UpdateProfileRequest(
        first_name=first_name
    ))
    await borg(functions.account.UpdateProfileRequest(
        last_name=last_name
    ))
    await borg(functions.account.UpdateProfileRequest(
        about=user_bio
    ))
    n = 1
    pfile = await borg.upload_file(profile_pic)  # pylint:disable=E060      
    await borg(functions.photos.UploadProfilePhotoRequest(  # pylint:disable=E0602
        pfile
    ))
    await event.delete()
    await borg.send_message(
      event.chat_id,
      "**LET US BE AS ONE**",
      reply_to=reply_message
      )
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, f"#CLONED\nSuccesfulley cloned [{first_name}](tg://user?id={user_id })")
    
@borg.on(admin_cmd(pattern="revert$"))
async def _(event):
    if event.fwd_from:
        return
    name = f"{DEFAULTUSER}"
    bio = f"{DEFAULTUSERBIO}"
    n = 1
    await borg(functions.photos.DeletePhotosRequest(await event.client.get_profile_photos("me", limit= n)))    
    await borg(functions.account.UpdateProfileRequest(about=f"{bio}"))
    await borg(functions.account.UpdateProfileRequest(first_name=f"{name}"))
    await event.edit("succesfully reverted to your account back")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, f"#REVERT\nSuccesfully reverted back to your profile")
    
    
    
async def get_full_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.forward.from_id or previous_message.forward.channel_id
                )
            )
            return replied_user, None
        else:
            replied_user = await event.client(
                GetFullUserRequest(
                    previous_message.from_id
                )
            )
            return replied_user, None
    else:
        input_str = None
        try:
            input_str = event.pattern_match.group(1)
        except IndexError as e:
            return None, e
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            else:
                try:
                    user_object = await event.client.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await event.client(GetFullUserRequest(user_id))
                    return replied_user, None
                except Exception as e:
                    return None, e
        elif event.is_private:
            try:
                user_id = event.chat_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e
        else:
            try:
                user_object = await event.client.get_entity(int(input_str))
                user_id = user_object.id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user, None
            except Exception as e:
                return None, e

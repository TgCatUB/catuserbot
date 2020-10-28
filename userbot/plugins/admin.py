# Userbot module to help you manage a group

# Copyright (C) 2019 The Raphielscape Company LLC.
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

from asyncio import sleep

from telethon import functions
from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from ..utils import admin_cmd, edit_or_reply, errors_handler, sudo_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP, LOGS
from .sql_helper.mute_sql import is_muted, mute, unmute

# =================== CONSTANT ===================

PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = "`I don't have sufficient permissions! This is so sed. Alexa play despacito`"
CHAT_PP_CHANGED = "`Chat Picture Changed`"
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

# ================================================


@borg.on(admin_cmd("setgpic$"))
@borg.on(sudo_cmd(pattern="setgpic$", allow_sudo=True))
@errors_handler
async def set_group_photo(gpic):
    if not gpic.is_group:
        await edit_or_reply(gpic, "`I don't think this is a group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None
    if not admin and not creator:
        await edit_or_reply(gpic, NO_ADMIN)
        return
    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await edit_or_reply(gpic, INVALID_MEDIA)
    sandy = None
    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            await edit_or_reply(gpic, CHAT_PP_CHANGED)
            sandy = True
        except PhotoCropSizeSmallError:
            await edit_or_reply(gpic, PP_TOO_SMOL)
        except ImageProcessFailedError:
            await edit_or_reply(gpic, PP_ERROR)
        except Exception as e:
            await edit_or_reply(gpic, f"**Error : **`{str(e)}`")
        if BOTLOG and sandy:
            await gpic.client.send_message(
                BOTLOG_CHATID,
                "#GROUPPIC\n"
                f"Group profile pic changed "
                f"CHAT: {gpic.chat.title}(`{gpic.chat_id}`)",
            )


@borg.on(admin_cmd("promote(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="promote(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def promote(promt):
    chat = await promt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(promt, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    catevent = await edit_or_reply(promt, "`Promoting...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Admin"
    if not user:
        return
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await catevent.edit("`Promoted Successfully! Now gib Party`")
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)",
        )


@borg.on(admin_cmd("demote(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="demote(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def demote(dmod):
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(dmod, NO_ADMIN)
        return
    catevent = await edit_or_reply(dmod, "`Demoting...`")
    rank = "admeme"
    user = await get_user_from_event(dmod)
    user = user[0]
    if not user:
        return
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    try:
        await dmod.client(EditAdminRequest(dmod.chat_id, user.id, newrights, rank))
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    await catevent.edit("`Demoted Successfully! Betterluck next time`")
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID,
            "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)",
        )


@borg.on(admin_cmd("ban(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="ban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def ban(bon):
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(bon, NO_ADMIN)
        return
    user, reason = await get_user_from_event(bon)
    if not user:
        return
    catevent = await edit_or_reply(bon, "`Whacking the pest!`")
    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        await catevent.edit(NO_PERM)
        return
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await catevent.edit(
            "`I dont have message nuking rights! But still he is banned!`"
        )
        return
    if reason:
        await catevent.edit(f"`{str(user.id)}` is banned !!\nReason: {reason}")
    else:
        await catevent.edit(f"`{str(user.id)}` is banned !!")
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID,
            "#BAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {bon.chat.title}(`{bon.chat_id}`)",
        )


@borg.on(admin_cmd("unban(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="unban(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def nothanos(unbon):
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(unbon, NO_ADMIN)
        return
    catevent = await edit_or_reply(unbon, "`Unbanning...`")
    user = await get_user_from_event(unbon)
    user = user[0]
    if not user:
        return
    try:
        await unbon.client(EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await catevent.edit("```Unbanned Successfully. Granting another chance.```")
        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)",
            )
    except UserIdInvalidError:
        await catevent.edit("`Uh oh my unban logic broke!`")


@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@borg.on(admin_cmd("mute(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="mute(?: |$)(.*)", allow_sudo=True))
async def startmute(event):
    if event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await sleep(3)
        await event.get_reply_message()
        userid = event.chat_id
        replied_user = await event.client(GetFullUserRequest(userid))
        chat_id = event.chat_id
        if is_muted(userid, chat_id):
            return await event.edit(
                "This user is already muted in this chat ~~lmfao sed rip~~"
            )
        try:
            mute(userid, chat_id)
        except Exception as e:
            await event.edit("Error occured!\nError is " + str(e))
        else:
            await event.edit("Successfully muted that person.\n**｀-´)⊃━☆ﾟ.*･｡ﾟ **")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_MUTE\n"
                f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)",
            )
    else:
        chat = await event.get_chat()
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == bot.uid:
            return await edit_or_reply(event, "Sorry, I can't mute myself")
        if is_muted(user.id, event.chat_id):
            return await edit_or_reply(
                event, "This user is already muted in this chat ~~lmfao sed rip~~"
            )
        try:
            admin = chat.admin_rights
            creator = chat.creator
            if not admin and not creator:
                await edit_or_reply(
                    event, "`You can't mute a person without admin rights niqq.` ಥ﹏ಥ  "
                )
                return
            result = await event.client(
                functions.channels.GetParticipantRequest(
                    channel=event.chat_id, user_id=user.id
                )
            )
            try:
                if result.participant.banned_rights.send_messages:
                    return await edit_or_reply(
                        event,
                        "This user is already muted in this chat ~~lmfao sed rip~~",
                    )
            except:
                pass
            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await edit_or_reply(
                        event,
                        "`You can't mute a person if you dont have delete messages permission. ಥ﹏ಥ`",
                    )
            elif "creator" not in vars(chat):
                return await edit_or_reply(
                    event, "`You can't mute a person without admin rights niqq.` ಥ﹏ಥ  "
                )
            try:
                mute(user.id, event.chat_id)
            except Exception as e:
                return await edit_or_reply(event, "Error occured!\nError is " + str(e))
        except Exception as e:
            return await edit_or_reply(event, f"**Error : **`{str(e)}`")
        if reason:
            await edit_or_reply(
                event,
                f"{user.first_name} is muted in {event.chat.title}\n"
                f"`Reason:`{reason}",
            )
        else:
            await edit_or_reply(
                event, f"{user.first_name} is muted in {event.chat.title}"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#MUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)",
            )


@borg.on(admin_cmd("unmute(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="unmute(?: |$)(.*)", allow_sudo=True))
async def endmute(event):
    if event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await sleep(3)
        userid = event.chat_id
        replied_user = await event.client(GetFullUserRequest(userid))
        chat_id = event.chat_id
        if not is_muted(userid, chat_id):
            return await event.edit(
                "__This user is not muted in this chat__\n（ ^_^）o自自o（^_^ ）"
            )
        try:
            unmute(userid, chat_id)
        except Exception as e:
            await event.edit("Error occured!\nError is " + str(e))
        else:
            await event.edit("Successfully unmuted that person\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)",
            )
    else:
        user = await get_user_from_event(event)
        user = user[0]
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
            else:
                result = await event.client(
                    functions.channels.GetParticipantRequest(
                        channel=event.chat_id, user_id=user.id
                    )
                )
                try:
                    if result.participant.banned_rights.send_messages:
                        await event.client(
                            EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                        )
                except:
                    return await edit_or_reply(
                        event,
                        "This user can already speak freely in this chat ~~lmfao sed rip~~",
                    )
        except Exception as e:
            return await edit_or_reply(event, f"**Error : **`{str(e)}`")
        await edit_or_reply(
            event, "Successfully unmuted that person\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)",
            )


@borg.on(admin_cmd("pin($| (.*))"))
@borg.on(sudo_cmd(pattern="pin($| (.*))", allow_sudo=True))
@errors_handler
async def pin(msg):
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(msg, NO_ADMIN)
        return
    to_pin = msg.reply_to_msg_id
    if not to_pin:
        await edit_or_reply(msg, "`Reply to a message to pin it.`")
        return
    options = msg.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await edit_or_reply(msg, NO_PERM)
        return
    hmm = await edit_or_reply(msg, "`Pinned Successfully!`")
    user = await get_user_from_id(msg.from_id, msg)
    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID,
            "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}",
        )
    await sleep(3)
    try:
        await hmm.delete()
    except:
        pass


@borg.on(admin_cmd("kick(?: |$)(.*)"))
@borg.on(sudo_cmd(pattern="kick(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def kick(usr):
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(usr, NO_ADMIN)
        return
    user, reason = await get_user_from_event(usr)
    if not user:
        await edit_or_reply(usr, "`Couldn't fetch user.`")
        return
    catevent = await edit_or_reply(usr, "`Kicking...`")
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await catevent.edit(NO_PERM + f"\n{str(e)}")
        return
    if reason:
        await catevent.edit(
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}"
        )
    else:
        await catevent.edit(f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")
    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n",
        )


@borg.on(admin_cmd("iundlt$"))
@borg.on(sudo_cmd(pattern="iundlt$", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await borg.get_admin_log(event.chat_id, limit=5, edit=False, delete=True)
        deleted_msg = "Deleted message in this group:"
        for i in a:
            deleted_msg += "\n👉`{}`".format(i.old.message)
        await edit_or_reply(event, deleted_msg)
    else:
        await edit_or_reply(
            event, "`You need administrative permissions in order to do this command`"
        )
        await sleep(3)
        try:
            await event.delete()
        except:
            pass


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await event.edit("Could not fetch info of that user.")
            return None
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


CMD_HELP.update(
    {
        "admin": "**Plugin : **`admin`\
        \n\n**Syntax : **`.setgpic` <reply to image>\
        \n**Usage : **Changes the group's display picture\
        \n\n**Syntax : **`.promote` <username/reply> <custom rank (optional)>\
        \n**Usage : **Provides admin rights to the person in the chat.\
        \n\n**Syntax : **`.demote `<username/reply>\
        \n**Usage : **Revokes the person's admin permissions in the chat.\
        \n\n**Syntax : **`.ban` <username/reply> <reason (optional)>\
        \n**Usage : **Bans the person off your chat.\
        \n\n**Syntax : **`.unban` <username/reply>\
        \n**Usage : **Removes the ban from the person in the chat.\
        \n\n**Syntax : **`.mute` <username/reply> <reason (optional)>\
        \n**Usage : **Mutes the person in the chat, works on admins too.\
        \n\n**Syntax : **`.unmute` <username/reply>\
        \n**Usage : **Removes the person from the muted list.\
        \n\n**Syntax : **`.pin `<reply> or `.pin loud`\
        \n**Usage : **Pins the replied message in Group\
        \n\n**Syntax : **`.kick `<username/reply> \
        \n**Usage : **kick the person off your chat.\
        \n\n**Syntax : **`.iundlt`\
        \n**Usage : **display last 5 deleted messages in group."
    }
)

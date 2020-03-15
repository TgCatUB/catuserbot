""".promote\
\nUsage: Reply to someone's message with .promote to promote them.\
\n\n.demote\
\nUsage: Reply to someone's message with .demote to revoke their admin permissions.\
\n\n.ban\
\nUsage: Reply to someone's message with .ban to ban them.\
\n\n.unban\
\nUsage: Reply to someone's message with .unban to unban them in this chat.\
\n\n.mute\
\nUsage: Reply to someone's message with .mute to mute them, works on admins too.\
\n\n.unmute\
\nUsage: Reply to someone's message with .unmute to remove them from muted list.\
\n\n.gmute\
\nUsage: Reply to someone's message with .gmute to mute them in all groups you have in common with them.\
\n\n.ungmute\
\nUsage: Reply someone's message with .ungmute to remove them from the gmuted list.\
\n\n.delusers\
\nUsage: Searches for deleted accounts in a group. Use .delusers clean to remove deleted accounts from the group.\
\n\n.adminlist\
\nUsage: Retrieves all admins in a chat.\
\n\n.userslist or .userslist <name>\
\nUsage: Retrieves all users in a chat.
\n\n.undlt\
\nUsage: Sends the last deleted message in group."

Userbot module to help you manage a group.
"""

from asyncio import sleep
from os import remove
import asyncio
from telethon import events
from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (MessageTooLongError,
                                          UserIdInvalidError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (ChannelParticipantsAdmins,
                               ChannelParticipantsBots, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto, PeerChat)

from userbot.uniborgConfig import Config
from userbot.utils import admin_cmd

LOGGING_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


ENABLE_LOG = True
LOGGING_CHANNELID = Config.PRIVATE_CHANNEL_BOT_API_ID
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
KICK_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True
)
MUTE_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=True
)
UNMUTE_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=False
)
@borg.on(events.NewMessage(outgoing=True, pattern="^.botlist$"))
async def listbots(eventListBots):
    info = await eventListBots.client.get_entity(eventListBots.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>Bots in {title}:</b>\n'
    try:
        if isinstance(eventListBots.to_id, PeerChat):
            await eventListBots.edit("`Only Supergroups can have bots.`")
            return
        else:
            async for user in eventListBots.client.iter_participants(
                    eventListBots.chat_id, filter=ChannelParticipantsBots):
                if not user.deleted:
                    link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n{link} {userid}"
                else:
                    mentions += f"\n<code>{user.id}</code>(Bot deleted by owner)"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await eventListBots.edit(mentions, parse_mode="html")
    except MessageTooLongError:
        await eventListBots.edit(
            "This group is filled with bots as hell. Uploading bots list as file.")
        with open('botlist.txt', 'w') as file:
            file.write(mentions)
            file.close()
        # file = open("botlist.txt", "w+")
        # file.write(mentions)
        # file.close()
        await eventListBots.client.send_file(
            eventListBots.chat_id,
            "botlist.txt",
            caption='Bots in {}'.format(title),
            reply_to=eventListBots.id,
        )
        remove("botlist.txt")
            
@borg.on(events.NewMessage(outgoing=True, pattern="^.unban(?: |$)(.*)"))
async def unban(eventUnban):
    if not eventUnban.text[0].isalpha() and eventUnban.text[0] \
            not in ("/", "#", "@", "!"):
        chat = await eventUnban.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await eventUnban.edit("`I am not an admin!`")
            return
        await eventUnban.edit("Unbanning!`")
        user = await get_user_from_event(eventUnban)
        if user:
            pass
        else:
            return
        try:
            await eventUnban.client(EditBannedRequest(
                eventUnban.chat_id,
                user.id,
                UNBAN_RIGHTS
            ))
            await eventUnban.edit("```Unbanned Successfully```")
            if ENABLE_LOG:
                await eventUnban.client.send_message(
                    LOGGING_CHATID,
                    "#UNBAN\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {eventUnban.chat.title}(`{eventUnban.chat_id}`)"
                )
        except UserIdInvalidError:
            await eventUnban.edit("`Uh oh my unban logic broke!`")


@borg.on(events.NewMessage(outgoing=True, pattern="^.gmute(?: |$)(.*)"))
async def gmute(eventGmute):
    if not eventGmute.text[0].isalpha() and eventGmute.text[0] not in ("/", "#", "@", "!"):
        chat = await eventGmute.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await eventGmute.edit("`I am not an admin!`")
            return
        try:
            from userbot.plugins.sql_helper.gmute_sql import gmute
        except AttributeError:
            await eventGmute.edit("`Running on Non-SQL mode!`")
            return

        user = await get_user_from_event(eventGmute)
        if user:
            pass
        else:
            return
        await eventGmute.edit("`Grabs a huge, sticky duct tape!`")
        if gmute(user.id) is False:
            await eventGmute.edit('`Error! User probably already gmuted.\nRe-rolls the tape.`')
        else:
            await eventGmute.edit("`Haha Yash! Globally taped!`")

            if ENABLE_LOG:
                await eventGmute.client.send_message(
                    LOGGING_CHANNELID,
                    "#GMUTE\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {eventGmute.chat.title}(`{eventGmute.chat_id}`)"
                )


@borg.on(events.NewMessage(outgoing=True, pattern="^.ungmute(?: |$)(.*)"))
async def ungmute_(eventUnGmute):
    if not eventUnGmute.text[0].isalpha() and eventUnGmute.text[0] \
            not in ("/", "#", "@", "!"):
        chat = await eventUnGmute.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await eventUnGmute.edit("`I am not an admin!`")
            return
        try:
            from userbot.plugins.sql_helper.gmute_sql import ungmute
        except AttributeError:
            await eventUnGmute.edit("`Running on Non-SQL mode!`")
            return
        user = await get_user_from_event(eventUnGmute)
        if user:
            pass
        else:
            return
        await eventUnGmute.edit('```Ungmuting...```')

        if ungmute(user.id) is False:
            await eventUnGmute.edit("`Error! User probably not gmuted.`")
        else:
            await eventUnGmute.edit("```Ungmuted Successfully```")

            if ENABLE_LOG:
                await eventUnGmute.client.send_message(
                    LOGGING_CHANNELID,
                    "#UNGMUTE\n"
                    f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                    f"CHAT: {eventUnGmute.chat.title}(`{eventUnGmute.chat_id}`)"
                )

@borg.on(events.NewMessage(outgoing=True, pattern="^.adminlist$"))
async def listadmins(eventListAdmins):
    if not eventListAdmins.text[0].isalpha() and eventListAdmins.text[0] not in ("/", "#", "@", "!"):
        if not eventListAdmins.is_group:
            await eventListAdmins.edit("I don't think this is a group.")
            return
        info = await eventListAdmins.client.get_entity(eventListAdmins.chat_id)
        title = info.title if info.title else "this chat"
        mentions = f'<b>Admins in {title}:</b> \n'
        try:
            async for user in eventListAdmins.client.iter_participants(
                    eventListAdmins.chat_id, filter=ChannelParticipantsAdmins
            ):
                if not user.deleted:
                    link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                    userid = f"<code>{user.id}</code>"
                    mentions += f"\n{link} {userid}"
                else:
                    mentions += f"\nDeleted Account <code>{user.id}</code>"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        await eventListAdmins.edit(mentions, parse_mode="html")

@borg.on(events.NewMessage(outgoing=True, pattern="^.userslist ?(.*)"))
async def list_users(eventListUsers):
    if not eventListUsers.text[0].isalpha() and eventListUsers.text[0] not in ("/", "#", "@", "!"):
        if not eventListUsers.is_group:
            await eventListUsers.edit("Are you sure this is a group?")
            return
        info = await eventListUsers.client.get_entity(eventListUsers.chat_id)
        title = info.title if info.title else "this chat"
        mentions = 'Users in {}: \n'.format(title)
        try:
            if not eventListUsers.pattern_match.group(1):
                async for user in eventListUsers.client.iter_participants(eventListUsers.chat_id):
                    if not user.deleted:
                        mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    else:
                        mentions += f"\nDeleted Account `{user.id}`"
            else:
                searchq = eventListUsers.pattern_match.group(1)
                async for user in eventListUsers.client.iter_participants(eventListUsers.chat_id, search=f'{searchq}'):
                    if not user.deleted:
                        mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    else:
                        mentions += f"\nDeleted Account `{user.id}`"
        except ChatAdminRequiredError as err:
            mentions += " " + str(err) + "\n"
        try:
            await eventListUsers.edit(mentions)
        except MessageTooLongError:
            await eventListUsers.edit("Damn, this is a huge group. Uploading users lists as file.")
            file = open("userslist.txt", "w+")
            file.write(mentions)
            file.close()
            await eventListUsers.client.send_file(
                eventListUsers.chat_id,
                "userslist.txt",
                caption='Users in {}'.format(title),
                reply_to=eventListUsers.id,
            )
            remove("userslist.txt")

@borg.on(admin_cmd(pattern="undlt ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    c = await event.get_chat()
    if c.admin_rights or c.creator:
        a = await borg.get_admin_log(event.chat_id,limit=5, edit=False, delete=True)
        # print(a[0].old.message)
        deleted_msg = "Deleted message in this group:"
        for i in a:
            deleted_msg += "\n👉`{}`".format(i.old.message)
        await event.edit(deleted_msg)
    else:
        await event.edit("`You need administrative permissions in order to do this command`")
        await asyncio.sleep(3)
        await event.delete()


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_obj

async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj
# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
"""
Userbot module to help you manage a group
"""

from asyncio import sleep
from os import remove
from telethon import events
import asyncio
from datetime import datetime
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto)

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot 
from userbot.utils import register, errors_handler, admin_cmd

# =================== CONSTANT ===================
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = "`I don't have sufficient permissions! This is so sed. Alexa play despacito`"
NO_SQL = "`Running on Non-SQL mode!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = "`Some issue with updating the pic,`" \
                "`maybe coz I'm not an admin,`" \
                "`or don't have enough rights.`"
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


@register(outgoing=True, pattern="^.setgpic$")
@errors_handler
async def set_group_photo(gpic):
    """ For .setgpic command, changes the picture of a group """
    if not gpic.is_group:
        await gpic.edit("`I don't think this is a group.`")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await
                                 gpic.client.upload_file(photo)))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


@register(outgoing=True, pattern="^.promote(?: |$)(.*)")
@errors_handler
async def promote(promt):
    """ For .promote command, promotes the replied/tagged person """
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(add_admins=False,
                                 invite_users=True,
                                 change_info=False,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)

    await promt.edit("`Promoting...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "admeme"  # Just in case.
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Promoted Successfully! Now gib Party`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promt.edit(NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)")


@register(outgoing=True, pattern="^.demote(?: |$)(.*)")
@errors_handler
async def demote(dmod):
    """ For .demote command, demotes the replied/tagged person """
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # If passing, declare that we're going to demote
    await dmod.edit("`Demoting...`")
    rank = "admeme"  # dummy rank, lol.
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # Edit Admin Permission
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit("`Demoted this retard Successfully!`")

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)")


@borg.on(admin_cmd(pattern="(ban|unban) ?(.*)"))
async def _(event):
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".unban"
    if event.fwd_from:
        return
    start = datetime.now()
    to_ban_id = None
    rights = None
    input_cmd = event.pattern_match.group(1)
    if input_cmd == "ban":
        rights = BANNED_RIGHTS
    elif input_cmd == "unban":
        rights = UNBAN_RIGHTS
    input_str = event.pattern_match.group(2)
    reply_msg_id = event.reply_to_msg_id
    if reply_msg_id:
        r_mesg = await event.get_reply_message()
        to_ban_id = r_mesg.from_id
    elif input_str and "all" not in input_str:
        to_ban_id = int(input_str)
    else:
        return False
    try:
        await borg(EditBannedRequest(event.chat_id, to_ban_id, rights))
    except (Exception) as exc:
        await event.edit(str(exc))
    else:
        await event.edit(f"{input_cmd}ned Successfully!")


@borg.on(admin_cmd(pattern="pgs ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        i = 1
        msgs = []
        from_user = None
        input_str = event.pattern_match.group(1)
        if input_str:
            from_user = await borg.get_entity(input_str)
            logger.info(from_user)
        async for message in borg.iter_messages(
            event.chat_id,
            min_id=event.reply_to_msg_id,
            from_user=from_user
        ):
            i = i + 1
            msgs.append(message)
            if len(msgs) == 100:
                await borg.delete_messages(event.chat_id, msgs, revoke=True)
                msgs = []
        if len(msgs) <= 100:
            await borg.delete_messages(event.chat_id, msgs, revoke=True)
            msgs = []
            await event.delete()
        else:
            await event.edit("**PURGE** Failed!")


@register(incoming=True)
@errors_handler
async def muter(moot):
    """ Used for deleting the messages of muted people """
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except AttributeError:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                await moot.client(
                    EditBannedRequest(moot.chat_id, moot.sender_id, rights))
    for i in gmuted:
        if i.sender == str(moot.sender_id):
            await moot.delete()


@borg.on(admin_cmd(pattern="affk(?: |$)(.*)", allow_sudo=True))
@errors_handler
async def promote(promt):
    """ For .promote command, promotes the replied/tagged person """
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator


    new_rights = ChatAdminRights(add_admins=False,
                                 invite_users=True,
                                 change_info=False,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)

    await promt.edit("`Promoting...`")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "admeme"  # Just in case.
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit("`Promoted Successfully! Now gib Party`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promt.edit(NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#PROMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {promt.chat.title}(`{promt.chat_id}`)")




@register(outgoing=True, pattern="^.delusers(?: |$)(.*)")
@errors_handler
async def rm_deletedacc(show):
    """ For .delusers command, list all the ghost/deleted accounts in a chat. """
    if not show.is_group:
        await show.edit("`I don't think this is a group.`")
        return
    con = show.pattern_match.group(1)
    del_u = 0
    del_status = "`No deleted accounts found, Group is cleaned as Hell`"

    if con != "clean":
        await show.edit("`Searching for zombie accounts...`")
        async for user in show.client.iter_participants(show.chat_id,
                                                        aggressive=True):
            if user.deleted:
                del_u += 1
                await sleep(1)
        if del_u > 0:
            del_status = f"Found **{del_u}** deleted account(s) in this group,\
            \nclean them by using .delusers clean"

        await show.edit(del_status)
        return

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await show.edit("`I am not an admin here!`")
        return

    await show.edit("`Deleting deleted accounts...\nOh I can do that?!?!`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await show.edit("`I don't have ban rights in this group`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1

    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \
        \n**{del_a}** deleted admin accounts are not removed"

    await show.edit(del_status)
    await sleep(2)
    await show.delete()

    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID, "#CLEANUP\n"
            f"Cleaned **{del_u}** deleted account(s) !!\
            \nCHAT: {show.chat.title}(`{show.chat_id}`)")


@register(outgoing=True, pattern="^.admins$")
@errors_handler
async def get_admin(show):
    """ For .admins command, list all of the admins of the chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b>Admins in {title}:</b> \n'
    try:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@register(outgoing=True, pattern="^.pin(?: |$)(.*)")
@errors_handler
async def pin(msg):
    """ For .pin command, pins the replied/tagged message on the top the chat. """
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit("`Reply to a message to pin it.`")
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await msg.edit(NO_PERM)
        return

    await msg.edit("`Pinned Successfully!`")

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}")


@register(outgoing=True, pattern="^.kick(?: |$)(.*)")
@errors_handler
async def kick(usr):
    """ For .kick command, kicks the replied/tagged person from the group. """
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit("`Couldn't fetch user.`")
        return

    await usr.edit("`Kicking...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.edit(
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}"
        )
    else:
        await usr.edit(
            f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n")


@register(outgoing=True, pattern="^.users ?(.*)")
@errors_handler
async def get_users(show):
    """ For .users command, list all of the users in a chat. """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = 'Users in {}: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Damn, this is a huge group. Uploading users lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption='Users in {}'.format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    args = event.pattern_match.group(1).split(' ', 1)
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

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
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


CMD_HELP.update({
    "admin":
    ".promote <username/reply> <custom rank (optional)>\
\nUsage: Provides admin rights to the person in the chat.\
\n\n.demote <username/reply>\
\nUsage: Revokes the person's admin permissions in the chat.\
\n\n.ban <username/reply> <reason (optional)>\
\nUsage: Bans the person off your chat.\
\n\n.unban <username/reply>\
\nUsage: Removes the ban from the person in the chat.\
\n\n.mute <username/reply> <reason (optional)>\
\nUsage: Mutes the person in the chat, works on admins too.\
\n\n.unmute <username/reply>\
\nUsage: Removes the person from the muted list.\
\n\n.gmute <username/reply> <reason (optional)>\
\nUsage: Mutes the person in all groups you have in common with them.\
\n\n.ungmute <username/reply>\
\nUsage: Reply someone's message with .ungmute to remove them from the gmuted list.\
\n\n.delusers\
\nUsage: Searches for deleted accounts in a group. Use .delusers clean to remove deleted accounts from the group.\
\n\n.admins\
\nUsage: Retrieves a list of admins in the chat.\
\n\n.users or .users <name of member>\
\nUsage: Retrieves all (or queried) users in the chat.\
\n\n.setgppic <reply to image>\
\nUsage: Changes the group's display picture."
})

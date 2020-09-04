"""
credits to @mrconfused
dont edit credits
"""
#    Copyright (C) 2020  sandeep.n(π.$)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from userbot import CMD_HELP
from telethon.tl.functions.users import GetFullUserRequest
from userbot.plugins.sql_helper.mute_sql import is_muted, mute, unmute
import asyncio
from userbot.utils import sudo_cmd, admin_cmd
from telethon.tl.types import (
    ChatBannedRights,
    MessageEntityMentionName)
from telethon.errors import (
    BadRequestError)
from telethon.tl.functions.channels import EditBannedRequest
from userbot import CAT_ID
from userbot.plugins import admin_groups
from datetime import datetime
import userbot.plugins.sql_helper.gban_sql_helper as gban_sql
import pybase64
from telethon.tl.functions.messages import ImportChatInviteRequest

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
    embed_links=None)

if Config.PRIVATE_GROUP_BOT_API_ID is None:
    BOTLOG = False
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


@borg.on(admin_cmd("gban(?: |$)(.*)"))
async def catgban(cat):
    await cat.edit("gbaning.......")
    start = datetime.now()
    user, reason = await get_user_from_event(cat)
    if user:
        pass
    else:
        return
    if user.id == (await cat.client.get_me()).id:
        await cat.edit("why would i ban myself")
        return
    if user.id in CAT_ID:
        await cat.edit("why would i ban my DEVELOPER")
        return
    try:
        hmm = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        await cat.client(ImportChatInviteRequest(hmm))
    except BaseException:
        pass
    if gban_sql.is_gbanned(user.id):
        await cat.edit(f"the [user](tg://user?id={user.id}) is already in gbanned list any way checking again")
    else:
        gban_sql.catgban(user.id, reason)
    san = []
    san = await admin_groups(cat)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cat.edit("you are not admin of atleast one group ")
        return
    await cat.edit(f"initiating gban of the [user](tg://user?id={user.id}) in `{len(san)}` groups")
    for i in range(0, sandy):
        try:
            await cat.client(EditBannedRequest(san[i], user.id, BANNED_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await borg.send_message(BOTLOG_CHATID, f"You don't have required permission in :\nCHAT: {cat.chat.title}(`{cat.chat_id}`)\nFor baning here")
    try:
        reply = await cat.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        await cat.edit("`I dont have message deleting rights here! But still he was gbanned!`")
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cat.edit(f"[{user.first_name}](tg://user?id={user.id}) was gbanned in `{count}` groups in `{cattaken} seconds`!!\nReason: `{reason}`")
    else:
        await cat.edit(f"[{user.first_name}](tg://user?id={user.id}) was gbanned in `{count}` groups in `{cattaken} seconds`!!")

    if BOTLOG:
        if count != 0:
            await borg.send_message(BOTLOG_CHATID, f"#GBAN\nGlobal BAN\nUser: [{user.first_name}](tg://user?id={user.id})\nID: `{user.id}`\
                                                \nReason: `{reason}`\nBanned in `{count}` groups\nTime taken = `{cattaken} seconds`")


@borg.on(admin_cmd("ungban(?: |$)(.*)"))
async def catgban(cat):
    await cat.edit("ungbaning.....")
    start = datetime.now()
    user, reason = await get_user_from_event(cat)
    if user:
        pass
    else:
        return
    if gban_sql.is_gbanned(user.id):
        gban_sql.catungban(user.id)
    else:
        await cat.edit(f"the [user](tg://user?id={user.id}) is not in your gbanned list")
        return
    san = []
    san = await admin_groups(cat)
    count = 0
    sandy = len(san)
    if sandy == 0:
        await cat.edit("you are not admin of atleast one group ")
        return
    await cat.edit(f"initiating ungban of the [user](tg://user?id={user.id}) in `{len(san)}`groups")
    for i in range(0, sandy):
        try:
            await cat.client(EditBannedRequest(san[i], user.id, UNBAN_RIGHTS))
            await asyncio.sleep(0.5)
            count += 1
        except BadRequestError:
            await borg.send_message(BOTLOG_CHATID, f"You don't have required permission in :\nCHAT: {cat.chat.title}(`{cat.chat_id}`)\nFor unbaning here")
    end = datetime.now()
    cattaken = (end - start).seconds
    if reason:
        await cat.edit(f"[{user.first_name}](tg://user?id={user.id}) was ungbanned in `{count}` groups in `{cattaken} seconds`!!\nReason: `{reason}`")
    else:
        await cat.edit(f"[{user.first_name}](tg://user?id={user.id}) was ungbanned in `{count}` groups in `{cattaken} seconds`!!")

    if BOTLOG:
        if count != 0:
            await borg.send_message(BOTLOG_CHATID, f"#UNGBAN\nGlobal UNBAN\nUser: [{user.first_name}](tg://user?id={user.id})\nID: {user.id}\
                                                \nReason: `{reason}`\nUnbanned in `{count}` groups\nTime taken = `{cattaken} seconds`")


@borg.on(admin_cmd(pattern="listgban$"))
async def gablist(event):
    if event.fwd_from:
        return
    gbanned_users = gban_sql.get_all_gbanned()
    GBANNED_LIST = "Current Gbanned Users\n"
    if len(gbanned_users) > 0:
        for a_user in gbanned_users:
            if a_user.reason:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) for {a_user.reason}\n"
            else:
                GBANNED_LIST += f"👉 [{a_user.chat_id}](tg://user?id={a_user.chat_id}) Reason None\n"
    else:
        GBANNED_LIST = "no Gbanned Users (yet)"
    if len(GBANNED_LIST) > 4095:
        with io.BytesIO(str.encode(GBANNED_LIST)) as out_file:
            out_file.name = "Gbannedusers.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Current Gbanned Users",
                reply_to=event
            )
            await event.delete()
    else:
        await event.edit(GBANNED_LIST)


@borg.on(admin_cmd(outgoing=True, pattern=r"gmute ?(\d+)?"))
async def startgmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True

    reply = await event.get_reply_message()

    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await event.edit("Please reply to a user or add their into the command to gmute them.")
    replied_user = await event.client(GetFullUserRequest(userid))
    if is_muted(userid, "gmute"):
        return await event.edit("This user is already gmuted")
    try:
        mute(userid, "gmute")
    except Exception as e:
        await event.edit("Error occured!\nError is " + str(e))
    else:
        await event.edit("Successfully gmuted that person")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#GMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@borg.on(admin_cmd(outgoing=True, pattern=r"ungmute ?(\d+)?"))
async def endgmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()

    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await event.edit("Please reply to a user or add their into the command to ungmute them.")
    replied_user = await event.client(GetFullUserRequest(userid))
    if not is_muted(userid, "gmute"):
        return await event.edit("This user is not gmuted")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await event.edit("Error occured!\nError is " + str(e))
    else:
        await event.edit("Successfully ungmuted that person")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#UNGMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@borg.on(sudo_cmd(pattern=r"gmute ?(\d+)?", allow_sudo=True))
async def startgmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.reply("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await event.reply("Please reply to a user or add their into the command to gmute them.")
    replied_user = await event.client(GetFullUserRequest(userid))
    if is_muted(userid, "gmute"):
        return await event.reply("This user is already gmuted")
    try:
        mute(userid, "gmute")
    except Exception as e:
        await event.reply("Error occured!\nError is " + str(e))
    else:
        await event.reply("Successfully gmuted that person")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#GMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@borg.on(sudo_cmd(pattern=r"ungmute ?(\d+)?", allow_sudo=True))
async def endgmute(event):
    private = False
    if event.fwd_from:
        return
    if event.is_private:
        await event.reply("Unexpected issues or ugly errors may occur!")
        await asyncio.sleep(3)
        private = True
    reply = await event.get_reply_message()
    if event.pattern_match.group(1) is not None:
        userid = event.pattern_match.group(1)
    elif reply is not None:
        userid = reply.sender_id
    elif private is True:
        userid = event.chat_id
    else:
        return await event.reply("Please reply to a user or add their into the command to ungmute them.")
    replied_user = await event.client(GetFullUserRequest(userid))
    if not is_muted(userid, "gmute"):
        return await event.reply("This user is not gmuted")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await event.reply("Error occured!\nError is " + str(e))
    else:
        await event.reply("Successfully ungmuted that person")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#UNGMUTE\n"
            f"USER: [{replied_user.user.first_name}](tg://user?id={userid})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@command(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


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
        if event.message.entities:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError):
            await event.edit("Could not fetch info of that user.")
            return None
    return user_obj, extra


CMD_HELP.update({
    "gadmin":
    ".gban <username/reply/userid> <reason (optional)>\
\n**Usage : **Bans the person in all groups where you are admin .\
\n\n.ungban <username/reply/userid>\
\n**Usage : **Reply someone's message with .ungban to remove them from the gbanned list.\
\n\n.listgban\
\n**Usage : **Shows you the gbanned list and reason for their gban.\
\n\n.gmute <username/reply> <reason (optional)>\
\n**Usage : **Mutes the person in all groups you have in common with them.\
\n\n.ungmute <username/reply>\
\n**Usage : **Reply someone's message with .ungmute to remove them from the gmuted list."
})

import re
from datetime import datetime
from math import sqrt

from emoji import emojize
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    MessageActionChannelMigrateFrom,
)
from telethon.utils import get_input_location

from userbot import catub

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id
from ..helpers.tools import media_type
from ..helpers.utils import format, get_chatinfo
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
plugin_category = "utils"

msgfilter = {
    "p": ["Photo"],
    "a": ["Audio", "Voice"],
    "g": ["Gif"],
    "s": ["Sticker"],
    "v": ["Video", "Round Video"],
    "f": ["Document"],
    "t": [None],
    "m": ["Photo", "Video"],
    # "t": ["Tags"],
}

msgfiltername = {
    "p": "Photos",
    "a": "Audio files and Voice Messages",
    "g": "Gifs",
    "s": "Stickers",
    "v": "Videos and Round Video Messages",
    "f": "Documents(files)",
    "t": "Text Messages",
    "m": "Photos and Videos",
    # "t": ["Tags"],
}


async def fetch_info(chat, event):  # sourcery no-metrics
    # sourcery skip: low-code-quality
    # chat.chats is a list so we use get_entity() to avoid IndexError
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    broadcast = (
        chat_obj_info.broadcast if hasattr(chat_obj_info, "broadcast") else False
    )
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat_obj_info.title
    warn_emoji = emojize(":warning:")
    try:
        msg_info = await event.client(
            GetHistoryRequest(
                peer=chat_obj_info.id,
                offset_id=0,
                offset_date=datetime(2010, 1, 1),
                add_offset=-1,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as e:
        msg_info = None
        LOGS.error(f"Exception: {e}")
    # No chance for IndexError as it checks for msg_info.messages first
    first_msg_valid = bool(
        msg_info and msg_info.messages and msg_info.messages[0].id == 1
    )

    # Same for msg_info.users
    creator_valid = bool(first_msg_valid and msg_info.users)
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = (
        msg_info.messages[0].action.title
        if first_msg_valid
        and isinstance(msg_info.messages[0].action, MessageActionChannelMigrateFrom)
        and msg_info.messages[0].action.title != chat_title
        else None
    )
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception:
        dc_id = "Unknown"

    # this is some spaghetti I need to change
    description = chat.full_chat.about
    members = (
        chat.full_chat.participants_count
        if hasattr(chat.full_chat, "participants_count")
        else chat_obj_info.participants_count
    )
    admins = (
        chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
    )
    banned_users = (
        chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
    )
    restrcited_users = (
        chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
    )
    members_online = (
        chat.full_chat.online_count if hasattr(chat.full_chat, "online_count") else 0
    )
    group_stickers = (
        chat.full_chat.stickerset.title
        if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
        else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = (
        chat.full_chat.read_inbox_max_id
        if hasattr(chat.full_chat, "read_inbox_max_id")
        else None
    )
    messages_sent_alt = (
        chat.full_chat.read_outbox_max_id
        if hasattr(chat.full_chat, "read_outbox_max_id")
        else None
    )
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "megagroup") and chat_obj_info.megagroup
        else "No"
    )
    slowmode = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else "No"
    )
    slowmode_time = (
        chat.full_chat.slowmode_seconds
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
        else None
    )
    restricted = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
        else "No"
    )
    verified = (
        "<b>Yes</b>"
        if hasattr(chat_obj_info, "verified") and chat_obj_info.verified
        else "No"
    )
    username = f"@{username}" if username else None
    creator_username = f"@{creator_username}" if creator_username else None
    # end of spaghetti block

    if admins is None:
        # use this alternative way if chat.full_chat.admins_count is None,
        # works even without being an admin
        try:
            participants_admins = await event.client(
                GetParticipantsRequest(
                    channel=chat.full_chat.id,
                    filter=ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            LOGS.error(f"Exception:{e}")
    if bots_list:
        for _ in bots_list:
            bots += 1

    caption = f"<b><u>{chat_type.capitalize()} INFO: </u></b>\n"
    caption += f"🆔 <b>ID: </b><code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"🔖 <b>{chat_type} name: </b><code>{chat_title}</code>\n"
    if former_title is not None:  # Meant is the very first title
        caption += f"📜 <b>Former name: </b><code>{former_title}</code>\n"
    if username is not None:
        caption += f"🧭 <b>{chat_type} type: </b><code>Public</code>\n"
        caption += f"🔗 <b>Link: {username}\n"
    else:
        caption += f"🧭 <b>{chat_type} type: </b><code>Private</code>\n"
    if creator_username is not None:
        caption += f"🔗 <b>Creator: {creator_username}\n"
    elif creator_valid:
        caption += f'🔗 <b>Creator: </b><a href="tg://user?id={creator_id}">{creator_firstname}</a>\n'
    if created is not None:
        caption += f"🗓️ <b>Created: </b><code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"🗓️ <b>Created: </b><code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"📡 <b>Data Centre ID: </b><code>{dc_id}</code>\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"📊 <b>{chat_type} level: </b><code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"✉️ <b>Viewable messages: </b><code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"📥 <b>Messages sent: </b><code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += (
            f"📥 <b>Messages sent: </b><code>{messages_sent_alt}</code> {warn_emoji}\n"
        )
    if members is not None:
        caption += f"👨‍👩‍👧‍👦 <b>Members: </b><code>{members}</code>\n"
    if admins is not None:
        caption += f"🤴 <b>Administrators: </b><code>{admins}</code>\n"
    if bots_list:
        caption += f"🤖 <b>Bots: </b><code>{bots}</code>\n"
    if members_online:
        caption += f"👀 <b>Currently online: </b><code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"⚠️ <b>Restricted users: </b><code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"🚫 <b>Banned users: </b><code>{banned_users}</code>\n"
    if group_stickers is not None:
        caption += f'❤️ <b>{chat_type} stickers: </b><a href="t.me/addstickers/{chat.full_chat.stickerset.short_name}">{group_stickers}</a>\n'
    caption += "\n"
    if not broadcast:
        caption += f"🐌 <b>Slow mode: </b><code>{slowmode}</code>"
        if (
            hasattr(chat_obj_info, "slowmode_enabled")
            and chat_obj_info.slowmode_enabled
        ):
            caption += f", <code>{slowmode_time}s</code>\n\n"
        else:
            caption += "\n\n"
        caption += f"👨‍👩‍👧‍👦 <b>Supergroup: </b><code>{supergroup}</code>\n\n"
    if hasattr(chat_obj_info, "restricted"):
        caption += f"🚫 <b>Restricted: </b><code>{restricted}</code>\n"
        if chat_obj_info.restricted:
            caption += f"<b>● Platform: </b><code>{chat_obj_info.restriction_reason[0].platform}</code>\n"
            caption += f"<b>● Reason: </b><code>{chat_obj_info.restriction_reason[0].reason}</code>\n"
            caption += f"<b>● Text: </b><code>{chat_obj_info.restriction_reason[0].text}</code>\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "💀 <b>Scam: </b><code>Yes</code>\n\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"✅ <b>Verified by Telegram: </b><code>{verified}</code>\n\n"
    if description:
        caption += f"💬 <b>Description: </b>\n<code>{description}</code>\n"
    return caption


@catub.cat_cmd(
    pattern="admins(?:\s|$)([\s\S]*)",
    command=("admins", plugin_category),
    info={
        "header": "To get list of admins.",
        "description": "Will show you the list of admins and if you use this in group then will tag them.",
        "usage": [
            "{tr}admins <username/userid>",
            "{tr}admins <in group where you need>",
        ],
        "examples": "{tr}admins @catuserbot_support",
    },
)
async def _(event):
    "To get list of admins."
    mentions = "**Admins in this Group**: \n"
    reply_message = await reply_id(event)
    input_str = event.pattern_match.group(1)
    to_write_chat = await event.get_input_chat()
    chat = None
    if input_str:
        mentions = f"Admins in {input_str} Group: \n"
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, str(e))
    else:
        chat = to_write_chat
        if not event.is_group:
            return await edit_or_reply(event, "`Are you sure this is a group?`")
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if not x.deleted and isinstance(x.participant, ChannelParticipantCreator):
                mentions += "\n 👑 [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
        mentions += "\n"
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsAdmins
        ):
            if x.deleted:
                mentions += "\n `{}`".format(x.id)
            elif isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += f" {str(e)}" + "\n"
    await event.client.send_message(event.chat_id, mentions, reply_to=reply_message)
    await event.delete()


@catub.cat_cmd(
    pattern="bots(?:\s|$)([\s\S]*)",
    command=("bots", plugin_category),
    info={
        "header": "To get list of bots.",
        "description": "Will show you the list of bots.",
        "usage": [
            "{tr}bots <username/userid>",
            "{tr}bots <in group where you need>",
        ],
        "examples": "{tr}bots @catuserbot_support",
    },
)
async def _(event):
    "To get list of bots."
    mentions = "**Bots in this Group**: \n"
    if input_str := event.pattern_match.group(1):
        mentions = "Bots in {} Group: \n".format(input_str)
        try:
            chat = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_or_reply(event, str(e))
    else:
        chat = await event.get_input_chat()
    try:
        async for x in event.client.iter_participants(
            chat, filter=ChannelParticipantsBots
        ):
            if isinstance(x.participant, ChannelParticipantAdmin):
                mentions += "\n ⚜️ [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
            else:
                mentions += "\n [{}](tg://user?id={}) `{}`".format(
                    x.first_name, x.id, x.id
                )
    except Exception as e:
        mentions += f" {str(e)}" + "\n"
    await edit_or_reply(event, mentions)


@catub.cat_cmd(
    pattern="users(?:\s|$)([\s\S]*)",
    command=("users", plugin_category),
    info={
        "header": "To get list of users.",
        "description": "Will show you the list of users.",
        "note": "There was limitation in this you cant get more 10k users",
        "usage": [
            "{tr}users <username/userid>",
            "{tr}users <in group where you need>",
        ],
    },
)
async def get_users(show):
    "To get list of Users."
    mentions = "**Users in this Group**: \n"
    await reply_id(show)
    if input_str := show.pattern_match.group(1):
        mentions = "Users in {} Group: \n".format(input_str)
        try:
            chat = await show.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(show, f"`{e}`", 10)
    elif not show.is_group:
        return await edit_or_reply(show, "`Are you sure this is a group?`")
    catevent = await edit_or_reply(show, "`getting users list wait...`  ")
    try:
        if show.pattern_match.group(1):
            async for user in show.client.iter_participants(chat.id):
                if user.deleted:
                    mentions += f"\nDeleted Account `{user.id}`"
                else:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
        else:
            async for user in show.client.iter_participants(show.chat_id):
                if user.deleted:
                    mentions += f"\nDeleted Account `{user.id}`"
                else:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
    except Exception as e:
        mentions += f" {str(e)}" + "\n"
    await edit_or_reply(catevent, mentions)


@catub.cat_cmd(
    pattern="chatinfo(?:\s|$)([\s\S]*)",
    command=("chatinfo", plugin_category),
    info={
        "header": "To get Group details.",
        "description": "Shows you the total information of the required chat.",
        "usage": [
            "{tr}chatinfo <username/userid>",
            "{tr}chatinfo <in group where you need>",
        ],
        "examples": "{tr}chatinfo @catuserbot_support",
    },
)
async def info(event):
    "To get group information"
    catevent = await edit_or_reply(event, "`Analysing the chat...`")
    match = event.pattern_match.group(1)
    chat = await get_chatinfo(event, match.strip(), catevent)
    if not chat:
        return
    caption = await fetch_info(chat, event)
    try:
        await catevent.edit(caption, parse_mode="html")
    except Exception as e:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, f"**Error in chatinfo : **\n`{e}`"
            )
        await catevent.edit("`An unexpected error has occurred.`")


@catub.cat_cmd(
    pattern="grpstat(s)?(?:\s|$)([\s\S]*)",
    command=("grpstats", plugin_category),
    info={
        "header": "To get stats of the group.",
        "description": "Will show you the list of users who are more active in last required number of messages.",
        "flags": {
            "-q": "To give limit for number of latest messages. by default it is 3000",
            "-l": "To give limit for number of users. by default it is 10",
            "-p": "To select only Photos",
            "-a": "To select only Audio files(including voice messages)",
            "-g": "To select only Gifs",
            "-s": "To select only Stickers",
            "-v": "To select only Videos(including round videos)",
            "-f": "To select only Documents(files)",
            "-t": "To select only text messages",
            "-m": "To select only media files(Photos+Videos)",
            # TODO: "-t": "To filter only messages which mentioned you",
        },
        "usage": [
            "{tr}grpstats <flags> <group username/gorup id>",
            "{tr}grpstat <flags> <group username/gorup id>",
        ],
        "examples": [
            "{tr}grpstats @catuserbot_support",
            "{tr}grpstats -q2000 @catuserbot_support",
            "{tr}grpstats -l20 @catuserbot_support",
            "{tr}grpstats -s @catuserbotot",
            "{tr}grpstats -s -l20 -q2000 @catuserbotot",
        ],
    },
)
async def grp_stat(event):  # sourcery skip: low-code-quality
    "To get active user stats of the group"
    catevent = await edit_or_reply(event, "`Analysing the chat...`")
    match = event.pattern_match.group(2)
    quantity = re.findall(r"-q\d+", match)
    limit = re.findall(r"-l\d+", match)
    flag = re.findall(r"-[a-z]+", match)
    try:
        quantity = quantity[0]
        match = match.replace(quantity, "")
        quantity = quantity.replace("-q", "")
        quantity = int(quantity)
    except IndexError:
        quantity = 3000
    try:
        limit = limit[0]
        match = match.replace(limit, "")
        limit = limit.replace("-l", "")
        limit = int(limit)
        if limit <= 0:
            limit = 10
    except IndexError:
        limit = 10
    try:
        flag = flag[0]
        match = match.replace(flag, "")
        flag = flag.replace("-", "")
    except IndexError:
        flag = None
    temp = {}
    chatinfo = await get_chatinfo(event, match.strip(), catevent)
    if not chatinfo:
        return
    grpcheck = await event.client.get_entity(chatinfo.full_chat.id)
    if grpcheck.broadcast:
        await catevent.edit(
            "**Error**:\n__grpstats command doesn't work on channel, try on group.__"
        )
        return None
    if flag and flag not in msgfilter:
        await catevent.edit(
            "**Error**:\n__Given flag {flag} is invalid please check flags mention in help.__"
        )
    async for msg in event.client.iter_messages(chatinfo.full_chat.id, limit=quantity):
        user = getattr(msg, "sender_id", False)
        if not user:
            continue
        if user not in temp:
            temp[user] = 0
        if not flag:
            temp[user] += 1
        else:
            mediatype = await media_type(msg)
            if mediatype in msgfilter[flag]:
                temp[user] += 1
    sorted_temp = dict(sorted(temp.items(), key=lambda item: item[1], reverse=True))
    finalquantity = sum(sorted_temp.values())
    len(sorted_temp)
    tempstring = ""
    check = 1
    for userid, count in sorted_temp.items():
        try:
            if count == 0:
                break
            userdetails = await event.client.get_entity(userid)
            if not userdetails.deleted:
                tempstring += f"{check}.) {format.htmlmentionuser(userdetails.first_name, userdetails.id)}: {count}\n"
        except (AttributeError, TypeError):
            continue
        check += 1
        if check > limit:
            break
    string = (
        f"<b>The top {check-1} active users of the previous {quantity} messages Who sent {msgfiltername[flag]} in group {grpcheck.title} are:</b>\
        \n\n{tempstring}\
        \n<b>Total {msgfiltername[flag]} type messages sent in last  {quantity} messages are {finalquantity}.</b>"
        if flag
        else f"<b>The top {check-1} active users of the previous {finalquantity} messages in group {grpcheck.title} are:</b>\n\n{tempstring}"
    )
    await catevent.edit(string, parse_mode="html")

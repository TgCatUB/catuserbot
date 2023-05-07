# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import asyncio
import contextlib
import time
from datetime import datetime

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.custom import Dialog
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.types import Channel, Chat, User

from userbot import catub
from userbot.core.managers import edit_delete, edit_or_reply
from userbot.helpers import delete_conv

from ..sql_helper import global_collectionjson as sql
from . import BOTLOG, BOTLOG_CHATID

plugin_category = "utils"

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
STAT_INDICATION = "`Collecting stats, Wait man`"
CHANNELS_STR = "<b>The list of channels in which you are their are here </b>\n\n"
CHANNELS_ADMINSTR = "<b>The list of channels in which you are admin are here </b>\n\n"
CHANNELS_OWNERSTR = "<b>The list of channels in which you are owner are here </b>\n\n"
GROUPS_STR = "<b>The list of groups in which you are their are here </b>\n\n"
GROUPS_ADMINSTR = "<b>The list of groups in which you are admin are here </b>\n\n"
GROUPS_OWNERSTR = "<b>The list of groups in which you are owner are here </b>\n\n"
# =========================================================== #
#                                                             #
# =========================================================== #


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


@catub.cat_cmd(
    pattern="stat$",
    command=("stat", plugin_category),
    info={
        "header": "To get statistics of your telegram account.",
        "description": "Shows you the count of  your groups, channels, private chats...etc if no input is given.",
        "flags": {
            "p": "To show public group/channels only",
            "g": "To get list of all group you in",
            "ga": "To get list of all groups where you are admin",
            "go": "To get list of all groups where you are owner/creator.",
            "c": "To get list of all channels you in",
            "ca": "To get list of all channels where you are admin",
            "co": "To get list of all channels where you are owner/creator.",
        },
        "usage": ["{tr}stat", "{tr}stat <flag>", "{tr}pstat <flag>"],
        "examples": ["{tr}stat g", "{tr}stat ca", "{tr}pstat ca"],
    },
)
async def stats(event):  # sourcery no-metrics # sourcery skip: low-code-quality
    "To get statistics of your telegram account."
    cat = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    admingroupids = []
    broadcastchannelids = []
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
                broadcastchannelids.append(entity.id)
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
                admingroupids.append(entity.id)
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    date = str(datetime.now().strftime("%B %d, %Y, %H:%M"))
    response = f"📌 **Stats for {full_name}** \n\n"
    response += f"**Private Chats:** {private_chats} \n"
    response += f"   ★ `Users: {private_chats - bots}` \n"
    response += f"   ★ `Bots: {bots}` \n"
    response += f"**Groups:** {groups} \n"
    response += f"**Channels:** {broadcast_channels} \n"
    response += f"**Admin in Groups:** {admin_in_groups} \n"
    response += f"   ★ `Creator: {creator_in_groups}` \n"
    response += f"   ★ `Admin Rights: {admin_in_groups - creator_in_groups}` \n"
    response += f"**Admin in Channels:** {admin_in_broadcast_channels} \n"
    response += f"   ★ `Creator: {creator_in_channels}` \n"
    response += (
        f"   ★ `Admin Rights: {admin_in_broadcast_channels - creator_in_channels}` \n"
    )
    response += f"**Unread:** {unread} \n"
    response += f"**Unread Mentions:** {unread_mentions} \n\n"
    response += f"📌 __It Took:__ {stop_time:.02f}s \n"
    await cat.edit(response)
    try:
        agc = sql.get_collection("admin_list").json
    except AttributeError:
        agc = {}
    agc = {"groups": admingroupids, "channels": broadcastchannelids, "date": date}
    sql.del_collection("admin_list")
    sql.add_collection("admin_list", agc, {})
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#ADMIN_LIST\n"
            f"Admin groups list has been succesfully updated on {date}. If you want to update it again, do  `.stat` or `.adminlist`",
        )


@catub.cat_cmd(
    pattern="(|p)stat (g|ga|go|c|ca|co)$",
)
async def full_stats(event):  # sourcery no-metrics # sourcery skip: low-code-quality
    flag = event.pattern_match.group(1)
    catcmd = event.pattern_match.group(2)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    grp = []
    message = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            if flag == "":
                if catcmd == "c":
                    grp.append(
                        f"<a href = https://t.me/c/{entity.id}/1>{entity.title}</a>"
                    )
                    output = CHANNELS_STR
                if (entity.creator or entity.admin_rights) and catcmd == "ca":
                    grp.append(
                        f"<a href = https://t.me/c/{entity.id}/1>{entity.title}</a>"
                    )
                    output = CHANNELS_ADMINSTR
                if entity.creator and catcmd == "co":
                    grp.append(
                        f"<a href = https://t.me/c/{entity.id}/1>{entity.title}</a>"
                    )
                    output = CHANNELS_OWNERSTR
            elif flag == "p":
                with contextlib.suppress(AttributeError):
                    if entity.username and catcmd == "c":
                        grp.append(
                            f"<a href = https://t.me/{entity.username}>{entity.title}</a>"
                        )
                        output = CHANNELS_STR
                    if (
                        (entity.creator or entity.admin_rights) and entity.username
                    ) and catcmd == "ca":
                        grp.append(
                            f"<a href = https://t.me/{entity.username}>{entity.title}</a>"
                        )
                        output = CHANNELS_ADMINSTR
                    if (entity.creator and entity.username) and catcmd == "co":
                        grp.append(
                            f"<a href = https://t.me/{entity.username}>{entity.title}</a>"
                        )
                        output = CHANNELS_OWNERSTR
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            if flag == "":
                if catcmd == "g":
                    grp.append(
                        f"<a href = https://t.me/c/{entity.id}/1>{entity.title}</a>"
                    )
                    output = GROUPS_STR
                if (entity.creator or entity.admin_rights) and catcmd == "ga":
                    grp.append(
                        f"<a href = https://t.me/c/{entity.id}/1>{entity.title}</a>"
                    )
                    output = GROUPS_ADMINSTR
                if entity.creator and catcmd == "go":
                    grp.append(
                        f"<a href = https://t.me/c/{entity.id}/1>{entity.title}</a>"
                    )
                    output = GROUPS_OWNERSTR
            elif flag == "p":
                with contextlib.suppress(AttributeError):
                    if entity.username and catcmd == "g":
                        grp.append(
                            f"<a href = https://t.me/{entity.username}>{entity.title}</a>"
                        )
                        output = GROUPS_STR
                    if (
                        (entity.creator or entity.admin_rights) and entity.username
                    ) and catcmd == "ga":
                        grp.append(
                            f"<a href = https://t.me/{entity.username}>{entity.title}</a>"
                        )
                        output = GROUPS_ADMINSTR
                    if (entity.creator and entity.username) and catcmd == "go":
                        grp.append(
                            f"<a href = https://t.me/{entity.username}>{entity.title}</a>"
                        )
                        output = GROUPS_OWNERSTR
    for k, i in enumerate(grp, start=1):
        output += f"{k} .) {i}\n"
        if k % 99 == 0:
            message.append(output)
            output = ""
    stop_time = time.time() - start_time
    if output:
        message.append(output)
    count = len(message)
    message[count - 1] = f"{message[count-1]}\n<b>Time Taken : </b> {stop_time:.02f}s"
    await catevent.edit(message[0], parse_mode="html")
    reply_to_msg = event.id
    if count > 1:
        for i in range(1, count):
            new_event = await catub.send_message(
                event.chat_id, message[i], parse_mode="html", reply_to=reply_to_msg
            )
            reply_to_msg = new_event.id


@catub.cat_cmd(
    pattern="ustat(?:\s|$)([\s\S]*)",
    command=("ustat", plugin_category),
    info={
        "header": "To get list of public groups of repled person or mentioned person.",
        "usage": "{tr}ustat <reply/userid/username>",
    },
)
async def ustat(event):
    "To get replied user's public groups."
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        return await edit_delete(
            event,
            "`reply to  user's text message to get name/username history or give userid/username`",
        )
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await edit_delete(
                    event, "`Give userid or username to find name history`"
                )
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@BRScan_bot"
    catevent = await edit_or_reply(event, "`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            purgeflag = await conv.send_message(f"/search {uid}")
        except YouBlockedUserError:
            await catub(unblock("BRScan_bot"))
            purgeflag = await conv.send_message(f"/search {uid}")
        msg = ""
        chat_list = []
        msg_list = []
        while True:
            try:
                response = await conv.get_response(timeout=2)
            except asyncio.TimeoutError:
                break
            chat_list += response.text.splitlines()
        await event.client.send_read_acknowledge(conv.chat_id)
    await delete_conv(event, chat, purgeflag)
    if "user is not in my database" in chat_list[0]:
        return await edit_delete(catevent, "`User not found in database!`")
    rng = 5 if chat_list[4] == "" else 4
    for i in chat_list[:4]:
        msg += f"{i}\n"
    msg += "\n"
    for k, i in enumerate(chat_list[rng:], start=1):
        msg += f"**{k}. {i[2:]}**\n"
        if k % 99 == 0:
            msg_list.append(msg)
            msg = ""
    if msg:
        msg_list.append(msg)
    checker = len(msg_list)
    await catevent.edit(msg_list[0])
    reply_to_msg = event.id
    if checker > 1:
        for i in range(1, checker):
            new_event = await catub.send_message(
                event.chat_id, msg_list[i], reply_to=reply_to_msg
            )
            reply_to_msg = new_event.id

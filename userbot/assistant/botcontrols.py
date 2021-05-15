from datetime import datetime

from telethon.utils import get_display_name

from userbot import catub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import (
    add_user_to_bl,
    check_is_black_list,
    get_all_bl_users,
    rem_user_from_bl,
)
from ..sql_helper.bot_pms_sql import get_user_id
from ..sql_helper.bot_starters import get_all_starters
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)

plugin_category = "bot"
botusername = Config.TG_BOT_USERNAME


async def get_user_and_reason(event):
    id_reason = event.pattern_match.group(1)
    replied = await reply_id(event)
    user_id, reason = None, None
    if replied:
        users = get_user_id(replied)
        if users is not None:
            for usr in users:
                user_id = int(usr.chat_id)
                break
            reason = id_reason
    else:
        if id_reason:
            data = id_reason.split(maxsplit=1)
            if len(data) == 2:
                user, reason = data
            elif len(data) == 1:
                user = data[0]
            if user.isdigit():
                user_id = int(user)
            if user.startswith("@"):
                user_id = user
    return user_id, reason

#taken from https://github.com/code-rgb/USERGE-X/blob/f95766027ef95854d05e523b42cd158c2e8cdbd0/userge/plugins/bot/bot_forwards.py#L420
def progress_str(total: int, current: int) -> str:
    percentage = current * 100 / total
    prog_arg = "**Progress** : `{}%`\n" "```[{}{}]```"
    return prog_arg.format(
        percentage,
        "".join((Config.FINISHED_PROGRESS_STR for i in range(floor(percentage / 5)))),
        "".join(
            (Config.UNFINISHED_PROGRESS_STR for i in range(20 - floor(percentage / 5)))
        ),
    )

async def ban_user_from_bot(user, reason, event, reply_to):
    try:
        date = str(datetime.now().strftime("%B %d, %Y"))
        add_user_to_bl(user.id, get_display_name(user), user.username, reason, date)
    except Exception as e:
        LOGS.error(str(e))
    banned_msg = (
        f"**You have been Banned Forever from using this bot.\nReason** : {reason}"
    )
    await event.client.send_message(user.id, banned_msg)
    info = f"**#Banned_Bot_PM_User**\
            \n\n👤 {_format.mentionuser(get_display_name(user) , user.id)}\
            \n**First Name:** {user.first_name}\
            \n**User ID:** `{user.id}`\
            \n**Reason:** `{reason}`"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, info)
    return info


async def unban_user_from_bot(user, reason, event, reply_to):
    try:
        rem_user_from_bl(user.id)
    except Exception as e:
        LOGS.error(str(e))
    banned_msg = f"**You have been Unbanned from this bot. From now on you can send messages here to contact my master.**"
    if reason is not None:
        banned_msg += f"\n**Reason:** __{reason}__"
    await event.client.send_message(user.id, banned_msg)
    info = f"**#Unbanned_Bot_PM_User**\
            \n\n👤 {_format.mentionuser(get_display_name(user) , user.id)}\
            \n**First Name:** {user.first_name}\
            \n**User ID:** `{user.id}`"
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, info)
    return info


@catub.cat_cmd(
    pattern=f"bot_users$",
    command=("bot_users", plugin_category),
    info={
        "header": "To get users list who started bot.",
        "description": "To get compelete list of users who started your bot",
        "usage": "{tr}bot_users",
    },
)
async def ban_starters(event):
    "To get list of users who started bot."
    list = get_all_starters()
    if len(list) == 0:
        return await edit_delete(event, "`No one started your bot yet.`")
    msg = "**The list of users who started your bot are :\n\n**"
    for user in list:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.user_id)}\n**ID:** `{user.user_id}`\n**UserName:** @{user.username}\n**Date: **__{user.date}__\n\n"
    await edit_or_reply(event, msg)


@catub.bot_cmd(
    pattern=f"^/ban\s+(.*)",
    from_users=Config.OWNER_ID,
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "`I can't find user to ban`", reply_to=reply_to
        )
    if not reason:
        return await event.client.send_message(
            event.chat_id, "`To ban the user provide reason first`", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**Error:**\n`{str(e)}`")
    if user_id == Config.OWNER_ID:
        return await event.reply("I can't ban you master")
    check = check_is_black_list(user.id)
    if check:
        return await event.client.send_message(
            event.chat_id,
            f"#Already_banned\
            \nUser already exists in my Banned Users list.\
            \n**Reason For Bot BAN:** `{check.reason}`\
            \n**Date:** `{check.date}`.",
        )
    msg = await ban_user_from_bot(user, reason, event, reply_to)
    await event.reply(msg)


@catub.bot_cmd(
    pattern=f"^/unban(?: |$)(.*)",
    from_users=Config.OWNER_ID,
)
async def ban_botpms(event):
    user_id, reason = await get_user_and_reason(event)
    reply_to = await reply_id(event)
    if not user_id:
        return await event.client.send_message(
            event.chat_id, "`I can't find user to unban`", reply_to=reply_to
        )
    try:
        user = await event.client.get_entity(user_id)
        user_id = user.id
    except Exception as e:
        return await event.reply(f"**Error:**\n`{str(e)}`")
    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"#User_Not_Banned\
            \n👤 {_format.mentionuser(user.first_name , user.id)} doesn't exist in my Banned Users list.",
        )
    msg = await unban_user_from_bot(user, reason, event, reply_to)
    await event.reply(msg)


@catub.cat_cmd(
    pattern=f"bblist$",
    command=("bblist", plugin_category),
    info={
        "header": "To get users list who are banned in bot.",
        "description": "To get list of users who are banned in bot.",
        "usage": "{tr}bblist",
    },
)
async def ban_starters(event):
    "To get list of users who are banned in bot."
    list = get_all_bl_users()
    if len(list) == 0:
        return await edit_delete(event, "`No one are banned in your bot yet.`")
    msg = "**The list of users who are banned in your bot are :\n\n**"
    for user in list:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.chat_id)}\n**ID:** `{user.chat_id}`\n**UserName:** @{user.username}\n**Date: **__{user.date}__\n**Reason:** __{user.reason}__\n\n"
    await edit_or_reply(event, msg)

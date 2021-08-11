import asyncio
from datetime import datetime

from telethon.errors import BadRequestError, FloodWaitError, ForbiddenError

from userbot import catub

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import reply_id, time_formatter
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list, get_all_bl_users
from ..sql_helper.bot_starters import del_starter_from_db, get_all_starters
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import (
    ban_user_from_bot,
    get_user_and_reason,
    progress_str,
    unban_user_from_bot,
)

LOGS = logging.getLogger(__name__)

plugin_category = "bot"
botusername = Config.TG_BOT_USERNAME
cmhd = Config.COMMAND_HAND_LER


@catub.bot_cmd(pattern="^/help$", from_users=Config.OWNER_ID)
async def bot_help(event):
    await event.reply(
        f"""The commands in the bot are:
**Note : **__This commands work only in this bot__ {botusername}

• **Cmd : **/uinfo <reply to user message>
• **Info : **__You have noticed that forwarded stickers/emoji doesn't have forward tag so you can identify the user who sent thoose messages by this cmd.__
• **Note : **__It works for all forwarded messages. even for users who's permission forward message nobody.__

• **Cmd : **/ban <reason> or /ban <username/userid> <reason>
• **Info : **__Reply to a user message with reason so he will be notified as you banned from the bot and his messages will not be forworded to you further.__
• **Note : **__Reason is must. without reason it won't work. __

• **Cmd : **/unban <reason(optional)> or /unban <username/userid>
• **Info : **__Reply to user message or provide username/userid to unban from the bot.__
• **Note : **__To check banned users list use__ `{cmhd}bblist`.

• **Cmd : **/broadcast
• **Info : **__Reply to a message to get broadcasted to every user who started your bot. To get list of users use__ `{cmhd}bot_users`.
• **Note : **__if user stoped/blocked the bot then he will be removed from your database that is he will erased from the bot_starters list.__
"""
    )


@catub.bot_cmd(pattern="^/broadcast$", from_users=Config.OWNER_ID)
async def bot_broadcast(event):
    replied = await event.get_reply_message()
    if not replied:
        return await event.reply("Reply to a message for Broadcasting First !")
    start_ = datetime.now()
    br_cast = await replied.reply("Broadcasting ...")
    blocked_users = []
    count = 0
    bot_users_count = len(get_all_starters())
    if bot_users_count == 0:
        return await event.reply("`No one started your bot yet.`")
    users = get_all_starters()
    if users is None:
        return await event.reply("`Errors ocured while fetching users list.`")
    for user in users:
        try:
            await event.client.send_message(
                int(user.user_id), "🔊 You received a **new** Broadcast."
            )
            await event.client.send_message(int(user.user_id), replied)
            await asyncio.sleep(0.8)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
        except (BadRequestError, ValueError, ForbiddenError):
            del_starter_from_db(int(user.user_id))
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID, f"**Error while broadcasting**\n`{e}`"
                )

        else:
            count += 1
            if count % 5 == 0:
                try:
                    prog_ = (
                        "🔊 Broadcasting ...\n\n"
                        + progress_str(
                            total=bot_users_count,
                            current=count + len(blocked_users),
                        )
                        + f"\n\n• ✔️ **Success** :  `{count}`\n"
                        + f"• ✖️ **Failed** :  `{len(blocked_users)}`"
                    )
                    await br_cast.edit(prog_)
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
    end_ = datetime.now()
    b_info = f"🔊  Successfully broadcasted message to ➜  <b>{count} users.</b>"
    if len(blocked_users) != 0:
        b_info += f"\n🚫  <b>{len(blocked_users)} users</b> blocked your bot recently, so have been removed."
    b_info += (
        f"\n⏳  <code>Process took: {time_formatter((end_ - start_).seconds)}</code>."
    )
    await br_cast.edit(b_info, parse_mode="html")


@catub.cat_cmd(
    pattern="bot_users$",
    command=("bot_users", plugin_category),
    info={
        "header": "To get users list who started bot.",
        "description": "To get compelete list of users who started your bot",
        "usage": "{tr}bot_users",
    },
)
async def ban_starters(event):
    "To get list of users who started bot."
    ulist = get_all_starters()
    if len(ulist) == 0:
        return await edit_delete(event, "`No one started your bot yet.`")
    msg = "**The list of users who started your bot are :\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.user_id)}\n**ID:** `{user.user_id}`\n**UserName:** @{user.username}\n**Date: **__{user.date}__\n\n"
    await edit_or_reply(event, msg)


@catub.bot_cmd(pattern="^/ban\\s+([\\s\\S]*)", from_users=Config.OWNER_ID)
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
        return await event.reply(f"**Error:**\n`{e}`")
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
    msg = await ban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@catub.bot_cmd(pattern="^/unban(?:\\s|$)([\\s\\S]*)", from_users=Config.OWNER_ID)
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
        return await event.reply(f"**Error:**\n`{e}`")
    check = check_is_black_list(user.id)
    if not check:
        return await event.client.send_message(
            event.chat_id,
            f"#User_Not_Banned\
            \n👤 {_format.mentionuser(user.first_name , user.id)} doesn't exist in my Banned Users list.",
        )
    msg = await unban_user_from_bot(user, reason, reply_to)
    await event.reply(msg)


@catub.cat_cmd(
    pattern="bblist$",
    command=("bblist", plugin_category),
    info={
        "header": "To get users list who are banned in bot.",
        "description": "To get list of users who are banned in bot.",
        "usage": "{tr}bblist",
    },
)
async def ban_starters(event):
    "To get list of users who are banned in bot."
    ulist = get_all_bl_users()
    if len(ulist) == 0:
        return await edit_delete(event, "`No one is banned in your bot yet.`")
    msg = "**The list of users who are banned in your bot are :\n\n**"
    for user in ulist:
        msg += f"• 👤 {_format.mentionuser(user.first_name , user.chat_id)}\n**ID:** `{user.chat_id}`\n**UserName:** @{user.username}\n**Date: **__{user.date}__\n**Reason:** __{user.reason}__\n\n"
    await edit_or_reply(event, msg)


@catub.cat_cmd(
    pattern="bot_antif (on|off)$",
    command=("bot_antif", plugin_category),
    info={
        "header": "To enable or disable bot antiflood.",
        "description": "if it was turned on then after 10 messages or 10 edits of same messages in less time then your bot auto loacks them.",
        "usage": [
            "{tr}bot_antif on",
            "{tr}bot_antif off",
        ],
    },
)
async def ban_antiflood(event):
    "To enable or disable bot antiflood."
    input_str = event.pattern_match.group(1)
    if input_str == "on":
        if gvarstatus("bot_antif") is not None:
            return await edit_delete(event, "`Bot Antiflood was already enabled.`")
        addgvar("bot_antif", True)
        await edit_delete(event, "`Bot Antiflood Enabled.`")
    elif input_str == "off":
        if gvarstatus("bot_antif") is None:
            return await edit_delete(event, "`Bot Antiflood was already disabled.`")
        delgvar("bot_antif")
        await edit_delete(event, "`Bot Antiflood Disabled.`")

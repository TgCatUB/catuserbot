import asyncio
from collections import defaultdict
from datetime import datetime
from typing import Optional, Union
import re
from telethon import Button, events
from telethon.events import CallbackQuery
from telethon.utils import get_display_name

from userbot import Config, catub

from ..core import check_owner, pool
from ..core.logger import logging
from ..core.session import tgbot
from ..helpers import reply_id
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list
from ..sql_helper.bot_pms_sql import (
    add_user_to_db,
    get_user_id,
    get_user_logging,
    get_user_reply,
)
from ..sql_helper.bot_starters import add_starter_to_db, get_starter_details
from . import BOTLOG, BOTLOG_CHATID
from .botcontrols import ban_user_from_bot

LOGS = logging.getLogger(__name__)

plugin_category = "bot"
botusername = Config.TG_BOT_USERNAME


async def check_bot_started_users(user, event):
    if user.id == Config.OWNER_ID:
        return
    check = get_starter_details(user.id)
    if check is None:
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        notification = f"👤 {_format.mentionuser(user.first_name , user.id)} has started me.\
                \n**ID: **`{user.id}`\
                \n**Name: **{get_display_name(user)}"
    else:
        start_date = check.date
        notification = f"👤 {_format.mentionuser(user.first_name , user.id)} has restarted me.\
                \n**ID: **`{user.id}`\
                \n**Name: **{get_display_name(user)}"
    try:
        add_starter_to_db(user.id, get_display_name(user), start_date, user.username)
    except Exception as e:
        LOGS.error(str(e))
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, notification)


@catub.bot_cmd(
    pattern=f"^/start({botusername})?([\s]+)?$",
    incoming=True,
    func=lambda e: e.is_private,
)
async def bot_start(event):
    chat = await event.get_chat()
    user = await catub.get_me()
    if check_is_black_list(chat.id):
        return
    reply_to = await reply_id(event)
    if chat.id != Config.OWNER_ID:
        start_msg = f"Hey! 👤{_format.mentionuser(chat.first_name , chat.id)},\
                    \nI am {_format.mentionuser(user.first_name , user.id)}'s assistant bot.\
                    \nYou can contact to my master from here.\
                    \n\nPowered by [Catuserbot](https://t.me/catuserbot17)"
        buttons = [
            (
                Button.url("Repo", "https://github.com/sandy1709/catuserbot"),
                Button.url(
                    "Deploy",
                    "https://dashboard.heroku.com/new?button-url=https%3A%2F%2Fgithub.com%2FMr-confused%2Fcatpack&template=https%3A%2F%2Fgithub.com%2FMr-confused%2Fcatpack",
                ),
            )
        ]
    else:
        start_msg = "Hey Master!\
            \nHow can i help you ?"
        buttons = None
    try:
        await event.client.send_message(
            chat.id,
            start_msg,
            link_preview=False,
            buttons=buttons,
            reply_to=reply_to,
        )
    except Exception as e:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"**Error**\nThere was a error while user starting your bot.\
                \n`{str(e)}`",
            )
    else:
        await check_bot_started_users(chat, event)


@catub.bot_cmd(incoming=True, func=lambda e: e.is_private)
async def bot_pms(event):  # sourcery no-metrics
    chat = await event.get_chat()
    if check_is_black_list(chat.id):
        return
    if chat.id != Config.OWNER_ID:
        msg = await event.forward_to(Config.OWNER_ID)
        try:
            add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"**Error**\nWhile storing messages details in database\n`{str(e)}`",
                )
    else:
        if event.text.startswith("/"):
            return
        reply_to = await reply_id(event)
        if reply_to is None:
            return
        users = get_user_id(reply_to)
        if users is None:
            return
        for usr in users:
            user_id = int(usr.chat_id)
            reply_msg = usr.reply_id
            user_name = usr.first_name
            break
        if user_id is not None:
            try:
                if event.media:
                    msg = await event.client.send_file(
                        user_id, event.media, caption=event.text, reply_to=reply_msg
                    )
                else:
                    msg = await event.client.send_message(
                        user_id, event.text, reply_to=reply_msg
                    )
            except Exception as e:
                await event.reply(f"**Error:**\n`{str(e)}`")
            try:
                add_user_to_db(
                    reply_to, user_name, user_id, reply_msg, event.id, msg.id
                )
            except Exception as e:
                LOGS.error(str(e))
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"**Error**\nWhile storing messages details in database\n`{str(e)}`",
                    )


@catub.bot_cmd(edited=True)
async def bot_pms_edit(event):  # sourcery no-metrics
    chat = await event.get_chat()
    if check_is_black_list(chat.id):
        return
    if chat.id != Config.OWNER_ID:
        users = get_user_reply(event.id)
        if users is None:
            return
        for user in users:
            if user.chat_id == str(chat.id):
                reply_msg = user.message_id
                break
        if reply_msg:
            await event.client.send_message(
                Config.OWNER_ID,
                f"⬆️ **This message was edited by the user** {_format.mentionuser(get_display_name(chat) , chat.id)} as :",
                reply_to=reply_msg,
            )
            msg = await event.forward_to(Config.OWNER_ID)
            try:
                add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
            except Exception as e:
                LOGS.error(str(e))
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"**Error**\nWhile storing messages details in database\n`{str(e)}`",
                    )
    else:
        reply_to = await reply_id(event)
        if reply_to is not None:
            users = get_user_id(reply_to)
            result_id = 0
            for usr in users:
                if event.id == usr.logger_id:
                    user_id = int(usr.chat_id)
                    reply_msg = usr.reply_id
                    result_id = usr.result_id
                    break
            if result_id != 0:
                try:
                    await event.client.edit_message(
                        user_id, result_id, event.text, file=event.media
                    )
                except Exception as e:
                    LOGS.error(str(e))


@tgbot.on(events.MessageDeleted)
async def handler(event):
    for msg_id in event.deleted_ids:
        users_1 = get_user_reply(msg_id)
        users_2 = get_user_logging(msg_id)
        if users_2 is not None:
            result_id = 0
            for usr in users_2:
                if msg_id == usr.logger_id:
                    user_id = int(usr.chat_id)
                    result_id = usr.result_id
                    break
            if result_id != 0:
                try:
                    await event.client.delete_messages(user_id, result_id)
                except Exception as e:
                    LOGS.error(str(e))
        if users_1 is not None:
            for user in users_1:
                if user.chat_id != Config.OWNER_ID:
                    reply_msg = user.message_id
                    break
            try:
                users = get_user_id(reply_msg)
                for usr in users:
                    user_id = int(usr.chat_id)
                    user_name = usr.first_name
                    break
                if check_is_black_list(user_id):
                    return
                if reply_msg:
                    await event.client.send_message(
                        Config.OWNER_ID,
                        f"⬆️ **This message was deleted by the user** {_format.mentionuser(user_name , user_id)}.",
                        reply_to=reply_msg,
                    )
            except Exception as e:
                LOGS.error(str(e))


@catub.bot_cmd(
    pattern=f"^/uinfo$",
    from_users=Config.OWNER_ID,
)
async def bot_start(event):
    reply_to = await reply_id(event)
    if not reply_to:
        return await event.reply("Reply to a message to get message info")
    info_msg = await event.client.send_message(
        event.chat_id,
        "`🔎 Searching for this user in my database ...`",
        reply_to=reply_to,
    )
    users = get_user_id(reply_to)
    if users is None:
        return await info_msg.edit(
            "**ERROR:** \n`Sorry !, Can't Find this user in my database :(`"
        )
    for usr in users:
        user_id = int(usr.chat_id)
        user_name = usr.first_name
        break
    if user_id is None:
        return await info_msg.edit(
            "**ERROR:** \n`Sorry !, Can't Find this user in my database :(`"
        )
    uinfo = f"This message was sent by 👤 {_format.mentionuser(user_name , user_id)}\
            \n**First Name:** {user_name}\
            \n**User ID:** `{user_id}`"
    await info_msg.edit(uinfo)


class FloodConfig:
    BANNED_USERS = {}
    USERS = defaultdict(list)
    MESSAGES = 3
    SECONDS = 6
    OWNER = [Config.OWNER_ID]
    ALERT = defaultdict(dict)
    AUTOBAN = 10


async def send_flood_alert(user_) -> None:
    # sourcery no-metrics
    buttons = [
        (
            Button.inline("🚫  BAN", data=f"bot_pm_ban_{user_.id}"),
            Buttton.inline(
                "➖ Bot Antiflood [OFF]",
                data="toggle_bot-antiflood_off",
            ),
        )
    ]
    found = False
    if FloodConfig.ALERT and (user_.id in FloodConfig.ALERT.keys()):
        found = True
        FloodConfig.ALERT[user_.id]["count"] += 1
        flood_count = FloodConfig.ALERT[user_.id]["count"]
    else:
        flood_count = FloodConfig.ALERT[user_.id]["count"] = 1

    flood_msg = (
        r"⚠️ <b>\\#Flood_Warning//</b>"
        "\n\n"
        f"  ID: <code>{user_.id}</code>\n"
        f"  Name: {user_.flname}\n"
        f"  👤 User: {user_.mention}"
        f"\n\n**Is spamming your bot !** ->  [ Flood rate **({flood_count})** ]\n"
        "__Quick Action__: Ignored from bot for a while."
    )

    if found:
        if flood_count >= FloodConfig.AUTOBAN:
            if user_.id in Config.SUDO_USERS:
                sudo_spam = (
                    f"**Sudo User** {_format.mentionuser(user_.first_name , user_.id)}:\n  ID: {user_.id}\n\n"
                    "Is Flooding your bot !, Check `.help delsudo` to remove the user from Sudo."
                )
                if BOTLOG:
                    await catub.tgbot.send_message(BOTLOG_CHATID, sudo_spam)
            else:
                await ban_user_from_bot(
                    user_,
                    f"Automated Ban for Flooding bot [exceeded flood rate of **({FloodConfig.AUTOBAN})**]",
                )
                FloodConfig.USERS[user_.id].clear()
                FloodConfig.ALERT[user_.id].clear()
                FloodConfig.BANNED_USERS.remove(user_.id)
            return
        fa_id = FloodConfig.ALERT[user_.id].get("fa_id")
        if not fa_id:
            return
        try:
            msg_ = await catub.tgbot.get_messages(Config.BOTLOG_CHATID, fa_id)
            if msg_.text != flood_msg:
                await msg_.edit(flood_msg, reply_markup=buttons)
        except Exception as fa_id_err:
            LOGS.debug(fa_id_err)
            return
    else:
        if BOTLOG:
            fa_msg = await catub.tgbot.send_message(
                Config.BOTLOG_CHATID,
                flood_msg,
                reply_markup=buttons,
            )
        try:
            await catub.tgbot.send_message(
                Config.OWNER_ID,
                f"⚠️  **[Bot Flood Warning !]({fa_msg.link})**",
            )
        except UserIsBlocked:
            if BOTLOG:
                await catub.tgbot.send_message(
                    Config.BOTLOG_CHATID, "**Unblock your bot !**"
                )
    if FloodConfig.ALERT[user_.id].get("fa_id") is None and fa_msg:
        FloodConfig.ALERT[user_.id]["fa_id"] = fa_msg.message_id


@catub.tgbot.on(CallbackQuery(data=re.compile(b"bot_pm_ban_([0-9]+)")))
@check_owner
async def bot_pm_ban_cb(c_q: CallbackQuery):
    user_id = int(c_q.pattern_match.group(1))
    try:
        user = await catub.get_entity(user_id)
    except Exception as e:
        await c_q.answer(f"Error:\n{str(e)}")
    else:
        await asyncio.gather(
            c_q.answer(f"Banning UserID -> {user_id} ...", show_alert=False),
            ban_user_from_bot(user, "Spamming Bot"),
            c_q.edit(f"✅ **Successfully Banned**  User ID: {user_id}"),
        )


def time_now() -> Union[float, int]:
    return datetime.timestamp(datetime.now())


@pool.run_in_thread
def is_flood(uid: int) -> Optional[bool]:
    """Checks if a user is flooding"""
    FloodConfig.USERS[uid].append(time_now())
    if (
        len(
            list(
                filter(
                    lambda x: time_now() - int(x) < FloodConfig.SECONDS,
                    FloodConfig.USERS[uid],
                )
            )
        )
        > FloodConfig.MESSAGES
    ):
        FloodConfig.USERS[uid] = list(
            filter(
                lambda x: time_now() - int(x) < FloodConfig.SECONDS,
                FloodConfig.USERS[uid],
            )
        )
        return True


@catub.tgbot.on(CallbackQuery(data=re.compile(b"toggle_bot-antiflood_off$")))
@check_owner
async def settings_toggle(c_q: CallbackQuery):
    Config.BOT_ANTIFLOOD = False
    await asyncio.gather(
        c_q.answer(),
        c_q.edit_message_text("BOT_ANTIFLOOD is now disabled !"),
    )


@catub.bot_cmd(incoming=True, func=lambda e: e.is_private)
async def antif_on_msg(event):
    chat = await event.get_chat()
    if chat.id == Config.OWNER_ID:
        return
    user_id = chat.id
    if check_is_black_list(user_id):
        await event.stop_propagation()
    elif await is_flood(user_id):
        await send_flood_alert(chat)
        FloodConfig.BANNED_USERS.add(user_id)
        await msg.stop_propagation()
    elif user_id in FloodConfig.BANNED_USERS:
        FloodConfig.BANNED_USERS.remove(user_id)

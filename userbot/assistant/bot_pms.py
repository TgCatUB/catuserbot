from datetime import datetime

from telethon import Button
from telethon.utils import get_display_name

from userbot import UPSTREAM_REPO_URL, catub
from userbot.core.logger import logging

from ..Config import Config
from ..helpers import reply_id
from ..helpers.utils import _format
from ..sql_helper.bot_pms_sql import (
    add_user_to_db,
    get_user_id,
    get_user_name,
    get_user_reply,
)
from ..sql_helper.bot_starters import add_starter_to_db, get_starter_details
from . import BOTLOG, BOTLOG_CHATID

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
                \n**ID: **{user.id}\
                \n**Name: **{get_display_name(user)}"
    else:
        start_date = check.date
        notification = f"👤 {_format.mentionuser(user.first_name , user.id)} has restarted me.\
                \n**ID: **{user.id}\
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
    reply_to = await reply_id(event)
    if chat.id != Config.OWNER_ID:
        start_msg = f"Hey! 👤{_format.mentionuser(chat.first_name , chat.id)},\
                    \nI am {_format.mentionuser(user.first_name , user.id)}'s assistant bot.\
                    \nYou can contact to my master from here.\
                    \n\nPowered by [Catuserbot](https://t.me/catuserbot17)"
        buttons = [
            (
                Button.url("Repo", UPSTREAM_REPO_URL),
                Button.url("Deploy", "https://github.com/Mr-confused/catpack"),
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
async def bot_pms(event):
    if event.text.startswith("/start"):
        return
    chat = await event.get_chat()
    if chat.id != Config.OWNER_ID:
        msg = await event.forward_to(Config.OWNER_ID)
        try:
            add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0)
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"**Error**\nWhile storing messages details in database\n`{str(e)}`",
                )
    else:
        reply_to = await reply_id(event)
        if reply_to is None:
            return
        user_id, reply_msg, result_id = get_user_id(reply_to)
        user_id, user_name = get_user_name(reply_to)
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
                add_user_to_db(reply_to, user_name, user_id, reply_msg, msg.id)
            except Exception as e:
                LOGS.error(str(e))
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"**Error**\nWhile storing messages details in database\n`{str(e)}`",
                    )


@catub.bot_cmd(edited=True)
async def bot_pms_edit(event):
    chat = await event.get_chat()
    if chat.id != Config.OWNER_ID:
        users = get_user_reply(event.id)
        if users is None:
            return
        for user in users:
            if user.chat_id == str(chat.id):
                reply_msg = user.reply_id
                break
        if reply_msg:
            await event.client.send_message(
                Config.OWNER_ID,
                f"⬆️ This message was edited by the user {get_display_name(chat)} as :",
                reply_to = reply_msg
            )
            msg = await event.forward_to(Config.OWNER_ID)
            try:
                add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0)
            except Exception as e:
                LOGS.error(str(e))
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"**Error**\nWhile storing messages details in database\n`{str(e)}`",
                    )
    else:
        reply_to = await reply_id(event)
        if reply_to is None:
            return
        user_id, reply_msg, result_id = get_user_id(reply_to)
        if user_id is not None and result_id != 0:
            try:
                await event.client.edit_message(
                    user_id, result_id, event.text, file=event.media
                )
            except Exception as e:
                LOGS.error(str(e))

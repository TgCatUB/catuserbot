#    Haruka Aya (A telegram bot project)
#    Copyright (C) 2017-2019 Paul Larsen
#    Copyright (C) 2019-2020 Akito Mizukito (Haruka Network Development)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import html
from typing import List

from telegram import Update, Bot
from telegram.error import BadRequest
from telegram.ext import Filters
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import mention_html
from telegram import ParseMode

from haruka import dispatcher, LOGGER, SUDO_USERS
from haruka.modules.helper_funcs.chat_status import bot_admin, user_admin, is_user_admin, can_restrict, is_user_ban_protected
from haruka.modules.helper_funcs.extraction import extract_user, extract_user_and_text
from haruka.modules.helper_funcs.string_handling import extract_time
from haruka.modules.log_channel import loggable

from haruka.modules.tr_engine.strings import tld
from haruka.modules.connection import connected
from haruka.modules.disable import DisableAbleCommandHandler


@run_async
@bot_admin
@user_admin
@loggable
def mute(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    conn = connected(bot, update, chat, user.id)
    if conn:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            return
        else:
            chatD = chat

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "mute_invalid"))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "mute_not_myself"))
        return ""

    member = chatD.get_member(int(user_id))

    if member:

        if user_id in SUDO_USERS:
            message.reply_text(tld(chat.id, "mute_not_sudo"))

        elif is_user_admin(chatD, user_id, member=member):
            message.reply_text(tld(chat.id, "mute_not_m_admin"))

        elif member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chatD.id,
                                     user_id,
                                     can_send_messages=False)
            keyboard = []
            reply = tld(chat.id, "mute_success").format(
                mention_html(member.user.id, member.user.first_name),
                chatD.title)
            message.reply_text(reply,
                               reply_markup=keyboard,
                               parse_mode=ParseMode.HTML)
            return "<b>{}:</b>" \
                   "\n#MUTE" \
                   "\n<b>Admin:</b> {}" \
                   "\n<b>User:</b> {}".format(html.escape(chatD.title),
                                              mention_html(user.id, user.first_name),
                                              mention_html(member.user.id, member.user.first_name))

        else:
            message.reply_text(
                tld(chat.id, "mute_already_mute").format(chatD.title))
    else:
        message.reply_text(
            tld(chat.id, "mute_not_in_chat").format(chatD.title))

    return ""


@run_async
@bot_admin
@user_admin
@loggable
def unmute(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    conn = connected(bot, update, chat, user.id)
    if conn:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            return
        else:
            chatD = chat

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "unmute_invalid"))
        return ""

    try:
        member = chatD.get_member(int(user_id))
    except BadRequest as excp:
        if excp.message == "User not found.":
            message.reply_text(tld(chat.id, "bans_err_usr_not_found"))
            return ""
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text(tld(chat.id, "unmute_is_an_admin"))
        return ""

    if member.status != 'kicked' and member.status != 'left':
        if member.can_send_messages and member.can_send_media_messages \
                and member.can_send_other_messages and member.can_add_web_page_previews:
            message.reply_text(
                tld(chat.id, "unmute_not_muted").format(chatD.title))
        else:
            bot.restrict_chat_member(chatD.id,
                                     int(user_id),
                                     can_send_messages=True,
                                     can_send_media_messages=True,
                                     can_send_other_messages=True,
                                     can_add_web_page_previews=True)
            keyboard = []
            reply = tld(chat.id, "unmute_success").format(
                mention_html(member.user.id, member.user.first_name),
                chatD.title)
            message.reply_text(reply,
                               reply_markup=keyboard,
                               parse_mode=ParseMode.HTML)
            return "<b>{}:</b>" \
                   "\n#UNMUTE" \
                   "\n<b>• Admin:</b> {}" \
                   "\n<b>• User:</b> {}" \
                   "\n<b>• ID:</b> <code>{}</code>".format(html.escape(chatD.title),
                                                           mention_html(user.id, user.first_name),
                                                           mention_html(member.user.id, member.user.first_name), user_id)
    else:
        message.reply_text(tld(chat.id, "unmute_not_in_chat"))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_mute(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    conn = connected(bot, update, chat, user.id)
    if conn:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            return
        else:
            chatD = chat

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "mute_not_refer"))
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "mute_not_existed"))
            return ""
        else:
            raise

    if is_user_admin(chat, user_id, member):
        message.reply_text(tld(chat.id, "mute_is_admin"))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "mute_is_bot"))
        return ""

    if not reason:
        message.reply_text(tld(chat.id, "tmute_no_time"))
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    mutetime = extract_time(message, time_val)

    if not mutetime:
        return ""

    log = "<b>{}:</b>" \
          "\n#TEMP MUTED" \
          "\n<b>Admin:</b> {}" \
          "\n<b>User:</b> {}" \
          "\n<b>Time:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name),
                                     mention_html(member.user.id, member.user.first_name), time_val)
    if reason:
        log += tld(chat.id, "bans_logger_reason").format(reason)

    try:
        if member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chat.id,
                                     user_id,
                                     until_date=mutetime,
                                     can_send_messages=False)
            message.reply_text(
                tld(chat.id, "tmute_success").format(time_val, chatD.title))
            return log
        else:
            message.reply_text(
                tld(chat.id, "mute_already_mute").format(chatD.title))

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(tld(chat.id, "tmute_success").format(
                time_val, chatD.title),
                               quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR muting user %s in chat %s (%s) due to %s",
                             user_id, chat.title, chat.id, excp.message)
            message.reply_text(tld(chat.id, "mute_cant_mute"))

    return ""


@run_async
@bot_admin
@user_admin
@loggable
def nomedia(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    conn = connected(bot, update, chat, user.id)
    if conn:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            return
        else:
            chatD = chat

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "restrict_invalid"))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "restrict_is_bot"))
        return ""

    member = chatD.get_member(int(user_id))

    if member:
        if is_user_admin(chatD, user_id, member=member):
            message.reply_text(tld(chat.id, "restrict_is_admin"))

        elif member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chatD.id,
                                     user_id,
                                     can_send_messages=True,
                                     can_send_media_messages=False,
                                     can_send_other_messages=False,
                                     can_add_web_page_previews=False)
            keyboard = []
            reply = tld(chat.id, "restrict_success").format(
                mention_html(member.user.id, member.user.first_name),
                chatD.title)
            message.reply_text(reply,
                               reply_markup=keyboard,
                               parse_mode=ParseMode.HTML)
            return "<b>{}:</b>" \
                   "\n#RESTRICTED" \
                   "\n<b>• Admin:</b> {}" \
                   "\n<b>• User:</b> {}" \
                   "\n<b>• ID:</b> <code>{}</code>".format(html.escape(chatD.title),
                                              mention_html(user.id, user.first_name),
                                              mention_html(member.user.id, member.user.first_name), user_id)

        else:
            message.reply_text(tld(chat.id, "restrict_already_restricted"))
    else:
        message.reply_text(
            tld(chat.id, "mute_not_in_chat").format(chatD.title))

    return ""


@run_async
@bot_admin
@user_admin
@loggable
def media(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    conn = connected(bot, update, chat, user.id)
    if conn:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            return
        else:
            chatD = chat

    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(tld(chat.id, "unrestrict_invalid"))
        return ""

    member = chatD.get_member(int(user_id))

    if member.status != 'kicked' and member.status != 'left':
        if member.can_send_messages and member.can_send_media_messages \
                and member.can_send_other_messages and member.can_add_web_page_previews:
            message.reply_text(
                tld(chat.id, "unrestrict_not_restricted").format(chatD.title))
        else:
            bot.restrict_chat_member(chatD.id,
                                     int(user_id),
                                     can_send_messages=True,
                                     can_send_media_messages=True,
                                     can_send_other_messages=True,
                                     can_add_web_page_previews=True)
            keyboard = []
            reply = tld(chat.id, "unrestrict_success").format(
                mention_html(member.user.id, member.user.first_name),
                chatD.title)
            message.reply_text(reply,
                               reply_markup=keyboard,
                               parse_mode=ParseMode.HTML)
            return "<b>{}:</b>" \
                   "\n#UNRESTRICTED" \
                   "\n<b>• Admin:</b> {}" \
                   "\n<b>• User:</b> {}" \
                   "\n<b>• ID:</b> <code>{}</code>".format(html.escape(chatD.title),
                                                           mention_html(user.id, user.first_name),
                                                           mention_html(member.user.id, member.user.first_name), user_id)
    else:
        message.reply_text(tld(chat.id, "unrestrict_not_in_chat"))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_nomedia(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    conn = connected(bot, update, chat, user.id)
    if conn:
        chatD = dispatcher.bot.getChat(conn)
    else:
        if chat.type == "private":
            return
        else:
            chatD = chat

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "mute_not_refer"))
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "mute_not_existed"))
            return ""
        else:
            raise

    if is_user_admin(chat, user_id, member):
        message.reply_text(tld(chat.id, "restrict_is_admin"))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "restrict_is_bot"))
        return ""

    if not reason:
        message.reply_text(tld(chat.id, "nomedia_need_time"))
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    mutetime = extract_time(message, time_val)

    if not mutetime:
        return ""

    log = "<b>{}:</b>" \
          "\n#TEMP RESTRICTED" \
          "\n<b>• Admin:</b> {}" \
          "\n<b>• User:</b> {}" \
          "\n<b>• ID:</b> <code>{}</code>" \
          "\n<b>• Time:</b> {}".format(html.escape(chat.title), mention_html(user.id, user.first_name),
                                       mention_html(member.user.id, member.user.first_name), user_id, time_val)
    if reason:
        log += tld(chat.id, "bans_logger_reason").format(reason)

    try:
        if member.can_send_messages is None or member.can_send_messages:
            bot.restrict_chat_member(chat.id,
                                     user_id,
                                     until_date=mutetime,
                                     can_send_messages=True,
                                     can_send_media_messages=False,
                                     can_send_other_messages=False,
                                     can_add_web_page_previews=False)
            message.reply_text(
                tld(chat.id, "nomedia_success").format(time_val, chatD.title))
            return log
        else:
            message.reply_text(
                tld(chat.id,
                    "restrict_already_restricted").format(chatD.title))

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(tld(chat.id, "nomedia_success").format(
                time_val, chatD.title),
                               quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR muting user %s in chat %s (%s) due to %s",
                             user_id, chat.title, chat.id, excp.message)
            message.reply_text(tld(chat.id, "restrict_cant_restricted"))

    return ""


@run_async
@bot_admin
@can_restrict
def muteme(bot: Bot, update: Update, args: List[str]) -> str:
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat
    user = update.effective_user
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text(tld(chat.id, "mute_is_admin"))
        return

    res = bot.restrict_chat_member(chat.id, user_id, can_send_messages=False)
    if res:
        update.effective_message.reply_text(tld(chat.id, "muteme_muted"))
        log = "<b>{}:</b>" \
              "\n#MUTEME" \
              "\n<b>User:</b> {}" \
              "\n<b>ID:</b> <code>{}</code>".format(html.escape(chat.title),
                                                    mention_html(user.id, user.first_name), user_id)
        return log

    else:
        update.effective_message.reply_text(tld(chat.id, "mute_cant_mute"))


MUTE_HANDLER = DisableAbleCommandHandler("mute",
                                         mute,
                                         pass_args=True,
                                         admin_ok=True)
UNMUTE_HANDLER = DisableAbleCommandHandler("unmute",
                                           unmute,
                                           pass_args=True,
                                           admin_ok=True)
TEMPMUTE_HANDLER = DisableAbleCommandHandler(["tmute", "tempmute"],
                                             temp_mute,
                                             pass_args=True,
                                             admin_ok=True)
TEMP_NOMEDIA_HANDLER = DisableAbleCommandHandler(["trestrict", "temprestrict"],
                                                 temp_nomedia,
                                                 pass_args=True,
                                                 admin_ok=True)
NOMEDIA_HANDLER = DisableAbleCommandHandler(["restrict", "nomedia"],
                                            nomedia,
                                            pass_args=True,
                                            admin_ok=True)
MEDIA_HANDLER = DisableAbleCommandHandler("unrestrict",
                                          media,
                                          pass_args=True,
                                          admin_ok=True)
MUTEME_HANDLER = DisableAbleCommandHandler("muteme",
                                           muteme,
                                           pass_args=True,
                                           filters=Filters.group,
                                           admin_ok=True)

dispatcher.add_handler(MUTE_HANDLER)
dispatcher.add_handler(UNMUTE_HANDLER)
dispatcher.add_handler(TEMPMUTE_HANDLER)
dispatcher.add_handler(TEMP_NOMEDIA_HANDLER)
dispatcher.add_handler(NOMEDIA_HANDLER)
dispatcher.add_handler(MEDIA_HANDLER)
dispatcher.add_handler(MUTEME_HANDLER)

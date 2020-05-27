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
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User, ParseMode
from telegram.error import BadRequest
from telegram.ext import run_async, Filters
from telegram.utils.helpers import mention_html

from haruka import dispatcher, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.chat_status import bot_admin, user_admin, is_user_ban_protected, can_restrict, \
    is_user_admin, is_user_in_chat
from haruka.modules.helper_funcs.extraction import extract_user_and_text
from haruka.modules.helper_funcs.string_handling import extract_time
from haruka.modules.log_channel import loggable

from haruka.modules.tr_engine.strings import tld


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "common_err_no_user"))
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found.":
            message.reply_text(tld(chat.id, "bans_err_usr_not_found"))
            return ""
        else:
            raise

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "bans_err_usr_is_bot"))
        return ""

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text(tld(chat.id, "bans_err_usr_is_admin"))
        return ""

    log = tld(chat.id, "bans_logger").format(
        html.escape(chat.title), mention_html(user.id, user.first_name),
        mention_html(member.user.id, member.user.first_name), user_id)

    reply = tld(chat.id, "bans_banned_success").format(
        mention_html(user.id, user.first_name),
        mention_html(member.user.id, member.user.first_name),
        html.escape(chat.title))

    if reason:
        log += tld(chat.id, "bans_logger_reason").format(reason)
        reply += tld(chat.id, "bans_logger_reason").format(reason)

    try:
        chat.kick_member(user_id)
        message.reply_text(reply, parse_mode=ParseMode.HTML)
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(reply, quote=False, parse_mode=ParseMode.HTML)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s",
                             user_id, chat.title, chat.id, excp.message)
            message.reply_text(
                tld(chat.id, "bans_err_unknown").format("banning"))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "common_err_no_user"))
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found.":
            message.reply_text(tld(chat.id, "bans_err_usr_not_found"))
            return ""
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text(tld(chat.id, "bans_err_usr_is_admin"))
        return ""

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "bans_err_usr_is_bot"))
        return ""

    if not reason:
        message.reply_text(tld(chat.id, "bans_err_tban_no_arg"))
        return ""

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    bantime = extract_time(message, time_val)

    if not bantime:
        return ""

    log = tld(chat.id, "bans_tban_logger").format(
        html.escape(chat.title), mention_html(user.id, user.first_name),
        mention_html(member.user.id, member.user.first_name), member.user.id,
        time_val)
    if reason:
        log += tld(chat.id, "bans_logger_reason").format(reason)

    try:
        chat.kick_member(user_id, until_date=bantime)
        reply = tld(chat.id, "bans_tbanned_success").format(
            mention_html(user.id, user.first_name),
            mention_html(member.user.id, member.user.first_name),
            html.escape(chat.title), time_val)
        reply += tld(chat.id, "bans_logger_reason").format(reason)
        message.reply_text(reply, parse_mode=ParseMode.HTML)
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(tld(chat.id, "bans_tbanned_success").format(
                mention_html(user.id, user.first_name),
                mention_html(member.user.id, member.user.first_name),
                html.escape(chat.title), time_val),
                               quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s",
                             user_id, chat.title, chat.id, excp.message)
            message.reply_text(
                tld(chat.id, "bans_err_unknown").format("tbanning"))

    return ""


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def kick(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text(tld(chat.id, "common_err_no_user"))
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found.":
            message.reply_text(tld(chat.id, "bans_err_usr_not_found"))
            return ""
        else:
            raise

    if user_id == bot.id:
        message.reply_text(tld(chat.id, "bans_kick_is_bot"))
        return ""

    if is_user_ban_protected(chat, user_id):
        message.reply_text(tld(chat.id, "bans_kick_is_admin"))
        return ""

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        reply = tld(chat.id, "bans_kick_success").format(
            mention_html(user.id, user.first_name),
            mention_html(member.user.id, member.user.first_name),
            html.escape(chat.title))
        if reason:
            reply += tld(chat.id, "bans_logger_reason").format(reason)

        message.reply_text(reply, parse_mode=ParseMode.HTML)

        log = tld(chat.id, "bans_kick_logger").format(
            html.escape(chat.title), mention_html(user.id, user.first_name),
            mention_html(member.user.id, member.user.first_name),
            member.user.id)
        if reason:
            log += tld(chat.id, "bans_logger_reason").format(reason)

        return log

    else:
        message.reply_text(tld(chat.id, "bans_err_unknown").format("kicking"))

    return ""


@run_async
@bot_admin
@can_restrict
def kickme(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]

    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text(tld(chat.id, "bans_kick_is_admin"))
        return

    res = update.effective_chat.unban_member(
        user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text(tld(chat.id,
                                                "bans_kickme_success"))
    else:
        update.effective_message.reply_text(tld(chat.id, "bans_kickme_failed"))


@run_async
@bot_admin
@can_restrict
@loggable
def banme(bot: Bot, update: Update):
    user_id = update.effective_message.from_user.id
    chat = update.effective_chat
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text(
            tld(chat.id, "bans_err_usr_is_admin"))
        return

    res = update.effective_chat.kick_member(user_id)
    if res:
        update.effective_message.reply_text(tld(chat.id,
                                                "bans_kickme_success"))

    else:
        update.effective_message.reply_text(tld(chat.id, "bans_kickme_failed"))


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def unban(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message  # type: Optional[Message]
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text(tld(chat.id, "common_err_no_user"))
            return ""
        else:
            raise

    if is_user_in_chat(chat, user_id):
        message.reply_text(tld(chat.id, "bans_unban_user_in_chat"))
        return ""

    chat.unban_member(user_id)
    message.reply_text(tld(chat.id, "bans_unban_success"))

    log = tld(chat.id, "bans_unban_logger").format(
        html.escape(chat.title), mention_html(user.id, user.first_name),
        mention_html(member.user.id, member.user.first_name), member.user.id)
    if reason:
        log += tld(chat.id, "bans_logger_reason").format(reason)

    return log


@run_async
@bot_admin
@can_restrict
@user_admin
@loggable
def sban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    update.effective_message.delete()

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        return ""

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            return ""
        else:
            raise

    if is_user_ban_protected(chat, user_id, member):
        return ""

    if user_id == bot.id:
        return ""

    log = tld(chat.id, "bans_sban_logger").format(
        html.escape(chat.title), mention_html(user.id, user.first_name),
        mention_html(member.user.id, member.user.first_name), user_id)
    if reason:
        log += tld(chat.id, "bans_logger_reason").format(reason)

    try:
        chat.kick_member(user_id)
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s",
                             user_id, chat.title, chat.id, excp.message)
    return ""


__help__ = True

BAN_HANDLER = DisableAbleCommandHandler("ban",
                                        ban,
                                        pass_args=True,
                                        filters=Filters.group,
                                        admin_ok=True)
TEMPBAN_HANDLER = DisableAbleCommandHandler(["tban", "tempban"],
                                            temp_ban,
                                            pass_args=True,
                                            filters=Filters.group,
                                            admin_ok=True)
KICK_HANDLER = DisableAbleCommandHandler("kick",
                                         kick,
                                         pass_args=True,
                                         filters=Filters.group,
                                         admin_ok=True)
UNBAN_HANDLER = DisableAbleCommandHandler("unban",
                                          unban,
                                          pass_args=True,
                                          filters=Filters.group,
                                          admin_ok=True)
KICKME_HANDLER = DisableAbleCommandHandler("kickme",
                                           kickme,
                                           filters=Filters.group)
SBAN_HANDLER = DisableAbleCommandHandler("sban",
                                         sban,
                                         pass_args=True,
                                         filters=Filters.group,
                                         admin_ok=True)
BANME_HANDLER = DisableAbleCommandHandler("banme",
                                          banme,
                                          filters=Filters.group)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(KICK_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(KICKME_HANDLER)
dispatcher.add_handler(BANME_HANDLER)
dispatcher.add_handler(SBAN_HANDLER)

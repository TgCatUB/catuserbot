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
import re
from typing import List

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, User
from telegram import Message, Chat, Update, Bot
from telegram.error import BadRequest
from telegram.ext import CommandHandler, run_async, DispatcherHandlerStop, MessageHandler, Filters, CallbackQueryHandler
from telegram.utils.helpers import mention_html

from haruka import dispatcher
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.chat_status import is_user_admin, bot_admin, user_admin, \
    can_restrict
from haruka.modules.helper_funcs.extraction import extract_text, extract_user_and_text, extract_user
from haruka.modules.helper_funcs.filters import CustomFilters
from haruka.modules.helper_funcs.misc import split_message
from haruka.modules.helper_funcs.string_handling import split_quotes
from haruka.modules.log_channel import loggable
from haruka.modules.sql import warns_sql as sql
import haruka.modules.sql.rules_sql as rules_sql
from haruka.modules.tr_engine.strings import tld

WARN_HANDLER_GROUP = 9


# Not async
def warn(user: User,
         chat: Chat,
         reason: str,
         message: Message,
         warner: User = None) -> str:
    bot = dispatcher.bot

    if is_user_admin(chat, user.id):
        message.reply_text(tld(chat.id, 'warns_warn_admin_no_warn'))
        return ""

    if warner:
        warner_tag = mention_html(warner.id, warner.first_name)
    else:
        warner_tag = tld(chat.id, 'warns_warn_admin_autofilter')

    limit, soft_warn = sql.get_warn_setting(chat.id)
    num_warns, reasons = sql.warn_user(user.id, chat.id, reason)
    if num_warns >= limit:
        sql.reset_warns(user.id, chat.id)
        if soft_warn:  # kick
            chat.unban_member(user.id)
            reply = tld(chat.id, 'warns_max_warn_kick').format(
                limit, mention_html(user.id, user.first_name))

        else:  # ban
            chat.kick_member(user.id)
            reply = tld(chat.id, 'warns_max_warn_ban').format(
                limit, mention_html(user.id, user.first_name))

        for warn_reason in reasons:
            reply += "\n - {}".format(html.escape(warn_reason))

        keyboard = []
        log_reason = tld(chat.id, 'warns_warn_ban_log_channel').format(
            html.escape(chat.title), warner_tag,
            mention_html(user.id, user.first_name), user.id, reason, num_warns,
            limit)

    else:
        keyboard = [[
            InlineKeyboardButton(tld(chat.id, 'warns_btn_remove_warn'),
                                 callback_data="rm_warn({})".format(user.id))
        ]]
        rules = rules_sql.get_rules(chat.id)

        if rules:
            keyboard[0].append(
                InlineKeyboardButton(tld(chat.id, 'warns_btn_rules'),
                                     url="t.me/{}?start={}".format(
                                         bot.username, chat.id)))

        reply = tld(chat.id, 'warns_user_warned').format(
            mention_html(user.id, user.first_name), num_warns, limit)
        if reason:
            reply += tld(chat.id, 'warns_latest_warn_reason').format(
                html.escape(reason))

        log_reason = tld(chat.id, 'warns_warn_log_channel').format(
            html.escape(chat.title), warner_tag,
            mention_html(user.id, user.first_name), user.id, reason, num_warns,
            limit)

    try:
        message.reply_text(reply,
                           reply_markup=InlineKeyboardMarkup(keyboard),
                           parse_mode=ParseMode.HTML)
    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(reply,
                               reply_markup=InlineKeyboardMarkup(keyboard),
                               parse_mode=ParseMode.HTML,
                               quote=False)
        else:
            raise
    return log_reason


@run_async
@bot_admin
@loggable
def rmwarn_handler(bot: Bot, update: Update) -> str:
    chat = update.effective_chat
    query = update.callback_query
    user = update.effective_user
    match = re.match(r"rm_warn\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        if not is_user_admin(chat, int(user.id)):
            query.answer(text=tld(chat.id, 'warns_remove_admin_only'),
                         show_alert=True)
            return ""
        res = sql.remove_warn(user_id, chat.id)
        if res:
            update.effective_message.edit_text(tld(
                chat.id, 'warns_remove_success').format(
                    mention_html(user.id, user.first_name)),
                                               parse_mode=ParseMode.HTML)
            user_member = chat.get_member(user_id)
            return tld(chat.id, 'warns_remove_log_channel').format(
                html.escape(chat.title), mention_html(user.id,
                                                      user.first_name),
                mention_html(user_member.user.id, user_member.user.first_name),
                user_member.user.id)
        else:
            update.effective_message.edit_text(tld(
                chat.id, 'warns_user_has_no_warns').format(
                    mention_html(user.id, user.first_name)),
                                               parse_mode=ParseMode.HTML)

    return ""


@run_async
@bot_admin
@loggable
def sendrules_handler(bot: Bot, update: Update) -> str:
    query = update.callback_query
    print(query)
    print(query.data)
    match = re.match(r"send_rules\((.+?)\)", query.data)
    if match:
        chat_id = match.group(1)
        send_rules(update, chat_id, True)

    return ""


@run_async
@user_admin
@bot_admin
@loggable
def remove_warns(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    user_id = extract_user(message, args)

    if user_id:
        sql.remove_warn(user_id, chat.id)
        message.reply_text(tld(chat.id, 'warns_latest_remove_success'))
        warned = chat.get_member(user_id).user
        return tld(chat.id, 'warns_remove_log_channel').format(
            html.escape(chat.title), mention_html(user.id, user.first_name),
            mention_html(warned.id, warned.first_name), warned.id)
    else:
        message.reply_text(tld(chat.id, 'common_err_no_user'))
    return ""


@run_async
@user_admin
@can_restrict
@loggable
def warn_user(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    chat = update.effective_chat
    warner = update.effective_user

    user_id, reason = extract_user_and_text(message, args)

    if user_id:
        if message.reply_to_message and message.reply_to_message.from_user.id == user_id:
            return warn(message.reply_to_message.from_user, chat, reason,
                        message.reply_to_message, warner)
        else:
            return warn(
                chat.get_member(user_id).user, chat, reason, message, warner)
    else:
        message.reply_text(tld(chat.id, 'common_err_no_user'))
    return ""


@run_async
@user_admin
@bot_admin
@loggable
def reset_warns(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    user_id = extract_user(message, args)

    if user_id:
        sql.reset_warns(user_id, chat.id)
        message.reply_text(tld(chat.id, 'warns_reset_success'))
        warned = chat.get_member(user_id).user
        return tld(chat.id, 'warns_reset_log_channel').format(
            html.escape(chat.title), mention_html(user.id, user.first_name),
            mention_html(warned.id, warned.first_name), warned.id)
    else:
        message.reply_text(tld(chat.id, 'common_err_no_user'))
    return ""


@run_async
def warns(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(message, args) or update.effective_user.id
    result = sql.get_warns(user_id, chat.id)
    num = 1

    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = sql.get_warn_setting(chat.id)

        if reasons:
            text = tld(chat.id, 'warns_list_warns').format(num_warns, limit)
            for reason in reasons:
                text += "\n {}. {}".format(num, reason)
                num += 1

            msgs = split_message(text)
            for msg in msgs:
                update.effective_message.reply_text(msg)
        else:
            update.effective_message.reply_text(
                tld(chat.id,
                    'warns_list_warns_no_reason').format(num_warns, limit))
    else:
        update.effective_message.reply_text(
            tld(chat.id, 'warns_list_warns_none'))


# Dispatcher handler stop - do not async
@user_admin
def add_warn_filter(bot: Bot, update: Update):
    chat = update.effective_chat
    msg = update.effective_message

    args = msg.text.split(
        None,
        1)  # use python's maxsplit to separate Cmd, keyword, and reply_text

    if len(args) < 2:
        return

    extracted = split_quotes(args[1])

    if len(extracted) >= 2:
        # set trigger -> lower, so as to avoid adding duplicate filters with different cases
        keyword = extracted[0].lower()
        content = extracted[1]

    else:
        return

    # Note: perhaps handlers can be removed somehow using sql.get_chat_filters
    for handler in dispatcher.handlers.get(WARN_HANDLER_GROUP, []):
        if handler.filters == (keyword, chat.id):
            dispatcher.remove_handler(handler, WARN_HANDLER_GROUP)

    sql.add_warn_filter(chat.id, keyword, content)

    update.effective_message.reply_text(
        tld(chat.id, 'warns_handler_add_success').format(keyword))
    raise DispatcherHandlerStop


@user_admin
def remove_warn_filter(bot: Bot, update: Update):
    chat = update.effective_chat
    msg = update.effective_message

    args = msg.text.split(
        None,
        1)  # use python's maxsplit to separate Cmd, keyword, and reply_text

    if len(args) < 2:
        return

    extracted = split_quotes(args[1])

    if len(extracted) < 1:
        return

    to_remove = extracted[0]

    chat_filters = sql.get_chat_warn_triggers(chat.id)

    if not chat_filters:
        msg.reply_text(tld(chat.id, 'warns_filters_list_empty'))
        return

    for filt in chat_filters:
        if filt == to_remove:
            sql.remove_warn_filter(chat.id, to_remove)
            msg.reply_text(tld(chat.id, 'warns_filters_remove_success'))
            raise DispatcherHandlerStop

    msg.reply_text(tld(chat.id, 'warns_filter_doesnt_exist'))


@run_async
def list_warn_filters(bot: Bot, update: Update):
    chat = update.effective_chat
    all_handlers = sql.get_chat_warn_triggers(chat.id)

    if not all_handlers:
        update.effective_message.reply_text(
            tld(chat.id, 'warns_filters_list_empty'))
        return

    filter_list = tld(chat.id, 'warns_filters_list')
    for keyword in all_handlers:
        entry = " - {}\n".format(html.escape(keyword))
        if len(entry) + len(filter_list) > telegram.MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(filter_list,
                                                parse_mode=ParseMode.HTML)
            filter_list = entry
        else:
            filter_list += entry

    if not filter_list == tld(chat.id, 'warns_filters_list'):
        update.effective_message.reply_text(filter_list,
                                            parse_mode=ParseMode.HTML)


@run_async
@loggable
def reply_filter(bot: Bot, update: Update) -> str:
    chat = update.effective_chat
    message = update.effective_message

    chat_warn_filters = sql.get_chat_warn_triggers(chat.id)
    to_match = extract_text(message)
    if not to_match:
        return ""

    for keyword in chat_warn_filters:
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            user = update.effective_user
            warn_filter = sql.get_warn_filter(chat.id, keyword)
            return warn(user, chat, warn_filter.reply, message)
    return ""


@run_async
@user_admin
@loggable
def set_warn_limit(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if args:
        if args[0].isdigit():
            if int(args[0]) < 1:
                msg.reply_text(tld(chat.id, 'warns_warnlimit_min_1'))
            else:
                sql.set_warn_limit(chat.id, int(args[0]))
                msg.reply_text(
                    tld(chat.id,
                        'warns_warnlimit_updated_success').format(args[0]))
                return tld(chat.id, 'warns_set_warn_limit_log_channel').format(
                    html.escape(chat.title),
                    mention_html(user.id, user.first_name), args[0])
        else:
            msg.reply_text(tld(chat.id, 'warns_warnlimit_invalid_arg'))
    else:
        limit, soft_warn = sql.get_warn_setting(chat.id)

        msg.reply_text(tld(chat.id, 'warns_warnlimit_current').format(limit))
    return ""


@run_async
@user_admin
def set_warn_strength(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    user = update.effective_user
    msg = update.effective_message

    if args:
        if args[0].lower() in ("on", "yes"):
            sql.set_warn_strength(chat.id, False)
            msg.reply_text(tld(chat.id, 'warns_strength_on'))
            return tld(chat.id, 'warns_strength_on_log_channel').format(
                html.escape(chat.title), mention_html(user.id,
                                                      user.first_name))

        elif args[0].lower() in ("off", "no"):
            sql.set_warn_strength(chat.id, True)
            msg.reply_text(tld(chat.id, 'warns_strength_off'))
            return tld(chat.id, 'warns_strength_off_log_channel').format(
                html.escape(chat.title), mention_html(user.id,
                                                      user.first_name))

        else:
            msg.reply_text(tld(chat.id, 'warns_strength_invalid_arg'))
    else:
        soft_warn = sql.get_soft_warn(chat.id)
        if soft_warn:
            msg.reply_text(tld(chat.id, 'warns_strength_off'),
                           parse_mode=ParseMode.MARKDOWN)
        else:
            msg.reply_text(tld(chat.id, 'warns_strength_on'),
                           parse_mode=ParseMode.MARKDOWN)
    return ""


def __stats__():
    return "• `{}` overall warns, across `{}` chats.\n" \
           "• `{}` warn filters, across `{}` chats.".format(sql.num_warns(), sql.num_warn_chats(),
                                                      sql.num_warn_filters(), sql.num_warn_filter_chats())


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


__help__ = True

WARN_HANDLER = DisableAbleCommandHandler("warn",
                                         warn_user,
                                         pass_args=True,
                                         filters=Filters.group,
                                         admin_ok=True)
RESET_WARN_HANDLER = DisableAbleCommandHandler(["resetwarn", "resetwarns"],
                                               reset_warns,
                                               pass_args=True,
                                               filters=Filters.group)
RMWARN_QUERY_HANDLER = CallbackQueryHandler(rmwarn_handler, pattern=r"rm_warn")
SENDRULES_QUERY_HANDLER = CallbackQueryHandler(sendrules_handler,
                                               pattern=r"send_rules")
MYWARNS_HANDLER = DisableAbleCommandHandler("warns",
                                            warns,
                                            pass_args=True,
                                            filters=Filters.group,
                                            admin_ok=True)
ADD_WARN_HANDLER = DisableAbleCommandHandler("addwarn",
                                             add_warn_filter,
                                             filters=Filters.group,
                                             admin_ok=True)
RM_WARN_HANDLER = DisableAbleCommandHandler(["nowarn", "stopwarn"],
                                            remove_warn_filter,
                                            filters=Filters.group,
                                            admin_ok=True)
LIST_WARN_HANDLER = DisableAbleCommandHandler(["warnlist", "warnfilters"],
                                              list_warn_filters,
                                              filters=Filters.group,
                                              admin_ok=True)
WARN_FILTER_HANDLER = MessageHandler(CustomFilters.has_text & Filters.group,
                                     reply_filter)
WARN_LIMIT_HANDLER = DisableAbleCommandHandler("warnlimit",
                                               set_warn_limit,
                                               pass_args=True,
                                               filters=Filters.group,
                                               admin_ok=True)
WARN_STRENGTH_HANDLER = CommandHandler("strongwarn",
                                       set_warn_strength,
                                       pass_args=True,
                                       filters=Filters.group)
REMOVE_WARNS_HANDLER = CommandHandler(["rmwarn", "unwarn"],
                                      remove_warns,
                                      pass_args=True,
                                      filters=Filters.group)

dispatcher.add_handler(WARN_HANDLER)
dispatcher.add_handler(RMWARN_QUERY_HANDLER)
dispatcher.add_handler(SENDRULES_QUERY_HANDLER)
dispatcher.add_handler(RESET_WARN_HANDLER)
dispatcher.add_handler(MYWARNS_HANDLER)
dispatcher.add_handler(ADD_WARN_HANDLER)
dispatcher.add_handler(RM_WARN_HANDLER)
dispatcher.add_handler(LIST_WARN_HANDLER)
dispatcher.add_handler(WARN_LIMIT_HANDLER)
dispatcher.add_handler(WARN_STRENGTH_HANDLER)
dispatcher.add_handler(WARN_FILTER_HANDLER, WARN_HANDLER_GROUP)
dispatcher.add_handler(REMOVE_WARNS_HANDLER)

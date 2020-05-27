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
from telegram.ext import Filters, MessageHandler, CommandHandler, run_async
from telegram.utils.helpers import mention_html

from haruka import dispatcher
from haruka.modules.helper_funcs.chat_status import is_user_admin, user_admin, can_restrict
from haruka.modules.log_channel import loggable
from haruka.modules.sql import antiflood_sql as sql

from haruka.modules.tr_engine.strings import tld

FLOOD_GROUP = 3


@run_async
@loggable
def check_flood(bot: Bot, update: Update) -> str:
    user = update.effective_user
    chat = update.effective_chat
    msg = update.effective_message

    if not user:  # ignore channels
        return ""

    # ignore admins
    if is_user_admin(chat, user.id):
        sql.update_flood(chat.id, None)
        return ""

    should_ban = sql.update_flood(chat.id, user.id)
    if not should_ban:
        return ""

    try:
        bot.restrict_chat_member(chat.id, user.id, can_send_messages=False)
        msg.reply_text(tld(chat.id, "flood_mute"))

        return tld(chat.id, "flood_logger_success").format(
            html.escape(chat.title), mention_html(user.id, user.first_name))

    except BadRequest:
        msg.reply_text(tld(chat.id, "flood_err_no_perm"))
        sql.set_flood(chat.id, 0)
        return tld(chat.id, "flood_logger_fail").format(chat.title)


@run_async
@user_admin
@can_restrict
@loggable
def set_flood(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    if len(args) >= 1:
        val = args[0].lower()
        if val == "off" or val == "no" or val == "0":
            sql.set_flood(chat.id, 0)
            message.reply_text(tld(chat.id, "flood_set_off"))

        elif val.isdigit():
            amount = int(val)
            if amount <= 0:
                sql.set_flood(chat.id, 0)
                message.reply_text(tld(chat.id, "flood_set_off"))
                return tld(chat.id, "flood_logger_set_off").format(
                    html.escape(chat.title),
                    mention_html(user.id, user.first_name))

            elif amount < 3:
                message.reply_text(tld(chat.id, "flood_err_num"))
                return ""

            else:
                sql.set_flood(chat.id, amount)
                message.reply_text(tld(chat.id, "flood_set").format(amount))
                return tld(chat.id, "flood_logger_set_on").format(
                    html.escape(chat.title),
                    mention_html(user.id, user.first_name), amount)

        else:
            message.reply_text(tld(chat.id, "flood_err_args"))

    return ""


@run_async
def flood(bot: Bot, update: Update):
    chat = update.effective_chat

    limit = sql.get_flood_limit(chat.id)
    if limit == 0:
        update.effective_message.reply_text(tld(chat.id, "flood_status_off"))
    else:
        update.effective_message.reply_text(
            tld(chat.id, "flood_status_on").format(limit))


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


__help__ = True

# TODO: Add actions: ban/kick/mute/tban/tmute

FLOOD_BAN_HANDLER = MessageHandler(
    Filters.all & ~Filters.status_update & Filters.group, check_flood)
SET_FLOOD_HANDLER = CommandHandler("setflood",
                                   set_flood,
                                   pass_args=True,
                                   filters=Filters.group)
FLOOD_HANDLER = CommandHandler("flood", flood, filters=Filters.group)

dispatcher.add_handler(FLOOD_BAN_HANDLER, FLOOD_GROUP)
dispatcher.add_handler(SET_FLOOD_HANDLER)
dispatcher.add_handler(FLOOD_HANDLER)

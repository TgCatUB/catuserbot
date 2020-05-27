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
from telegram import ParseMode, MAX_MESSAGE_LENGTH
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown

import haruka.modules.sql.userinfo_sql as sql
from haruka import dispatcher, SUDO_USERS, OWNER_ID
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.extraction import extract_user

from haruka.modules.tr_engine.strings import tld


@run_async
def about_me(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    user_id = extract_user(message, args)
    chat = update.effective_chat

    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text("*{}*:\n{}".format(
            user.first_name, escape_markdown(info)),
                                            parse_mode=ParseMode.MARKDOWN)
    elif message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(
            tld(chat.id, 'userinfo_about_not_set').format(username))
    else:
        update.effective_message.reply_text(
            tld(chat.id, 'userinfo_about_not_set_you'))


@run_async
def set_about_me(bot: Bot, update: Update):
    chat = update.effective_chat
    message = update.effective_message
    user_id = message.from_user.id
    text = message.text
    info = text.split(
        None, 1
    )  # use python's maxsplit to only remove the cmd, hence keeping newlines.
    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            message.reply_text(tld(chat.id, 'userinfo_about_set_success'))
        else:
            message.reply_text(
                tld(chat.id,
                    'userinfo_about_too_long').format(MAX_MESSAGE_LENGTH // 4,
                                                      len(info[1])))


@run_async
def about_bio(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(message, args)
    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text("*{}*:\n{}".format(
            user.first_name, escape_markdown(info)),
                                            parse_mode=ParseMode.MARKDOWN)
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            tld(chat.id, 'userinfo_bio_none_they').format(username))
    else:
        update.effective_message.reply_text(
            tld(chat.id, 'userinfo_bio_none_you'))


@run_async
def set_about_bio(bot: Bot, update: Update):
    chat = update.effective_chat
    message = update.effective_message
    sender = update.effective_user
    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id
        if user_id == message.from_user.id:
            message.reply_text(tld(chat.id, 'userinfo_bio_you_cant_set'))
            return
        elif user_id == bot.id and sender.id not in SUDO_USERS:
            message.reply_text(tld(chat.id, 'userinfo_bio_bot_sudo_only'))
            return
        elif user_id in SUDO_USERS and sender.id not in SUDO_USERS:
            message.reply_text(tld(chat.id, 'userinfo_bio_sudo_sudo_only'))
            return
        elif user_id == OWNER_ID:
            message.reply_text(tld(chat.id, 'userinfo_bio_owner_nobio'))
            return

        text = message.text
        bio = text.split(
            None, 1
        )  # use python's maxsplit to only remove the cmd, hence keeping newlines.
        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text("Updated {}'s bio!".format(
                    repl_message.from_user.first_name))
            else:
                message.reply_text(
                    tld(chat.id, 'userinfo_bio_too_long').format(
                        MAX_MESSAGE_LENGTH // 4, len(bio[1])))
    else:
        message.reply_text(tld(chat.id, 'userinfo_bio_set_no_reply'))


def __user_info__(user_id, chat_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    if bio and me:
        return tld(chat_id, "userinfo_what_i_and_other_say").format(me, bio)
    elif bio:
        return tld(chat_id, "userinfo_what_other_say").format(bio)
    elif me:
        return tld(chat_id, "userinfo_what_i_say").format(me)
    else:
        return ""


def __gdpr__(user_id):
    sql.clear_user_info(user_id)
    sql.clear_user_bio(user_id)


__help__ = True

SET_BIO_HANDLER = DisableAbleCommandHandler("setbio", set_about_bio)
GET_BIO_HANDLER = DisableAbleCommandHandler("bio", about_bio, pass_args=True)

SET_ABOUT_HANDLER = DisableAbleCommandHandler("setme", set_about_me)
GET_ABOUT_HANDLER = DisableAbleCommandHandler("me", about_me, pass_args=True)

dispatcher.add_handler(SET_BIO_HANDLER)
dispatcher.add_handler(GET_BIO_HANDLER)
dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)

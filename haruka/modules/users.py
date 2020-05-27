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

import re
from time import sleep
from typing import List
from telegram import TelegramError, Update, Bot, ParseMode
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram.ext.dispatcher import run_async

import haruka.modules.sql.users_sql as sql
from haruka import dispatcher, OWNER_ID, LOGGER, SUDO_USERS, SUPPORT_USERS
from telegram.utils.helpers import escape_markdown
from haruka.modules.helper_funcs.filters import CustomFilters
from haruka.modules.helper_funcs.chat_status import bot_admin

from haruka.modules.tr_engine.strings import tld

USERS_GROUP = 4
CHAT_GROUP = 10


def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith('@'):
        username = username[1:]

    users = sql.get_userid_by_name(username)

    if not users:
        return None

    elif len(users) == 1:
        return users[0].user_id

    else:
        for user_obj in users:
            try:
                userdat = dispatcher.bot.get_chat(user_obj.user_id)
                if userdat.username == username:
                    return userdat.id

            except BadRequest as excp:
                if excp.message == 'Chat not found':
                    pass
                else:
                    LOGGER.exception("Error extracting user ID")

    return None


@run_async
def broadcast(bot: Bot, update: Update):
    to_send = update.effective_message.text.split(None, 1)
    if len(to_send) >= 2:
        chats = sql.get_all_chats() or []
        failed = 0
        for chat in chats:
            try:
                bot.sendMessage(int(chat.chat_id), to_send[1])
                sleep(0.1)
            except TelegramError:
                failed += 1
                LOGGER.warning("Couldn't send broadcast to %s, group name %s",
                               str(chat.chat_id), str(chat.chat_name))

        update.effective_message.reply_text(
            "Broadcast complete. {} groups failed to receive the message, probably "
            "due to being kicked.".format(failed))


@run_async
def log_user(bot: Bot, update: Update):
    chat = update.effective_chat
    msg = update.effective_message

    sql.update_user(msg.from_user.id, msg.from_user.username, chat.id,
                    chat.title)

    if msg.reply_to_message:
        sql.update_user(msg.reply_to_message.from_user.id,
                        msg.reply_to_message.from_user.username, chat.id,
                        chat.title)

    if msg.forward_from:
        sql.update_user(msg.forward_from.id, msg.forward_from.username)


@run_async
def snipe(bot: Bot, update: Update, args: List[str]):
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError as excp:
        update.effective_message.reply_text(
            "Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "Couldn't send the message. Perhaps I'm not part of that group?"
            )


@run_async
@bot_admin
def getlink(bot: Bot, update: Update, args: List[int]):
    message = update.effective_message
    if args:
        pattern = re.compile(r'-\d+')
    else:
        message.reply_text("You don't seem to be referring to any chats.")
    links = "Invite link(s):\n"
    for chat_id in pattern.findall(message.text):
        try:
            chat = bot.getChat(chat_id)
            bot_member = chat.get_member(bot.id)
            if bot_member.can_invite_users:
                invitelink = bot.exportChatInviteLink(chat_id)
                links += str(chat_id) + ":\n" + invitelink + "\n"
            else:
                links += str(
                    chat_id
                ) + ":\nI don't have access to the invite link." + "\n"
        except BadRequest as excp:
            links += str(chat_id) + ":\n" + excp.message + "\n"
        except TelegramError as excp:
            links += str(chat_id) + ":\n" + excp.message + "\n"

    message.reply_text(links)


@bot_admin
def leavechat(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = int(args[0])
    else:
        try:
            chat = update.effective_chat
            if chat.type == "private":
                update.effective_message.reply_text(
                    "You do not seem to be referring to a chat!")
                return
            chat_id = chat.id
            reply_text = "`I'll leave this group`"
            bot.send_message(chat_id,
                             reply_text,
                             parse_mode='Markdown',
                             disable_web_page_preview=True)
            bot.leaveChat(chat_id)
        except BadRequest as excp:
            if excp.message == "Chat not found":
                update.effective_message.reply_text(
                    "It looks like I've been kicked out of the group :p")
            else:
                return

    try:
        chat = bot.getChat(chat_id)
        titlechat = bot.get_chat(chat_id).title
        reply_text = "`I'll Go Away!`"
        bot.send_message(chat_id,
                         reply_text,
                         parse_mode='Markdown',
                         disable_web_page_preview=True)
        bot.leaveChat(chat_id)
        update.effective_message.reply_text(
            "I'll left group {}".format(titlechat))

    except BadRequest as excp:
        if excp.message == "Chat not found":
            update.effective_message.reply_text(
                "It looks like I've been kicked out of the group :p")
        else:
            return


@run_async
def slist(bot: Bot, update: Update):
    message = update.effective_message
    text1 = "My sudo users are:"
    text2 = "My support users are:"
    for user_id in SUDO_USERS:
        try:
            user = bot.get_chat(user_id)
            name = "[{}](tg://user?id={})".format(
                user.first_name + (user.last_name or ""), user.id)
            if user.username:
                name = escape_markdown("@" + user.username)
            text1 += "\n - `{}`".format(name)
        except BadRequest as excp:
            if excp.message == 'Chat not found':
                text1 += "\n - ({}) - not found".format(user_id)
    for user_id in SUPPORT_USERS:
        try:
            user = bot.get_chat(user_id)
            name = "[{}](tg://user?id={})".format(
                user.first_name + (user.last_name or ""), user.id)
            if user.username:
                name = escape_markdown("@" + user.username)
            text2 += "\n - `{}`".format(name)
        except BadRequest as excp:
            if excp.message == 'Chat not found':
                text2 += "\n - ({}) - not found".format(user_id)
    message.reply_text(text1 + "\n" + text2 + "\n",
                       parse_mode=ParseMode.MARKDOWN)
    #message.reply_text(text2 + "\n", parse_mode=ParseMode.MARKDOWN)


@run_async
def chat_checker(bot: Bot, update: Update):
    if update.effective_message.chat.get_member(
            bot.id).can_send_messages == False:
        bot.leaveChat(update.effective_message.chat.id)


def __user_info__(user_id, chat_id):
    if user_id == dispatcher.bot.id:
        return tld(chat_id, "users_seen_is_bot")
    num_chats = sql.get_user_num_chats(user_id)
    return tld(chat_id, "users_seen").format(num_chats)


def __stats__():
    return "• `{}` users, across `{}` chats".format(sql.num_users(),
                                                    sql.num_chats())


def __gdpr__(user_id):
    sql.del_user(user_id)


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


BROADCAST_HANDLER = CommandHandler("broadcasts",
                                   broadcast,
                                   filters=Filters.user(OWNER_ID))
USER_HANDLER = MessageHandler(Filters.all & Filters.group, log_user)
SNIPE_HANDLER = CommandHandler("snipe",
                               snipe,
                               pass_args=True,
                               filters=Filters.user(OWNER_ID))
GETLINK_HANDLER = CommandHandler("getlink",
                                 getlink,
                                 pass_args=True,
                                 filters=Filters.user(OWNER_ID))
LEAVECHAT_HANDLER = CommandHandler("leavechat",
                                   leavechat,
                                   pass_args=True,
                                   filters=Filters.user(OWNER_ID))
SLIST_HANDLER = CommandHandler("slist",
                               slist,
                               filters=CustomFilters.sudo_filter
                               | CustomFilters.support_filter)
CHAT_CHECKER_HANDLER = MessageHandler(Filters.all & Filters.group,
                                      chat_checker)

dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(GETLINK_HANDLER)
dispatcher.add_handler(LEAVECHAT_HANDLER)
dispatcher.add_handler(SLIST_HANDLER)
dispatcher.add_handler(USER_HANDLER, USERS_GROUP)
dispatcher.add_handler(BROADCAST_HANDLER)
dispatcher.add_handler(CHAT_CHECKER_HANDLER, CHAT_GROUP)

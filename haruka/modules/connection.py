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

from typing import Optional, List

from telegram import ParseMode
from telegram import Chat, Update, Bot, User
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async

import haruka.modules.sql.connection_sql as sql
from haruka import dispatcher, SUDO_USERS
from haruka.modules.helper_funcs.chat_status import user_admin

from haruka.modules.tr_engine.strings import tld

from haruka.modules.keyboard import keyboard


@user_admin
@run_async
def allow_connections(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    if chat.type != chat.PRIVATE:
        if len(args) >= 1:
            var = args[0]
            print(var)
            if var == "no" or var == "off":
                sql.set_allow_connect_to_chat(chat.id, False)
                update.effective_message.reply_text(
                    tld(chat.id, "connection_disable"))
            elif var == "yes" or var == "on":
                sql.set_allow_connect_to_chat(chat.id, True)
                update.effective_message.reply_text(
                    tld(chat.id, "connection_enable"))
            else:
                update.effective_message.reply_text(
                    tld(chat.id, "connection_err_wrong_arg"))
        else:
            update.effective_message.reply_text(
                tld(chat.id, "connection_err_wrong_arg"))
    else:
        update.effective_message.reply_text(
            tld(chat.id, "connection_err_wrong_arg"))


@run_async
def connect_chat(bot, update, args):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    if update.effective_chat.type == 'private':
        if len(args) >= 1:
            try:
                connect_chat = int(args[0])
            except ValueError:
                update.effective_message.reply_text(
                    tld(chat.id, "common_err_invalid_chatid"))
                return
            if (bot.get_chat_member(
                    connect_chat, update.effective_message.from_user.id).status
                    in ('administrator', 'creator') or
                (sql.allow_connect_to_chat(connect_chat) == True)
                    and bot.get_chat_member(
                        connect_chat,
                        update.effective_message.from_user.id).status in
                ('member')) or (user.id in SUDO_USERS):

                connection_status = sql.connect(
                    update.effective_message.from_user.id, connect_chat)
                if connection_status:
                    chat_name = dispatcher.bot.getChat(
                        connected(bot, update, chat, user.id,
                                  need_admin=False)).title
                    update.effective_message.reply_text(
                        tld(chat.id, "connection_success").format(chat_name),
                        parse_mode=ParseMode.MARKDOWN)

                    #Add chat to connection history
                    history = sql.get_history(user.id)
                    if history:
                        #Vars
                        if history.chat_id1:
                            history1 = int(history.chat_id1)
                        if history.chat_id2:
                            history2 = int(history.chat_id2)
                        if history.chat_id3:
                            history3 = int(history.chat_id3)
                        if history.updated:
                            number = history.updated

                        if number == 1 and connect_chat != history2 and connect_chat != history3:
                            history1 = connect_chat
                            number = 2
                        elif number == 2 and connect_chat != history1 and connect_chat != history3:
                            history2 = connect_chat
                            number = 3
                        elif number >= 3 and connect_chat != history2 and connect_chat != history1:
                            history3 = connect_chat
                            number = 1
                        else:
                            print("Error")

                        print(history.updated)
                        print(number)

                        sql.add_history(user.id, history1, history2, history3,
                                        number)
                        # print(history.user_id, history.chat_id1, history.chat_id2, history.chat_id3, history.updated)
                    else:
                        sql.add_history(user.id, connect_chat, "0", "0", 2)
                    # Rebuild user's keyboard
                    keyboard(bot, update)

                else:
                    update.effective_message.reply_text(
                        tld(chat.id, "connection_fail"))
            else:
                update.effective_message.reply_text(
                    tld(chat.id, "connection_err_not_allowed"))
        else:
            update.effective_message.reply_text(
                tld(chat.id, "connection_err_no_chatid"))
            history = sql.get_history(user.id)
            # print(history.user_id, history.chat_id1, history.chat_id2, history.chat_id3, history.updated)

    elif update.effective_chat.type == 'supergroup':
        connect_chat = chat.id
        if (bot.get_chat_member(
                connect_chat, update.effective_message.from_user.id).status in
            ('administrator', 'creator') or
            (sql.allow_connect_to_chat(connect_chat) == True)
                and bot.get_chat_member(connect_chat, update.effective_message.
                                        from_user.id).status in 'member') or (
                                            user.id in SUDO_USERS):

            connection_status = sql.connect(
                update.effective_message.from_user.id, connect_chat)
            if connection_status:
                update.effective_message.reply_text(
                    tld(chat.id, "connection_success").format(chat.id),
                    parse_mode=ParseMode.MARKDOWN)
            else:
                update.effective_message.reply_text(
                    tld(chat.id, "connection_fail"),
                    parse_mode=ParseMode.MARKDOWN)
        else:
            update.effective_message.reply_text(
                tld(chat.id, "common_err_no_admin"))

    else:
        update.effective_message.reply_text(tld(chat.id, "common_cmd_pm_only"))


def disconnect_chat(bot, update):
    chat = update.effective_chat  # type: Optional[Chat]
    if update.effective_chat.type == 'private':
        disconnection_status = sql.disconnect(
            update.effective_message.from_user.id)
        if disconnection_status:
            sql.disconnected_chat = update.effective_message.reply_text(
                tld(chat.id, "connection_dis_success"))
            #Rebuild user's keyboard
            keyboard(bot, update)
        else:
            update.effective_message.reply_text(
                tld(chat.id, "connection_dis_fail"))
    elif update.effective_chat.type == 'supergroup':
        disconnection_status = sql.disconnect(
            update.effective_message.from_user.id)
        if disconnection_status:
            sql.disconnected_chat = update.effective_message.reply_text(
                tld(chat.id, "connection_dis_success"))
            # Rebuild user's keyboard
            keyboard(bot, update)
        else:
            update.effective_message.reply_text(
                tld(chat.id, "connection_dis_fail"))
    else:
        update.effective_message.reply_text(tld(chat.id, "common_cmd_pm_only"))


def connected(bot, update, chat, user_id, need_admin=True):
    chat = update.effective_chat  # type: Optional[Chat]
    if chat.type == chat.PRIVATE and sql.get_connected_chat(user_id):
        conn_id = sql.get_connected_chat(user_id).chat_id
        if (bot.get_chat_member(
                conn_id, user_id).status in ('administrator', 'creator') or
            (sql.allow_connect_to_chat(connect_chat) == True)
                and bot.get_chat_member(
                    user_id, update.effective_message.from_user.id).status in
            ('member')) or (user_id in SUDO_USERS):
            if need_admin:
                if bot.get_chat_member(
                        conn_id,
                        update.effective_message.from_user.id).status in (
                            'administrator',
                            'creator') or user_id in SUDO_USERS:
                    return conn_id
                else:
                    update.effective_message.reply_text(
                        tld(chat.id, "connection_err_no_admin"))
                    return
            else:
                return conn_id
        else:
            update.effective_message.reply_text(
                tld(chat.id, "connection_err_unknown"))
            disconnect_chat(bot, update)
            return
    else:
        return False


__help__ = True

CONNECT_CHAT_HANDLER = CommandHandler(["connect", "connection"],
                                      connect_chat,
                                      allow_edited=True,
                                      pass_args=True)
DISCONNECT_CHAT_HANDLER = CommandHandler("disconnect",
                                         disconnect_chat,
                                         allow_edited=True)
ALLOW_CONNECTIONS_HANDLER = CommandHandler("allowconnect",
                                           allow_connections,
                                           allow_edited=True,
                                           pass_args=True)

dispatcher.add_handler(CONNECT_CHAT_HANDLER)
dispatcher.add_handler(DISCONNECT_CHAT_HANDLER)
dispatcher.add_handler(ALLOW_CONNECTIONS_HANDLER)

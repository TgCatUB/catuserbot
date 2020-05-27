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

from telegram import ReplyKeyboardMarkup, KeyboardButton

from haruka import dispatcher
from haruka.modules.tr_engine.strings import tld
from telegram.ext import CommandHandler

import haruka.modules.sql.connection_sql as con_sql


def keyboard(bot, update):
    chat = update.effective_chat
    user = update.effective_user
    conn_id = con_sql.get_connected_chat(user.id)
    if conn_id and not conn_id == False:
        btn1 = "/disconnect - {}".format(tld(chat.id, "keyboard_disconnect"))
        btn2 = ""
        btn3 = ""
    else:
        if con_sql.get_history(user.id):
            history = con_sql.get_history(user.id)
        try:
            chat_name1 = dispatcher.bot.getChat(history.chat_id1).title
        except Exception:
            chat_name1 = ""

        try:
            chat_name2 = dispatcher.bot.getChat(history.chat_id2).title
        except Exception:
            chat_name2 = ""

        try:
            chat_name3 = dispatcher.bot.getChat(history.chat_id3).title
        except Exception:
            chat_name3 = ""

        if chat_name1:
            btn1 = "/connect {} - {}".format(history.chat_id1, chat_name1)
        else:
            btn1 = "/connect - {}".format(tld(chat.id, "keyboard_connect"))
        if chat_name2:
            btn2 = "/connect {} - {}".format(history.chat_id2, chat_name2)
        else:
            btn2 = ""
        if chat_name3:
            btn3 = "/connect {} - {}".format(history.chat_id3, chat_name3)
        else:
            btn3 = ""

        #TODO: Remove except garbage

    update.effective_message.reply_text(
        tld(chat.id, "keyboard_updated"),
        reply_markup=ReplyKeyboardMarkup([[
            KeyboardButton("/help"),
            KeyboardButton("/notes - {}".format(tld(chat.id,
                                                    "keyboard_notes")))
        ], [KeyboardButton(btn1)], [KeyboardButton(btn2)],
                                          [KeyboardButton(btn3)]]))


KEYBOARD_HANDLER = CommandHandler(["keyboard"], keyboard)
dispatcher.add_handler(KEYBOARD_HANDLER)

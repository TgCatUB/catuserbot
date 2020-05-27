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
from typing import List

from telegram import MAX_MESSAGE_LENGTH, ParseMode, InlineKeyboardMarkup
from telegram import Bot, Update
from telegram.error import BadRequest
from telegram.ext import CommandHandler, RegexHandler
from telegram.ext.dispatcher import run_async

import haruka.modules.sql.notes_sql as sql
from haruka import dispatcher, MESSAGE_DUMP, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.chat_status import user_admin
from haruka.modules.helper_funcs.misc import build_keyboard, revert_buttons
from haruka.modules.helper_funcs.msg_types import get_note_type

from haruka.modules.tr_engine.strings import tld
from haruka.modules.connection import connected

FILE_MATCHER = re.compile(r"^###file_id(!photo)?###:(.*?)(?:\s|$)")
STICKER_MATCHER = re.compile(r"^###sticker(!photo)?###:")
BUTTON_MATCHER = re.compile(r"^###button(!photo)?###:(.*?)(?:\s|$)")
MYFILE_MATCHER = re.compile(r"^###file(!photo)?###:")
MYPHOTO_MATCHER = re.compile(r"^###photo(!photo)?###:")
MYAUDIO_MATCHER = re.compile(r"^###audio(!photo)?###:")
MYVOICE_MATCHER = re.compile(r"^###voice(!photo)?###:")
MYVIDEO_MATCHER = re.compile(r"^###video(!photo)?###:")
MYVIDEONOTE_MATCHER = re.compile(r"^###video_note(!photo)?###:")

ENUM_FUNC_MAP = {
    sql.Types.TEXT.value: dispatcher.bot.send_message,
    sql.Types.BUTTON_TEXT.value: dispatcher.bot.send_message,
    sql.Types.STICKER.value: dispatcher.bot.send_sticker,
    sql.Types.DOCUMENT.value: dispatcher.bot.send_document,
    sql.Types.PHOTO.value: dispatcher.bot.send_photo,
    sql.Types.AUDIO.value: dispatcher.bot.send_audio,
    sql.Types.VOICE.value: dispatcher.bot.send_voice,
    sql.Types.VIDEO.value: dispatcher.bot.send_video,
    sql.Types.VIDEO_NOTE.value: dispatcher.bot.send_video_note
}


# Do not async
def get(bot, update, notename, show_none=True, no_format=False):
    chat = update.effective_chat
    user = update.effective_user
    conn = connected(bot, update, chat, user.id, need_admin=False)
    if conn:
        chat_id = conn
        send_id = user.id
    else:
        chat_id = update.effective_chat.id
        send_id = chat_id

    note = sql.get_note(chat_id, notename)
    message = update.effective_message

    if note:
        pass
    elif notename[0] == "#":
        hashnote = sql.get_note(chat_id, notename[1:])
        if hashnote:
            note = hashnote
    elif show_none:
        message.reply_text(tld(chat.id, "note_not_existed"))
        return

    # If we're replying to a message, reply to that message (unless it's an error)
    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id
    else:
        reply_id = message.message_id

    if note and note.is_reply:
        if MESSAGE_DUMP:
            try:
                bot.forward_message(chat_id=chat_id,
                                    from_chat_id=MESSAGE_DUMP,
                                    message_id=note.value)
            except BadRequest as excp:
                if excp.message == "Message to forward not found":
                    message.reply_text(tld(chat.id, "note_lost"))
                    sql.rm_note(chat_id, notename)
                else:
                    raise
        else:
            try:
                bot.forward_message(chat_id=chat_id,
                                    from_chat_id=chat_id,
                                    message_id=note.value)

            except BadRequest as excp:
                if excp.message == "Message to forward not found":
                    message.reply_text(tld(chat.id, "note_msg_del"))
                sql.rm_note(chat_id, notename)

            else:
                raise
    else:
        if note:
            text = note.value
        else:
            text = None

        keyb = []
        parseMode = ParseMode.MARKDOWN
        buttons = sql.get_buttons(chat_id, notename)
        if no_format:
            parseMode = None
            text += revert_buttons(buttons)
        else:
            keyb = build_keyboard(buttons)

        keyboard = InlineKeyboardMarkup(keyb)

        try:
            if note and note.msgtype in (sql.Types.BUTTON_TEXT,
                                         sql.Types.TEXT):
                try:
                    bot.send_message(send_id,
                                     text,
                                     reply_to_message_id=reply_id,
                                     parse_mode=parseMode,
                                     disable_web_page_preview=True,
                                     reply_markup=keyboard)
                except BadRequest as excp:
                    if excp.message == "Wrong http url":
                        failtext = tld(chat.id, "note_url_invalid")
                        failtext += "\n\n```\n{}```".format(
                            note.value + revert_buttons(buttons))
                        message.reply_text(failtext, parse_mode="markdown")

            else:
                if note:
                    ENUM_FUNC_MAP[note.msgtype](send_id,
                                                note.file,
                                                caption=text,
                                                reply_to_message_id=reply_id,
                                                parse_mode=parseMode,
                                                disable_web_page_preview=True,
                                                reply_markup=keyboard)

        except BadRequest as excp:
            if excp.message == "Entity_mention_user_invalid":
                message.reply_text(tld(chat.id, "note_mention_invalid"))

            elif FILE_MATCHER.match(note.value):
                message.reply_text(tld(chat.id, "note_incorrect_import"))
                sql.rm_note(chat_id, notename)
            else:
                message.reply_text(tld(chat.id, "note_cannot_send"))
                LOGGER.exception("Could not parse message #%s in chat %s",
                                 notename, str(chat_id))
                LOGGER.warning("Message was: %s", str(note.value))

    return


@run_async
def cmd_get(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    if len(args) >= 2 and args[1].lower() == "noformat":
        get(bot, update, args[0].lower(), show_none=True, no_format=True)
    elif len(args) >= 1:
        get(bot, update, args[0].lower(), show_none=True)
    else:
        update.effective_message.reply_text(tld(chat.id, "get_invalid"))


@run_async
def hash_get(bot: Bot, update: Update):
    message = update.effective_message.text
    fst_word = message.split()[0]
    no_hash = fst_word[1:].lower()
    get(bot, update, no_hash, show_none=False)


# TODO: FIX THIS
@run_async
@user_admin
def save(bot: Bot, update: Update):
    chat = update.effective_chat
    user = update.effective_user
    conn = connected(bot, update, chat, user.id)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = tld(chat.id, "note_is_local")
        else:
            chat_name = chat.title

    msg = update.effective_message

    note_name, text, data_type, content, buttons = get_note_type(msg)
    note_name = note_name.lower()

    if data_type is None:
        msg.reply_text(tld(chat.id, "save_invalid"))
        return

    if len(text.strip()) == 0:
        text = note_name

    if not sql.get_note(chat_id, note_name):
        sql.add_note_to_db(chat_id,
                           note_name,
                           text,
                           data_type,
                           buttons=buttons,
                           file=content)
        msg.reply_text(tld(chat.id,
                           "save_success").format(note_name, chat_name,
                                                  note_name, note_name),
                       parse_mode=ParseMode.MARKDOWN)
    else:
        sql.add_note_to_db(chat_id,
                           note_name,
                           text,
                           data_type,
                           buttons=buttons,
                           file=content)
        msg.reply_text(tld(chat.id,
                           "save_updated").format(note_name, chat_name,
                                                  note_name, note_name),
                       parse_mode=ParseMode.MARKDOWN)


@run_async
@user_admin
def clear(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    user = update.effective_user
    conn = connected(bot, update, chat, user.id)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = tld(chat.id, "note_is_local")
        else:
            chat_name = chat.title

    if len(args) >= 1:
        notename = args[0].lower()

        if sql.rm_note(chat_id, notename):
            update.effective_message.reply_text(tld(
                chat.id, "clear_success").format(chat_name),
                                                parse_mode=ParseMode.MARKDOWN)
        else:
            update.effective_message.reply_text(
                tld(chat.id, "note_not_existed"))


@run_async
def list_notes(bot: Bot, update: Update):
    chat = update.effective_chat
    user = update.effective_user
    conn = connected(bot, update, chat, user.id, need_admin=False)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
        msg = tld(chat.id, "note_in_chat")
    else:
        chat_id = update.effective_chat.id
        if chat.type == "private":
            chat_name = tld(chat.id, "note_is_local")
            msg = tld(chat.id, "note_in_local")
        else:
            chat_name = chat.title
            msg = tld(chat.id, "note_in_chat")

    note_list = sql.get_all_chat_notes(chat_id)

    for note in note_list:
        note_name = " • `#{}`\n".format(note.name.lower())
        if len(msg) + len(note_name) > MAX_MESSAGE_LENGTH:
            update.effective_message.reply_text(msg,
                                                parse_mode=ParseMode.MARKDOWN)
            msg = ""
        msg += note_name

    if not note_list:
        update.effective_message.reply_text(tld(
            chat.id, "note_none_in_chat").format(chat_name),
                                            parse_mode=ParseMode.MARKDOWN)

    elif len(msg) != 0:
        msg += tld(chat.id, "note_get")
        update.effective_message.reply_text(msg.format(chat_name),
                                            parse_mode=ParseMode.MARKDOWN)


@run_async
@user_admin
def remove_all_notes(bot: Bot, update: Update):
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message

    if chat.type == "private":
        chat.title = tld(chat.id, "note_is_local")
    else:
        owner = chat.get_member(user.id)
        chat.title = chat.title
        if owner.status != 'creator':
            message.reply_text(tld(chat.id, "notes_must_be_creator"))
            return

    note_list = sql.get_all_chat_notes(chat.id)
    if not note_list:
        message.reply_text(tld(chat.id,
                               "note_none_in_chat").format(chat.title),
                           parse_mode=ParseMode.MARKDOWN)
        return

    x = 0
    a_note = []
    for notename in note_list:
        x += 1
        note = notename.name.lower()
        a_note.append(note)

    for note in a_note:
        sql.rm_note(chat.id, note)

    message.reply_text(tld(chat.id, "notes_cleanup_success").format(x))


def __stats__():
    return "• `{}` notes, accross `{}` chats.".format(sql.num_notes(),
                                                      sql.num_chats())


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


__help__ = True

GET_HANDLER = CommandHandler("get", cmd_get, pass_args=True)
HASH_GET_HANDLER = RegexHandler(r"^#[^\s]+", hash_get)

SAVE_HANDLER = CommandHandler("save", save)
REMOVE_ALL_NOTES_HANDLER = CommandHandler("clearall", remove_all_notes)
DELETE_HANDLER = CommandHandler("clear", clear, pass_args=True)

LIST_HANDLER = DisableAbleCommandHandler(["notes", "saved"],
                                         list_notes,
                                         admin_ok=True)

dispatcher.add_handler(GET_HANDLER)
dispatcher.add_handler(SAVE_HANDLER)
dispatcher.add_handler(LIST_HANDLER)
dispatcher.add_handler(DELETE_HANDLER)
dispatcher.add_handler(HASH_GET_HANDLER)
dispatcher.add_handler(REMOVE_ALL_NOTES_HANDLER)

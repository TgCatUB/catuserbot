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

import os
import math
import urllib.request as urllib

from PIL import Image

from typing import List
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import TelegramError
from telegram import Update, Bot
from telegram.ext import run_async
from telegram.utils.helpers import escape_markdown

from haruka import dispatcher
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.tr_engine.strings import tld


@run_async
def stickerid(bot: Bot, update: Update):
    chat = update.effective_chat
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(tld(
            chat.id, 'stickers_stickerid').format(
                escape_markdown(msg.reply_to_message.sticker.file_id)),
                                            parse_mode=ParseMode.MARKDOWN)
    else:
        update.effective_message.reply_text(
            tld(chat.id, 'stickers_stickerid_no_reply'))


@run_async
def getsticker(bot: Bot, update: Update):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        newFile = bot.get_file(file_id)
        newFile.download('images/sticker.png')
        bot.send_document(chat_id, document=open('images/sticker.png', 'rb'))
        os.remove("images/sticker.png")
    else:
        update.effective_message.reply_text(
            tld(chat_id, 'stickers_getsticker_no_reply'))


@run_async
def kang(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user
    packnum = 0
    packname = "c" + str(user.id) + "_by_" + bot.username
    packname_found = 0
    max_stickers = 120
    while packname_found == 0:
        try:
            stickerset = bot.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = "c" + str(packnum) + "_" + str(
                    user.id) + "_by_" + bot.username
            else:
                packname_found = 1
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                packname_found = 1
    kangsticker = "images/kangsticker.png"
    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            file_id = msg.reply_to_message.sticker.file_id
        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text(tld(chat.id, 'stickers_kang_error'))
        kang_file = bot.get_file(file_id)
        kang_file.download('images/kangsticker.png')
        if args:
            sticker_emoji = str(args[0])
        elif msg.reply_to_message.sticker and msg.reply_to_message.sticker.emoji:
            sticker_emoji = msg.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "🤔"
        try:
            im = Image.open(kangsticker)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            if not msg.reply_to_message.sticker:
                im.save(kangsticker, "PNG")
            bot.add_sticker_to_set(user_id=user.id,
                                   name=packname,
                                   png_sticker=open('images/kangsticker.png',
                                                    'rb'),
                                   emojis=sticker_emoji)
            msg.reply_text(tld(chat.id, 'stickers_kang_success').format(
                packname, sticker_emoji),
                           parse_mode=ParseMode.MARKDOWN)
        except OSError as e:
            msg.reply_text(tld(chat.id, 'stickers_kang_only_img'))
            print(e)
            return
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                makepack_internal(msg, user,
                                  open('images/kangsticker.png', 'rb'),
                                  sticker_emoji, bot, packname, packnum, chat)
            elif e.message == "Sticker_png_dimensions":
                im.save(kangsticker, "PNG")
                bot.add_sticker_to_set(user_id=user.id,
                                       name=packname,
                                       png_sticker=open(
                                           'images/kangsticker.png', 'rb'),
                                       emojis=sticker_emoji)
                msg.reply_text(tld(chat.id, 'stickers_kang_success').format(
                    packname, sticker_emoji),
                               parse_mode=ParseMode.MARKDOWN)
            elif e.message == "Invalid sticker emojis":
                msg.reply_text(tld(chat.id, 'stickers_kang_invalid_emoji'))
            elif e.message == "Stickers_too_much":
                msg.reply_text(tld(chat.id, 'stickers_kang_too_much'))
            elif e.message == "Internal Server Error: sticker set not found (500)":
                msg.reply_text(tld(chat.id, 'stickers_kang_success').format(
                    packname, sticker_emoji),
                               parse_mode=ParseMode.MARKDOWN)
            print(e)
    elif args:
        try:
            try:
                urlemoji = msg.text.split(" ")
                png_sticker = urlemoji[1]
                sticker_emoji = urlemoji[2]
            except IndexError:
                sticker_emoji = "🤔"
            urllib.urlretrieve(png_sticker, kangsticker)
            im = Image.open(kangsticker)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            im.save(kangsticker, "PNG")
            msg.reply_photo(photo=open('images/kangsticker.png', 'rb'))
            bot.add_sticker_to_set(user_id=user.id,
                                   name=packname,
                                   png_sticker=open('images/kangsticker.png',
                                                    'rb'),
                                   emojis=sticker_emoji)
            msg.reply_text(tld(chat.id, 'stickers_kang_success').format(
                packname, sticker_emoji),
                           parse_mode=ParseMode.MARKDOWN)
        except OSError as e:
            msg.reply_text(tld(chat.id, 'stickers_kang_only_img'))
            print(e)
            return
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                makepack_internal(msg, user,
                                  open('images/kangsticker.png', 'rb'),
                                  sticker_emoji, bot, packname, packnum, chat)
            elif e.message == "Sticker_png_dimensions":
                im.save(kangsticker, "PNG")
                bot.add_sticker_to_set(user_id=user.id,
                                       name=packname,
                                       png_sticker=open(
                                           'images/kangsticker.png', 'rb'),
                                       emojis=sticker_emoji)
                msg.reply_text(tld(chat.id, 'stickers_kang_success').format(
                    packname, sticker_emoji),
                               parse_mode=ParseMode.MARKDOWN)
            elif e.message == "Invalid sticker emojis":
                msg.reply_text(tld(chat.id, 'stickers_kang_invalid_emoji'))
            elif e.message == "Stickers_too_much":
                msg.reply_text(tld(chat.id, 'stickers_kang_too_much'))
            elif e.message == "Internal Server Error: sticker set not found (500)":
                msg.reply_text(tld(chat.id, 'stickers_kang_success').format(
                    packname, sticker_emoji),
                               parse_mode=ParseMode.MARKDOWN)
            print(e)
    else:
        packs = tld(chat.id, 'stickers_kang_no_reply')
        if packnum > 0:
            firstpackname = "c" + str(user.id) + "_by_" + bot.username
            for i in range(0, packnum + 1):
                if i == 0:
                    packs += f"[pack](t.me/addstickers/{firstpackname})\n"
                else:
                    packs += f"[pack{i}](t.me/addstickers/{packname})\n"
        else:
            packs += f"[pack](t.me/addstickers/{packname})"
        msg.reply_text(packs, parse_mode=ParseMode.MARKDOWN)
    if os.path.isfile("images/kangsticker.png"):
        os.remove("images/kangsticker.png")


def makepack_internal(msg, user, png_sticker, emoji, bot, packname, packnum,
                      chat):
    name = user.first_name
    name = name[:50]
    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        success = bot.create_new_sticker_set(user.id,
                                             packname,
                                             f"{name}s haruka pack" +
                                             extra_version,
                                             png_sticker=png_sticker,
                                             emojis=emoji)
    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text(tld(chat.id, 'stickers_pack_name_exists') %
                           packname,
                           parse_mode=ParseMode.MARKDOWN)
        elif e.message == "Peer_id_invalid":
            msg.reply_text(tld(chat.id, 'stickers_pack_contact_pm'),
                           reply_markup=InlineKeyboardMarkup([[
                               InlineKeyboardButton(text="Start",
                                                    url=f"t.me/{bot.username}")
                           ]]))
        elif e.message == "Internal Server Error: created sticker set not found (500)":
            msg.reply_text(tld(chat.id, 'stickers_kang_success').format(
                packname, sticker_emoji),
                           parse_mode=ParseMode.MARKDOWN)
        return

    if success:
        msg.reply_text(tld(chat.id,
                           'stickers_kang_success').format(packname, emoji),
                       parse_mode=ParseMode.MARKDOWN)
    else:
        msg.reply_text(tld(chat.id, 'stickers_pack_create_error'))


__help__ = True

STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker)
KANG_HANDLER = DisableAbleCommandHandler("kang",
                                         kang,
                                         pass_args=True,
                                         admin_ok=True)

dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(KANG_HANDLER)

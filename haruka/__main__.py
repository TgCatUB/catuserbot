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

import datetime
from sys import argv
import importlib
import re
from typing import List

from telegram import Update, Bot
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import (Unauthorized, BadRequest, TimedOut, NetworkError,
                            ChatMigrated, TelegramError)
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop, Dispatcher

# Needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from haruka.modules import ALL_MODULES
from haruka import dispatcher, updater, LOGGER, TOKEN, tbot
from haruka.modules.helper_funcs.misc import paginate_modules
from haruka.modules.tr_engine.strings import tld

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

GDPR = []

importlib.import_module("haruka.modules.tr_engine.language")

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("haruka.modules." + module_name)
    modname = imported_module.__name__.split('.')[2]

    if not modname.lower() in IMPORTED:
        IMPORTED[modname.lower()] = imported_module
    else:
        raise Exception(
            "Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[modname.lower()] = tld(0, "modname_" + modname).strip()

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)


# Do NOT async this!
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(
            paginate_modules(chat_id, 0, HELPABLE, "help"))

    dispatcher.bot.send_message(chat_id=chat_id,
                                text=text,
                                parse_mode=ParseMode.MARKDOWN,
                                reply_markup=keyboard,
                                disable_web_page_preview=True)


@run_async
def test(bot: Bot, update: Update):
    # pprint(eval(str(update)))
    # update.effective_message.reply_text("Hola tester! _I_ *have* `markdown`", parse_mode=ParseMode.MARKDOWN)
    update.effective_message.reply_text("This person edited a message")
    print(update.effective_message)


@run_async
def start(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    # query = update.callback_query #Unused variable
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(
                    update.effective_chat.id,
                    tld(chat.id,
                        "send-help").format(dispatcher.bot.first_name,
                                            tld(chat.id, "cmd_multitrigger")))

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            send_start(bot, update)
    else:
        try:
            update.effective_message.reply_text(
                tld(chat.id, 'main_start_group'))
        except Exception:
            print("Nut")


def send_start(bot, update):
    chat = update.effective_chat

    # chat = update.effective_chat and unused variable
    text = tld(chat.id, 'main_start_pm')

    keyboard = [[
        InlineKeyboardButton(text=tld(chat.id, 'main_start_btn_support'),
                             url="https://t.me/HarukaAyaGroup")
    ]]
    keyboard += [[
        InlineKeyboardButton(text=tld(chat.id, 'main_start_btn_lang'),
                             callback_data="set_lang_"),
        InlineKeyboardButton(text=tld(chat.id, 'btn_help'),
                             callback_data="help_back")
    ]]

    try:
        query = update.callback_query
        # query.message.delete()
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text=text,
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=InlineKeyboardMarkup(keyboard),
                              disable_web_page_preview=True)
    except Exception:
        pass

    if query:
        try:
            bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=text,
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=InlineKeyboardMarkup(keyboard),
                                  disable_web_page_preview=True)
        except Exception:
            return
    else:
        update.effective_message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)


# for test purposes
def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        LOGGER.warning(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        LOGGER.warning(error)

        # handle malformed requests - read more below!
    except TimedOut:
        LOGGER.warning("NO NONO3")
        # handle slow connection problems
    except NetworkError:
        LOGGER.warning("NO NONO4")
        # handle other connection problems
    except ChatMigrated as err:
        LOGGER.warning(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        LOGGER.warning(error)
        # handle all other telegram related errors


@run_async
def help_button(bot: Bot, update: Update):
    query = update.callback_query
    chat = update.effective_chat
    back_match = re.match(r"help_back", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    try:
        if mod_match:
            module = mod_match.group(1)
            mod_name = tld(chat.id, "modname_" + module).strip()
            help_txt = tld(
                chat.id, module +
                "_help")  # tld_help(chat.id, HELPABLE[module].__mod_name__)

            if not help_txt:
                LOGGER.exception(f"Help string for {module} not found!")

            text = tld(chat.id, "here_is_help").format(mod_name, help_txt)

            bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=text,
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=InlineKeyboardMarkup([[
                                      InlineKeyboardButton(
                                          text=tld(chat.id, "btn_go_back"),
                                          callback_data="help_back")
                                  ]]),
                                  disable_web_page_preview=True)

        elif back_match:
            bot.edit_message_text(chat_id=query.message.chat_id,
                                  message_id=query.message.message_id,
                                  text=tld(chat.id, "send-help").format(
                                      dispatcher.bot.first_name,
                                      tld(chat.id, "cmd_multitrigger")),
                                  parse_mode=ParseMode.MARKDOWN,
                                  reply_markup=InlineKeyboardMarkup(
                                      paginate_modules(chat.id, 0, HELPABLE,
                                                       "help")),
                                  disable_web_page_preview=True)

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


@run_async
def get_help(bot: Bot, update: Update):
    chat = update.effective_chat
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        update.effective_message.reply_text(
            tld(chat.id, 'help_pm_only'),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(text=tld(chat.id, 'btn_help'),
                                     url="t.me/{}?start=help".format(
                                         bot.username))
            ]]))
        return

    if len(args) >= 2:
        mod_name = None
        for x in HELPABLE:
            if args[1].lower() == HELPABLE[x].lower():
                mod_name = tld(chat.id, "modname_" + x).strip()
                module = x
                break

        if mod_name:
            help_txt = tld(chat.id, module + "_help")

            if not help_txt:
                LOGGER.exception(f"Help string for {module} not found!")

            text = tld(chat.id, "here_is_help").format(mod_name, help_txt)
            send_help(
                chat.id, text,
                InlineKeyboardMarkup([[
                    InlineKeyboardButton(text=tld(chat.id, "btn_go_back"),
                                         callback_data="help_back")
                ]]))

            return

        update.effective_message.reply_text(tld(
            chat.id, "help_not_found").format(args[1]),
                                            parse_mode=ParseMode.HTML)
        return

    send_help(
        chat.id,
        tld(chat.id, "send-help").format(dispatcher.bot.first_name,
                                         tld(chat.id, "cmd_multitrigger")))


def migrate_chats(bot: Bot, update: Update):
    msg = update.effective_message
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    raise DispatcherHandlerStop


def main():
    # test_handler = CommandHandler("test", test) #Unused variable
    start_handler = CommandHandler("start", start, pass_args=True)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")

    start_callback_handler = CallbackQueryHandler(send_start,
                                                  pattern=r"bot_start")

    migrate_handler = MessageHandler(Filters.status_update.migrate,
                                     migrate_chats)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(start_callback_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(migrate_handler)
    # dispatcher.add_error_handler(error_callback)

    # add antiflood processor
    Dispatcher.process_update = process_update

    LOGGER.info("Using long polling.")
    # updater.start_polling(timeout=15, read_latency=4, clean=True)
    updater.start_polling(poll_interval=0.0,
                          timeout=10,
                          clean=True,
                          bootstrap_retries=-1,
                          read_latency=3.0)

    LOGGER.info("Successfully loaded")
    if len(argv) not in (1, 3, 4):
        tbot.disconnect()
    else:
        tbot.run_until_disconnected()

    updater.idle()


CHATS_CNT = {}
CHATS_TIME = {}


def process_update(self, update):
    # An error happened while polling
    if isinstance(update, TelegramError):
        try:
            self.dispatch_error(None, update)
        except Exception:
            self.logger.exception(
                'An uncaught error was raised while handling the error')
        return

    if update.effective_chat:  # Checks if update contains chat object
        now = datetime.datetime.utcnow()
    try:
        cnt = CHATS_CNT.get(update.effective_chat.id, 0)
    except AttributeError:
        self.logger.exception(
            'An uncaught error was raised while updating process')
        return

    t = CHATS_TIME.get(update.effective_chat.id, datetime.datetime(1970, 1, 1))
    if t and now > t + datetime.timedelta(0, 1):
        CHATS_TIME[update.effective_chat.id] = now
        cnt = 0
    else:
        cnt += 1

    if cnt > 10:
        return

    CHATS_CNT[update.effective_chat.id] = cnt

    for group in self.groups:
        try:
            for handler in (x for x in self.handlers[group]
                            if x.check_update(update)):
                handler.handle_update(update, self)
                break

        # Stop processing with any other handler.
        except DispatcherHandlerStop:
            self.logger.debug(
                'Stopping further handlers due to DispatcherHandlerStop')
            break

        # Dispatch any error.
        except TelegramError as te:
            self.logger.warning(
                'A TelegramError was raised while processing the Update')

            try:
                self.dispatch_error(update, te)
            except DispatcherHandlerStop:
                self.logger.debug('Error handler stopped further handlers')
                break
            except Exception:
                self.logger.exception(
                    'An uncaught error was raised while handling the error')

        # Errors should not stop the thread.
        except Exception:
            self.logger.exception(
                'An uncaught error was raised while processing the update')


if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    tbot.start(bot_token=TOKEN)
    main()

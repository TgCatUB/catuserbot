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

import random
from typing import Optional, List

from telegram import Message, Update, Bot, ParseMode, Chat
from telegram.ext import run_async

from haruka import dispatcher
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.string_handling import remove_emoji
from haruka.modules.tr_engine.strings import tld, tld_list

from googletrans import LANGUAGES, Translator


@run_async
def do_translate(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]
    lan = " ".join(args)

    if msg.reply_to_message and (msg.reply_to_message.audio
                                 or msg.reply_to_message.voice) or (
                                     args and args[0] == 'animal'):
        reply = random.choice(tld_list(chat.id, 'translator_animal_lang'))

        if args:
            translation_type = "text"
        else:
            translation_type = "audio"

        msg.reply_text(tld(chat.id, 'translator_animal_translated').format(
            translation_type, reply),
                       parse_mode=ParseMode.MARKDOWN)
        return

    if msg.reply_to_message:
        to_translate_text = remove_emoji(msg.reply_to_message.text)
    else:
        msg.reply_text(tld(chat.id, "translator_no_str"))
        return

    if not args:
        msg.reply_text(tld(chat.id, 'translator_no_args'))
        return

    translator = Translator()
    try:
        translated = translator.translate(to_translate_text, dest=lan)
    except ValueError as e:
        msg.reply_text(tld(chat.id, 'translator_err').format(e))

    src_lang = LANGUAGES[f'{translated.src.lower()}'].title()
    dest_lang = LANGUAGES[f'{translated.dest.lower()}'].title()
    translated_text = translated.text
    msg.reply_text(tld(chat.id,
                       'translator_translated').format(src_lang,
                                                       to_translate_text,
                                                       dest_lang,
                                                       translated_text),
                   parse_mode=ParseMode.MARKDOWN)


__help__ = True

dispatcher.add_handler(
    DisableAbleCommandHandler("tr", do_translate, pass_args=True))

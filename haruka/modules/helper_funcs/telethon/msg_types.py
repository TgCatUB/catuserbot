#    Haruka Aya (A telegram bot project)
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
from enum import IntEnum, unique

from telethon import utils
from haruka.modules.helper_funcs.string_handler import message_parser

NOTE_REGEX = re.compile(r"(^\S+|^\".*\")(?: |$)")


@unique
class Types(IntEnum):
    TEXT = 0
    BUTTON_TEXT = 1
    FILE = 2


async def get_note_type(message):
    data_type = None
    content = None
    text = ""
    split = message.text[len("/save "):]
    splitter = re.match(NOTE_REGEX, split)
    note_name = splitter.group(1).strip('"')

    reply = await message.get_reply_message()

    buttons = []
    # determine what the contents of the filter are - text, image, sticker, etc
    if not reply:
        note = re.sub(NOTE_REGEX, "", split)
        text, buttons = message_parser(note)
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            if len(text) != 0:
                data_type = Types.TEXT

    elif reply and reply.text:
        text, buttons = message_parser(reply.text)
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            data_type = Types.TEXT

    elif reply and reply.media:
        content = utils.pack_bot_file_id(reply.media)
        text = reply.text
        data_type = Types.FILE

    string = re.sub(' +', ' ', text).strip()
    return note_name, string, data_type, content, buttons


async def get_message_type(message, split: None):
    data_type = None
    content = None
    text = ""
    reply = await message.get_reply_message()

    buttons = []
    # determine what the contents of the filter are - text, image, sticker, etc
    if split:
        text, buttons = message_parser(split)
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            data_type = Types.TEXT

    elif reply and reply.media:
        content = utils.pack_bot_file_id(reply.media)
        text = reply.text
        data_type = Types.FILE

    string = re.sub(' +', ' ', text).strip()
    return string, data_type, content, buttons

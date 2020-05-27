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

from enum import IntEnum, unique

from telegram import Message

from haruka.modules.helper_funcs.string_handling import button_markdown_parser


@unique
class Types(IntEnum):
    TEXT = 0
    BUTTON_TEXT = 1
    STICKER = 2
    DOCUMENT = 3
    PHOTO = 4
    AUDIO = 5
    VOICE = 6
    VIDEO = 7
    VIDEO_NOTE = 8


def get_note_type(msg: Message):
    data_type = None
    content = None
    text = ""
    raw_text = msg.text or msg.caption
    args = raw_text.split(None,
                          2)  # use python's maxsplit to separate cmd and args
    note_name = args[1]

    buttons = []
    # determine what the contents of the filter are - text, image, sticker, etc
    if len(args) >= 3:
        offset = len(args[2]) - len(
            raw_text)  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(args[2],
                                               entities=msg.parse_entities()
                                               or msg.parse_caption_entities(),
                                               offset=offset)
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            data_type = Types.TEXT

    elif msg.reply_to_message:
        entities = msg.reply_to_message.parse_entities()
        msgtext = msg.reply_to_message.text or msg.reply_to_message.caption
        if len(args) >= 2 and msg.reply_to_message.text:  # not caption, text
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            if buttons:
                data_type = Types.BUTTON_TEXT
            else:
                data_type = Types.TEXT

        elif msg.reply_to_message.sticker:
            content = msg.reply_to_message.sticker.file_id
            data_type = Types.STICKER

        elif msg.reply_to_message.document:
            content = msg.reply_to_message.document.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.DOCUMENT

        elif msg.reply_to_message.photo:
            content = msg.reply_to_message.photo[
                -1].file_id  # last elem = best quality
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.PHOTO

        elif msg.reply_to_message.audio:
            content = msg.reply_to_message.audio.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.AUDIO

        elif msg.reply_to_message.voice:
            content = msg.reply_to_message.voice.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VOICE

        elif msg.reply_to_message.video:
            content = msg.reply_to_message.video.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VIDEO

        elif msg.reply_to_message.video_note:
            content = msg.reply_to_message.video_note.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VIDEO_NOTE

    return note_name, text, data_type, content, buttons


# note: add own args?
def get_welcome_type(msg: Message):
    data_type = None
    content = None
    text = ""

    try:
        if msg.reply_to_message:
            if msg.reply_to_message.text:
                args = msg.reply_to_message.text
            else:
                args = msg.reply_to_message.caption
        else:
            args = msg.text.split(
                None, 1)  # use python's maxsplit to separate cmd and args
    except AttributeError:
        args = False

    buttons = []
    # determine what the contents of the filter are - text, image, sticker, etc
    if args:
        if msg.reply_to_message:
            if msg.reply_to_message.caption:
                argumen = msg.reply_to_message.caption
            elif msg.reply_to_message.text:
                argumen = msg.reply_to_message.text
        else:
            argumen = args[1]
        offset = len(argumen) - len(
            msg.text)  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(argumen,
                                               entities=msg.parse_entities(),
                                               offset=offset)
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            data_type = Types.TEXT

    if msg.reply_to_message and msg.reply_to_message.sticker:
        content = msg.reply_to_message.sticker.file_id
        text = None
        data_type = Types.STICKER

    elif msg.reply_to_message and msg.reply_to_message.document:
        content = msg.reply_to_message.document.file_id
        # text = msg.reply_to_message.caption
        data_type = Types.DOCUMENT

    elif msg.reply_to_message and msg.reply_to_message.photo:
        content = msg.reply_to_message.photo[
            -1].file_id  # last elem = best quality
        # text = msg.reply_to_message.caption
        data_type = Types.PHOTO

    elif msg.reply_to_message and msg.reply_to_message.audio:
        content = msg.reply_to_message.audio.file_id
        # text = msg.reply_to_message.caption
        data_type = Types.AUDIO

    elif msg.reply_to_message and msg.reply_to_message.voice:
        content = msg.reply_to_message.voice.file_id
        text = None
        data_type = Types.VOICE

    elif msg.reply_to_message and msg.reply_to_message.video:
        content = msg.reply_to_message.video.file_id
        # text = msg.reply_to_message.caption
        data_type = Types.VIDEO

    elif msg.reply_to_message and msg.reply_to_message.video_note:
        content = msg.reply_to_message.video_note.file_id
        text = None
        data_type = Types.VIDEO_NOTE

    return text, data_type, content, buttons


def get_message_type(msg: Message):
    data_type = None
    content = None
    text = ""
    raw_text = msg.text or msg.caption
    args = raw_text.split(None,
                          1)  # use python's maxsplit to separate cmd and args

    buttons = []
    # determine what the contents of the filter are - text, image, sticker, etc
    if len(args) >= 2:
        offset = len(args[1]) - len(
            raw_text)  # set correct offset relative to command + notename
        text, buttons = button_markdown_parser(args[1],
                                               entities=msg.parse_entities()
                                               or msg.parse_caption_entities(),
                                               offset=offset)
        if buttons:
            data_type = Types.BUTTON_TEXT
        else:
            data_type = Types.TEXT

    elif msg.reply_to_message:
        entities = msg.reply_to_message.parse_entities()
        msgtext = msg.reply_to_message.text or msg.reply_to_message.caption
        if len(args) >= 1 and msg.reply_to_message.text:  # not caption, text
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            if buttons:
                data_type = Types.BUTTON_TEXT
            else:
                data_type = Types.TEXT

        elif msg.reply_to_message.sticker:
            content = msg.reply_to_message.sticker.file_id
            data_type = Types.STICKER

        elif msg.reply_to_message.document:
            content = msg.reply_to_message.document.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.DOCUMENT

        elif msg.reply_to_message.photo:
            content = msg.reply_to_message.photo[
                -1].file_id  # last elem = best quality
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.PHOTO

        elif msg.reply_to_message.audio:
            content = msg.reply_to_message.audio.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.AUDIO

        elif msg.reply_to_message.voice:
            content = msg.reply_to_message.voice.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VOICE

        elif msg.reply_to_message.video:
            content = msg.reply_to_message.video.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VIDEO

        elif msg.reply_to_message.video_note:
            content = msg.reply_to_message.video_note.file_id
            text, buttons = button_markdown_parser(msgtext, entities=entities)
            data_type = Types.VIDEO_NOTE

    return text, data_type, content, buttons

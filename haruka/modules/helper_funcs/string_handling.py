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
import time
from typing import Dict, List
import bleach
import markdown2

import emoji
from telegram import MessageEntity
from telegram.utils.helpers import escape_markdown

from haruka.modules.tr_engine.strings import tld

# NOTE: the url \ escape may cause double escapes
# match * (bold) (don't escape if in url)
# match _ (italics) (don't escape if in url)
# match ` (code)
# match []() (markdown link)
# else, escape *, _, `, and [
MATCH_MD = re.compile(r'\*(.*?)\*|'
                      r'_(.*?)_|'
                      r'`(.*?)`|'
                      r'(?<!\\)(\[.*?\])(\(.*?\))|'
                      r'(?P<esc>[*_`\[])')

# regex to find []() links -> hyperlinks/buttons
LINK_REGEX = re.compile(r'(?<!\\)\[.+?\]\((.*?)\)')
BTN_URL_REGEX = re.compile(
    r"(\[([^\[]+?)\]\(buttonurl:(?:/{0,2})(.+?)(:same)?\))")


def _selective_escape(to_parse: str) -> str:
    """
    Escape all invalid markdown

    :param to_parse: text to escape
    :return: valid markdown string
    """
    offset = 0  # offset to be used as adding a \ character causes the string to shift
    for match in MATCH_MD.finditer(to_parse):
        if match.group('esc'):
            ent_start = match.start()
            to_parse = to_parse[:ent_start +
                                offset] + '\\' + to_parse[ent_start + offset:]
            offset += 1
    return to_parse


# This is a fun one.
def _calc_emoji_offset(to_calc) -> int:
    # Get all emoji in text.
    emoticons = emoji.get_emoji_regexp().finditer(to_calc)
    # Check the utf16 length of the emoji to determine the offset it caused.
    # Normal, 1 character emoji don't affect; hence sub 1.
    # special, eg with two emoji characters (eg face, and skin col) will have length 2, so by subbing one we
    # know we'll get one extra offset,
    return sum(len(e.group(0).encode('utf-16-le')) // 2 - 1 for e in emoticons)


def markdown_parser(txt: str,
                    entities: Dict[MessageEntity, str] = None,
                    offset: int = 0) -> str:
    """
    Parse a string, escaping all invalid markdown entities.

    Escapes URL's so as to avoid URL mangling.
    Re-adds any telegram code entities obtained from the entities object.

    :param txt: text to parse
    :param entities: dict of message entities in text
    :param offset: message offset - command and notename length
    :return: valid markdown string
    """
    if not entities:
        entities = {}
    if not txt:
        return ""

    prev = 0
    res = ""
    # Loop over all message entities, and:
    # reinsert code
    # escape free-standing urls
    for ent, ent_text in entities.items():
        if ent.offset < -offset:
            continue

        start = ent.offset + offset  # start of entity
        end = ent.offset + offset + ent.length - 1  # end of entity

        # we only care about code, url, text links
        if ent.type in ("code", "url", "text_link"):
            # count emoji to switch counter
            count = _calc_emoji_offset(txt[:start])
            start -= count
            end -= count

            # URL handling -> do not escape if in [](), escape otherwise.
            if ent.type == "url":
                if any(
                        match.start(1) <= start and end <= match.end(1)
                        for match in LINK_REGEX.finditer(txt)):
                    continue
                # else, check the escapes between the prev and last and forcefully escape the url to avoid mangling
                else:
                    # TODO: investigate possible offset bug when lots of emoji are present
                    res += _selective_escape(txt[prev:start]
                                             or "") + escape_markdown(ent_text)

            # code handling
            elif ent.type == "code":
                res += _selective_escape(
                    txt[prev:start]) + '`' + ent_text + '`'

            # handle markdown/html links
            elif ent.type == "text_link":
                res += _selective_escape(txt[prev:start]) + "[{}]({})".format(
                    ent_text, ent.url)

            end += 1

        # anything else
        else:
            continue

        prev = end

    res += _selective_escape(txt[prev:])  # add the rest of the text
    return res


def button_markdown_parser(txt: str,
                           entities: Dict[MessageEntity, str] = None,
                           offset: int = 0) -> (str, List):
    markdown_note = markdown_parser(txt, entities, offset)
    prev = 0
    note_data = ""
    buttons = []
    for match in BTN_URL_REGEX.finditer(markdown_note):
        # Check if btnurl is escaped
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and markdown_note[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        # if even, not escaped -> create button
        if n_escapes % 2 == 0:
            # create a thruple with button label, url, and newline status
            buttons.append(
                (match.group(2), match.group(3), bool(match.group(4))))
            note_data += markdown_note[prev:match.start(1)]
            prev = match.end(1)
        # if odd, escaped -> move along
        else:
            note_data += markdown_note[prev:to_check]
            prev = match.start(1) - 1
    else:
        note_data += markdown_note[prev:]

    return note_data, buttons


def escape_invalid_curly_brackets(text: str, valids: List[str]) -> str:
    new_text = ""
    idx = 0
    while idx < len(text):
        if text[idx] == "{":
            if idx + 1 < len(text) and text[idx + 1] == "{":
                idx += 2
                new_text += "{{{{"
                continue
            else:
                success = False
                for v in valids:
                    if text[idx:].startswith('{' + v + '}'):
                        success = True
                        break
                if success:
                    new_text += text[idx:idx + len(v) + 2]
                    idx += len(v) + 2
                    continue
                else:
                    new_text += "{{"

        elif text[idx] == "}":
            if idx + 1 < len(text) and text[idx + 1] == "}":
                idx += 2
                new_text += "}}}}"
                continue
            else:
                new_text += "}}"

        else:
            new_text += text[idx]
        idx += 1

    return new_text


SMART_OPEN = '“'
SMART_CLOSE = '”'
START_CHAR = ('\'', '"', SMART_OPEN)


def split_quotes(text: str) -> List:
    if any(text.startswith(char) for char in START_CHAR):
        counter = 1  # ignore first char -> is some kind of quote
        while counter < len(text):
            if text[counter] == "\\":
                counter += 1
            elif text[counter] == text[0] or (text[0] == SMART_OPEN and
                                              text[counter] == SMART_CLOSE):
                break
            counter += 1
        else:
            return text.split(None, 1)

        # 1 to avoid starting quote, and counter is exclusive so avoids ending
        key = remove_escapes(text[1:counter].strip())
        # index will be in range, or `else` would have been executed and returned
        rest = text[counter + 1:].strip()
        if not key:
            key = text[0] + text[0]
        return list(filter(None, [key, rest]))
    else:
        return text.split(None, 1)


def remove_escapes(text: str) -> str:
    counter = 0
    res = ""
    is_escaped = False
    while counter < len(text):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
        counter += 1
    return res


def escape_chars(text: str, to_escape: List[str]) -> str:
    to_escape.append("\\")
    new_text = ""
    for x in text:
        if x in to_escape:
            new_text += "\\"
        new_text += x
    return new_text


def extract_time(message, time_val):
    if any(time_val.endswith(unit) for unit in ('m', 'h', 'd')):
        chat = message.chat
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            message.reply_text(
                tld(chat.id, 'helpers_string_handling_invalid_time_amount'))
            return ""

        if unit == 'm':
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == 'h':
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == 'd':
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            # how even...?
            return ""
        return bantime
    else:
        message.reply_text(
            tld(chat.id, 'helpers_string_handling_invalid_time_type').format(
                time_val[-1]))
        return ""


def markdown_to_html(text):
    text = text.replace("*", "**")
    text = text.replace("`", "```")
    _html = markdown2.markdown(text)
    return bleach.clean(_html,
                        tags=['strong', 'em', 'a', 'code', 'pre'],
                        strip=True)[:-1]


def remove_emoji(inputString):
    """ Remove emojis and other non-safe characters from string """
    return emoji.get_emoji_regexp().sub(u'', inputString)

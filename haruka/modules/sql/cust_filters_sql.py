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

import threading

from sqlalchemy import Column, String, UnicodeText, Boolean, Integer, distinct, func

from haruka.modules.sql import BASE, SESSION


class CustomFilters(BASE):
    __tablename__ = "cust_filters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText, nullable=False)
    is_sticker = Column(Boolean, nullable=False, default=False)
    is_document = Column(Boolean, nullable=False, default=False)
    is_image = Column(Boolean, nullable=False, default=False)
    is_audio = Column(Boolean, nullable=False, default=False)
    is_voice = Column(Boolean, nullable=False, default=False)
    is_video = Column(Boolean, nullable=False, default=False)

    has_buttons = Column(Boolean, nullable=False, default=False)
    # NOTE: Here for legacy purposes, to ensure older filters don't mess up.
    has_markdown = Column(Boolean, nullable=False, default=False)

    def __init__(self,
                 chat_id,
                 keyword,
                 reply,
                 is_sticker=False,
                 is_document=False,
                 is_image=False,
                 is_audio=False,
                 is_voice=False,
                 is_video=False,
                 has_buttons=False):
        self.chat_id = str(chat_id)  # ensure string
        self.keyword = keyword
        self.reply = reply
        self.is_sticker = is_sticker
        self.is_document = is_document
        self.is_image = is_image
        self.is_audio = is_audio
        self.is_voice = is_voice
        self.is_video = is_video
        self.has_buttons = has_buttons
        self.has_markdown = True

    def __repr__(self):
        return "<Permissions for %s>" % self.chat_id

    def __eq__(self, other):
        return bool(
            isinstance(other, CustomFilters) and self.chat_id == other.chat_id
            and self.keyword == other.keyword)


class Buttons(BASE):
    __tablename__ = "cust_filter_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, keyword, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.name = name
        self.url = url
        self.same_line = same_line


CustomFilters.__table__.create(checkfirst=True)
Buttons.__table__.create(checkfirst=True)

CUST_FILT_LOCK = threading.RLock()
BUTTON_LOCK = threading.RLock()
CHAT_FILTERS = {}


def get_all_filters():
    try:
        return SESSION.query(CustomFilters).all()
    finally:
        SESSION.close()


def add_filter(chat_id,
               keyword,
               reply,
               is_sticker=False,
               is_document=False,
               is_image=False,
               is_audio=False,
               is_voice=False,
               is_video=False,
               buttons=None):
    global CHAT_FILTERS

    if buttons is None:
        buttons = []

    with CUST_FILT_LOCK:
        prev = SESSION.query(CustomFilters).get((str(chat_id), keyword))
        if prev:
            with BUTTON_LOCK:
                prev_buttons = SESSION.query(Buttons).filter(
                    Buttons.chat_id == str(chat_id),
                    Buttons.keyword == keyword).all()
                for btn in prev_buttons:
                    SESSION.delete(btn)
            SESSION.delete(prev)

        filt = CustomFilters(str(chat_id), keyword, reply, is_sticker,
                             is_document, is_image, is_audio, is_voice,
                             is_video, bool(buttons))

        if keyword not in CHAT_FILTERS.get(str(chat_id), []):
            CHAT_FILTERS[str(chat_id)] = sorted(
                CHAT_FILTERS.get(str(chat_id), []) + [keyword],
                key=lambda x: (-len(x), x))

        SESSION.add(filt)
        SESSION.commit()

    for b_name, url, same_line in buttons:
        add_note_button_to_db(chat_id, keyword, b_name, url, same_line)


def remove_filter(chat_id, keyword):
    global CHAT_FILTERS
    with CUST_FILT_LOCK:
        filt = SESSION.query(CustomFilters).get((str(chat_id), keyword))
        if filt:
            if keyword in CHAT_FILTERS.get(str(chat_id), []):  # Sanity check
                CHAT_FILTERS.get(str(chat_id), []).remove(keyword)

            with BUTTON_LOCK:
                prev_buttons = SESSION.query(Buttons).filter(
                    Buttons.chat_id == str(chat_id),
                    Buttons.keyword == keyword).all()
                for btn in prev_buttons:
                    SESSION.delete(btn)

            SESSION.delete(filt)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def get_chat_triggers(chat_id):
    return CHAT_FILTERS.get(str(chat_id), set())


def get_chat_filters(chat_id):
    try:
        return SESSION.query(CustomFilters).filter(
            CustomFilters.chat_id == str(chat_id)).order_by(
                func.length(CustomFilters.keyword).desc()).order_by(
                    CustomFilters.keyword.asc()).all()
    finally:
        SESSION.close()


def get_filter(chat_id, keyword):
    try:
        return SESSION.query(CustomFilters).get((str(chat_id), keyword))
    finally:
        SESSION.close()


def add_note_button_to_db(chat_id, keyword, b_name, url, same_line):
    with BUTTON_LOCK:
        button = Buttons(chat_id, keyword, b_name, url, same_line)
        SESSION.add(button)
        SESSION.commit()


def get_buttons(chat_id, keyword):
    try:
        return SESSION.query(Buttons).filter(
            Buttons.chat_id == str(chat_id),
            Buttons.keyword == keyword).order_by(Buttons.id).all()
    finally:
        SESSION.close()


def num_filters():
    try:
        return SESSION.query(CustomFilters).count()
    finally:
        SESSION.close()


def num_chats():
    try:
        return SESSION.query(func.count(distinct(
            CustomFilters.chat_id))).scalar()
    finally:
        SESSION.close()


def __load_chat_filters():
    global CHAT_FILTERS
    try:
        chats = SESSION.query(CustomFilters.chat_id).distinct().all()
        for (chat_id, ) in chats:  # remove tuple by ( ,)
            CHAT_FILTERS[chat_id] = []

        all_filters = SESSION.query(CustomFilters).all()
        for x in all_filters:
            CHAT_FILTERS[x.chat_id] += [x.keyword]

        CHAT_FILTERS = {
            x: sorted(set(y), key=lambda i: (-len(i), i))
            for x, y in CHAT_FILTERS.items()
        }

    finally:
        SESSION.close()


def migrate_chat(old_chat_id, new_chat_id):
    with CUST_FILT_LOCK:
        chat_filters = SESSION.query(CustomFilters).filter(
            CustomFilters.chat_id == str(old_chat_id)).all()
        for filt in chat_filters:
            filt.chat_id = str(new_chat_id)
        SESSION.commit()
        CHAT_FILTERS[str(new_chat_id)] = CHAT_FILTERS[str(old_chat_id)]
        del CHAT_FILTERS[str(old_chat_id)]

        with BUTTON_LOCK:
            chat_buttons = SESSION.query(Buttons).filter(
                Buttons.chat_id == str(old_chat_id)).all()
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)
            SESSION.commit()


__load_chat_filters()

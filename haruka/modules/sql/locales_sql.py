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
from sqlalchemy import Column, String, UnicodeText
from haruka.modules.sql import SESSION, BASE


class Locales(BASE):
    __tablename__ = "locales"
    chat_id = Column(String(14), primary_key=True)
    locale_name = Column(UnicodeText)

    def __init__(self, chat_id, locale_name):
        self.chat_id = str(chat_id)  # ensure string
        self.locale_name = locale_name


Locales.__table__.create(checkfirst=True)
LOCALES_INSERTION_LOCK = threading.RLock()


def switch_to_locale(chat_id, locale_name):
    with LOCALES_INSERTION_LOCK:
        prev = SESSION.query(Locales).get((str(chat_id)))
        if prev:
            SESSION.delete(prev)
        switch_locale = Locales(str(chat_id), locale_name)
        SESSION.add(switch_locale)
        SESSION.commit()


def prev_locale(chat_id):
    try:
        return SESSION.query(Locales).get((str(chat_id)))
    finally:
        SESSION.close()

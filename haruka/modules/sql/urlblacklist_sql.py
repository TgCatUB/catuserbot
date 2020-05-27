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

from haruka.modules.sql import BASE, SESSION


class URLBlackListFilters(BASE):
    __tablename__ = "url_blacklist"
    chat_id = Column(String(14), primary_key=True)
    domain = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, chat_id, domain):
        self.chat_id = str(chat_id)
        self.domain = str(domain)


URLBlackListFilters.__table__.create(checkfirst=True)

URL_BLACKLIST_FILTER_INSERTION_LOCK = threading.RLock()

CHAT_URL_BLACKLISTS = {}


def blacklist_url(chat_id, domain):
    with URL_BLACKLIST_FILTER_INSERTION_LOCK:
        domain_filt = URLBlackListFilters(str(chat_id), domain)

        SESSION.merge(domain_filt)
        SESSION.commit()
        CHAT_URL_BLACKLISTS.setdefault(str(chat_id), set()).add(domain)


def rm_url_from_blacklist(chat_id, domain):
    with URL_BLACKLIST_FILTER_INSERTION_LOCK:
        domain_filt = SESSION.query(URLBlackListFilters).get(
            (str(chat_id), domain))
        if domain_filt:
            if domain in CHAT_URL_BLACKLISTS.get(str(chat_id), set()):
                CHAT_URL_BLACKLISTS.get(str(chat_id), set()).remove(domain)
            SESSION.delete(domain_filt)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def get_blacklisted_urls(chat_id):
    return CHAT_URL_BLACKLISTS.get(str(chat_id), set())


def _load_chat_blacklist():
    global CHAT_URL_BLACKLISTS
    try:
        chats = SESSION.query(URLBlackListFilters.chat_id).distinct().all()
        for (chat_id, ) in chats:
            CHAT_URL_BLACKLISTS[chat_id] = []

        all_urls = SESSION.query(URLBlackListFilters).all()
        for url in all_urls:
            CHAT_URL_BLACKLISTS[url.chat_id] += [url.domain]
        CHAT_URL_BLACKLISTS = {
            k: set(v)
            for k, v in CHAT_URL_BLACKLISTS.items()
        }
    finally:
        SESSION.close()


_load_chat_blacklist()

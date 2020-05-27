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
from typing import Union

from sqlalchemy import Column, String, Boolean, Integer

from haruka.modules.sql import SESSION, BASE


class ChatAccessConnectionSettings(BASE):
    __tablename__ = "access_connection"
    chat_id = Column(String(14), primary_key=True)
    allow_connect_to_chat = Column(Boolean, default=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)

    def __repr__(self):
        return "<Chat access settings ({})>".format(self.chat_id)


class Connection(BASE):
    __tablename__ = "connection"
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(String(14))

    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = str(chat_id)  #Ensure String


class ConnectionHistory(BASE):
    __tablename__ = "connection_history5"
    user_id = Column(Integer, primary_key=True)
    chat_id1 = Column(String(14))
    chat_id2 = Column(String(14))
    chat_id3 = Column(String(14))
    updated = Column(Integer)

    def __init__(self, user_id, chat_id1, chat_id2, chat_id3, updated):
        self.user_id = user_id
        self.chat_id1 = str(chat_id1)  #Ensure String
        self.chat_id2 = str(chat_id2)  #Ensure String
        self.chat_id3 = str(chat_id3)  #Ensure String
        self.updated = updated


ChatAccessConnectionSettings.__table__.create(checkfirst=True)
Connection.__table__.create(checkfirst=True)
ConnectionHistory.__table__.create(checkfirst=True)

CHAT_ACCESS_LOCK = threading.RLock()
CONNECTION_INSERTION_LOCK = threading.RLock()
HISTORY_LOCK = threading.RLock()


def add_history(user_id, chat_id1, chat_id2, chat_id3, updated):
    with HISTORY_LOCK:
        prev = SESSION.query(ConnectionHistory).get((int(user_id)))
        if prev:
            SESSION.delete(prev)
        history = ConnectionHistory(user_id, chat_id1, chat_id2, chat_id3,
                                    updated)
        SESSION.add(history)
        SESSION.commit()


def get_history(user_id):
    try:
        return SESSION.query(ConnectionHistory).get(str(user_id))
    finally:
        SESSION.close()


def allow_connect_to_chat(chat_id: Union[str, int]) -> bool:
    try:
        chat_setting = SESSION.query(ChatAccessConnectionSettings).get(
            str(chat_id))
        if chat_setting:
            return chat_setting.allow_connect_to_chat
        return False
    finally:
        SESSION.close()


def set_allow_connect_to_chat(chat_id: Union[int, str], setting: bool):
    with CHAT_ACCESS_LOCK:
        chat_setting = SESSION.query(ChatAccessConnectionSettings).get(
            str(chat_id))
        if not chat_setting:
            chat_setting = ChatAccessConnectionSettings(chat_id)

        chat_setting.allow_connect_to_chat = setting
        SESSION.add(chat_setting)
        SESSION.commit()


def connect(user_id, chat_id):
    with CONNECTION_INSERTION_LOCK:
        prev = SESSION.query(Connection).get((int(user_id)))
        if prev:
            SESSION.delete(prev)
        connect_to_chat = Connection(int(user_id), chat_id)
        SESSION.add(connect_to_chat)
        SESSION.commit()
        return True


def get_connected_chat(user_id):
    try:
        return SESSION.query(Connection).get((int(user_id)))
    finally:
        SESSION.close()


def curr_connection(chat_id):
    try:
        return SESSION.query(Connection).get((str(chat_id)))
    finally:
        SESSION.close()


def disconnect(user_id):
    with CONNECTION_INSERTION_LOCK:
        disconnect = SESSION.query(Connection).get((int(user_id)))
        if disconnect:
            SESSION.delete(disconnect)
            SESSION.commit()
            return True
        else:
            SESSION.close()
            return False

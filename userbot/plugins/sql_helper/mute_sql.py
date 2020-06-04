#   Copyright 2019 - 2020 DarkPrinc3

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
try:
    from userbot.plugins.sql_helper import SESSION, BASE
except ImportError:
    raise Exception("Hello!")

from sqlalchemy import Column, String, UnicodeText


class Mute(BASE):
    __tablename__ = "mute"
    sender = Column(String(14), primary_key=True)
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, sender, chat_id):
        self.sender = str(sender)
        self.chat_id = str(chat_id)


Mute.__table__.create(checkfirst=True)


def is_muted(sender, chat_id):
    user = SESSION.query(Mute).get((str(sender), str(chat_id)))
    if user:
        return True
    else:
        return False


def mute(sender, chat_id):
    adder = Mute(str(sender), str(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def unmute(sender, chat_id):
    rem = SESSION.query(Mute).get((str(sender), str(chat_id)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()

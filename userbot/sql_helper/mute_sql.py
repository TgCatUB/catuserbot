# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from sqlalchemy import Column, String

from . import BASE, SESSION


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
    return bool(user)


def mute(sender, chat_id):
    adder = Mute(str(sender), str(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def unmute(sender, chat_id):
    if rem := SESSION.query(Mute).get((str(sender), str(chat_id))):
        SESSION.delete(rem)
        SESSION.commit()

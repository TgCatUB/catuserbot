from sqlalchemy import Column, String

from . import BASE, SESSION, create_table


class Mute(BASE):
    __tablename__ = "mute"
    sender = Column(String(14), primary_key=True)
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, sender, chat_id):
        self.sender = str(sender)
        self.chat_id = str(chat_id)


create_table(Mute.__table__)


def is_muted(sender, chat_id):
    user = SESSION.get(Mute, (str(sender), str(chat_id)))
    return bool(user)


def mute(sender, chat_id):
    adder = Mute(str(sender), str(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def unmute(sender, chat_id):
    if rem := SESSION.get(Mute, (str(sender), str(chat_id))):
        SESSION.delete(rem)
        SESSION.commit()

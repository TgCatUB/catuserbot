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

def get_all_muted():
    rem = SESSION.query(Mute).all()
    SESSION.close()
    return rem

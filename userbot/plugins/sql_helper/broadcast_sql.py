# Credits : @HeisenbergTheDanger

from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE


class ghdb(BASE):
    __tablename__ = "channels"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


ghdb.__table__.create(checkfirst=True)


def in_channels(chat_id):
    try:
        return SESSION.query(ghdb).filter(ghdb.chat_id == str(chat_id)).one()
    except:
        return None
    finally:
        SESSION.close()


def add_channel(chat_id):
    adder = ghdb(str(chat_id))
    SESSION.add(adder)
    SESSION.commit()


def rm_channel(chat_id):
    rem = SESSION.query(ghdb).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_channels():
    rem = SESSION.query(ghdb).all()
    SESSION.close()
    return rem

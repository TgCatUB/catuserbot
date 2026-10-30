from sqlalchemy import Column, String, select

from . import BASE, SESSION, create_table


class GBan(BASE):
    __tablename__ = "gban"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(String(127))

    def __init__(self, chat_id, reason=""):
        self.chat_id = chat_id
        self.reason = reason


create_table(GBan.__table__)


def is_gbanned(chat_id):
    try:
        return SESSION.scalars(
            select(GBan).where(GBan.chat_id == str(chat_id))
        ).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_gbanuser(chat_id):
    try:
        return SESSION.get(GBan, str(chat_id))
    finally:
        SESSION.close()


def catgban(chat_id, reason):
    adder = GBan(str(chat_id), str(reason))
    SESSION.add(adder)
    SESSION.commit()


def catungban(chat_id):
    if rem := SESSION.get(GBan, str(chat_id)):
        SESSION.delete(rem)
        SESSION.commit()


def get_all_gbanned():
    rem = SESSION.scalars(select(GBan)).all()
    SESSION.close()
    return rem

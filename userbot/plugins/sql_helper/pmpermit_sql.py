from sqlalchemy import Column, String

from userbot.plugins.sql_helper import BASE, SESSION


class PMPermit(BASE):
    __tablename__ = "pmpermit"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(String(127))

    def __init__(self, chat_id, reason=""):
        self.chat_id = chat_id
        self.reason = reason


PMPermit.__table__.create(checkfirst=True)


def is_approved(chat_id):
    try:
        return SESSION.query(PMPermit).filter(PMPermit.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def approve(chat_id, reason):
    adder = PMPermit(str(chat_id), str(reason))
    SESSION.add(adder)
    SESSION.commit()


def disapprove(chat_id):
    rem = SESSION.query(PMPermit).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_approved():
    rem = SESSION.query(PMPermit).all()
    SESSION.close()
    return rem


def disapprove_all():
    SESSION.query(PMPermit).delete()
    SESSION.commit()

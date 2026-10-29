from sqlalchemy import Column, Numeric, select

from . import BASE, SESSION, create_table


class NOLogPMs(BASE):
    __tablename__ = "no_log_pms"
    chat_id = Column(Numeric, primary_key=True)

    def __init__(self, chat_id, reason=""):
        self.chat_id = chat_id


create_table(NOLogPMs.__table__)


def is_approved(chat_id):
    try:
        return SESSION.scalars(
            select(NOLogPMs).where(NOLogPMs.chat_id == chat_id)
        ).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def approve(chat_id):
    adder = NOLogPMs(chat_id)
    SESSION.add(adder)
    SESSION.commit()


def disapprove(chat_id):
    if rem := SESSION.get(NOLogPMs, chat_id):
        SESSION.delete(rem)
        SESSION.commit()

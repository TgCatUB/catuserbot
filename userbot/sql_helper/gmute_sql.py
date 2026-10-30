from sqlalchemy import Column, String, select

from . import BASE, SESSION, create_table


class GMute(BASE):
    __tablename__ = "gmute"
    sender = Column(String(14), primary_key=True)

    def __init__(self, sender):
        self.sender = str(sender)


create_table(GMute.__table__)


def is_gmuted(sender_id):
    try:
        return SESSION.scalars(select(GMute)).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def gmute(sender):
    adder = GMute(str(sender))
    SESSION.add(adder)
    SESSION.commit()


def ungmute(sender):
    if rem := SESSION.get(GMute, str(sender)):
        SESSION.delete(rem)
        SESSION.commit()

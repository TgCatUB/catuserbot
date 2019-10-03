try:
    from userbot.plugins.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError

from sqlalchemy import Column, UnicodeText, LargeBinary, Numeric


class Snips(BASE):
    __tablename__ = "snips"
    snip = Column(UnicodeText, primary_key=True)
    f_mesg_id = Column(Numeric)

    def __init__(self, snip, f_mesg_id):
        self.snip = snip
        self.f_mesg_id = f_mesg_id


Snips.__table__.create(checkfirst=True)


def get_snip(keyword):
    try:
        return SESSION.query(Snips).get(keyword)
    finally:
        SESSION.close()


def get_snips():
    try:
        return SESSION.query(Snips).all()
    finally:
        SESSION.close()


def add_snip(keyword, f_mesg_id):
    to_check = get_snip(keyword)
    if not to_check:
        adder = Snips(keyword, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(Snips).filter(Snips.snip == keyword)
        SESSION.delete(rem)
        SESSION.commit()
        adder = Snips(keyword, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return False


def remove_snip(keyword):
    to_check = get_snip(keyword)
    if not to_check:
        return False
    else:
        rem = SESSION.query(Snips).filter(Snips.snip == keyword)
        rem.delete()
        SESSION.commit()
        return True

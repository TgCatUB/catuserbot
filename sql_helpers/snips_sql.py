from sqlalchemy import Column, UnicodeText, LargeBinary, Numeric
from sql_helpers import SESSION, BASE


class Snips(BASE):
    __tablename__ = "snips"
    snip = Column(UnicodeText, primary_key=True)
    f_mesg_id = Column(Numeric)

    def __init__(
        self,
        snip,
        f_mesg_id
    ):
        self.snip = snip
        self.f_mesg_id = f_mesg_id


Snips.__table__.create(checkfirst=True)


def get_snips(keyword):
    try:
        return SESSION.query(Snips).get(keyword)
    except:
        return None
    finally:
        SESSION.close()


def get_all_snips():
    try:
        return SESSION.query(Snips).all()
    except:
        return None
    finally:
        SESSION.close()


def add_snip(keyword, f_mesg_id):
    adder = SESSION.query(Snips).get(keyword)
    if adder:
        adder.f_mesg_id = f_mesg_id
    else:
        adder = Snips(keyword, f_mesg_id)
    SESSION.add(adder)
    SESSION.commit()


def remove_snip(keyword):
    note = SESSION.query(Snips).filter(Snips.snip == keyword)
    if note:
        note.delete()
        SESSION.commit()

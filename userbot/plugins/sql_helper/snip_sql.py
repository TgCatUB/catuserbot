from sqlalchemy import Column, Numeric, String, UnicodeText

from . import BASE, SESSION


class Snips(BASE):
    __tablename__ = "snip"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, keyword, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id


Snips.__table__.create(checkfirst=True)


def get_note(chat_id, keyword):
    try:
        return SESSION.query(Snips).get((str(chat_id), keyword))
    finally:
        SESSION.close()


def get_notes(chat_id):
    try:
        return SESSION.query(Snips).filter(Snips.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_note(chat_id, keyword, reply, f_mesg_id):
    to_check = get_note(chat_id, keyword)
    if not to_check:
        adder = Snips(str(chat_id), keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(Snips).get((str(chat_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        adder = Snips(str(chat_id), keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return False


def rm_note(chat_id, keyword):
    to_check = get_note(chat_id, keyword)
    if not to_check:
        return False
    else:
        rem = SESSION.query(Snips).get((str(chat_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        return True

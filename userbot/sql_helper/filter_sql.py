from sqlalchemy import Column, Numeric, String, UnicodeText, delete, select

from . import BASE, SESSION, create_table


class Filter(BASE):
    __tablename__ = "catfilters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, keyword, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id

    def __eq__(self, other):
        return isinstance(other, Filter) and self.chat_id == other.chat_id and self.keyword == other.keyword


create_table(Filter.__table__)


def get_filter(chat_id, keyword):
    try:
        return SESSION.get(Filter, (str(chat_id), keyword))
    finally:
        SESSION.close()


def get_filters(chat_id):
    try:
        return SESSION.scalars(
            select(Filter).where(Filter.chat_id == str(chat_id))
        ).all()
    finally:
        SESSION.close()


def add_filter(chat_id, keyword, reply, f_mesg_id):
    to_check = get_filter(chat_id, keyword)
    if not to_check:
        adder = Filter(str(chat_id), keyword, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.get(Filter, (str(chat_id), keyword))
    SESSION.delete(rem)
    SESSION.commit()
    adder = Filter(str(chat_id), keyword, reply, f_mesg_id)
    SESSION.add(adder)
    SESSION.commit()
    return False


def remove_filter(chat_id, keyword):
    to_check = get_filter(chat_id, keyword)
    if not to_check:
        return False
    rem = SESSION.get(Filter, (str(chat_id), keyword))
    SESSION.delete(rem)
    SESSION.commit()
    return True


def remove_all_filters(chat_id):
    SESSION.execute(delete(Filter).where(Filter.chat_id == str(chat_id)))
    SESSION.commit()

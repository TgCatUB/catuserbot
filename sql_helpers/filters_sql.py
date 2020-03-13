from sqlalchemy import Column, UnicodeText, LargeBinary, Numeric, String
from sql_helpers import SESSION, BASE


class Filters(BASE):
    __tablename__ = "filters"
    chat_id = Column(Numeric, primary_key=True)
    keyword = Column(UnicodeText, primary_key=True)
    f_mesg_id = Column(Numeric)


    def __init__(
        self,
        chat_id,
        keyword,
        f_mesg_id
    ):
        self.chat_id = chat_id
        self.keyword = keyword
        self.f_mesg_id = f_mesg_id


Filters.__table__.create(checkfirst=True)


def get_filter(chat_id, keyword):
    try:
        return SESSION.query(Filters).get((chat_id, keyword))
    except:
        return None
    finally:
        SESSION.close()


def get_all_filters(chat_id):
    try:
        return SESSION.query(Filters).filter(Filters.chat_id == chat_id).all()
    except:
        return None
    finally:
        SESSION.close()


def add_filter(chat_id, keyword, f_mesg_id):
    adder = SESSION.query(Filters).get((chat_id, keyword))
    if adder:
        adder.f_mesg_id = f_mesg_id
    else:
        adder = Filters(chat_id, keyword, f_mesg_id)
    SESSION.add(adder)
    SESSION.commit()


def remove_filter(chat_id, keyword):
    saved_filter = SESSION.query(Filters).get((chat_id, keyword))
    if saved_filter:
        SESSION.delete(saved_filter)
        SESSION.commit()


def remove_all_filters(chat_id):
    saved_filter = SESSION.query(Filters).filter(Filters.chat_id == chat_id)
    if saved_filter:
        saved_filter.delete()
        SESSION.commit()

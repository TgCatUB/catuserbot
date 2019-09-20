try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError
from sqlalchemy import Column, UnicodeText, LargeBinary, Numeric, String


class Filters(BASE):
    __tablename__ = "filters"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText, nullable=False)
    snip_type = Column(Numeric)
    media_id = Column(UnicodeText)
    media_access_hash = Column(UnicodeText)
    media_file_reference = Column(LargeBinary)

    def __init__(self,
                 chat_id,
                 keyword,
                 reply,
                 snip_type,
                 media_id=None,
                 media_access_hash=None,
                 media_file_reference=None):
        self.chat_id = str(chat_id)  # ensure string
        self.keyword = keyword
        self.reply = reply
        self.snip_type = snip_type
        self.media_id = media_id
        self.media_access_hash = media_access_hash
        self.media_file_reference = media_file_reference

    def __eq__(self, other):
        return bool(
            isinstance(other, Filters) and self.chat_id == other.chat_id
            and self.keyword == other.keyword)


Filters.__table__.create(checkfirst=True)


def get_filter(chat_id, keyword):
    try:
        return SESSION.query(Filters).get((str(chat_id), keyword))
    finally:
        SESSION.close()


def get_filters(chat_id):
    try:
        return SESSION.query(Filters).filter(
            Filters.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def add_filter(chat_id, keyword, reply, snip_type, media_id, media_access_hash,
               media_file_reference):
    to_check = get_filter(chat_id, keyword)
    if not to_check:
        adder = Filters(str(chat_id), keyword, reply, snip_type, media_id,
                        media_access_hash, media_file_reference)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(Filters).get((str(chat_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        adder = Filters(str(chat_id), keyword, reply, snip_type, media_id,
                        media_access_hash, media_file_reference)
        SESSION.add(adder)
        SESSION.commit()
        return False


def remove_filter(chat_id, keyword):
    to_check = get_filter(chat_id, keyword)
    if not to_check:
        return False
    else:
        rem = SESSION.query(Filters).get((str(chat_id), keyword))
        SESSION.delete(rem)
        SESSION.commit()
        return True


def rm_all_filters(chat_id):
    filters = SESSION.query(Filters).filter(Filters.chat_id == str(chat_id))
    if filters:
        filters.delete()
        SESSION.commit()

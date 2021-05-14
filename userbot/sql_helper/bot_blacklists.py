from sqlalchemy import Column, String, UnicodeText

from . import BASE, SESSION


class Bot_BlackList(BASE):
    __tablename__ = "bot_blacklist"
    chat_id = Column(String(14), primary_key=True)
    username = Column(UnicodeText)
    reason = Column(UnicodeText)

    def __init__(self, chat_id, reason):
        self.chat_id = str(chat_id)
        self.username = username
        self.reason = reason

    def __repr__(self):
        return "<BL %s>" % self.chat_id


Bot_BlackList.__table__.create(checkfirst=True)


def add_user_to_bl(chat_id: int,username: str, reason: str):
    """add the user to the blacklist"""
    __user = Bot_BlackList(str(chat_id),username, reason)
    SESSION.add(__user)
    SESSION.commit()


def check_is_black_list(chat_id: int):
    """check if user_id is blacklisted"""
    try:
        return SESSION.query(Bot_BlackList).get(str(chat_id))
    finally:
        SESSION.close()


def rem_user_from_bl(chat_id: int):
    """remove the user from the blacklist"""
    s__ = SESSION.query(Bot_BlackList).get(str(chat_id))
    if s__:
        SESSION.delete(s__)
        SESSION.commit()
        return True
    SESSION.close()
    return False


def get_all_bl_users():
    try:
        return SESSION.query(Bot_BlackList).all()
    except BaseException:
        return None
    finally:
        SESSION.close()

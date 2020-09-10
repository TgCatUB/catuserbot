try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError

from sqlalchemy import BigInteger, Column, Numeric, String, UnicodeText


class Welcome(BASE):
    __tablename__ = "welcome"
    chat_id = Column(String(14), primary_key=True)
    previous_welcome = Column(BigInteger)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, previous_welcome, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.previous_welcome = previous_welcome
        self.reply = reply
        self.f_mesg_id = f_mesg_id


Welcome.__table__.create(checkfirst=True)


def get_welcome(chat_id):
    try:
        return SESSION.query(Welcome).get(str(chat_id))
    finally:
        SESSION.close()


def get_current_welcome_settings(chat_id):
    try:
        return SESSION.query(Welcome).filter(
            Welcome.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_welcome_setting(chat_id, previous_welcome, reply, f_mesg_id):
    to_check = get_welcome(chat_id)
    if not to_check:
        adder = Welcome(chat_id, previous_welcome, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(Welcome).get(str(chat_id))
        SESSION.delete(rem)
        SESSION.commit()
        adder = Welcome(chat_id, previous_welcome, reply, f_mesg_id)
        SESSION.commit()
        return False


def rm_welcome_setting(chat_id):
    try:
        rem = SESSION.query(Welcome).get(str(chat_id))
        if rem:
            SESSION.delete(rem)
            SESSION.commit()
            return True
    except BaseException:
        return False


def update_previous_welcome(chat_id, previous_welcome):
    row = SESSION.query(Welcome).get(str(chat_id))
    row.previous_welcome = previous_welcome
    SESSION.commit()

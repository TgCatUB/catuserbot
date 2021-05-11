try:
    from . import BASE, SESSION
except ImportError:
    raise AttributeError

from sqlalchemy import BigInteger, Column, Numeric, String, UnicodeText


class JoinWelcome(BASE):
    __tablename__ = "joinwelcome"
    chat_id = Column(String(14), primary_key=True)
    previous_welcome = Column(BigInteger)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)

    def __init__(self, chat_id, previous_welcome, reply, f_mesg_id):
        self.chat_id = str(chat_id)
        self.previous_welcome = previous_welcome
        self.reply = reply
        self.f_mesg_id = f_mesg_id


JoinWelcome.__table__.create(checkfirst=True)


def getwelcome(chat_id):
    try:
        return SESSION.query(JoinWelcome).get(str(chat_id))
    finally:
        SESSION.close()


def getcurrent_welcome_settings(chat_id):
    try:
        return (
            SESSION.query(JoinWelcome).filter(JoinWelcome.chat_id == str(chat_id)).one()
        )
    except BaseException:
        return None
    finally:
        SESSION.close()


def addwelcome_setting(chat_id, previous_welcome, reply, f_mesg_id):
    to_check = getwelcome(chat_id)
    if not to_check:
        adder = JoinWelcome(chat_id, previous_welcome, reply, f_mesg_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.query(JoinWelcome).get(str(chat_id))
    SESSION.delete(rem)
    SESSION.commit()
    adder = JoinWelcome(chat_id, previous_welcome, reply, f_mesg_id)
    SESSION.commit()
    return False


def rmwelcome_setting(chat_id):
    try:
        rem = SESSION.query(JoinWelcome).get(str(chat_id))
        if rem:
            SESSION.delete(rem)
            SESSION.commit()
            return True
    except BaseException:
        return False


def updateprevious_welcome(chat_id, previous_welcome):
    row = SESSION.query(JoinWelcome).get(str(chat_id))
    row.previous_welcome = previous_welcome
    SESSION.commit()

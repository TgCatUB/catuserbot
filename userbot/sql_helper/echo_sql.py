from sqlalchemy import Column, String, UnicodeText, delete, select

from . import BASE, SESSION, create_table


class Echos(BASE):
    __tablename__ = "echos"
    chat_id = Column(String(14), primary_key=True)
    user_id = Column(String(14), primary_key=True, nullable=False)
    chat_name = Column(UnicodeText)
    user_name = Column(UnicodeText)
    user_username = Column(UnicodeText)
    chat_type = Column(UnicodeText)

    def __init__(self, chat_id, user_id, chat_name, user_name, user_username, chat_type):
        self.chat_id = str(chat_id)
        self.user_id = str(user_id)
        self.chat_name = chat_name
        self.user_name = user_name
        self.user_username = user_username
        self.chat_type = chat_type

    def __eq__(self, other):
        return isinstance(other, Echos) and self.chat_id == other.chat_id and self.user_id == other.user_id


create_table(Echos.__table__)


def is_echo(chat_id, user_id):
    try:
        return SESSION.get(Echos, (str(chat_id), str(user_id)))
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_echos(chat_id):
    try:
        return SESSION.scalars(
            select(Echos).where(Echos.chat_id == str(chat_id))
        ).all()
    finally:
        SESSION.close()


def get_all_echos():
    try:
        return SESSION.scalars(select(Echos)).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def addecho(chat_id, user_id, chat_name, user_name, user_username, chat_type):
    to_check = is_echo(chat_id, user_id)
    if not to_check:
        adder = Echos(str(chat_id), str(user_id), chat_name, user_name, user_username, chat_type)
        SESSION.add(adder)
        SESSION.commit()
        return True
    rem = SESSION.get(Echos, (str(chat_id), str(user_id)))
    SESSION.delete(rem)
    SESSION.commit()
    adder = Echos(str(chat_id), str(user_id), chat_name, user_name, user_username, chat_type)
    SESSION.add(adder)
    SESSION.commit()
    return False


def remove_echo(chat_id, user_id):
    to_check = is_echo(chat_id, user_id)
    if not to_check:
        return False
    rem = SESSION.get(Echos, (str(chat_id), str(user_id)))
    SESSION.delete(rem)
    SESSION.commit()
    return True


def remove_echos(chat_id):
    SESSION.execute(delete(Echos).where(Echos.chat_id == str(chat_id)))
    SESSION.commit()


def remove_all_echos():
    SESSION.execute(delete(Echos))
    SESSION.commit()

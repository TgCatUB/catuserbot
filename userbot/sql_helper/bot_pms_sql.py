from sqlalchemy import Column, Integer, String, UnicodeText

from . import BASE, SESSION


class Bot_Users(BASE):
    __tablename__ = "bot_pms_data"
    message_id = Column(Integer, primary_key=True)
    first_name = Column(UnicodeText)
    chat_id = Column(String(14))
    reply_id = Column(Integer)
    result_id = Column(Integer, primary_key=True)

    def __init__(self, message_id, first_name, chat_id, reply_id, result_id):
        self.message_id = message_id
        self.first_name = first_name
        self.chat_id = str(chat_id)
        self.reply_id = reply_id
        self.result_id = result_id


Bot_Users.__table__.create(checkfirst=True)


def add_user_to_db(message_id, first_name, chat_id, reply_id, result_id):
    user = Bot_Users(message_id, first_name, str(chat_id), reply_id, result_id)
    SESSION.add(user)
    SESSION.commit()
    return True


def get_user_id(message_id):
    try:
        _result = (
            SESSION.query(Bot_Users)
            .filter(Bot_Users.message_id == str(message_id))
            .all()
        )
        if _result:
            _result = _result[-1]
            return int(_result.chat_id), _result.reply_id, _result.result_id
        return None, None, None
    finally:
        SESSION.close()


def get_user_name(message_id):
    try:
        _result = (
            SESSION.query(Bot_Users)
            .filter(Bot_Users.message_id == str(message_id))
            .all()
        )
        if _result:
            _result = _result[-1]
            return int(_result.chat_id), _result.first_name
        return None, None
    finally:
        SESSION.close()


def get_user_reply(reply_id):
    try:
        _result = SESSION.query(Bot_Users).filter(Bot_Users.reply_id == reply_id).all()
        if _result:
            return _result
        return None
    finally:
        SESSION.close()

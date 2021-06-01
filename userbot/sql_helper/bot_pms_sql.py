from sqlalchemy import Column, Integer, String, UnicodeText

from . import BASE, SESSION


class Bot_Users(BASE):
    __tablename__ = "bot_pms_data"
    # pm logger message id
    message_id = Column(Integer, primary_key=True)
    first_name = Column(UnicodeText)
    chat_id = Column(String(14))
    # in opposite user message id
    reply_id = Column(Integer)
    # pm logger message reply id
    logger_id = Column(Integer)
    # pm opposite user reply message id
    result_id = Column(Integer, primary_key=True)

    def __init__(self, message_id, first_name, chat_id, reply_id, logger_id, result_id):
        self.message_id = message_id
        self.first_name = first_name
        self.chat_id = str(chat_id)
        self.reply_id = reply_id
        self.logger_id = logger_id
        self.result_id = result_id


Bot_Users.__table__.create(checkfirst=True)


def add_user_to_db(message_id, first_name, chat_id, reply_id, logger_id, result_id):
    user = Bot_Users(
        message_id, first_name, str(chat_id), reply_id, logger_id, result_id
    )
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
            return _result
        return None
    finally:
        SESSION.close()


def del_user_from_db(message_id):
    try:
        _result = (
            SESSION.query(Bot_Users)
            .filter(Bot_Users.message_id == str(message_id))
            .all()
        )
        if _result:
            for rst in _result:
                rem = SESSION.query(Bot_Users).get((str(rst.message_id), rst.result_id))
                SESSION.delete(rem)
                SESSION.commit()
            return True
        return False
    finally:
        SESSION.close()


def get_user_reply(reply_id):
    try:
        _result = (
            SESSION.query(Bot_Users).filter(Bot_Users.reply_id == str(reply_id)).all()
        )
        if _result:
            return _result
        return None
    finally:
        SESSION.close()


def get_user_results(result_id):
    try:
        _result = (
            SESSION.query(Bot_Users).filter(Bot_Users.result_id == str(result_id)).all()
        )
        if _result:
            return _result
        return None
    finally:
        SESSION.close()


def get_user_logging(logger_id):
    try:
        _result = (
            SESSION.query(Bot_Users).filter(Bot_Users.logger_id == str(logger_id)).all()
        )
        if _result:
            return _result
        return None
    finally:
        SESSION.close()

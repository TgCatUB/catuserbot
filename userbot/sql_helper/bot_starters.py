from sqlalchemy import (
    Column,
    String,
    Integer,
    UnicodeText
)
from . import (
    SESSION,
    BASE
)

class Bot_Starters(BASE):
    """ Table to store the received messages """
    __tablename__ = "bot_starters"
    user_id = Column(String(14), primary_key=True)
    first_name = Column(UnicodeText)
    date = Column(UnicodeText))
    username = Column(UnicodeText)

    def __init__(self, user_id, first_name, date, username):
        self.user_id = str(user_id)
        self.first_name = first_name
        self.date = date
        self.username = username



Bot_Starters.__table__.create(checkfirst=True)

def add_starter_to_db(
    user_id,
    first_name,
    date,
    username,
):
    user = Bot_Starters(str(user_id),first_name, date, username)
    SESSION.add(user)
    SESSION.commit()
    return True

def get_starter_details(user_id):
    try:
        _result = SESSION.query(Bot_Starters).get(str(user_id))
        if _result:
            return _result
        return None
    finally:
        SESSION.close()

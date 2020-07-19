from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE

class Gdrive(BASE):
    __tablename__ = "gdrive"
    chat_id = Column(String, primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)

Gdrive.__table__.create(checkfirst=True)

def is_folder(chat_id):
    try:
        return SESSION.query(Gdrive).filter(Gdrive.chat_id == str(chat_id)).one()
    except:
        return None
    finally:
        SESSION.close()

def gparent_id(chat_id):
    adder = Gdrive(str(chat_id))
    SESSION.add(adder)
    SESSION.commit()

def rmparent_id(chat_id):
    rem = SESSION.query(Gdrive).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()

def get_parent_id():
    rem = SESSION.query(Gdrive).all()
    SESSION.close()
    return rem

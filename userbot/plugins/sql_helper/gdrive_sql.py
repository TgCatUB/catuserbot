from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE

class Gdrive(BASE):
    __tablename__ = "gdrive"
    chatid = Column(String(50), primary_key=True)

    def __init__(self, chatid):
        self.chatid = str(chatid)

Gdrive.__table__.create(checkfirst=True)

def is_folder(chatid):
    try:
        return SESSION.query(Gdrive).filter(Gdrive.chatid == str(chatid)).one()
    except:
        return None
    finally:
        SESSION.close()

def gparent_id(chatid):
    adder = Gdrive(str(chatid))
    SESSION.add(adder)
    SESSION.commit()

def rmparent_id(chatid):
    rem = SESSION.query(Gdrive).get(str(chatid))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()

def get_parent_id():
    rem = SESSION.query(Gdrive).all()
    SESSION.close()
    return rem

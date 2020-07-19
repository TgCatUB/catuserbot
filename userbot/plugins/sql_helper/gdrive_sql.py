from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE

class Gdrive(BASE):
    __tablename__ = "gdrive"
    cat = Column(String(50), primary_key=True)

    def __init__(self, cat):
        self.cat = cat

Gdrive.__table__.create(checkfirst=True)

def is_folder(cat):
    try:
        return SESSION.query(Gdrive).filter(Gdrive.cat == str(cat)).one()
    except:
        return None
    finally:
        SESSION.close()

def gparent_id(cat):
    adder = Gdrive(str(cat))
    SESSION.add(adder)
    SESSION.commit()

def rmparent_id(cat):
    rem = SESSION.query(Gdrive).get(str(cat))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()

def get_parent_id():
    rem = SESSION.query(Gdrive).all()
    SESSION.close()
    return rem

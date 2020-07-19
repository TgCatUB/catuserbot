from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE

class Gdrive(BASE):
    __tablename__ = "gdrive"
    catid = Column(String(50), primary_key=True)

    def __init__(self, catid):
        self.catid = str(catid)

Gdrive.__table__.create(checkfirst=True)

def is_folder(catid):
    try:
        return SESSION.query(Gdrive).filter(Gdrive.catid == str(catid)).one()
    except:
        return None
    finally:
        SESSION.close()

def gparent_id(catid):
    adder = Gdrive(str(catid))
    SESSION.add(adder)
    SESSION.commit()

def rmparent_id(catid):
    rem = SESSION.query(Gdrive).get(str(catid))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()

def get_parent_id():
    rem = SESSION.query(Gdrive).all()
    SESSION.close()
    return rem

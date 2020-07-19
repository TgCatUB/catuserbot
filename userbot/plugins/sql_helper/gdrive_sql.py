from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE


class Gdrive(BASE):
    __tablename__ = "catgdrive"
    cat= Column(String(50), primary_key=True)

    def __init__(self,cat):
        self.cat = cat

Gdrive.__table__.create(checkfirst=True)

def is_folder(folder_id):
    try:
        return SESSION.query(Gdrive).filter(Gdrive.cat == str(folder_id))
    except:
        return None
    finally:
        SESSION.close()

def gparent_id(folder_id):
    adder = SESSION.query(Gdrive).get(folder_id)
    if not adder:
        adder = Gdrive(folder_id)
    SESSION.add(adder)
    SESSION.commit()
    
def get_parent_id():
    try:
        return SESSION.query(Gdrive).all()
    except:
        return None
    finally:
        SESSION.close()

def rmparent_id(folder_id):
    note = SESSION.query(Gdrive).filter(Gdrive.cat == folder_id)
    if note:
        note.delete()
        SESSION.commit()

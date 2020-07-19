from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE


class Gdrive(BASE):
    __tablename__ = "gdrive"
    folder_id = Column(String(50), primary_key=True)

    def __init__(self,folder_id):
        self.folder_id = folder_id


Gdrive.__table__.create(checkfirst=True)


def is_folder(folder_id):
    try:
        return SESSION.query(Gdrive).filter(Gdrive.folder_id == str(folder_id)).one()
    except:
        return None
    finally:
        SESSION.close()


def gparent_id(folder_id):
    adder = Gdrive(str(folder_id))
    SESSION.add(adder)
    SESSION.commit()
    return True

def rmparent_id(folder_id):
    rem = SESSION.query(Gdrive).get(str(folder_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()
    return True

def get_parent_id():
    rem = SESSION.query(Gdrive)
    if not rem:
        rem = None
    SESSION.close()
    return rem

from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE


class GDrive(BASE):
    __tablename__ = "gdrive"
    chat_id = Column(String(14))
    folderid = Column(String(40), primary_key=True)

    def __init__(self, chat_id),  folderid ):
        self.folderid = folderid
        self.chat_id = chat_id

GDrive.__table__.create(checkfirst=True)


def is_folder(folderid):
    try:
        return SESSION.query(GDrive).filter(GDrive.folderid == str(folderid)).one()
    except:
        return None
    finally:
        SESSION.close()


def gparent_id(folderid):
    adder = GDrive(str(folderid))
    SESSION.add(adder)
    SESSION.commit()


def rmparent_id(folderid):
    rem = SESSION.query(GDrive).get(str(folderid))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_parent_id():
    rem = SESSION.query(GDrive).all()
    SESSION.close()
    return rem

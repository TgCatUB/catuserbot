from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE


class GDrive(BASE):
    __tablename__ = "gdrive"
    folderid = Column(String(40), primary_key=True)

    def __init__(self, folderid):
        self.folderid = folderid


GDrive.__table__.create(checkfirst=True)


def is_GDrivened(folderid):
    try:
        return SESSION.query(GDrive).filter(GDrive.folderid == str(folderid)).one()
    except:
        return None
    finally:
        SESSION.close()


def catGDrive(folderid):
    adder = GDrive(str(folderid))
    SESSION.add(adder)
    SESSION.commit()


def catunGDrive(folderid):
    rem = SESSION.query(GDrive).get(str(folderid))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_GDrivened():
    rem = SESSION.query(GDrive).all()
    SESSION.close()
    return rem

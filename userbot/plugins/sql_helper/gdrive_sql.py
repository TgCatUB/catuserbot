from sqlalchemy import Column, UnicodeText, LargeBinary, Numeric
from userbot.plugins.sql_helper import SESSION, BASE


class Gdrive(BASE):
    __tablename__ = "gdrive"
    snip = Column(UnicodeText, primary_key=True)
    reply = Column(UnicodeText)

    def __init__(
        self,
        snip, reply
    ):
        self.snip = snip
        self.reply = reply


Gdrive.__table__.create(checkfirst=True)


def is_folder(keyword):
    try:
        return SESSION.query(Gdrive).get(keyword)
    except:
        return None
    finally:
        SESSION.close()


def get_parent_id():
    try:
        return SESSION.query(Gdrive).all()
    except:
        return None
    finally:
        SESSION.close()


def gparent_id((keyword, reply):
    adder = SESSION.query(Gdrive).get(keyword)
    if adder:
        adder.reply = reply
    else:
        adder = Gdrive(keyword, reply)
    SESSION.add(adder)
    SESSION.commit()


def rmparent_id(keyword):
    note = SESSION.query(Gdrive).filter(Gdrive.snip == keyword)
    if note:
        note.delete()
        SESSION.commit()

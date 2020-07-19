from sqlalchemy import Column, String
from userbot.plugins.sql_helper import SESSION, BASE


class Gdrive(BASE):
    __tablename__ = "gdrive"
    cat= Column(String(5), primary_key=True)
    catid = Column(String(50))

    def __init__(self,cat,catid):
        self.cat = cat
        self.catid = catid


Gdrive.__table__.create(checkfirst=True)


def is_folder(hmm):
    try:
        return SESSION.query(Gdrive).filter(Gdrive.cat == str(hmm)).one()
    except:
        return None
    finally:
        SESSION.close()


def gparent_id(hmm , folder_id):
    adder = SESSION.query(Gdrive).get(hmm)
    if not adder:
        adder = Gdrive(hmm , folder_id)
    SESSION.add(adder)
    SESSION.commit()
    
def get_parent_id():
    try:
        return SESSION.query(Gdrive).all()
    except:
        return None
    finally:
        SESSION.close()

def rmparent_id(hmm):
    note = SESSION.query(Gdrive).filter(Gdrive.cat == hmm)
    if note:
        note.delete()
        SESSION.commit()

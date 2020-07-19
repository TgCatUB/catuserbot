from sqlalchemy import Column, String
try:
    from userbot.plugins.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError

class Gdrive(BASE):
    __tablename__ = "gdrive"
    folderid = Column(String(50) , primary_key=True)
    name = Column(String(127))
    
    def __init__(self, folderid, name = ""):
        self.folderid = str(folderid)
        self.name = name
        
        
Gdrive.__table__.create(checkfirst=True)

def is_folder(folderid):
    try:
        return SESSION.query(Gdrive).filter(Gdrive.folderid == str(folderid)).one()
    except:
        return None
    finally:
        SESSION.close()

def gparent_id(folderid , name):
    adder = Gdrive(str(folderid), str(name))
    SESSION.add(adder)
    SESSION.commit()

def rmparent_id(folderid):
    rem = SESSION.query(Gdrive).get(str(folderid))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()

def get_parent_id():
    rem = SESSION.query(Gdrive).all()
    SESSION.close()
    return rem

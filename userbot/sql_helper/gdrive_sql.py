from sqlalchemy import Column, String, delete, select

from . import BASE, SESSION, create_table


class Gdrive(BASE):
    __tablename__ = "catgdrive"
    cat = Column(String(50), primary_key=True)

    def __init__(self, cat):
        self.cat = cat


create_table(Gdrive.__table__)


def is_folder(folder_id):
    try:
        return SESSION.scalars(
            select(Gdrive).where(Gdrive.cat == str(folder_id))
        ).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def gparent_id(folder_id):
    adder = SESSION.get(Gdrive, folder_id)
    if not adder:
        adder = Gdrive(folder_id)
    SESSION.add(adder)
    SESSION.commit()


def get_parent_id():
    try:
        return SESSION.scalars(select(Gdrive)).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def rmparent_id(folder_id):
    SESSION.execute(delete(Gdrive).where(Gdrive.cat == folder_id))
    SESSION.commit()

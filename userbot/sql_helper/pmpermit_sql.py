from sqlalchemy import Column, String, UnicodeText

from . import BASE, SESSION


class PmPermit_Sql(BASE):
    __tablename__ = "pmpermit_sql"
    user_id = Column(String(14), primary_key=True)
    first_name = Column(UnicodeText)
    date = Column(UnicodeText)
    username = Column(UnicodeText)
    reason = Column(UnicodeText)

    def __init__(self, user_id, first_name, date, username, reason):
        self.user_id = str(user_id)
        self.first_name = first_name
        self.date = date
        self.username = username
        self.reason = reason


PmPermit_Sql.__table__.create(checkfirst=True)


def approve(user_id, first_name, date, username, reason):
    to_check = is_approved(user_id)
    if not to_check:
        user = PmPermit_Sql(str(user_id), first_name, date, username, reason)
        SESSION.add(user)
        SESSION.commit()
        return True
    rem = SESSION.query(PmPermit_Sql).get(str(user_id))
    SESSION.delete(rem)
    SESSION.commit()
    user = PmPermit_Sql(str(user_id), first_name, date, username, reason)
    SESSION.add(user)
    SESSION.commit()
    return True


def disapprove(user_id):
    to_check = is_approved(user_id)
    if not to_check:
        return False
    rem = SESSION.query(PmPermit_Sql).get(str(user_id))
    SESSION.delete(rem)
    SESSION.commit()
    return True


def is_approved(user_id):
    try:
        if _result := SESSION.query(PmPermit_Sql).get(str(user_id)):
            return _result
        return None
    finally:
        SESSION.close()


def get_all_approved():
    try:
        return SESSION.query(PmPermit_Sql).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def disapprove_all():
    try:
        SESSION.query(PmPermit_Sql).delete()
        SESSION.commit()
        return True
    except BaseException:
        return False
    finally:
        SESSION.close()

from sqlalchemy import BigInteger, Boolean, Column, LargeBinary, Numeric, String, UnicodeText
from sql_helpers import SESSION, BASE


class Welcome(BASE):
    __tablename__ = "welcome"
    chat_id = Column(Numeric, primary_key=True)
    should_clean_welcome = Column(Boolean, default=False)
    previous_welcome = Column(BigInteger)
    f_mesg_id = Column(Numeric)

    def __init__(
        self,
        chat_id,
        should_clean_welcome,
        previous_welcome,
        f_mesg_id
    ):
        self.chat_id = chat_id
        self.should_clean_welcome = should_clean_welcome
        self.previous_welcome = previous_welcome
        self.f_mesg_id = f_mesg_id


Welcome.__table__.create(checkfirst=True)


def get_current_welcome_settings(chat_id):
    try:
        return SESSION.query(Welcome).filter(Welcome.chat_id == chat_id).one()
    except:
        return None
    finally:
        SESSION.close()


def add_welcome_setting(
    chat_id,
    should_clean_welcome,
    previous_welcome,
    f_mesg_id
):
    adder = SESSION.query(Welcome).get(chat_id)
    if adder:
        adder.should_clean_welcome = should_clean_welcome
        adder.previous_welcome = previous_welcome
        adder.f_mesg_id = f_mesg_id
    else:
        adder = Welcome(
            chat_id,
            should_clean_welcome,
            previous_welcome,
            f_mesg_id
        )
    SESSION.add(adder)
    SESSION.commit()


def rm_welcome_setting(chat_id):
    rem = SESSION.query(Welcome).get(chat_id)
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def update_previous_welcome(chat_id, previous_welcome):
    row = SESSION.query(Welcome).get(chat_id)
    row.previous_welcome = previous_welcome
    # commit the changes to the DB
    SESSION.commit()

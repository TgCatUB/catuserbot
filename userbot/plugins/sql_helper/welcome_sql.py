from sqlalchemy import BigInteger, Boolean, Column, String, UnicodeText
from userbot.plugins.sql_helper import SESSION, BASE


class Welcome(BASE):
    __tablename__ = "welcome"
    chat_id = Column(String(14), primary_key=True)
    custom_welcome_message = Column(UnicodeText)
    media_file_id = Column(UnicodeText)
    should_clean_welcome = Column(Boolean, default=False)
    previous_welcome = Column(BigInteger)

    def __init__(
        self,
        chat_id,
        custom_welcome_message,
        should_clean_welcome,
        previous_welcome,
        media_file_id=None,
    ):
        self.chat_id = chat_id
        self.custom_welcome_message = custom_welcome_message
        self.media_file_id = media_file_id
        self.should_clean_welcome = should_clean_welcome
        self.previous_welcome = previous_welcome


Welcome.__table__.create(checkfirst=True)


def get_current_welcome_settings(chat_id):
    try:
        return SESSION.query(Welcome).filter(Welcome.chat_id == str(chat_id)).one()
    except:
        return None
    finally:
        SESSION.close()


def add_welcome_setting(
    chat_id,
    custom_welcome_message,
    should_clean_welcome,
    previous_welcome,
    media_file_id
):
    # adder = SESSION.query(Welcome).get(chat_id)
    adder = Welcome(
        chat_id,
        custom_welcome_message,
        should_clean_welcome,
        previous_welcome,
        media_file_id
    )
    SESSION.add(adder)
    SESSION.commit()


def rm_welcome_setting(chat_id):
    rem = SESSION.query(Welcome).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def update_previous_welcome(chat_id, previous_welcome):
    row = SESSION.query(Welcome).get(chat_id)
    row.previous_welcome = previous_welcome
    # commit the changes to the DB
    SESSION.commit()

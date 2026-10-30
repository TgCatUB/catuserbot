from sqlalchemy import Column, String, Text

from . import BASE, SESSION, create_table


class GoogleDriveCreds(BASE):
    __tablename__ = "gdrive"
    user = Column(String, primary_key=True)
    credentials = Column(Text, nullable=False)

    def __init__(self, user):
        self.user = user


create_table(GoogleDriveCreds.__table__)


def save_credentials(user, credentials):
    saved_credentials = SESSION.get(GoogleDriveCreds, user)
    if not saved_credentials:
        saved_credentials = GoogleDriveCreds(user)

    saved_credentials.credentials = credentials

    SESSION.add(saved_credentials)
    SESSION.commit()
    return True


def get_credentials(user):
    try:
        saved_credentials = SESSION.get(GoogleDriveCreds, user)
        return saved_credentials.credentials if saved_credentials is not None else None
    finally:
        SESSION.close()


def clear_credentials(user):
    if saved_credentials := SESSION.get(GoogleDriveCreds, user):
        SESSION.delete(saved_credentials)
        SESSION.commit()
        return True

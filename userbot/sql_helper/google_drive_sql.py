# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# CatUserBot #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Copyright (C) 2020-2023 by TgCatUB@Github.

# This file is part of: https://github.com/TgCatUB/catuserbot
# and is released under the "GNU v3.0 License Agreement".

# Please see: https://github.com/TgCatUB/catuserbot/blob/master/LICENSE
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from sqlalchemy import Column, String, Text

from . import BASE, SESSION


class GoogleDriveCreds(BASE):
    __tablename__ = "gdrive"
    user = Column(String, primary_key=True)
    credentials = Column(Text, nullable=False)

    def __init__(self, user):
        self.user = user


GoogleDriveCreds.__table__.create(checkfirst=True)


def save_credentials(user, credentials):
    saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
    if not saved_credentials:
        saved_credentials = GoogleDriveCreds(user)

    saved_credentials.credentials = credentials

    SESSION.add(saved_credentials)
    SESSION.commit()
    return True


def get_credentials(user):
    try:
        saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
        return saved_credentials.credentials if saved_credentials is not None else None
    finally:
        SESSION.close()


def clear_credentials(user):
    if saved_credentials := SESSION.query(GoogleDriveCreds).get(user):
        SESSION.delete(saved_credentials)
        SESSION.commit()
        return True

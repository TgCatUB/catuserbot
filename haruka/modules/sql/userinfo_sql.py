#    Haruka Aya (A telegram bot project)
#    Copyright (C) 2017-2019 Paul Larsen
#    Copyright (C) 2019-2020 Akito Mizukito (Haruka Network Development)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import threading

from sqlalchemy import Column, Integer, UnicodeText

from haruka.modules.sql import SESSION, BASE


class UserInfo(BASE):
    __tablename__ = "userinfo"
    user_id = Column(Integer, primary_key=True)
    info = Column(UnicodeText)

    def __init__(self, user_id, info):
        self.user_id = user_id
        self.info = info

    def __repr__(self):
        return "<User info %d>" % self.user_id


class UserBio(BASE):
    __tablename__ = "userbio"
    user_id = Column(Integer, primary_key=True)
    bio = Column(UnicodeText)

    def __init__(self, user_id, bio):
        self.user_id = user_id
        self.bio = bio

    def __repr__(self):
        return "<User info %d>" % self.user_id


UserInfo.__table__.create(checkfirst=True)
UserBio.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def get_user_me_info(user_id):
    userinfo = SESSION.query(UserInfo).get(user_id)
    SESSION.close()
    if userinfo:
        return userinfo.info
    return None


def set_user_me_info(user_id, info):
    with INSERTION_LOCK:
        userinfo = SESSION.query(UserInfo).get(user_id)
        if userinfo:
            userinfo.info = info
        else:
            userinfo = UserInfo(user_id, info)
        SESSION.add(userinfo)
        SESSION.commit()


def get_user_bio(user_id):
    userbio = SESSION.query(UserBio).get(user_id)
    SESSION.close()
    if userbio:
        return userbio.bio
    return None


def set_user_bio(user_id, bio):
    with INSERTION_LOCK:
        userbio = SESSION.query(UserBio).get(user_id)
        if userbio:
            userbio.bio = bio
        else:
            userbio = UserBio(user_id, bio)

        SESSION.add(userbio)
        SESSION.commit()


def clear_user_info(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(UserInfo).get(user_id)
        if curr:
            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.close()
    return False


def clear_user_bio(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(UserBio).get(user_id)
        if curr:
            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.close()
    return False

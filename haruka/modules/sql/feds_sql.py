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

from sqlalchemy import Column, String, UnicodeText, Integer, Boolean

from haruka.modules.sql import SESSION, BASE


class Federations(BASE):
    __tablename__ = "feds"
    owner_id = Column(String(14))
    fed_name = Column(UnicodeText)
    fed_id = Column(UnicodeText, primary_key=True)
    fed_rules = Column(UnicodeText)
    fed_users = Column(UnicodeText)

    def __init__(self, owner_id, fed_name, fed_id, fed_rules, fed_users):
        self.owner_id = owner_id
        self.fed_name = fed_name
        self.fed_id = fed_id
        self.fed_rules = fed_rules
        self.fed_users = fed_users


class ChatF(BASE):
    __tablename__ = "chat_feds"
    chat_id = Column(String(14), primary_key=True)
    fed_id = Column(UnicodeText)

    def __init__(self, chat_id, fed_id):
        self.chat_id = chat_id
        self.fed_id = fed_id


class BansF(BASE):
    __tablename__ = "bans_feds"
    fed_id = Column(UnicodeText, primary_key=True)
    user_id = Column(String(14), primary_key=True)
    first_name = Column(UnicodeText, nullable=False)
    last_name = Column(UnicodeText)
    user_name = Column(UnicodeText)
    reason = Column(UnicodeText, default="")

    def __init__(self, fed_id, user_id, first_name, last_name, user_name,
                 reason):
        self.fed_id = fed_id
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.reason = reason


class FedsUserSettings(BASE):
    __tablename__ = "feds_settings"
    user_id = Column(Integer, primary_key=True)
    should_report = Column(Boolean, default=True)

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return "<Feds report settings ({})>".format(self.user_id)


# Dropping db
# Federations.__table__.drop()
# ChatF.__table__.drop()
# BansF.__table__.drop()

Federations.__table__.create(checkfirst=True)
ChatF.__table__.create(checkfirst=True)
BansF.__table__.create(checkfirst=True)
FedsUserSettings.__table__.create(checkfirst=True)

FEDS_LOCK = threading.RLock()
CHAT_FEDS_LOCK = threading.RLock()
FEDS_SETTINGS_LOCK = threading.RLock()

FEDERATION_BYNAME = {}
FEDERATION_BYOWNER = {}
FEDERATION_BYFEDID = {}

FEDERATION_CHATS = {}
FEDERATION_CHATS_BYID = {}

FEDERATION_BANNED_FULL = {}
FEDERATION_BANNED_USERID = {}

FEDERATION_NOTIFICATION = {}


def get_fed_info(fed_id):
    get = FEDERATION_BYFEDID.get(str(fed_id))
    if get == None:
        return False
    return get


def get_fed_id(chat_id):
    get = FEDERATION_CHATS.get(str(chat_id))
    if get == None:
        return False
    else:
        return get['fid']


def new_fed(owner_id, fed_name, fed_id):
    with FEDS_LOCK:
        global FEDERATION_BYOWNER, FEDERATION_BYFEDID, FEDERATION_BYNAME
        fed = Federations(str(owner_id), fed_name, str(fed_id),
                          'Rules is not set in this federation.',
                          str({
                              'owner': str(owner_id),
                              'members': '[]'
                          }))
        SESSION.add(fed)
        SESSION.commit()
        FEDERATION_BYOWNER[str(owner_id)] = ({
            'fid':
            str(fed_id),
            'fname':
            fed_name,
            'frules':
            'Rules is not set in this federation.',
            'fusers':
            str({
                'owner': str(owner_id),
                'members': '[]'
            })
        })
        FEDERATION_BYFEDID[str(fed_id)] = ({
            'owner':
            str(owner_id),
            'fname':
            fed_name,
            'frules':
            'Rules is not set in this federation.',
            'fusers':
            str({
                'owner': str(owner_id),
                'members': '[]'
            })
        })
        FEDERATION_BYNAME[fed_name] = ({
            'fid':
            str(fed_id),
            'owner':
            str(owner_id),
            'frules':
            'Rules is not set in this federation.',
            'fusers':
            str({
                'owner': str(owner_id),
                'members': '[]'
            })
        })
        return fed


def del_fed(fed_id):
    with FEDS_LOCK:
        global FEDERATION_BYOWNER, FEDERATION_BYFEDID, FEDERATION_BYNAME, FEDERATION_CHATS, FEDERATION_CHATS_BYID, FEDERATION_BANNED_USERID, FEDERATION_BANNED_FULL
        getcache = FEDERATION_BYFEDID.get(fed_id)
        if getcache == None:
            return False
        # Variables
        getfed = FEDERATION_BYFEDID.get(fed_id)
        owner_id = getfed['owner']
        fed_name = getfed['fname']
        # Delete from cache
        FEDERATION_BYOWNER.pop(owner_id)
        FEDERATION_BYFEDID.pop(fed_id)
        FEDERATION_BYNAME.pop(fed_name)
        if FEDERATION_CHATS_BYID.get(fed_id):
            for x in FEDERATION_CHATS_BYID[fed_id]:
                delchats = SESSION.query(ChatF).get(str(x))
                if delchats:
                    SESSION.delete(delchats)
                    SESSION.commit()
                FEDERATION_CHATS.pop(x)
            FEDERATION_CHATS_BYID.pop(fed_id)
        # Delete fedban users
        getall = FEDERATION_BANNED_USERID.get(fed_id)
        if getall:
            for x in getall:
                banlist = SESSION.query(BansF).get((fed_id, str(x)))
                if banlist:
                    SESSION.delete(banlist)
                    SESSION.commit()
        FEDERATION_BANNED_USERID.pop(fed_id)
        FEDERATION_BANNED_FULL.pop(fed_id)
        # Delete from database
        curr = SESSION.query(Federations).get(fed_id)
        if curr:
            SESSION.delete(curr)
            SESSION.commit()
        return True


def chat_join_fed(fed_id, chat_id):
    with FEDS_LOCK:
        global FEDERATION_CHATS, FEDERATION_CHATS_BYID
        r = ChatF(chat_id, fed_id)
        SESSION.add(r)
        FEDERATION_CHATS[str(chat_id)] = {'fid': fed_id}
        checkid = FEDERATION_CHATS_BYID.get(fed_id)
        if checkid == None:
            FEDERATION_CHATS_BYID[fed_id] = []
        FEDERATION_CHATS_BYID[fed_id].append(str(chat_id))
        SESSION.commit()
        return r


def search_fed_by_name(fed_name):
    allfed = FEDERATION_BYNAME.get(fed_name)
    if allfed == None:
        return False
    return allfed


def search_user_in_fed(fed_id, user_id):
    getfed = FEDERATION_BYFEDID.get(fed_id)
    if getfed == None:
        return False
    getfed = eval(getfed['fusers'])['members']
    if user_id in eval(getfed):
        return True
    else:
        return False


def user_demote_fed(fed_id, user_id):
    with FEDS_LOCK:
        global FEDERATION_BYOWNER, FEDERATION_BYFEDID, FEDERATION_BYNAME
        # Variables
        getfed = FEDERATION_BYFEDID.get(str(fed_id))
        owner_id = getfed['owner']
        fed_name = getfed['fname']
        fed_rules = getfed['frules']
        # Temp set
        try:
            members = eval(eval(getfed['fusers'])['members'])
        except ValueError:
            return False
        members.remove(user_id)
        # Set user
        FEDERATION_BYOWNER[str(owner_id)]['fusers'] = str({
            'owner':
            str(owner_id),
            'members':
            str(members)
        })
        FEDERATION_BYFEDID[str(fed_id)]['fusers'] = str({
            'owner': str(owner_id),
            'members': str(members)
        })
        FEDERATION_BYNAME[fed_name]['fusers'] = str({
            'owner': str(owner_id),
            'members': str(members)
        })
        # Set on database
        fed = Federations(
            str(owner_id), fed_name, str(fed_id), fed_rules,
            str({
                'owner': str(owner_id),
                'members': str(members)
            }))
        SESSION.merge(fed)
        SESSION.commit()
        return True


def user_join_fed(fed_id, user_id):
    with FEDS_LOCK:
        global FEDERATION_BYOWNER, FEDERATION_BYFEDID, FEDERATION_BYNAME
        # Variables
        getfed = FEDERATION_BYFEDID.get(str(fed_id))
        owner_id = getfed['owner']
        fed_name = getfed['fname']
        fed_rules = getfed['frules']
        # Temp set
        members = eval(eval(getfed['fusers'])['members'])
        members.append(user_id)
        # Set user
        FEDERATION_BYOWNER[str(owner_id)]['fusers'] = str({
            'owner':
            str(owner_id),
            'members':
            str(members)
        })
        FEDERATION_BYFEDID[str(fed_id)]['fusers'] = str({
            'owner': str(owner_id),
            'members': str(members)
        })
        FEDERATION_BYNAME[fed_name]['fusers'] = str({
            'owner': str(owner_id),
            'members': str(members)
        })
        # Set on database
        fed = Federations(
            str(owner_id), fed_name, str(fed_id), fed_rules,
            str({
                'owner': str(owner_id),
                'members': str(members)
            }))
        SESSION.merge(fed)
        SESSION.commit()
        __load_all_feds_chats()
        return True


def chat_leave_fed(chat_id):
    with FEDS_LOCK:
        global FEDERATION_CHATS, FEDERATION_CHATS_BYID
        # Set variables
        fed_info = FEDERATION_CHATS.get(str(chat_id))
        if fed_info == None:
            return False
        fed_id = fed_info['fid']
        # Delete from cache
        FEDERATION_CHATS.pop(str(chat_id))
        FEDERATION_CHATS_BYID[str(fed_id)].remove(str(chat_id))
        # Delete from db
        curr = SESSION.query(ChatF).all()
        for U in curr:
            if int(U.chat_id) == int(chat_id):
                SESSION.delete(U)
                SESSION.commit()
        return True


def all_fed_chats(fed_id):
    with FEDS_LOCK:
        getfed = FEDERATION_CHATS_BYID.get(fed_id)
        if getfed == None:
            return []
        else:
            return getfed


def all_fed_users(fed_id):
    with FEDS_LOCK:
        getfed = FEDERATION_BYFEDID.get(str(fed_id))
        if getfed == None:
            return False
        fed_owner = eval(eval(getfed['fusers'])['owner'])
        fed_admins = eval(eval(getfed['fusers'])['members'])
        fed_admins.append(fed_owner)
        return fed_admins


def all_fed_members(fed_id):
    with FEDS_LOCK:
        getfed = FEDERATION_BYFEDID.get(str(fed_id))
        fed_admins = eval(eval(getfed['fusers'])['members'])
        return fed_admins


def set_frules(fed_id, rules):
    with FEDS_LOCK:
        global FEDERATION_BYOWNER, FEDERATION_BYFEDID, FEDERATION_BYNAME
        # Variables
        getfed = FEDERATION_BYFEDID.get(str(fed_id))
        owner_id = getfed['owner']
        fed_name = getfed['fname']
        fed_members = getfed['fusers']
        fed_rules = str(rules)
        # Set user
        FEDERATION_BYOWNER[str(owner_id)]['frules'] = fed_rules
        FEDERATION_BYFEDID[str(fed_id)]['frules'] = fed_rules
        FEDERATION_BYNAME[fed_name]['frules'] = fed_rules
        # Set on database
        fed = Federations(str(owner_id), fed_name, str(fed_id), fed_rules,
                          str(fed_members))
        SESSION.merge(fed)
        SESSION.commit()
        return True


def get_frules(fed_id):
    with FEDS_LOCK:
        rules = FEDERATION_BYFEDID[str(fed_id)]['frules']
        return rules


def fban_user(fed_id, user_id, first_name, last_name, user_name, reason):
    with FEDS_LOCK:
        r = SESSION.query(BansF).all()
        for I in r:
            if I.fed_id == fed_id:
                if int(I.user_id) == int(user_id):
                    SESSION.delete(I)

        r = BansF(str(fed_id), str(user_id), first_name, last_name, user_name,
                  reason)

        SESSION.add(r)
        try:
            SESSION.commit()
        except Exception:
            SESSION.rollback()
            return False
        finally:
            SESSION.commit()
        __load_all_feds_banned()
        return r


def un_fban_user(fed_id, user_id):
    with FEDS_LOCK:
        r = SESSION.query(BansF).all()
        for I in r:
            if I.fed_id == fed_id:
                if int(I.user_id) == int(user_id):
                    SESSION.delete(I)
        try:
            SESSION.commit()
        except Exception:
            SESSION.rollback()
            return False
        finally:
            SESSION.commit()
        __load_all_feds_banned()
        return I


def get_fban_user(fed_id, user_id):
    list_fbanned = FEDERATION_BANNED_USERID.get(fed_id)
    if list_fbanned == None:
        FEDERATION_BANNED_USERID[fed_id] = []
    if user_id in FEDERATION_BANNED_USERID[fed_id]:
        r = SESSION.query(BansF).all()
        reason = None
        for I in r:
            if I.fed_id == fed_id:
                if int(I.user_id) == int(user_id):
                    reason = I.reason
        return True, reason
    else:
        return False, None


def get_all_fban_users(fed_id):
    list_fbanned = FEDERATION_BANNED_USERID.get(fed_id)
    if list_fbanned == None:
        FEDERATION_BANNED_USERID[fed_id] = []
    return FEDERATION_BANNED_USERID[fed_id]


def get_all_fban_users_target(fed_id, user_id):
    list_fbanned = FEDERATION_BANNED_FULL.get(fed_id)
    if list_fbanned == None:
        FEDERATION_BANNED_FULL[fed_id] = []
        return False
    getuser = list_fbanned[str(user_id)]
    return getuser


def get_all_fban_users_global():
    total = []
    for x in list(FEDERATION_BANNED_USERID):
        for y in FEDERATION_BANNED_USERID[x]:
            total.append(y)
    return total


def get_all_feds_users_global():
    total = []
    for x in list(FEDERATION_BYFEDID):
        total.append(FEDERATION_BYFEDID[x])
    return total


def search_fed_by_id(fed_id):
    get = FEDERATION_BYFEDID.get(fed_id)
    if get == None:
        return False
    else:
        return get
    result = False
    for Q in curr:
        if Q.fed_id == fed_id:
            result = Q.fed_id

    return result


def user_feds_report(user_id: int) -> bool:
    user_setting = FEDERATION_NOTIFICATION.get(str(user_id))
    if user_setting == None:
        user_setting = True
    return user_setting


def set_feds_setting(user_id: int, setting: bool):
    with FEDS_SETTINGS_LOCK:
        global FEDERATION_NOTIFICATION
        user_setting = SESSION.query(FedsUserSettings).get(user_id)
        if not user_setting:
            user_setting = FedsUserSettings(user_id)

        user_setting.should_report = setting
        FEDERATION_NOTIFICATION[str(user_id)] = setting
        SESSION.add(user_setting)
        SESSION.commit()


def __load_all_feds():
    global FEDERATION_BYOWNER, FEDERATION_BYFEDID, FEDERATION_BYNAME
    try:
        feds = SESSION.query(Federations).all()
        for x in feds:  # remove tuple by ( ,)
            # Fed by Owner
            check = FEDERATION_BYOWNER.get(x.owner_id)
            if check == None:
                FEDERATION_BYOWNER[x.owner_id] = []
            FEDERATION_BYOWNER[str(x.owner_id)] = {
                'fid': str(x.fed_id),
                'fname': x.fed_name,
                'frules': x.fed_rules,
                'fusers': str(x.fed_users)
            }
            # Fed By FedId
            check = FEDERATION_BYFEDID.get(x.fed_id)
            if check == None:
                FEDERATION_BYFEDID[x.fed_id] = []
            FEDERATION_BYFEDID[str(x.fed_id)] = {
                'owner': str(x.owner_id),
                'fname': x.fed_name,
                'frules': x.fed_rules,
                'fusers': str(x.fed_users)
            }
            # Fed By Name
            check = FEDERATION_BYNAME.get(x.fed_name)
            if check == None:
                FEDERATION_BYNAME[x.fed_name] = []
            FEDERATION_BYNAME[x.fed_name] = {
                'fid': str(x.fed_id),
                'owner': str(x.owner_id),
                'frules': x.fed_rules,
                'fusers': str(x.fed_users)
            }
    finally:
        SESSION.close()


def __load_all_feds_chats():
    global FEDERATION_CHATS, FEDERATION_CHATS_BYID
    try:
        qall = SESSION.query(ChatF).all()
        FEDERATION_CHATS = {}
        FEDERATION_CHATS_BYID = {}
        for x in qall:
            # Federation Chats
            check = FEDERATION_CHATS.get(x.chat_id)
            if check == None:
                FEDERATION_CHATS[x.chat_id] = {}
            FEDERATION_CHATS[x.chat_id] = {'fid': x.fed_id}
            # Federation Chats By ID
            check = FEDERATION_CHATS_BYID.get(x.fed_id)
            if check == None:
                FEDERATION_CHATS_BYID[x.fed_id] = []
            FEDERATION_CHATS_BYID[x.fed_id].append(x.chat_id)
    finally:
        SESSION.close()


def __load_all_feds_banned():
    global FEDERATION_BANNED_USERID, FEDERATION_BANNED_FULL
    try:
        FEDERATION_BANNED_USERID = {}
        FEDERATION_BANNED_FULL = {}
        qall = SESSION.query(BansF).all()
        for x in qall:
            check = FEDERATION_BANNED_USERID.get(x.fed_id)
            if check == None:
                FEDERATION_BANNED_USERID[x.fed_id] = []
            if int(x.user_id) not in FEDERATION_BANNED_USERID[x.fed_id]:
                FEDERATION_BANNED_USERID[x.fed_id].append(int(x.user_id))
            check = FEDERATION_BANNED_FULL.get(x.fed_id)
            if check == None:
                FEDERATION_BANNED_FULL[x.fed_id] = {}
            FEDERATION_BANNED_FULL[x.fed_id][x.user_id] = {
                'first_name': x.first_name,
                'last_name': x.last_name,
                'user_name': x.user_name,
                'reason': x.reason
            }
    finally:
        SESSION.close()


def __load_all_feds_settings():
    global FEDERATION_NOTIFICATION
    try:
        getuser = SESSION.query(FedsUserSettings).all()
        for x in getuser:
            FEDERATION_NOTIFICATION[str(x.user_id)] = x.should_report
    finally:
        SESSION.close()


__load_all_feds()
__load_all_feds_chats()
__load_all_feds_banned()
__load_all_feds_settings()

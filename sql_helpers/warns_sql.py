import threading

from sqlalchemy import Integer, Column, String, UnicodeText, func, distinct, Boolean

from sql_helpers import SESSION, BASE


class Warns(BASE):
    __tablename__ = "warns"

    user_id = Column(Integer, primary_key=True)
    chat_id = Column(String(14), primary_key=True)
    num_warns = Column(Integer, default=0)
    reasons = Column(UnicodeText)

    def __init__(self, user_id, chat_id):
        self.user_id = user_id
        self.chat_id = str(chat_id)
        self.num_warns = 0
        self.reasons = ""

    def __repr__(self):
        return "<{} warns for {} in {} for reasons {}>".format(self.num_warns, self.user_id, self.chat_id, self.reasons)


class WarnSettings(BASE):
    __tablename__ = "warn_settings"
    chat_id = Column(String(14), primary_key=True)
    warn_limit = Column(Integer, default=3)
    soft_warn = Column(Boolean, default=False)

    def __init__(self, chat_id, warn_limit=3, soft_warn=False):
        self.chat_id = str(chat_id)
        self.warn_limit = warn_limit
        self.soft_warn = soft_warn

    def __repr__(self):
        return "<{} has {} possible warns.>".format(self.chat_id, self.warn_limit)



Warns.__table__.create(checkfirst=True)
WarnSettings.__table__.create(checkfirst=True)


WARN_INSERTION_LOCK = threading.RLock()
WARN_SETTINGS_LOCK = threading.RLock()


def warn_user(user_id, chat_id, reason=None):
    with WARN_INSERTION_LOCK:
        warned_user = SESSION.query(Warns).get((user_id, str(chat_id)))
        if not warned_user:
            warned_user = Warns(user_id, str(chat_id))

        warned_user.num_warns += 1
        if reason:
            warned_user.reasons = warned_user.reasons + "\r\n\r\n" + reason  # TODO:: double check this wizardry

        reasons = warned_user.reasons
        num = warned_user.num_warns

        SESSION.add(warned_user)
        SESSION.commit()

        return num, reasons


def remove_warn(user_id, chat_id):
    with WARN_INSERTION_LOCK:
        removed = False
        warned_user = SESSION.query(Warns).get((user_id, str(chat_id)))

        if warned_user and warned_user.num_warns > 0:
            warned_user.num_warns -= 1

            SESSION.add(warned_user)
            SESSION.commit()
            removed = True

        SESSION.close()
        return removed


def reset_warns(user_id, chat_id):
    with WARN_INSERTION_LOCK:
        warned_user = SESSION.query(Warns).get((user_id, str(chat_id)))
        if warned_user:
            warned_user.num_warns = 0
            warned_user.reasons = ""

            SESSION.add(warned_user)
            SESSION.commit()
        SESSION.close()


def get_warns(user_id, chat_id):
    try:
        user = SESSION.query(Warns).get((user_id, str(chat_id)))
        if not user:
            return None
        reasons = user.reasons
        num = user.num_warns
        return num, reasons
    finally:
        SESSION.close()


def set_warn_limit(chat_id, warn_limit):
    with WARN_SETTINGS_LOCK:
        curr_setting = SESSION.query(WarnSettings).get(str(chat_id))
        if not curr_setting:
            curr_setting = WarnSettings(chat_id, warn_limit=warn_limit)

        curr_setting.warn_limit = warn_limit

        SESSION.add(curr_setting)
        SESSION.commit()


def set_warn_strength(chat_id, soft_warn):
    with WARN_SETTINGS_LOCK:
        curr_setting = SESSION.query(WarnSettings).get(str(chat_id))
        if not curr_setting:
            curr_setting = WarnSettings(chat_id, soft_warn=soft_warn)

        curr_setting.soft_warn = soft_warn

        SESSION.add(curr_setting)
        SESSION.commit()


def get_warn_setting(chat_id):
    try:
        setting = SESSION.query(WarnSettings).get(str(chat_id))
        if setting:
            return setting.warn_limit, setting.soft_warn
        else:
            return 3, False

    finally:
        SESSION.close()


def num_warns():
    try:
        return SESSION.query(func.sum(Warns.num_warns)).scalar() or 0
    finally:
        SESSION.close()


def num_warn_chats():
    try:
        return SESSION.query(func.count(distinct(Warns.chat_id))).scalar()
    finally:
        SESSION.close()

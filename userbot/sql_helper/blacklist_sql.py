import threading

from sqlalchemy import Column, String, UnicodeText, distinct, func

from . import BASE, SESSION


class BlackListFilters(BASE):
    __tablename__ = "blacklist"
    chat_id = Column(String(14), primary_key=True)
    trigger = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, chat_id, trigger):
        self.chat_id = str(chat_id)  # ensure string
        self.trigger = trigger

    def __repr__(self):
        return "<Blacklist filter '%s' for %s>" % (self.trigger, self.chat_id)

    def __eq__(self, other):
        return bool(
            isinstance(other, BlackListFilters)
            and self.chat_id == other.chat_id
            and self.trigger == other.trigger
        )


BlackListFilters.__table__.create(checkfirst=True)

BLACKLIST_FILTER_INSERTION_LOCK = threading.RLock()


class BLACKLIST_SQL:
    def __init__(self):
        self.CHAT_BLACKLISTS = {}


BLACKLIST_SQL_ = BLACKLIST_SQL()


def add_to_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = BlackListFilters(str(chat_id), trigger)

        SESSION.merge(blacklist_filt)  # merge to avoid duplicate key issues
        SESSION.commit()
        BLACKLIST_SQL_.CHAT_BLACKLISTS.setdefault(str(chat_id), set()).add(trigger)


def rm_from_blacklist(chat_id, trigger):
    with BLACKLIST_FILTER_INSERTION_LOCK:
        blacklist_filt = SESSION.query(BlackListFilters).get((str(chat_id), trigger))
        if blacklist_filt:
            if trigger in BLACKLIST_SQL_.CHAT_BLACKLISTS.get(
                str(chat_id), set()
            ):  # sanity check
                BLACKLIST_SQL_.CHAT_BLACKLISTS.get(str(chat_id), set()).remove(trigger)

            SESSION.delete(blacklist_filt)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def get_chat_blacklist(chat_id):
    return BLACKLIST_SQL_.CHAT_BLACKLISTS.get(str(chat_id), set())


def num_blacklist_filters():
    try:
        return SESSION.query(BlackListFilters).count()
    finally:
        SESSION.close()


def num_blacklist_chat_filters(chat_id):
    try:
        return (
            SESSION.query(BlackListFilters.chat_id)
            .filter(BlackListFilters.chat_id == str(chat_id))
            .count()
        )
    finally:
        SESSION.close()


def num_blacklist_filter_chats():
    try:
        return SESSION.query(func.count(distinct(BlackListFilters.chat_id))).scalar()
    finally:
        SESSION.close()


def __load_chat_blacklists():
    try:
        chats = SESSION.query(BlackListFilters.chat_id).distinct().all()
        for (chat_id,) in chats:  # remove tuple by ( ,)
            BLACKLIST_SQL_.CHAT_BLACKLISTS[chat_id] = []

        all_filters = SESSION.query(BlackListFilters).all()
        for x in all_filters:
            BLACKLIST_SQL_.CHAT_BLACKLISTS[x.chat_id] += [x.trigger]

        BLACKLIST_SQL_.CHAT_BLACKLISTS = {
            x: set(y) for x, y in BLACKLIST_SQL_.CHAT_BLACKLISTS.items()
        }

    finally:
        SESSION.close()


__load_chat_blacklists()

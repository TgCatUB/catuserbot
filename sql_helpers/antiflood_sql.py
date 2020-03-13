import threading

from sqlalchemy import Column, Integer, String

from sql_helpers import BASE, SESSION

DEF_COUNT = 0
DEF_LIMIT = 0
DEF_OBJ = (None, DEF_COUNT, DEF_LIMIT)


class FloodControl(BASE):
    __tablename__ = "antiflood"
    chat_id = Column(String(14), primary_key=True)
    user_id = Column(Integer)
    count = Column(Integer, default=DEF_COUNT)
    limit = Column(Integer, default=DEF_LIMIT)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)  # ensure string

    def __repr__(self):
        return "<flood control for %s>" % self.chat_id


FloodControl.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()

CHAT_FLOOD = {}


def set_flood(chat_id, amount):
    with INSERTION_LOCK:
        flood = SESSION.query(FloodControl).get(str(chat_id))
        if not flood:
            flood = FloodControl(str(chat_id))

        flood.user_id = None
        flood.limit = amount

        CHAT_FLOOD[str(chat_id)] = (None, DEF_COUNT, amount)

        SESSION.add(flood)
        SESSION.commit()


def update_flood(chat_id: str, user_id) -> bool:
    if str(chat_id) in CHAT_FLOOD:
        curr_user_id, count, limit = CHAT_FLOOD.get(str(chat_id), DEF_OBJ)

        if limit == 0:  # no antiflood
            return False

        if user_id != curr_user_id or user_id is None:  # other user
            CHAT_FLOOD[str(chat_id)] = (user_id, DEF_COUNT + 1, limit)
            return False

        count += 1
        if count > limit:  # too many msgs, kick
            CHAT_FLOOD[str(chat_id)] = (None, DEF_COUNT, limit)
            return True

        # default -> update
        CHAT_FLOOD[str(chat_id)] = (user_id, count, limit)
        return False


def get_flood_limit(chat_id):
    return CHAT_FLOOD.get(str(chat_id), DEF_OBJ)[2]


def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        flood = SESSION.query(FloodControl).get(str(old_chat_id))
        if flood:
            CHAT_FLOOD[str(new_chat_id)] = CHAT_FLOOD.get(str(old_chat_id), DEF_OBJ)
            flood.chat_id = str(new_chat_id)
            SESSION.commit()

        SESSION.close()


def __load_flood_settings():
    global CHAT_FLOOD
    try:
        all_chats = SESSION.query(FloodControl).all()
        CHAT_FLOOD = {chat.chat_id: (None, DEF_COUNT, chat.limit) for chat in all_chats}
    finally:
        SESSION.close()
    return CHAT_FLOOD



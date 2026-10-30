import threading

from sqlalchemy import Column, String, UnicodeText, delete, distinct, func, select

from . import BASE, SESSION, create_table


class CatGloballist(BASE):
    __tablename__ = "catglobal_list"
    keywoard = Column(UnicodeText, primary_key=True)
    group_id = Column(String, primary_key=True, nullable=False)

    def __init__(self, keywoard, group_id):
        self.keywoard = keywoard
        self.group_id = str(group_id)

    def __repr__(self):
        return f"<Cat global values '{self.group_id}' for {self.keywoard}>"

    def __eq__(self, other):
        return isinstance(other, CatGloballist) and self.keywoard == other.keywoard and self.group_id == other.group_id


create_table(CatGloballist.__table__)

CATGLOBALLIST_INSERTION_LOCK = threading.RLock()


class GLOBALLIST_SQL:
    def __init__(self):
        self.GLOBALLIST_VALUES = {}


GLOBALLIST_SQL_ = GLOBALLIST_SQL()


def add_to_list(keywoard, group_id):
    with CATGLOBALLIST_INSERTION_LOCK:
        broadcast_group = CatGloballist(keywoard, str(group_id))
        SESSION.merge(broadcast_group)
        SESSION.commit()
        GLOBALLIST_SQL_.GLOBALLIST_VALUES.setdefault(keywoard, set()).add(str(group_id))


def rm_from_list(keywoard, group_id):
    with CATGLOBALLIST_INSERTION_LOCK:
        if broadcast_group := SESSION.get(CatGloballist, (keywoard, str(group_id))):
            if str(group_id) in GLOBALLIST_SQL_.GLOBALLIST_VALUES.get(keywoard, set()):
                GLOBALLIST_SQL_.GLOBALLIST_VALUES.get(keywoard, set()).remove(str(group_id))

            SESSION.delete(broadcast_group)
            SESSION.commit()
            return True
        SESSION.close()
        return False


def is_in_list(keywoard, group_id):
    with CATGLOBALLIST_INSERTION_LOCK:
        broadcast_group = SESSION.get(CatGloballist, (keywoard, str(group_id)))
        return bool(broadcast_group)


def del_keyword_list(keywoard):
    with CATGLOBALLIST_INSERTION_LOCK:
        SESSION.execute(delete(CatGloballist).where(CatGloballist.keywoard == keywoard))
        GLOBALLIST_SQL_.GLOBALLIST_VALUES.pop(keywoard)
        SESSION.commit()


def get_collection_list(keywoard):
    return GLOBALLIST_SQL_.GLOBALLIST_VALUES.get(keywoard, set())


def get_list_keywords():
    try:
        chats = SESSION.execute(select(CatGloballist.keywoard).distinct()).all()
        return [i[0] for i in chats]
    finally:
        SESSION.close()


def num_list():
    try:
        return SESSION.scalar(select(func.count()).select_from(CatGloballist))
    finally:
        SESSION.close()


def num_list_keyword(keywoard):
    try:
        statement = select(func.count()).select_from(CatGloballist).where(
            CatGloballist.keywoard == keywoard
        )
        return SESSION.scalar(statement)
    finally:
        SESSION.close()


def num_list_keywords():
    try:
        return SESSION.scalar(select(func.count(distinct(CatGloballist.keywoard))))
    finally:
        SESSION.close()


def __load_chat_lists():
    try:
        chats = SESSION.execute(select(CatGloballist.keywoard).distinct()).all()
        for (keywoard,) in chats:
            GLOBALLIST_SQL_.GLOBALLIST_VALUES[keywoard] = []

        all_groups = SESSION.scalars(select(CatGloballist)).all()
        for x in all_groups:
            GLOBALLIST_SQL_.GLOBALLIST_VALUES[x.keywoard] += [x.group_id]

        GLOBALLIST_SQL_.GLOBALLIST_VALUES = {x: set(y) for x, y in GLOBALLIST_SQL_.GLOBALLIST_VALUES.items()}

    finally:
        SESSION.close()


__load_chat_lists()

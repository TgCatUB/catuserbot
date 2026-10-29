import threading

from sqlalchemy import Column, PickleType, UnicodeText, delete, distinct, func, select

from . import BASE, SESSION, create_table


class Cat_GlobalCollection(BASE):
    __tablename__ = "cat_globalcollection"
    keywoard = Column(UnicodeText, primary_key=True)
    contents = Column(PickleType, primary_key=True, nullable=False)

    def __init__(self, keywoard, contents):
        self.keywoard = keywoard
        self.contents = tuple(contents)

    def __repr__(self):
        return f"<Cat Global Collection lists '{self.contents}' for {self.keywoard}>"

    def __eq__(self, other):
        return isinstance(other, Cat_GlobalCollection) and self.keywoard == other.keywoard and self.contents == other.contents


create_table(Cat_GlobalCollection.__table__)

CAT_GLOBALCOLLECTION = threading.RLock()


class COLLECTION_SQL:
    def __init__(self):
        self.CONTENTS_LIST = {}


COLLECTION_SQL_ = COLLECTION_SQL()


def add_to_collectionlist(keywoard, contents):
    with CAT_GLOBALCOLLECTION:
        keyword_items = Cat_GlobalCollection(keywoard, tuple(contents))

        SESSION.merge(keyword_items)
        SESSION.commit()
        COLLECTION_SQL_.CONTENTS_LIST.setdefault(keywoard, set()).add(tuple(contents))


def rm_from_collectionlist(keywoard, contents):
    with CAT_GLOBALCOLLECTION:
        if keyword_items := SESSION.get(Cat_GlobalCollection, (keywoard, tuple(contents))):
            if tuple(contents) in COLLECTION_SQL_.CONTENTS_LIST.get(keywoard, set()):
                COLLECTION_SQL_.CONTENTS_LIST.get(keywoard, set()).remove(tuple(contents))
            SESSION.delete(keyword_items)
            SESSION.commit()
            return True

        SESSION.close()
        return False


def is_in_collectionlist(keywoard, contents):
    with CAT_GLOBALCOLLECTION:
        keyword_items = COLLECTION_SQL_.CONTENTS_LIST.get(keywoard, set())
        return any(tuple(contents) == list1 for list1 in keyword_items)


def del_keyword_collectionlist(keywoard):
    with CAT_GLOBALCOLLECTION:
        SESSION.execute(
            delete(Cat_GlobalCollection).where(Cat_GlobalCollection.keywoard == keywoard)
        )
        COLLECTION_SQL_.CONTENTS_LIST.pop(keywoard)
        SESSION.commit()


def get_item_collectionlist(keywoard):
    return COLLECTION_SQL_.CONTENTS_LIST.get(keywoard, set())


def get_collectionlist_items():
    try:
        chats = SESSION.execute(select(Cat_GlobalCollection.keywoard).distinct()).all()
        return [i[0] for i in chats]
    finally:
        SESSION.close()


def num_collectionlist():
    try:
        return SESSION.scalar(select(func.count()).select_from(Cat_GlobalCollection))
    finally:
        SESSION.close()


def num_collectionlist_item(keywoard):
    try:
        statement = select(func.count()).select_from(Cat_GlobalCollection).where(
            Cat_GlobalCollection.keywoard == keywoard
        )
        return SESSION.scalar(statement)
    finally:
        SESSION.close()


def num_collectionlist_items():
    try:
        return SESSION.scalar(select(func.count(distinct(Cat_GlobalCollection.keywoard))))
    finally:
        SESSION.close()


def __load_item_collectionlists():
    try:
        chats = SESSION.execute(select(Cat_GlobalCollection.keywoard).distinct()).all()
        for (keywoard,) in chats:
            COLLECTION_SQL_.CONTENTS_LIST[keywoard] = []

        all_groups = SESSION.scalars(select(Cat_GlobalCollection)).all()
        for x in all_groups:
            COLLECTION_SQL_.CONTENTS_LIST[x.keywoard] += [x.contents]

        COLLECTION_SQL_.CONTENTS_LIST = {x: set(y) for x, y in COLLECTION_SQL_.CONTENTS_LIST.items()}

    finally:
        SESSION.close()


__load_item_collectionlists()

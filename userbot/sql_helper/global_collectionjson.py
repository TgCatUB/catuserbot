from sqlalchemy import Column, PickleType, UnicodeText

from . import BASE, SESSION


class Cat_GlobalCollection_Json(BASE):
    __tablename__ = "cat_globalcollection_json"
    keywoard = Column(UnicodeText, primary_key=True)
    contents = Column(PickleType, primary_key=True, nullable=False)

    def __init__(self, keywoard, contents):
        self.keywoard = keywoard
        self.contents = contents

    def __repr__(self):
        return "<Cat Global Collection lists '%s' for %s>" % (
            self.contents,
            self.keywoard,
        )

    def __eq__(self, other):
        return bool(
            isinstance(other, Cat_GlobalCollection_Json)
            and self.keywoard == other.keywoard
            and self.contents == other.contents
        )


Cat_GlobalCollection_Json.__table__.create(checkfirst=True)


def add_to_collectionlist(keywoard, contents):
    keyword_items = Cat_GlobalCollection_Json(keywoard, contents)
    SESSION.merge(keyword_items)
    SESSION.commit()


def rm_from_collectionlist(keywoard, contents):
    keyword_items = SESSION.query(Cat_GlobalCollection_Json).get((keywoard, contents))
    if keyword_items:
        SESSION.delete(keyword_items)
        SESSION.commit()
        return True
    SESSION.close()
    return False


def get_item_collectionlist(keywoard):
    try:
        return SESSION.query(Cat_GlobalCollection_Json.keywoard).filter(
            Cat_GlobalCollection_Json.keywoard == keywoard
        )
    finally:
        SESSION.close()


def num_collectionlist():
    try:
        return SESSION.query(Cat_GlobalCollection_Json).count()
    finally:
        SESSION.close()


def num_collectionlist_item(keywoard):
    try:
        return (
            SESSION.query(Cat_GlobalCollection_Json.keywoard)
            .filter(Cat_GlobalCollection_Json.keywoard == keywoard)
            .count()
        )
    finally:
        SESSION.close()

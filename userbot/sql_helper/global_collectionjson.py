from sqlalchemy import Column, UnicodeText
from sqlalchemy_json import MutableJson, NestedMutableJson

from . import BASE, SESSION


class Cat_GlobalCollection_Json(BASE):
    __tablename__ = "cat_globalcollectionjson"
    keywoard = Column(UnicodeText, primary_key=True)
    json = Column(MutableJson)
    njson = Column(NestedMutableJson)

    def __init__(self, keywoard, json, njson):
        self.keywoard = keywoard
        self.json = json
        self.njson = njson


Cat_GlobalCollection_Json.__table__.create(checkfirst=True)


def get_collection(keywoard):
    try:
        return SESSION.query(Cat_GlobalCollection_Json).get(keywoard)
    finally:
        SESSION.close()


def add_collection(keywoard, json, njson):
    to_check = get_collection(keywoard)
    if not to_check:
        keyword_items = Cat_GlobalCollection_Json(keywoard, json, njson)
        SESSION.add(keyword_items)
        SESSION.commit()
        return True
    return False


def del_collection(keywoard):
    to_check = get_collection(keywoard)
    if not to_check:
        return False
    keyword_items = SESSION.query(Cat_GlobalCollection_Json).get(keywoard)
    SESSION.delete(keyword_items)
    SESSION.commit()
    return True


def get_collections():
    try:
        return SESSION.query(Cat_GlobalCollection_Json).all()
    finally:
        SESSION.close()

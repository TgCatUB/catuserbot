from sqlalchemy import Column, UnicodeText, select
from sqlalchemy_json import MutableJson, NestedMutableJson

from . import BASE, SESSION, create_table


class Cat_GlobalCollection_Json(BASE):
    __tablename__ = "cat_globalcollectionjson"
    keywoard = Column(UnicodeText, primary_key=True)
    json = Column(MutableJson)
    njson = Column(NestedMutableJson)

    def __init__(self, keywoard, json, njson):
        self.keywoard = keywoard
        self.json = json
        self.njson = njson


create_table(Cat_GlobalCollection_Json.__table__)


def get_collection(keywoard):
    try:
        return SESSION.get(Cat_GlobalCollection_Json, keywoard)
    finally:
        SESSION.close()


def add_collection(keywoard, json, njson=None):
    if njson is None:
        njson = {}
    if to_check := get_collection(keywoard):  # noqa F841
        keyword_items = SESSION.get(Cat_GlobalCollection_Json, keywoard)
        SESSION.delete(keyword_items)
    keyword_items = Cat_GlobalCollection_Json(keywoard, json, njson)
    SESSION.add(keyword_items)
    SESSION.commit()
    return True


def del_collection(keywoard):
    to_check = get_collection(keywoard)
    if not to_check:
        return False
    keyword_items = SESSION.get(Cat_GlobalCollection_Json, keywoard)
    SESSION.delete(keyword_items)
    SESSION.commit()
    return True


def get_collections():
    try:
        return SESSION.scalars(select(Cat_GlobalCollection_Json)).all()
    finally:
        SESSION.close()

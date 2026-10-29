from sqlalchemy import Column, String, UnicodeText, delete, select

from . import BASE, SESSION, create_table


class Globals(BASE):
    __tablename__ = "globals"
    variable = Column(String, primary_key=True, nullable=False)
    value = Column(UnicodeText, primary_key=True, nullable=False)

    def __init__(self, variable, value):
        self.variable = str(variable)
        self.value = value


create_table(Globals.__table__)


def gvarstatus(variable):
    try:
        return SESSION.scalars(
            select(Globals).where(Globals.variable == str(variable))
        ).first().value
    except BaseException:
        return None
    finally:
        SESSION.close()


def addgvar(variable, value):
    if SESSION.scalars(
        select(Globals).where(Globals.variable == str(variable))
    ).one_or_none():
        delgvar(variable)
    adder = Globals(str(variable), value)
    SESSION.add(adder)
    SESSION.commit()


def delgvar(variable):
    result = SESSION.execute(
        delete(Globals)
        .where(Globals.variable == str(variable))
        .execution_options(synchronize_session="fetch")
    )
    if result.rowcount:
        SESSION.commit()

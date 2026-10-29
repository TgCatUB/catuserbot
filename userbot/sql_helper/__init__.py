import os  # noqa F401

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

# the secret configuration specific things
from ..Config import Config
from ..core.logger import logging

LOGS = logging.getLogger(__name__)


def start() -> scoped_session:
    database_url = Config.DATABASE_URL.replace("postgres:", "postgresql:") if "postgres://" in Config.DATABASE_URL else Config.DATABASE_URL
    engine = create_engine(database_url)
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    # this is a dirty way for the work-around required for #23
    LOGS.error("DATABASE_URL is not configured. Features depending on the database might have issues.")
    LOGS.error(str(e))


def create_table(table):
    table.create(bind=SESSION.get_bind(), checkfirst=True)

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# the secret configuration specific things
ENV = bool(os.environ.get("ENV", False))
if ENV:
    from sample_config import Config
else:
    if os.path.exists("config.py"):
        from config import Development as Config


def start() -> scoped_session:
    engine = create_engine(Config.DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    # this is a dirty way for the work-around required for #23
    print("DB_URI is not configured. Features depending on the database might have issues.")
    print(str(e))


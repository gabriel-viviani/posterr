from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

from src.config import get_database_url, get_environment, TEST_ENV

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    env = get_environment()
    if env != TEST_ENV:
        Base.metadata.create_all(bind=engine)

    return

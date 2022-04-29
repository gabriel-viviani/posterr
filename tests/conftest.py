from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
import pytest

from src.repository.database import get_db, Base
from src.config import get_test_db_url
from src.main import app

from tests.helpers import (
    random_name,
    rand_date,
)
from src.model.user import User


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(get_test_db_url())
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    transaction = connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_first_user(db):
    _user = User(username=random_name())

    db.add(_user)
    db.flush()
    db.refresh(_user)

    yield _user


@pytest.fixture
def db_second_user(db):
    _user = User(username=random_name())

    db.add(_user)
    db.flush()
    db.refresh(_user)

    yield _user

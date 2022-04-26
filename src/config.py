import os
from datetime import date

DEFAULT_DATABASE_URL = "postgresql://user:password@localhost:5432/database"
DEFAULT_ENV = "DEV"
TEST_ENV = "TEST"


def generate_today() -> date:
    return date.today()


def get_database_url() -> str:
    return os.environ.get("DB_URL", DEFAULT_DATABASE_URL)


def get_test_db_url() -> str:
    return os.environ.get("TEST_DB_URL", DEFAULT_DATABASE_URL)


def get_environment() -> str:
    return os.environ.get("ENV", DEFAULT_ENV)

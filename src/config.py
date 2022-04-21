import os
from datetime import datetime

import pytz

DEFAULT_TIMEZONE_REGION = "America/Sao_Paulo"
DEFAULT_DATABASE_URL = "postgresql://user:password@localhost:5432/database"
DEFAULT_ENV = "DEV"
TEST_ENV = "TEST"


def get_timezone_region() -> str:
    return os.environ.get("TIMEZONE_REGION", DEFAULT_TIMEZONE_REGION)


def generate_now() -> datetime:
    tz = pytz.timezone(get_timezone_region())
    return datetime.now(tz)


def get_database_url() -> str:
    return os.environ.get("DB_URL", DEFAULT_DATABASE_URL)


def get_test_db_url() -> str:
    return os.environ.get("TEST_DB_URL", DEFAULT_DATABASE_URL)


def get_environment() -> str:
    return os.environ.get("ENV", DEFAULT_ENV)

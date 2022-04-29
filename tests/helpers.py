from uuid import uuid4, UUID
from datetime import date
from faker import Faker


def random_name() -> str:
    name: str = Faker().name()
    return name


def rand_date() -> date:
    x: date = Faker().date()
    return x


def rand_small_text() -> str:
    faker = Faker()
    text: str = faker.paragraph(nb_sentences=5, variable_nb_sentences=False)
    return text


def rand_giant_text() -> str:
    faker = Faker()
    txt: str = faker.paragraph(nb_sentences=20, variable_nb_sentences=False)
    return txt


def rand_uuid() -> UUID:
    return uuid4()

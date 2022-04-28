import logging
from fastapi import FastAPI

from src.entrypoint.router import api_router
from src.repository.database import init_db
from fastapi_pagination import add_pagination

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(api_router)

add_pagination(app)


init_db()

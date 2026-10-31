import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import URL

from functools import cache


def get_db_url() -> URL:
    return URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5555")),
        database=os.getenv("DB_NAME", "similarity_search_service_db"),
    )


@cache
def get_engine() -> Engine:
    return create_engine(get_db_url())

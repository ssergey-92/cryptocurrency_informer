"""Module for creating connection to db."""

from os import getenv

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool


def get_db_url() -> str:
    """Get url for connection to app db."""

    return "postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}".format(
        username=getenv("DB_USERNAME"),
        password=getenv("DB_PASSWORD"),
        host=getenv("DC_DB_NAME"),
        port=getenv("DB_PORT"),
        db_name=getenv("DB_NAME"),
    )


def get_async_engine() -> AsyncEngine:
    """Get asynchronous engine for production or testing purpose."""

    db_url = get_db_url()
    if getenv("APP_TESTING", "False") == "False":
        return create_async_engine(db_url)

    return create_async_engine(db_url, poolclass=NullPool)


Base = declarative_base()
async_engine = get_async_engine()
async_session = async_sessionmaker(async_engine)

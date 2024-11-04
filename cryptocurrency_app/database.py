"""Module for working with database."""

from app_logger import app_logger
from models.cryptocurrency import Cryptocurrency
from models.connection import Base, async_engine


class Database:

    @classmethod
    async def create_tables(cls) -> None:
        """Create tables which are not existed in db."""

        app_logger.info("Creating tables which are not existed in db.")
        app_logger.debug(f"Metadata tables: {Base.metadata.tables.keys()}")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def close_db_connection(cls) -> None:
        """Close db connection."""

        app_logger.info("Closing db connection.")
        await async_engine.dispose()

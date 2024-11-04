"""Configuration file for pytest."""

from os import environ, path
from pathlib import Path
from pytest_asyncio import fixture as async_fixture

from dotenv import load_dotenv

from cryptocurrency_app.database import Database

sql_query_clear_db_tables = """
TRUNCATE TABLE cryptocurrencies
RESTART IDENTITY;
"""

def pytest_configure():
    """Load env file and set APP_TESTING=True fortest."""

    load_dotenv(path.join(Path(__file__).parent.parent / ".env"))
    environ["APP_TESTING"] = "True"

@async_fixture(scope="session", autouse=True)
async def create_all_tables() -> None:
    """Remove and then create all tables for db."""

    await Database.create_tables()



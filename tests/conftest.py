"""Configuration file for pytest."""

from os import environ, getenv, path
from pathlib import Path

from aioresponses import aioresponses
from pytest import fixture
from pytest_asyncio import fixture as async_fixture

from dotenv import load_dotenv
from sqlalchemy import text


def pytest_configure():
    """Load env file and set APP_TESTING=True fortest."""

    if not getenv("GITHUB_ACTIONS"):
        load_dotenv(path.join(Path(__file__).parent.parent / ".env"))
    environ["APP_TESTING"] = "True"


@async_fixture(scope="session", autouse=True)
async def handle_db_tables() -> None:
    """Delete and then create all tables for tests."""

    from cryptocurrency_app.database import Database

    await Database.create_tables()
    yield
    await Database.delete_tables()


@fixture(scope="function", autouse=False)
def mock_response() -> aioresponses:
    with aioresponses() as m:
        yield m


@async_fixture(scope="function", autouse=False)
async def clean_tables_after_test() -> None:
    """Clear test db tables data"""

    yield
    from cryptocurrency_app.models.connection import async_engine

    sql_query_clear_db_tables = """
    TRUNCATE TABLE cryptocurrencies
    RESTART IDENTITY;
    """
    async with async_engine.begin() as conn:
        await conn.execute(text(sql_query_clear_db_tables))

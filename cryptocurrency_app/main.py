"""Module with FastAPI app."""

from contextlib import asynccontextmanager
from os import getenv

from fastapi import FastAPI

from app_logger import app_logger
from database import Database
from schedular import CustomScheduler
from routes.cryptocurrency import router

@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Implement logic before starting and stopping FastAPI app."""

    app_logger.debug("Initializing before app starting logic.")
    await Database.create_tables()
    CustomScheduler.add_start_up_jobs()
    CustomScheduler.scheduler.start()
    yield
    CustomScheduler.scheduler.stop()
    await Database.close_db_connection()


app = FastAPI(
    debug=getenv("APP_DEBUG") == "True",
    title=getenv("APP_TITLE"),
    lifespan=lifespan,
)
app.include_router(router)

"""Module with scheduler."""

from os import getenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app_logger import app_logger
from tasks.cryptocurrency_price import CryptocurrencyPrice


class CustomScheduler:
    scheduler = AsyncIOScheduler()

    @classmethod
    def add_start_up_jobs(cls) -> None:
        """Add job tasks before application startup."""

        app_logger.info("Adding tasks.")
        cryptocurrencies = getenv("APP_CRYPTOCURRENCIES").strip().split(" ")
        for currency in cryptocurrencies:
            cls.scheduler.add_job(
                func=CryptocurrencyPrice.handle_current_price,
                trigger="interval",
                seconds=int(getenv("APP_CRYPTOCURRENCIES_UPDATE_INTERVAL")),
                args=(currency,),
            )

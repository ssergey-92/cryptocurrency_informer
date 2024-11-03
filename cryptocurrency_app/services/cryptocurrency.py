from datetime import datetime, timedelta
from os import getenv

from cryptocurrency_app.models.cryptocurrency import Cryptocurrency


class HandleCryptocurrency:

    @classmethod
    async def get_all_data(cls, ticker: str) -> list[dict]:
        """Get and return all ticker data from db."""

        ticker_instances = await Cryptocurrency.get_ticker_data(ticker)
        return [
            {
                "id": i_ticker.id,
                "ticker":i_ticker.ticker,
                "index_price": i_ticker.index_price,
                "time": i_ticker.time,
            }
            for i_ticker in ticker_instances
        ]

    @classmethod
    async def get_last_price(cls, ticker: str) -> list[dict]:
        """Get and return last ticker price from db."""

        ticker = await Cryptocurrency.get_last_ticker_entry(ticker)
        if ticker:
            return [
                {
                    "ticker": ticker.ticker,
                    "index_price": ticker.index_price,
                    "price_currency": "usd",
                    "time": ticker.time,
                }
            ]

        return []

    @classmethod
    async def get_period_price(
        cls, ticker: str, start_date: str, end_date: str,
    ) -> list[dict]:
        """Get and return ticker price for period."""

        start_date, end_date = cls._get_unix_period(start_date, end_date)
        ticker_instances = await Cryptocurrency.get_data_by_period(
            ticker, start_date, end_date,
        )

        if not ticker_instances:
            return []

        return [
            {
                "ticker": i_ticker.ticker,
                "index_price": i_ticker.index_price,
                "price_currency": "usd",
                "time": i_ticker.time,
            }
            for i_ticker in ticker_instances
        ]

    @classmethod
    def _get_unix_period(
        cls, start_date: str, end_date: str,
    ) -> tuple[int, int]:
        """Convert start and end date to unix timestamp seconds period."""

        date_format = getenv("DATE_FORMAT")
        start_date = int(
            datetime.strptime(start_date, date_format).timestamp() * 1e6
        )
        end_date = datetime.strptime(end_date, date_format) + timedelta(days=1)
        end_date = int(end_date.timestamp() * 1e6)
        return start_date, end_date

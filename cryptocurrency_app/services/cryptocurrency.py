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

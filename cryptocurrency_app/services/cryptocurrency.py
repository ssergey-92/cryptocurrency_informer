from cryptocurrency_app.models.cryptocurrency import Cryptocurrency


class HandleCryptocurrency:

    @classmethod
    async def get_all_data(cls, ticker: str) -> list[dict]:
        """Get and return all ticker data from db."""

        ticker_instances = await Cryptocurrency.get_ticker_data(ticker)
        return [
            {
                "id": i_ticket.id,
                "ticker":i_ticket.ticker,
                "index_price": i_ticket.index_price,
                "time": i_ticket.time,
            }
            for i_ticket in ticker_instances
        ]

"""Module with schemas for Cryptocurrency.ticker validation."""

from os import getenv
from pydantic import BaseModel, field_validator


class CryptoCurrencyTicker(BaseModel):
    """Class to validate cryptocurrency ticker."""

    ticker: str

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, ticker: str) -> str:
        """Check that ticker is supported."""

        app_tickers = getenv("APP_CRYPTOCURRENCIES").strip(" ,.").split(" ")
        if ticker not in app_tickers:
            raise ValueError(
                f"App support only following tickers: {app_tickers}!"
            )

        return ticker

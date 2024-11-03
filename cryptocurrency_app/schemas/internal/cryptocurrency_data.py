"""Module with schemas for Cryptocurrency full details."""

from decimal import Decimal

from pydantic import BaseModel


class CryptocurrencyData(BaseModel):
    """Class for serializing Cryptocurrency instance."""

    id: int
    ticker: str
    index_price: Decimal
    time: int

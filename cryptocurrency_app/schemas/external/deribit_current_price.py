"""Models for Deribit cryptocurrency current price response."""

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class CurrentPriceResult(BaseModel):
    """Deribit success result for cryptocurrency current price."""
    
    estimated_delivery_price: Decimal
    index_price: Decimal


class DeribitCurrentPrice(BaseModel):
    """Deribit success response for cryptocurrency current price."""

    jsonrpc: str
    id: int
    result: CurrentPriceResult
    usIn: int
    usOut: int
    usDiff: int
    testnet: Literal[False]

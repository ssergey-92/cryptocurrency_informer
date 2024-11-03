"""Module with ORM table 'cryptocurrencies' and CRUD methods."""

from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL, insert, BigInteger

from .connection import Base, async_session
from cryptocurrency_app.app_logger import app_logger


class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrencies'

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(index=True, nullable=False)
    index_price: Mapped[DECIMAL] = mapped_column(DECIMAL(9, 2))
    time: Mapped[int] = mapped_column(BigInteger, index=True, nullable=False)

    @classmethod
    async def add(cls, ticker: str, index_price: Decimal, time: int) -> None:
        """Create new entry."""

        async with async_session() as session:
            async with session.begin():
                query = await session.execute(
                    insert(cls).
                    values(ticker=ticker, index_price=index_price, time=time).
                    returning(cls.id)
                )
                entry_id = query.scalar_one_or_none()
                app_logger.debug(f"Saved {ticker} under id: {entry_id}")

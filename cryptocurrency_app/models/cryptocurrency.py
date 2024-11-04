"""Module with ORM table 'cryptocurrencies' and CRUD methods."""

from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL, insert, BigInteger, select, Sequence, func

from .connection import Base, async_session
from cryptocurrency_app.app_logger import app_logger


class Cryptocurrency(Base):
    __tablename__ = "cryptocurrencies"

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

    @classmethod
    async def get_ticker_data(cls, ticker: str) -> Sequence["Cryptocurrency"]:
        """Get all ticker entries sorted by time DESC."""

        async with async_session() as session:
            query = await session.execute(
                select(cls).
                where(cls.ticker == ticker).
                order_by(cls.time.desc())
            )
            result = query.scalars().all()

        return result

    @classmethod
    async def get_last_ticker_entry(cls, ticker: str) -> "Cryptocurrency":
        """Get last ticker entry instance."""

        async with async_session() as session:
            query = await session.execute(
                select(cls).
                where(cls.ticker == ticker).
                order_by(cls.time.desc()).
                limit(1)
            )
            result = query.scalar_one_or_none()

        return result

    @classmethod
    async def get_data_by_period(
        cls, ticker: str, start_time: int, end_time: int,
    ) -> Sequence["Cryptocurrency"]:
        """Get ticker entries for period sorted by time DESC."""

        async with async_session() as session:
            query = await session.execute(
                select(cls).
                where(
                    cls.ticker == ticker,
                    cls.time.between(start_time, end_time)
                ).
                order_by(cls.time.desc())
            )
            result = query.scalars().all()

        return result

    @classmethod
    async def get_total_ticker_entries(cls, ticker: str) -> int:
        """Get total number of ticker entries."""

        async with async_session() as session:
            query = await session.execute(
                select(func.count(cls.id)).
                where(cls.ticker == ticker)
            )
            result = query.scalar_one_or_none()
        return result if result else 0

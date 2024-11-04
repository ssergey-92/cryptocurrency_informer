"""Module with cryptocurrency routes."""

from os import getenv
from traceback import format_exc
from typing import Union

from fastapi import APIRouter, Response
from pydantic import ValidationError

from cryptocurrency_app.app_logger import app_logger
from cryptocurrency_app.schemas.internal import (
    CryptoCurrencyTicker,
    DatesPeriod,
    ErrorResponse,
    SuccessResponse,
)
from cryptocurrency_app.services import HandleCryptocurrency

router = APIRouter()


@router.get(
    path="/cryptocurrency/records",
    description="Get all available records for cryptocurrency ticker.",
    responses={
        200: {"description": "Success", "model": SuccessResponse},
        400: {"description": "Bad Request", "model": ErrorResponse},
        500: {"description": "Internal Server Error", "model": ErrorResponse},
    },
)
async def get_all_cryptocurrency_details(
    ticker: str, response: Response,
) -> Union[SuccessResponse, ErrorResponse]:
    try:
        ticker = CryptoCurrencyTicker(ticker=ticker).ticker
        ticker_data = await HandleCryptocurrency.get_all_data(ticker)
        response.status_code = 200
        return SuccessResponse(result=ticker_data)
    except ValidationError as exc:
        response.status_code = 400
        return ErrorResponse(error=str(exc))
    except Exception:
        app_logger.error(format_exc())
        response.status_code = 500
        return ErrorResponse(error=getenv("APP_ERROR_MSG"))


@router.get(
    path="/cryptocurrency/price/current",
    description="Get current cryptocurrency ticker price.",
    responses={
        200: {"description": "Success", "model": SuccessResponse},
        400: {"description": "Bad Request", "model": ErrorResponse},
        500: {"description": "Internal Server Error", "model": ErrorResponse},
    },
)
async def get_current_ticker_price(
    ticker: str, response: Response,
) -> Union[SuccessResponse, ErrorResponse]:
    try:
        ticker = CryptoCurrencyTicker(ticker=ticker).ticker
        ticker_data = await HandleCryptocurrency.get_last_price(ticker)
        response.status_code = 200
        return SuccessResponse(result=ticker_data)
    except ValidationError as exc:
        response.status_code = 400
        return ErrorResponse(error=str(exc))
    except Exception:
        app_logger.error(format_exc())
        response.status_code = 500
        return ErrorResponse(error=getenv("APP_ERROR_MSG"))


@router.get(
    path="/cryptocurrency/price/period",
    description="Get cryptocurrency ticker price for period.",
    responses={
        200: {"description": "Success", "model": SuccessResponse},
        400: {"description": "Bad Request", "model": ErrorResponse},
        500: {"description": "Internal Server Error", "model": ErrorResponse},
    },
)
async def get_ticker_price_for_period(
    ticker: str, start_date: str, end_date: str, response: Response,
) -> Union[SuccessResponse, ErrorResponse]:
    try:
        ticker = CryptoCurrencyTicker(ticker=ticker).ticker
        price_period = DatesPeriod(start_date=start_date, end_date=end_date)
        ticker_data = await HandleCryptocurrency.get_period_price(
            ticker, price_period.start_date, price_period.end_date,
        )
        response.status_code = 200
        return SuccessResponse(result=ticker_data)
    except ValidationError as exc:
        response.status_code = 400
        return ErrorResponse(error=str(exc))
    except Exception:
        app_logger.error(format_exc())
        response.status_code = 500
        return ErrorResponse(error=getenv("APP_ERROR_MSG"))

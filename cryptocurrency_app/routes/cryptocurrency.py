from os import getenv
from traceback import format_exc
from typing import Union

from fastapi import APIRouter, Response
from pydantic import ValidationError

from cryptocurrency_app.app_logger import app_logger
from cryptocurrency_app.schemas.internal import (
    CryptoCurrencyTicker,
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
    path="/cryptocurrency/price",
    description="Get current cryptocurrency ticker price.",
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

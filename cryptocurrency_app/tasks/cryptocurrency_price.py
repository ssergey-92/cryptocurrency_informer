"""Module with schedule task for current cryptocurrency price."""

from asyncio import TimeoutError
from os import getenv
from traceback import format_exc

from aiohttp import ClientSession, ClientTimeout
from pydantic import ValidationError

from cryptocurrency_app.app_logger import app_logger
from cryptocurrency_app.models.cryptocurrency import Cryptocurrency
from cryptocurrency_app.schemas.external import DeribitCurrentPrice


class CryptocurrencyPrice:
    """Base Class CryptocurrencyPrice.

     Class is used to get and save data from Deribit website."""

    _url = getenv("DERIBIT_API_URL")
    _current_price_method = "public/get_index_price"
    _client_timeout = 5

    @classmethod
    async def handle_current_price(cls, currency: str) -> None:
        """Get cryptocurrency current price and save it in db."""

        try:
            status, response_data = await cls._get_current_price(
                cls._current_price_method, currency,
            )
            if status == 200:
                validated_data = DeribitCurrentPrice(**response_data)
                await Cryptocurrency.add(
                    currency,
                    validated_data.result.index_price,
                    validated_data.usOut,
                )
            else:
                app_logger.error(f"Response {status=}, {response_data=}")
        except ValidationError as exc:
            app_logger.info(
                f"Response data validation error for {currency}\n{exc}"
            )
        except TimeoutError:
            app_logger.info(f"Timeout for getting price for {currency}")
        except Exception:
            app_logger.error(f"Caught exception: {format_exc()=}")


    @classmethod
    def _get_json_rpc(cls, method: str, currency: str) -> dict:
        """Create json RPC for deribit get index price endpoint."""

        return {
            "jsonrpc": "2.0",
            "method": method,
            "id": 1,
            "params": {"index_name": currency}
        }

    @classmethod
    async def _get_current_price(
        cls, method: str, currency: str,
    ) -> tuple[int, dict]:
        """Create POST request to deribit get index price endpoint."""

        json_rpc = cls._get_json_rpc(method, currency)
        timeout_client = ClientTimeout(total=cls._client_timeout)
        async with ClientSession(timeout=timeout_client) as client:
            async with client.post(url=cls._url, json=json_rpc) as response:
                return response.status, await response.json()

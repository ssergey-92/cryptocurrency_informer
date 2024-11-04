"""Module with test for schedule task CryptocurrencyPrice."""

from os import getenv
from json import dumps

from aioresponses import aioresponses
from pytest import mark

from cryptocurrency_app.models.cryptocurrency import Cryptocurrency
from cryptocurrency_app.tasks.cryptocurrency_price import CryptocurrencyPrice


class TestTaskCryptocurrencyPrice:
    """Based class TestTaskCryptocurrencyPrice.

    Class is used for testing CryptocurrencyPrice methods.

    """

    _cryptocurrency_ticker = "btc_usd"  # btc_usd or eth_usd
    _current_price_method = "public/get_index_price"
    _json_rpc_version = "2.0"
    _valid_btc_json_rpc = {
        "jsonrpc": _json_rpc_version,
        "method": "public/get_index_price",
        "id": 1,
        "params": {"index_name": _cryptocurrency_ticker},
    }
    _deribit_valid_ticker_price = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "index_price": 68593.18,
            "estimated_delivery_price": 68593.18,
        },
        "usIn": 1730707478052914,
        "usOut": 1730707478053065,
        "usDiff": 151,
        "testnet": False,
    }
    _deribit_success_status = 200
    _deribit_unsuccess_status = 400  # Any http status except 200

    @mark.asyncio
    async def test_get_price_successfully(
        self, mock_response: aioresponses, clean_tables_after_test: None,
    ) -> None:
        """Test method 'handle_current_price'

        Test method when receive valid mock response with status code 200
        from deribit platform.

        """
        mock_response.post(
            url=getenv("DERIBIT_API_URL"),
            body=dumps(self._deribit_valid_ticker_price),
            status=self._deribit_success_status,
        )
        before_ticker_entries = await Cryptocurrency.get_total_ticker_entries(
            self._cryptocurrency_ticker,
        )
        await CryptocurrencyPrice.handle_current_price(
            self._cryptocurrency_ticker,
        )
        after_ticker_entries = await Cryptocurrency.get_total_ticker_entries(
            self._cryptocurrency_ticker,
        )
        assert before_ticker_entries == (after_ticker_entries - 1)

    @mark.asyncio
    async def test_get_price_unsuccessfully(
        self, mock_response: aioresponses, clean_tables_after_test: None,
    ) -> None:
        """Test method 'handle_current_price'

        Test method when receive invalid mock response or status code != 200
        from deribit platform.

        """
        for i_data in (
            (self._deribit_valid_ticker_price, self._deribit_unsuccess_status),
            ({}, self._deribit_success_status),
        ):
            mock_response.post(
                url=getenv("DERIBIT_API_URL"),
                body=dumps(i_data[0]),
                status=i_data[1],
            )
            before_entries = await Cryptocurrency.get_total_ticker_entries(
                self._cryptocurrency_ticker,
            )
            await CryptocurrencyPrice.handle_current_price(
                self._cryptocurrency_ticker,
            )
            after_entries = await Cryptocurrency.get_total_ticker_entries(
                self._cryptocurrency_ticker,
            )
            assert before_entries == after_entries

    @mark.asyncio
    async def test_get_current_price(
        self, mock_response: aioresponses,
    ) -> None:
        mock_response.post(
            url=getenv("DERIBIT_API_URL"),
            body=dumps(self._deribit_valid_ticker_price),
            status=self._deribit_success_status,
        )
        status, data = await CryptocurrencyPrice._get_current_price(
            self._current_price_method, self._cryptocurrency_ticker,
        )

        assert status == 200
        assert data == self._deribit_valid_ticker_price

    def test_get_json_rpc(self) -> None:
        json_rpc = CryptocurrencyPrice._get_json_rpc(
            self._current_price_method, self._cryptocurrency_ticker,
        )

        assert json_rpc.keys() == self._valid_btc_json_rpc.keys()
        assert json_rpc["jsonrpc"] == self._json_rpc_version
        assert json_rpc["method"] == self._current_price_method
        assert json_rpc["params"] == self._valid_btc_json_rpc["params"]

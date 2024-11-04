
from pytest import mark
from cryptocurrency_app.tasks.cryptocurrency_price import CryptocurrencyPrice

class TestTaskCryptocurrencyPrice:
    _cryptocurrency_ticker = "btc_usd"
    _current_price_method = "public/get_index_price"
    _json_rpc_version = "2.0"
    _valid_btc_json_rpc = {
            "jsonrpc": _json_rpc_version,
            "method": "public/get_index_price",
            "id": 1,
            "params": {"index_name": _cryptocurrency_ticker},
        }

    def test_get_json_rpc(self):
        json_rpc = CryptocurrencyPrice._get_json_rpc(
            self._current_price_method, self._cryptocurrency_ticker,
        )
        assert self._valid_btc_json_rpc.keys() == json_rpc.keys()
        assert self._json_rpc_version == json_rpc["jsonrpc"]
        assert self._current_price_method == json_rpc["method"]
        assert self._valid_btc_json_rpc["params"] == json_rpc["params"]
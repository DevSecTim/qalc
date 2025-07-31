import os
from typing import Any

from alpaca.trading.client import TradingClient

from qalc.providers.trading import BaseTradingPlatform
from qalc.types import OrderSide, OrderType

API_KEY_ID = os.environ.get("APCA_API_KEY_ID")
API_SECRET_KEY = os.environ.get("APCA_API_SECRET_KEY")


class AlpacaTrading(BaseTradingPlatform):
    def __init__(self, api_key=API_KEY_ID, api_secret=API_SECRET_KEY):
        self._client = TradingClient(api_key, api_secret, paper=True)

    def submit_order(
        self,
        symbol: str,
        qty: float,
        side: OrderSide,
        type_: OrderType = OrderType.MARKET,
    ) -> Any:
        # TODO: Map side and market to Alpaca's expected values
        return self.client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=type_,
        )

    def get_order(self, order_id: str) -> Any:
        return self.client.get_order_by_id(order_id)

    def cancel_order(self, order_id: str) -> Any:
        return self.client.cancel_order(order_id)

    def get_account(self) -> Any:
        return self.client.get_account()

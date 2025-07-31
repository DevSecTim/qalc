from abc import ABC, abstractmethod
from typing import Any

from qalc.types import OrderSide, OrderType


class BaseTradingPlatform(ABC):
    """
    Abstract base class for trading APIs.
    """

    @abstractmethod
    def submit_order(
        self,
        symbol: str,
        qty: float,
        side: OrderSide,
        type_: OrderType = OrderType.MARKET,
    ) -> Any:
        """Submit a new order (buy/sell)."""
        pass

    @abstractmethod
    def get_order(self, order_id: str) -> Any:
        """Get order status/details by order ID."""
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> Any:
        """Cancel an open order by order ID."""
        pass

    @abstractmethod
    def get_account(self) -> Any:
        """Get account details/balance."""
        pass

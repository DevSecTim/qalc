from enum import Enum


class AssetClass(Enum):
    STOCK = "stock"
    FOREX = "forex"
    CRYPTO = "crypto"
    FUTURES = "futures"
    OPTIONS = "options"

    @classmethod
    def from_string(cls, value: str) -> "AssetClass":
        """
        Convert a string to an AssetClass enum.
        """
        return cls(value.lower())

class OrderSide(Enum):
    """
    Enum representing the side of an order.
    """

    BUY = "buy"
    SELL = "sell"

    def __str__(self):
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "OrderSide":
        """
        Convert a string to an OrderSide enum.
        """
        return cls(value.lower())


class OrderType(Enum):
    """
    Enum representing the type of an order.
    """

    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

    def __str__(self):
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "OrderType":
        """
        Convert a string to an OrderType enum.
        """
        return cls(value.lower())

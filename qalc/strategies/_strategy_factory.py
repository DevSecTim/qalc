from enum import Enum
from .buy_and_hold import BuyAndHoldStrategy
from .rsi_trailing_stop import RSITrailingStop

class StrategyName(Enum):
    BUY_AND_HOLD = "buy_and_hold"
    RSI_TRAILING_STOP = "rsi_trailing_stop"

    @classmethod
    def from_string(cls, value: str) -> "StrategyName":
        value = value.lower()
        for member in cls:
            if member.value == value or member.name.lower() == value:
                return member
        raise ValueError(f"Unknown strategy: {value}")

class StrategyFactory:
    _LOOKUP = {
        StrategyName.BUY_AND_HOLD: BuyAndHoldStrategy,
        StrategyName.RSI_TRAILING_STOP: RSITrailingStop,
    }

    @classmethod
    def get_class(cls, name: str | StrategyName):
        """
        Return the strategy class for the given name or enum.
        Raises LookupError if not found.
        """
        if isinstance(name, str):
            name = StrategyName.from_string(name)
        strategy_cls = cls._LOOKUP.get(name)
        if strategy_cls is None:
            raise LookupError(f"Strategy '{name}' not found.")
        return strategy_cls

    @classmethod
    def create(cls, name: str | StrategyName, *args, **kwargs):
        strategy_cls = cls.get_class(name)
        return strategy_cls(*args, **kwargs)
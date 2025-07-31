from typing import Optional, Type
from .buy_and_hold import BuyAndHoldStrategy
from .rsi_trailing_stop import RSITrailingStop
from .base_strategy import BaseStrategy

STRATEGY_LOOKUP = {
    "buy_and_hold": BuyAndHoldStrategy,
    "rsi_trailing_stop": RSITrailingStop,
}

def get_data_provider_class(name: str) -> Type[BaseStrategy]:
    """
    Return the BaseDataProvider subclass for the given name.

    Args:
        name (str): The name of the data provider class.

    Returns:
        Type[BaseDataProvider]: The provider class.

    Raises:
        LookupError: If the provider class is not found.
    """
    provider_cls = STRATEGY_LOOKUP.get(name.lower())
    if provider_cls is None:
        raise LookupError(f"Data provider class '{name}' not found.")
    return provider_cls
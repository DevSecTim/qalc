from typing import Optional, Type
from .alpaca_data_api import AlpacaDataApi
from .base_data_provider import BaseDataProvider

DATA_PROVIDER_LOOKUP = {
    "alpaca": AlpacaDataApi,
}

def get_data_provider_class(name: str) -> Type[BaseDataProvider]:
    """
    Return the BaseDataProvider subclass for the given name.

    Args:
        name (str): The name of the data provider class.

    Returns:
        Type[BaseDataProvider]: The provider class.

    Raises:
        LookupError: If the provider class is not found.
    """
    provider_cls = DATA_PROVIDER_LOOKUP.get(name.lower())
    if provider_cls is None:
        raise LookupError(f"Data provider class '{name}' not found.")
    return provider_cls
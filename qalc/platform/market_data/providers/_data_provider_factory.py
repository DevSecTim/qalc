
from enum import Enum
from .alpaca_data_api import AlpacaDataApi

class DataProviderName(Enum):
    ALPACA = "alpaca"

    @classmethod
    def from_string(cls, value: str) -> "DataProviderName":
        value = value.lower()
        for member in cls:
            if member.value == value or member.name.lower() == value:
                return member
        raise ValueError(f"Unknown data provider: {value}")

class DataProviderFactory:
    _LOOKUP = {
        DataProviderName.ALPACA: AlpacaDataApi,
    }

    @classmethod
    def get_class(cls, name: str | DataProviderName):
        """
        Return the provider class for the given name or enum.
        Raises LookupError if not found.
        """
        if isinstance(name, str):
            name = DataProviderName.from_string(name)
        provider_cls = cls._LOOKUP.get(name)
        if provider_cls is None:
            raise LookupError(f"Data provider '{name}' not found.")
        return provider_cls

    @classmethod
    def create(cls, name: str | DataProviderName, *args, **kwargs):
        provider_cls = cls.get_class(name)
        return provider_cls(*args, **kwargs)



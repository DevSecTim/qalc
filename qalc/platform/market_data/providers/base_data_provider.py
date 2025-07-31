from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Callable, Optional, Type

import pandas as pd

from .. import AssetClass, TimeFrame


class BaseDataProvider(ABC):  # noqa: B024
    def __init__(self, symbol: str = None, asset_class: AssetClass = None):
        if symbol is None:
            raise ValueError("Symbol must be provided for BaseDataProvider")
        self.symbol = symbol

        if asset_class is not None and not isinstance(asset_class, AssetClass):
            raise ValueError("Asset class must be an instance of AssetClass Enum")
        self.asset_class = asset_class
        

class HistoricalDataProvider(BaseDataProvider):
    def __init__(self, symbol: str = None, asset_class: AssetClass = None):
        super().__init__(symbol, asset_class)

    @abstractmethod
    def get_bars(
        self, start: datetime, end: datetime, timeframe: TimeFrame = TimeFrame.MINUTE
    ) -> pd.DataFrame:
        pass

    def get_bars_window(
        self,
        window: timedelta,
        end: datetime = None,
        timeframe: TimeFrame = TimeFrame.MINUTE,
    ) -> pd.DataFrame:
        """
        Convenience method: fetch data for a window ending at `end` (default: now UTC).
        """
        if end is None:
            from datetime import timezone

            end = datetime.now(timezone.utc)
        start = end - window
        return self.get_bars(start, end, timeframe)


class StreamingDataProvider(BaseDataProvider):
    def __init__(self, symbol: str = None, asset_class: AssetClass = None):
        super().__init__(symbol, asset_class)

    @abstractmethod
    async def stream_bars(
        self, callback: Callable[[dict], None], timeframe: TimeFrame = TimeFrame.MINUTE
    ) -> None:
        pass

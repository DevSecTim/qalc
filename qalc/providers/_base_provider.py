from abc import ABC, abstractmethod
import pandas as pd

class BaseProvider(ABC):
    @abstractmethod
    def get_bars(self, symbol: str, timeframe: str, start: str, end: str) -> pd.DataFrame:
        """
        Fetch historical bar data for a symbol.
        Returns a pandas DataFrame with at least a 'close' column and a datetime index.
        """
        pass

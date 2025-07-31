import pandas as pd
from datetime import datetime
from qalc.platform.market_data.timeframe import TimeFrame
from qalc.platform.market_data.types import AssetClass
from qalc.platform.market_data.providers import HistoricalDataProvider
from qalc.platform.market_data.providers.get_data_provider import get_data_provider_class


def get_historical_data(
    data_provider: str, 
    symbol: str,
    asset_class: str = str(AssetClass.STOCK),
    start: str = "",
    end: str = "",
    timeframe: TimeFrame = TimeFrame.MINUTE,
) -> pd.DataFrame:
    """
    Fetch historical market data for a symbol for a given time window.

    Args:
        data_provider: Data provider to use for fetching historical data.
        symbol: Symbol to fetch historical data for (e.g., 'AAPL', 'BTC-USD').
        asset_class: Asset class of the symbol (e.g., 'STOCK', 'CRYPTO', 'OPTIONS').
        start: Start date in ISO format (YYYY-MM-DD or full ISO datetime).
        end: End date in ISO format (YYYY-MM-DD or full ISO datetime).
        timeframe: Timeframe for the historical data (e.g., MINUTE, HOUR, DAY).
    Returns:
        pd.DataFrame: Historical market data.
    """
    start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
    data_provider_class = get_data_provider_class(data_provider)
    if not issubclass(data_provider_class, HistoricalDataProvider):
        raise TypeError(f"Data provider '{data_provider}' is not a valid HistoricalDataProvider.")
    data_provider_instance = data_provider_class(symbol=symbol, asset_class=AssetClass.from_string(asset_class))
    return data_provider_instance.get_bars(start=start_dt, end=end_dt, timeframe=timeframe)
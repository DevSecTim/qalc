import pandas as pd
from datetime import datetime
from qalc.platform.market_data.timeframe import TimeFrame
from qalc.platform.market_data.types import AssetClass
from qalc.platform.market_data.providers import HistoricalDataProvider, DataProviderFactory


def get_historical_data(
    data_provider_name: str, 
    symbol: str,
    asset_class: str = str(AssetClass.STOCK),
    start: str = "",
    end: str = "",
    timeframe: TimeFrame = TimeFrame.MINUTE,
) -> pd.DataFrame:
    """
    Fetches historical market data for a given symbol and time window.

    # Overview
    This function retrieves historical price data from a specified data provider using the qalc framework's provider abstraction. Use this to analyze past performance, run backtests, or answer questions about historical prices.

    # Data Provider Registration
    Providers are registered via the factory/lookup pattern in `qalc/market_data/providers/`. To see the full list, check the provider factory or documentation. Common providers include:
    - 'Alpaca'
    - 'AlphaVantage'
    - 'IEXCloud'
    - 'Polygon'
    Names are case-insensitive and must match those registered in the provider factory. If an invalid provider name is given, an error will be returned.

    # Asset Classes
    Valid values (case-insensitive):
    - 'STOCK': Equities traded on exchanges (default)
    - 'CRYPTO': Cryptocurrency pairs
    - 'OPTIONS': Options contracts
    If an invalid asset class is provided, an error will be returned.

    # TimeFrame Enum
    Specify the granularity of the data using the `TimeFrame` enum. Available values:
    | Enum Value | Description           |
    |------------|----------------------|
    | MINUTE     | 1-minute intervals   |
    | HOUR       | Hourly data          |
    | DAY        | Daily data           |
    | WEEK       | Weekly data          |
    | MONTH      | Monthly data         |
    The minimum timeframe is 1 minute. If an invalid timeframe is provided, an error will be returned.

    # Date Format Examples
    Dates must be in ISO format:
    - Simple date: '2024-12-31'
    - Full ISO datetime: '2024-12-31T10:30:00Z'
    If the date format is invalid, an error will be returned.

    # Example Use Case
    User asks, "What was the closing price of Bitcoin every hour for the last 24 hours?" Call `get_historical_data` with:
    - data_provider_name='Alpaca'
    - symbol='BTC-USD'
    - asset_class='CRYPTO'
    - start='2024-07-31T00:00:00Z'
    - end='2024-08-01T00:00:00Z'
    - timeframe=TimeFrame.HOUR

    # Returns
    A Pandas DataFrame containing the historical data. Columns:
    - date: ISO string (YYYY-MM-DDTHH:MM:SSZ)
    - open: float
    - high: float
    - low: float
    - close: float
    - volume: integer

    # Args
    - data_provider_name (str): Name of the data provider to use (case-insensitive).
    - symbol (str): Stock ticker symbol or cryptocurrency pair (e.g., 'AAPL', 'BTC-USD').
    - asset_class (str, optional): Asset class ('STOCK', 'CRYPTO', 'OPTIONS'). Defaults to 'STOCK'.
    - start (str, optional): Start date in ISO format (YYYY-MM-DD or full ISO datetime). Defaults to "".
    - end (str, optional): End date in ISO format (YYYY-MM-DD or full ISO datetime). Defaults to "".
    - timeframe (TimeFrame, optional): Timeframe for the historical data. Defaults to TimeFrame.MINUTE.

    # Error Handling
    - If the data provider is not registered, an error message will be returned.
    - If the asset class or timeframe is invalid, an error message will be returned.
    - If the date format is incorrect, an error message will be returned.
    """

    # Format start and end dates
    start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
    end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))

    # Check if the data provider provides historical data (subclass of HistoricalDataProvider)
    data_provider_cls = DataProviderFactory.get_class(data_provider_name)
    if not issubclass(data_provider_cls, HistoricalDataProvider):
        raise TypeError(f"Data provider '{data_provider_cls}' is not a valid HistoricalDataProvider.")

    # Create an instance of the data provider
    data_provider = data_provider_cls(
        symbol=symbol, 
        asset_class=AssetClass.from_string(asset_class)
    )

    # Fetch the historical data
    return data_provider.get_bars(start=start_dt, end=end_dt, timeframe=timeframe)
import os
from datetime import datetime

import pandas as pd
from alpaca.data.enums import DataFeed
from alpaca.data.historical import (
    CryptoHistoricalDataClient,
    OptionHistoricalDataClient,
    StockHistoricalDataClient,
)
from alpaca.data.live.crypto import CryptoDataStream
from alpaca.data.live.option import OptionDataStream
from alpaca.data.live.stock import StockDataStream
from alpaca.data.requests import CryptoBarsRequest, OptionBarsRequest, StockBarsRequest

from .. import AssetClass, TimeFrame
from . import (
    HistoricalDataProvider,
    StreamingDataProvider,
)

API_KEY_ID = os.environ.get("ALPACA_API_KEY_ID")
API_SECRET_KEY = os.environ.get("ALPACA_API_SECRET_KEY")
DATA_FEED = os.environ.get("ALPACA_DATA_FEED", DataFeed.IEX)


class AlpacaDataApi(HistoricalDataProvider, StreamingDataProvider):
    def __init__(
        self,
        symbol: str,
        asset_class=AssetClass.STOCK,
        feed=DATA_FEED,
        api_key=API_KEY_ID,
        api_secret=API_SECRET_KEY,
    ):
        super().__init__(symbol, asset_class)

        if feed not in DataFeed:
            raise ValueError(f"Invalid feed: {feed}. Must be one of {list(DataFeed)}")
        self.feed = feed

        if not api_key or not api_secret:
            raise ValueError("API key and secret must be provided for AlpacaStockData")

        match asset_class:
            case AssetClass.STOCK:
                self._client = StockHistoricalDataClient(api_key, api_secret)
                self._stream = StockDataStream(api_key, api_secret)
            case AssetClass.CRYPTO:
                self._client = CryptoHistoricalDataClient(api_key, api_secret)
                self._stream = CryptoDataStream(api_key, api_secret)
            case AssetClass.OPTIONS:
                self._client = OptionHistoricalDataClient(api_key, api_secret)
                self._stream = OptionDataStream(api_key, api_secret)
            case _:
                raise NotImplementedError(
                    "AssetClass '{asset_class}' is not supported in this implementation"
                )
            

    def get_bars(
        self, start: datetime, end: datetime, timeframe: TimeFrame = TimeFrame.MINUTE
    ) -> pd.DataFrame:

        alpaca_tf = timeframe.to_alpaca()

        match self.asset_class:
            case AssetClass.STOCK:
                request = StockBarsRequest(
                    symbol_or_symbols=self.symbol,
                    timeframe=alpaca_tf,
                    start=start,
                    end=end,
                    feed=self.feed,
                )
                bars = self._client.get_stock_bars(request)
            case AssetClass.CRYPTO:
                request = CryptoBarsRequest(
                    symbol_or_symbols=self.symbol,
                    timeframe=alpaca_tf,
                    start=start,
                    end=end,
                    feed=self.feed,
                )
                bars = self._client.get_crypto_bars(request)
            case AssetClass.OPTIONS:
                request = OptionBarsRequest(
                    symbol_or_symbols=self.symbol,
                    timeframe=alpaca_tf,
                    start=start,
                    end=end,
                    feed=self.feed,
                )
                bars = self._client.get_option_bars(request)
        df = bars.df
        if self.symbol in df.columns.get_level_values(0):
            df = df[self.symbol]
        return df

    async def stream_bars(
        self, callback, timeframe: TimeFrame = TimeFrame.MINUTE
    ) -> None:
        if timeframe is not TimeFrame.MINUTE:
            raise ValueError(
                f"Timeframe {timeframe} is not supported for streaming with Alpaca."
                f"Only TimeFrame.MINUTE is supported."
            )
        self._stream.subscribe_bars(callback, self.symbol)
        await self._stream._run_forever()

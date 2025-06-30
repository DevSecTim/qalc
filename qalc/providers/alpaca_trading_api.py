import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient, TimeFrame
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame as AlpacaTimeFrame

class AlpacaTradingApi(BaseProvider):
    def __init__(self, api_key: str, api_secret: str, base_url: str):
        self.client = StockHistoricalDataClient(api_key, api_secret, base_url=base_url)

    def get_bars(self, symbol: str, timeframe: str, start: str, end: str) -> pd.DataFrame:
        # Map string timeframe to Alpaca's TimeFrame enum
        tf_map = {
            '1Min': AlpacaTimeFrame.Minute,
            '5Min': AlpacaTimeFrame.FiveMinutes,
            '15Min': AlpacaTimeFrame.FifteenMinutes,
            '1Hour': AlpacaTimeFrame.Hour,
            '1Day': AlpacaTimeFrame.Day
        }
        alpaca_tf = tf_map.get(timeframe, AlpacaTimeFrame.Minute)
        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=alpaca_tf,
            start=start,
            end=end
        )
        bars = self.client.get_stock_bars(request)
        df = bars.df
        if symbol in df.columns.get_level_values(0):
            df = df[symbol]
        return df

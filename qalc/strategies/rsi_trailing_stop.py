import os
from ta.momentum import RSIIndicator
from qalc.strategies._base_strategy import BaseStrategy

# 🎯 RSI Trailing Stop Strategy
class RSITrailingStop(BaseStrategy):
    def __init__(self, data_provider, symbol, trail_percent=0.03, rsi_period=14, rsi_threshold=30):
        super().__init__(data_provider, symbol, trail_percent)
        self.rsi_period = rsi_period
        self.rsi_threshold = rsi_threshold

    def should_buy(self, index, data):
        rsi = data.iloc[index]['rsi']
        return rsi < self.rsi_threshold

    def should_sell(self, price):
        return price <= self.highest_price * (1 - self.trail_percent)

    def backtest(self, start, end, timeframe='1Min'):
        print(f"\n[🔁 Backtesting {self.symbol} from {start} to {end}]\n")
        bars = self.api.get_bars(self.symbol, timeframe, start=start, end=end)
        if hasattr(bars, 'df'):
            bars = bars.df
        if bars is None or bars.empty:
            print("No data available for this range.")
            return

        bars = bars.tz_convert('UTC')  # Align timezone
        bars['rsi'] = RSIIndicator(close=bars['close'], window=self.rsi_period).rsi()

        holding = False
        entry_price = 0
        self.highest_price = 0
        cash = 10000
        shares = 0
        trade_log = []

        for i in range(self.rsi_period, len(bars)):
            row = bars.iloc[i]
            price = row['close']
            rsi = row['rsi']
            time_str = row.name.strftime('%Y-%m-%d %H:%M')

            if not holding and self.should_buy(i, bars):
                shares = cash // price
                entry_price = price
                self.highest_price = price
                cash -= shares * price
                holding = True
                trade_log.append(f"{time_str} BUY @ {price:.2f}, shares={shares}")
            elif holding:
                self.highest_price = max(self.highest_price, price)
                if self.should_sell(price):
                    cash += shares * price
                    trade_log.append(f"{time_str} SELL @ {price:.2f}, shares={shares}, PnL={(price-entry_price)*shares:.2f}")
                    shares = 0
                    holding = False

        final_value = cash + (shares * bars.iloc[-1]['close'] if holding else 0)
        print("\n".join(trade_log))
        print(f"\n[💰 Final Value]: ${final_value:.2f} | PnL: ${final_value - 10000:.2f}")


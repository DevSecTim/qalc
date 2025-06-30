from abc import ABC, abstractmethod

# 🧱 Base Strategy Class
class BaseStrategy(ABC):
    def __init__(self, api, symbol, trail_percent):
        self.api = api
        self.symbol = symbol
        self.trail_percent = trail_percent
        self.highest_price = 0

    @abstractmethod
    def should_buy(self, index, data):
        pass

    @abstractmethod
    def should_sell(self, price):
        pass

    @abstractmethod
    def backtest(self, start, end, timeframe):
        pass

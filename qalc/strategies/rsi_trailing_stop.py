import pandas as pd
from typing import Any, Dict
from pandas import DataFrame
from ta.momentum import RSIIndicator
from pydantic import BaseModel, Field
from ._base_strategy import BatchStrategy


class RSITrailingStopParams(BaseModel):
    initial_cash: float = Field(
        default=10000,
        description="Initial cash available for the strategy.",
    )
    trail_percent: float = Field(
        default=0.03,
        description="The percentage drop from the highest price since entry that "
        "triggers a trailing stop sell.",
    )
    rsi_period: int = Field(
        default=14,
        description="The number of bars (window size) used to calculate the RSI "
        "indicator. Typical values are 14 or 21.",
    )
    rsi_threshold: float = Field(
        default=30,
        description="The RSI value below which the strategy considers the asset "
        "oversold and triggers a buy.",
    )


class RSITrailingStopState(BaseModel):
    cash: float = Field(
        default=10000.0, description="Current cash available in the strategy."
    )
    shares: int = Field(
        default=0, description="Number of shares currently held by the strategy."
    )
    entry_price: float = Field(
        default=0.0, description="Price at which shares were bought."
    )
    highest_price: float = Field(
        default=0.0,
        description="Highest price since entry for trailing stop calculation.",
    )
    holding: bool = Field(
        default=False, description="Whether the strategy is currently holding shares."
    )
    trades: list[str] = Field(
        default_factory=list, description="Log of trades made during the strategy."
    )


class RSITrailingStop(BatchStrategy):
    """RSI with trailing stop strategy.

    Buys when RSI falls below threshold (oversold condition),
    sells when price drops by trail_percent from highest price since entry.
    """

    def __init__(self, **kwargs: Any):
        """Initialize RSI trailing stop strategy."""
        self._params = RSITrailingStopParams(**kwargs)
        self._state = RSITrailingStopState(cash=self._params.initial_cash)

    @property
    def name(self) -> str:
        return "RSI Trailing Stop"

    @property
    def params(self) -> RSITrailingStopParams:
        return self._params

    def reset_state(self) -> None:
        """Reset the strategy state for a new run."""
        self._state = RSITrailingStopState(cash=self._params.initial_cash)

    def _process_bar(self, bar, time_str):
        price = bar["close"]
        rsi = bar["rsi"]
        if not self._state.holding and rsi < self._params.rsi_threshold:
            shares = int(self._state.cash // price)
            if shares == 0:
                return
            self._state.entry_price = price
            self._state.highest_price = price
            self._state.cash -= shares * price
            self._state.holding = True
            self._state.shares = shares
            self._state.trades.append(f"{time_str} BUY @ {price:.2f}, shares={shares}")
        elif self._state.holding:
            self._state.highest_price = max(self._state.highest_price, price)
            if price <= self._state.highest_price * (1 - self._params.trail_percent):
                self._state.cash += self._state.shares * price
                self._state.trades.append(
                    f"{time_str} SELL @ {price:.2f}, shares={self._state.shares}, "
                    f"PnL={(price-self._state.entry_price)*self._state.shares:.2f}"
                )
                self._state.shares = 0
                self._state.holding = False

    def _finalize_position(self, final_price, time_str):
        self._state.cash += self._state.shares * final_price
        self._state.trades.append(
            f"{time_str} FINAL SELL @ {final_price:.2f}, shares={self._state.shares},"
            f"PnL={(final_price-self._state.entry_price)*self._state.shares:.2f}"
        )
        self._state.shares = 0
        self._state.holding = False

    def _run_backtest(self, bars: DataFrame, **kwargs) -> Dict[str, Any]:
        """
        Run a backtest for the RSI trailing stop strategy.
        Buys when RSI < threshold, sells when price drops by trail_percent
        from highest since entry.
        """
        # Ensure we have data to work with
        if bars.empty:
            raise ValueError("No data available for this range.")

        # Use provided params if they are provided
        if kwargs is not None:
            self._params = RSITrailingStopParams(**kwargs)

        # Reset state for new backtest
        self._state = RSITrailingStopState(cash=self._params.initial_cash)

        # Prepare data with RSI indicator
        bars = bars.copy()
        bars["rsi"] = RSIIndicator(
            close=bars["close"], window=self._params.rsi_period
        ).rsi()

        # Track portfolio value over time
        portfolio_values = []
        for i in range(self._params.rsi_period, len(bars)):
            row = bars.iloc[i]
            idx = row.name
            if isinstance(idx, tuple):
                dt = idx[1]
            else:
                dt = idx
            time_str = (
                dt.strftime("%Y-%m-%d %H:%M") if hasattr(dt, "strftime") else str(dt)
            )
            self._process_bar(row, time_str)
            # Calculate portfolio value after each bar
            value = self._state.cash + self._state.shares * row["close"]
            portfolio_values.append(value)

        # If still holding at the end, sell at last price
        if self._state.holding and self._state.shares > 0:
            final_price = bars.iloc[-1]["close"]
            dt = bars.iloc[-1].name
            if isinstance(dt, tuple):
                dt = dt[1]
            time_str = (
                dt.strftime("%Y-%m-%d %H:%M") if hasattr(dt, "strftime") else str(dt)
            )
            self._finalize_position(final_price, time_str)
            # Add final portfolio value
            portfolio_values[-1] = self._state.cash

        final_value = self._state.cash
        pnl = final_value - self._params.initial_cash

        # Calculate Sharpe ratio
        portfolio_series = pd.Series(
            portfolio_values, index=bars.index[self._params.rsi_period :]
        )
        returns = portfolio_series.pct_change().dropna()
        sharpe = RSITrailingStop.sharpe_ratio(returns)

        print("\n".join(self._state.trades))
        print(f"\n[💰 Final Value]: ${final_value:.2f} | PnL: ${pnl:.2f}")

        return {
            "final_value": final_value,
            "pnl": pnl,
            "params": self._params.model_dump(),
            "state": self._state.model_dump(),
            "sharpe_ratio": sharpe,
        }

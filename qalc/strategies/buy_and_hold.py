import pandas as pd
from typing import Any, Dict
from pandas import DataFrame
from pydantic import BaseModel, Field
from ._base_strategy import BatchStrategy


class BuyAndHoldParams(BaseModel):
    initial_cash: float = Field(
        default=10000.0, description="Initial cash available for the strategy."
    )


class BuyAndHoldState(BaseModel):
    cash: float = Field(
        default=10000.0, description="Current cash available in the strategy."
    )
    shares: int = Field(
        default=0, description="Number of shares currently held by the strategy."
    )
    buy_price: float = Field(
        default=0.0, description="Price at which shares were bought."
    )
    trades: list[str] = Field(
        default_factory=list, description="List of trades made during the strategy."
    )
    holding: bool = Field(
        default=False, description="Whether the strategy is currently holding shares."
    )


class BuyAndHoldStrategy(BatchStrategy):
    """Buy and hold strategy - buy at the beginning and hold until the end."""

    def __init__(self, **kwargs: Any):
        self._params = BuyAndHoldParams(**kwargs)
        self._state = BuyAndHoldState(cash=self._params.initial_cash)

    @property
    def name(self) -> str:
        return "Buy & Hold"

    @property
    def params(self) -> BuyAndHoldParams:
        return self._params

    def reset_state(self) -> None:
        """Reset the strategy state for a new run."""
        self._state = BuyAndHoldState(cash=self._params.initial_cash)

    def _run_backtest(self, bars: DataFrame, **kwargs) -> Dict[str, Any]:
        # Ensure we have data to work with
        if bars.empty:
            raise ValueError("No data available for this range.")

        # Use provided params if they are provided
        if kwargs is not None:
            self._params = BuyAndHoldParams(**kwargs)

        # Reset state for new backtest
        self._state = BuyAndHoldState(cash=self._params.initial_cash)

        # Buy at the first bar's open price
        self._state.buy_price = bars.iloc[0]["open"]
        self._state.shares = int(self._params.initial_cash // self._state.buy_price)
        remaining_cash = self._params.initial_cash - (
            self._state.shares * self._state.buy_price
        )
        self._state.holding = True
        self._state.trades.append(
            f"Buy {self._state.shares} shares at ${self._state.buy_price:.2f}"
        )

        # Track portfolio value over time
        portfolio_values = []
        for i in range(len(bars)):
            price = bars.iloc[i]["close"]
            value = self._state.shares * price + remaining_cash
            portfolio_values.append(value)

        # Sell at the last bar's close price
        sell_price = bars.iloc[-1]["close"]
        final_cash = self._state.shares * sell_price + remaining_cash
        self._state.trades.append(
            f"Sell {self._state.shares} shares at ${sell_price:.2f}"
        )

        pnl = final_cash - self._params.initial_cash

        # Calculate Sharpe ratio
        portfolio_series = pd.Series(portfolio_values, index=bars.index)
        returns = portfolio_series.pct_change().dropna()
        sharpe = BuyAndHoldStrategy.sharpe_ratio(returns)

        print(
            f"Start ${self._params.initial_cash:.2f}, End ${final_cash:.2f}, PnL: ${pnl:.2f}"
        )
        print("\n".join(self._state.trades))

        return {
            "final_value": final_cash,
            "pnl": pnl,
            "params": self._params,
            "state": self._state,
            "sharpe_ratio": sharpe,
        }

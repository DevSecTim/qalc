import pandas as pd
from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel


class BaseStrategy(ABC):
    """Base class for all trading strategies.

    This class defines the interface that all trading strategies must implement.
    """

    @staticmethod
    def sharpe_ratio(
        returns: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252
    ) -> float:
        """
        Calculate the annualized Sharpe ratio for a series of returns.

        Args:
            returns (pd.Series): Series of periodic returns (e.g., daily pct_change of portfolio value)
            risk_free_rate (float): Risk-free rate per period (default 0.0)
            periods_per_year (int): Number of periods per year (default 252 for daily)

        Returns:
            float: Annualized Sharpe ratio

        Usage in a subclass backtest:
            # After simulating the strategy, compute portfolio value per bar
            portfolio_values = ... # pd.Series of portfolio value over time
            returns = portfolio_values.pct_change().dropna()
            sharpe = BaseStrategy.sharpe_ratio(returns)
            # Include 'sharpe_ratio': sharpe in your backtest result dict
        """
        excess_returns = returns - risk_free_rate
        mean_excess = excess_returns.mean()
        std_excess = excess_returns.std(ddof=0)
        if std_excess == 0 or returns.empty:
            return float("nan")
        sharpe = (mean_excess / std_excess) * (periods_per_year**0.5)
        return sharpe

    @property
    @abstractmethod
    def params(self) -> BaseModel:
        """Get the parameters of the strategy.

        Returns:
            BaseModel: Parameters of the strategy

        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of the strategy.

        Returns:
            str: Name of the strategy
        """
        pass

    @abstractmethod
    def reset_state(self) -> None:
        """Reset the strategy state for a new run."""
        pass

class BatchStrategy(BaseStrategy):

    @abstractmethod
    def _run_backtest(self, bars: pd.DataFrame, **kwargs: Any) -> Dict[str, Any]:
        """
        Subclasses must implement this method to perform the actual backtest logic.
        Should return a dict including at least 'sharpe_ratio'.
        """
        pass

    def backtest(self, bars: pd.DataFrame, **kwargs: Any) -> Dict[str, Any]:
        """
        Run a backtest for this strategy.

        Args:
            bars: DataFrame containing OHLCV data
            kwargs: Optional parameters for the strategy

        Returns:
            Dict containing backtest results. Must include at least 'sharpe_ratio' (float).
        """
        result = self._run_backtest(bars, **kwargs)
        assert (
            "sharpe_ratio" in result
        ), "backtest() result must include 'sharpe_ratio' key."
        return result


class StreamingStrategy(BaseStrategy):
    """Interface for stateful, streaming-capable strategies."""

    @abstractmethod
    def on_bar(self, bar: dict) -> None:
        """Process a new bar from a data stream.

        Args:
            bar: A dict or custom object representing a single bar (OHLCV and timestamp)
        """
        pass

    @abstractmethod
    def close(self) -> Dict[str, Any]:
        """Finalize the strategy at the end of a stream (e.g., close open positions).

        Returns:
            Dict containing final results, trades, etc.
        """
        pass

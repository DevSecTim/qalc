import pandas as pd
from typing import Dict, Any, Optional, List
from qalc.strategies import BatchStrategy, StrategyFactory

def run_backtest(
    strategy_name: str,
    bars: Dict[str, List[Any]],
    strategy_params: Optional[Dict[str, Any]] = None,
    backtest_params: Optional[Dict[str, Any]] = None,
) -> Dict:
    """
    Runs a backtest using the specified trading strategy and historical market data.

    # Overview
    This function executes a backtest for a given strategy using historical price data. Use it to evaluate strategy performance before live deployment or for research.

    # Supported Strategies
    Strategies are registered via the StrategyFactory in `qalc/strategies/` and must be subclasses of `BatchStrategy`. Common strategies include:
    - 'buy_and_hold' (no parameters required)
    - 'rsi_trailing_stop' (parameters: rsi_period, trailing_stop_pct)
    - ...see strategy factory for full list
    Names are case-insensitive and must match those registered. If an invalid strategy name is given, an error will be returned.

    # Historical Data Format
    The `bars` argument should be a dictionary or DataFrame with the following columns:
    - date: ISO string (YYYY-MM-DDTHH:MM:SSZ)
    - open: float
    - high: float
    - low: float
    - close: float
    - volume: integer
    If columns or types are incorrect, an error will be returned.

    # Strategy Parameters Examples
    - For 'rsi_trailing_stop': {'rsi_period': 14, 'trailing_stop_pct': 0.05}
    - For 'buy_and_hold': {}
    - For other strategies, see their documentation or source for required parameters.

    # Backtest Parameters
    Pass additional parameters for the backtest run (e.g., initial_capital, slippage, commission) as a dictionary to `backtest_params`.

    # Example Use Case
    User asks, "How would an RSI trailing stop strategy have performed on Apple stock over the last 30 days?" Call `run_backtest` with:
    - strategy_name='rsi_trailing_stop'
    - bars=historical_data_dict (from get_historical_data)
    - strategy_params={'rsi_period': 14, 'trailing_stop_pct': 0.05}
    - backtest_params={'initial_capital': 10000}

    # Returns
    A JSON-serializable dictionary containing the backtest results. Example output:
    {
      "performance": "Good",
      "trades": 10,
      "equity_curve": [ {"date": "2024-01-01", "value": 10000}, {"date": "2024-01-02", "value": 10100} ],
      "metrics": { "sharpe_ratio": 0.5, "max_drawdown": -0.1 }
    }
    Typical keys include: performance, trades, equity_curve, metrics, etc.

    # Args
    - strategy_name (str): Name of the strategy to run the backtest on (case-insensitive).
    - bars (Dict[str, List[Any]]): Historical data for the backtest, as a dictionary or DataFrame.
    - strategy_params (dict, optional): Parameters to initialize the strategy. Defaults to None.
    - backtest_params (dict, optional): Parameters for the backtest run. Defaults to None.

    # Error Handling
    - If the strategy is not registered or not a BatchStrategy, an error message will be returned.
    - If the historical data format is incorrect, an error message will be returned.
    """

    # Check if the strategy is backtestable (subclass of BatchStrategy)
    strategy_cls = StrategyFactory.get_class(strategy_name)
    if not issubclass(strategy_cls, BatchStrategy):
        raise TypeError(f"Strategy '{strategy_cls}' is not a valid BatchStrategy.")
    
    # Create an instance of the strategy, passing the strategy parameters
    strategy = strategy_cls(**(strategy_params or {}))

    # Run the backtest and return the results, passing the backtest parameters
    return strategy.backtest(pd.DataFrame(bars), **(backtest_params or {}))
import pandas as pd
from typing import Dict, Any, Optional, List
from qalc.strategies import BaseStrategy, BatchStrategy
from qalc.strategies.get_data_provider import get_data_provider_class


def run_backtest(
    strategy: str,
    bars: Dict[str, List[Any]],
    strategy_params: Optional[Dict[str, Any]] = None,
    backtest_params: Optional[Dict[str, Any]] = None,
) -> Dict:
    """
    Run a backtest with the specified parameters. Returns a JSON-serializable dict for LLM consumption.

    Args:
        strategy: Name of the strategy to run backtest on.
        bars: Historical data to use for the backtest, as a DataFrame.
        strategy_params: Parameters to initialize the strategy.
        backtest_params: Parameters to pass to the backtest method.
    Returns:
        Dict: Backtest results.
    """
    strategy_class = get_data_provider_class(strategy)
    if not issubclass(strategy_class, BatchStrategy):
        raise TypeError(f"Strategy '{strategy}' is not a valid BatchStrategy.")
    strategy_instance = strategy_class(**(strategy_params or {}))
    return strategy_instance.backtest(pd.DataFrame(bars), **(backtest_params or {}))
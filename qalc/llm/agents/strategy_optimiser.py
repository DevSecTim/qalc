import json
import pandas as pd
from typing import Any, Dict
from langchain_core.language_models import BaseChatModel
from langgraph.graph import StateGraph, START, END
from qalc.util import BaseModel
from qalc.llm.agents import BaseAgent
from qalc.llm.tools import RunBacktest
from qalc.llm.prompts import get_prompt
from qalc.strategies import BatchStrategy

# Node name constants
NODE_RUN_BACKTEST = "run_backtest"
NODE_EVALUATE = "evaluate"
NODE_OPTIMISE = "optimise"


class StrategyOptimiser(BaseAgent):
    """
    LLM-powered agent for iterative parameter tuning of trading strategies.

    This agent takes a strategy and initial parameters, then uses LLM reasoning
    to iteratively adjust parameters to optimize performance over a given backtest
    time window.
    """

    def __init__(
        self,
        llm: BaseChatModel,
        strategy: BatchStrategy,
        bars: pd.DataFrame,
        optimization_goal: str = "maximize",
        target_metric: str = "sharpe_ratio",
        max_iterations: int = 5,
    ):
        self._llm = llm
        self._strategy = strategy
        self._bars = bars
        self._optimization_goal = optimization_goal
        self._target_metric = target_metric
        self._max_iterations = max_iterations
        self._best_params = None
        self._best_result = None
        self._tuning_history = []
        self._tools = {"run_backtest": RunBacktest(strategy)}

    def run(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Run the parameter tuning process using LangChain's native agent API.
        """

        start_time = kwargs.pop("start_time").isoformat()
        end_time = kwargs.pop("end_time").isoformat()

        print(f"🚀 Starting parameter tuning for {self._strategy.__class__.__name__}")
        print(f"📊 Backtest window: {start_time} to {end_time}")
        print(f"🎯 Optimizing: {self._optimization_goal} {self._target_metric}")
        print(f"🔄 Max iterations: {self._max_iterations}")

        # Use initial parameters or strategy defaults
        initial_params = kwargs.get("params", self._strategy.params.model_dump())

        # Define the graph nodes
        def run_backtest_node(state):
            # Run backtest tool
            backtest_results = self._tools["run_backtest"].invoke(
                input={
                    "bars": self._bars,
                    "params": state.params,
                }
            )
            return GraphState(
                params=state.params,
                iteration=state.iteration,
                backtest_result=backtest_results,
            )

        def evaluate_node(state):
            # Evaluate result and update best params
            result = state.backtest_result
            metric = self._target_metric
            value = result.get(metric, None)
            if self._optimization_goal == "maximize":
                if self._best_result is None or value > self._best_result.get(
                    metric, float("-inf")
                ):
                    self._best_result = result
                    self._best_params = state.params
            else:
                if self._best_result is None or value < self._best_result.get(
                    metric, float("inf")
                ):
                    self._best_result = result
                    self._best_params = state.params
            self._tuning_history.append(
                {
                    "params": state.params,
                    "result": result,
                }
            )
            return GraphState(
                params=state.params,
                iteration=state.iteration,
                backtest_result=result,
            )

        def optimise_node(state):
            # Use LLM to suggest new params and explain reasoning
            prompt = get_prompt(
                "strategy_optimiser",
                initial_params=initial_params,
                strategy_name=self._strategy.name,
                optimisation_goal=self._optimization_goal,
                target_metric=self._target_metric,
                results=json.dumps(state.backtest_result),
                params=state.params,
                iteration=state.iteration,
                max_iterations=self._max_iterations,
            )
            response = self._llm.invoke(prompt)
            print(f"🔍 LLM response: {response.content}")
            # Expecting LLM to return a JSON with 'params' and 'explanation' fields
            try:
                response_json = json.loads(str(response.content))
                if (
                    isinstance(response_json, dict)
                    and "params" in response_json
                    and "explanation" in response_json
                ):
                    new_params = response_json["params"]
                    explanation = response_json["explanation"]
                else:
                    # Fallback: treat as just params
                    new_params = response_json
                    explanation = None
            except Exception:
                new_params = json.loads(str(response.content))
                explanation = None
            if explanation:
                print(f"📝 LLM explanation for parameter change: {explanation}")
            return GraphState(
                params=new_params,
                iteration=state.iteration + 1,
                backtest_result=state.backtest_result,
            )

        class GraphState(BaseModel):
            params: Dict[str, Any]
            iteration: int
            backtest_result: Dict[str, Any]

        # Build the graph
        graph = StateGraph(state_schema=GraphState)

        # Define nodes using constants
        graph.add_node(NODE_RUN_BACKTEST, run_backtest_node)
        graph.add_node(NODE_EVALUATE, evaluate_node)
        graph.add_node(NODE_OPTIMISE, optimise_node)

        # Define edges using constants
        graph.add_edge(START, NODE_RUN_BACKTEST)
        graph.add_edge(NODE_RUN_BACKTEST, NODE_EVALUATE)
        graph.add_conditional_edges(
            NODE_EVALUATE,
            lambda state: (
                NODE_OPTIMISE if state.iteration < self._max_iterations else END
            ),
        )
        graph.add_edge(NODE_OPTIMISE, NODE_RUN_BACKTEST)

        # Compile and run (iterate with stream)
        compiled_graph = graph.compile()
        state = GraphState(
            params=initial_params,
            iteration=0,
            backtest_result={},
        )
        for step in compiled_graph.stream(state):
            state = step

        print("\n🎉 Parameter tuning complete!")
        if self._best_result:
            sharpe = self._best_result.get("sharpe_ratio", "N/A")
            pnl = self._best_result.get("pnl", "N/A")
            print("\n==============================")
            print(f"🏆 FINAL SHARPE RATIO: {sharpe}")
            print(f"💰 FINAL PnL: {pnl}")
            print("==============================\n")
        if self._best_params:
            print(f"Best parameters found: {json.dumps(self._best_params, indent=2)}")
        if self._best_result:
            print(f"Best result: {json.dumps(self._best_result, indent=2)}")

# qalc

qalc is a modular, strategy-driven trading CLI and backtesting framework for Python, managed by Poetry. It supports pluggable data providers (Alpaca by default), strategy selection via CLI, and is designed for rapid strategy development and testing.

## Features

- Strategy registration and selection via CLI
- Pluggable data provider abstraction (Alpaca default)
- Backtesting workflows
- VS Code debug and task integration
- Environment variable management via `.env`

## Installation

1. Clone the repository:

   ```sh
   git clone <repo-url>
   cd qalc
   ```

2. Install dependencies with Poetry (create .venv in project directory):

   ```sh
   POETRY_VIRTUALENVS_IN_PROJECT=true poetry install --with=dev
   ```

3. Copy and edit your `.env` file for API keys:

   ```sh
   cp .env.example .env
   # Edit .env with your Alpaca API keys
   ```

## Usage

### Run the CLI

```sh
poetry run qalc backtest --strategy rsi_trailing_stop --symbol AAPL --days 5
```

### Run as a module

```sh
poetry run python -m qalc backtest --strategy rsi_trailing_stop --symbol AAPL --days 5
```

### VS Code

- Use the included debug configuration to run and debug the CLI.
- Use tasks for install, update, lint, and test workflows.

## Example: Backtest RSI Trailing Stop

```sh
poetry run qalc backtest --strategy rsi_trailing_stop --symbol TSLA --trail_percent 0.05 --days 10
```

## Adding Strategies

- Register new strategies in `main.py` in the `STRATEGIES` dictionary.
- Implement your strategy in the `qalc/strategies/` directory.

## Linting & Testing

- Lint: `poetry run flake8 qalc`
- Test: `poetry run pytest`

---

For more, see `.github/copilot-instructions.md` and the VS Code tasks/debug configs.

# Copilot Instructions for qalc

## Project Overview
- **qalc** is a modular, strategy-driven trading and backtesting framework in Python.
- Major components: strategies (in `qalc/strategies/`), data providers (in `qalc/market_data/providers/`), trading platforms (in `qalc/trading/platforms/`), and the main CLI/app logic (in `qalc/app.py`, `qalc/__main__.py`).
- The system is designed for rapid development and testing of trading strategies, with a focus on extensibility and modularity.
- Data providers and strategies are pluggable via lookup/factory patterns.
- Environment variables (API keys, etc.) are managed via `.env` files.

## Key Developer Workflows
- **Install dependencies:** `POETRY_VIRTUALENVS_IN_PROJECT=true poetry install --with=dev`
- **Run CLI:** `poetry run qalc backtest --strategy rsi_trailing_stop --symbol AAPL --days 5`
- **Run as module:** `poetry run python -m qalc backtest ...`
- **Testing:** `poetry run pytest`
- **Linting:** `poetry run flake8 qalc`
- **Formatting:** `poetry run black qalc`
- **Docker builds:** See `Dockerfile` and `.github/workflows/docker-publish.yml` for multi-stage build and CI/CD details.

## Project-Specific Patterns & Conventions
- **Strategy registration:** Strategies are registered via lookup tables in `qalc/strategies/` and selected by CLI argument.
- **Data provider abstraction:** Data providers use a factory/lookup pattern (`qalc/market_data/providers/`).
- **Enums:** Use robust, case-insensitive `from_string` methods (see `qalc/market_data/types.py`).
- **Tool/agent registration:** FastMCP tools are dynamically discovered and registered (see `qalc/llm/agents/` and `qalc/llm/tools/`).
- **Testing:** Test fixtures and unit tests are in `tests/fixtures/` and `tests/unit/`.
- **CI/CD:** Docker images are built and pushed on tag via GitHub Actions, tagged with both the git tag and `latest`.

## Integration Points & External Dependencies
- **Alpaca API** (default data provider; requires API keys in `.env`).
- **FastMCP** (for LLM/agent server, see `qalc/llm/` and `qalc/mcp/`).
- **Poetry** for dependency management.
- **Docker** for containerization and deployment.

## Examples
- Add a new strategy: create a class in `qalc/strategies/`, register it in the lookup table, and expose it via CLI.
- Add a new data provider: implement in `qalc/market_data/providers/`, register in the factory.
- Run a backtest: `poetry run qalc backtest --strategy buy_and_hold --symbol MSFT --days 30`

## Key Files & Directories
- `qalc/strategies/` — Trading strategies
- `qalc/market_data/providers/` — Data providers
- `qalc/app.py`, `qalc/__main__.py` — CLI entry points
- `qalc/llm/` — LLM/agent integration
- `Dockerfile`, `.github/workflows/docker-publish.yml` — Build and CI/CD
- `README.md` — Usage, install, and workflow details

---

If you are unsure about a workflow or pattern, check the README or the relevant subdirectory for examples. When adding new features, follow the factory/lookup and registration patterns used throughout the codebase.

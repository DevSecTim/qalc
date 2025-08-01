
# Qalc

qalc is a modular, extensible Model Context Protocol (MCP) server and trading/backtesting framework for Python. It enables rapid development, testing, and serving of trading strategies and LLM-powered tools via a robust CLI and MCP-compatible API.

## Architecture & Features

- **Strategy registration:** Strategies are implemented in `qalc/strategies/` and registered via lookup tables for CLI selection.
- **Data providers:** Pluggable via factory/lookup pattern in `qalc/market_data/providers/` (Alpaca is default).
- **Trading platforms:** Modularized in `qalc/trading/platforms/`.
- **CLI & app logic:** Entrypoints in `qalc/app.py` and `qalc/__main__.py`.
- **LLM/agent integration:** FastMCP tools/agents in `qalc/llm/` and `qalc/mcp/`.
- **Environment variables:** Managed via `.env` (see `.env.example`).
- **CI/CD:** Docker images built and pushed on tag via GitHub Actions (`.github/workflows/docker-publish.yml`).

## Quickstart

```sh
# Install dependencies (with dev tools)
uv venv && uv pip install .

# Copy and edit .env for API keys
cp .env.example .env

# Start the MCP server
python -m qalc.mcp.main

```

## Developer Workflows

- **Start MCP server:** `python -m qalc.mcp.main`
- **Lint:** `uv pip install --system --no-cache-dir .[dev] && flake8 qalc`
- **Test:** `pytest`
- **Format:** `black qalc`
- **Docker build:** See `Dockerfile` and `.github/workflows/docker-publish.yml`
- **VS Code:** Use included debug configs and tasks for install, lint, test, and format.

## Extending qalc

- **Add a strategy:**
  1. Implement in `qalc/strategies/`.
  2. Register in the strategy lookup table.
  3. Expose via CLI argument.
- **Add a data provider:**
  1. Implement in `qalc/market_data/providers/`.
  2. Register in the provider factory.

## Key Files & Directories

- `qalc/strategies/` — Trading strategies
- `qalc/market_data/providers/` — Data providers
- `qalc/app.py`, `qalc/__main__.py` — CLI entry points
- `qalc/llm/` — LLM/agent integration
- `Dockerfile`, `.github/workflows/docker-publish.yml` — Build and CI/CD
- `README.md` — Usage, install, and workflow details

---

For more, see `.github/copilot-instructions.md` and the VS Code tasks/debug configs.

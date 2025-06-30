<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a Python project managed by Poetry. Use Poetry for dependency management and packaging.

- The main CLI entry point is `qalc.main:main` and is exposed as a Poetry script (`poetry run qalc`).
- The project supports running as a module: `python -m qalc`.
- VS Code debug and task configurations are set up for CLI and backtest workflows.
- Strategies are registered in a dictionary in `main.py` and selected by name via CLI arguments.
- Data providers are abstracted; Alpaca is the default, but others can be added.
- Use `.env` for API keys and secrets (dotenv is loaded automatically).

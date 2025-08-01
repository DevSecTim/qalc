import argparse
import pkgutil
import inspect
import qalc.mcp.tools as tools_module
from fastmcp import FastMCP


mcp = FastMCP(
    name="qalc",
    instructions="A collection of tools for financial analysis and trading strategies.",
    version="0.1.0",
)

def main():
    """
    Main entry point for the MCP server.
    Supports remote server configuration via command-line arguments.
    """
    
    # Try to load .env if python-dotenv is installed
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    # Parse command-line arguments for remote server configuration
    parser = argparse.ArgumentParser(description="Start the MCP server.")
    parser.add_argument("--host", default="localhost", help="Host for remote server")
    parser.add_argument("--port", type=int, default=8000, help="Port for remote server")
    args = parser.parse_args()

    # Discover and register all functions in the tools module as MCP tools
    for _, modname, _ in pkgutil.iter_modules(tools_module.__path__):
        module = __import__(f"{tools_module.__name__}.{modname}", fromlist=[modname])
        for _, obj in inspect.getmembers(module, inspect.isfunction):
            mcp.tool(obj)

    # Run the MCP server
    mcp.run(transport="http", show_banner=False, host=args.host, port=args.port)


if __name__ == "__main__":
    main()

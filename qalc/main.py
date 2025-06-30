def main():
    import os
    import argparse
    from dotenv import load_dotenv
    from datetime import datetime, timedelta, timezone
    from alpaca.trading.client import TradingClient as REST
    from qalc.strategies.rsi_trailing_stop import RSITrailingStopStrategy

    # Add more strategies here as needed
    STRATEGIES = {
        'rsi_trailing_stop': RSITrailingStopStrategy,
        # Add more strategies here
    }

    parser = argparse.ArgumentParser(description='Trading Strategy Runner')
    subparsers = parser.add_subparsers(dest='command', required=True)

    backtest_parser = subparsers.add_parser('backtest', help='Run a backtest')
    backtest_parser.add_argument('--strategy', required=True, help='Strategy name (e.g. rsi_trailing_stop)')
    backtest_parser.add_argument('--symbol', default='AAPL', help='Symbol to backtest')
    backtest_parser.add_argument('--trail_percent', type=float, default=0.03, help='Trailing stop percent')
    backtest_parser.add_argument('--days', type=int, default=5, help='Number of days to backtest')

    args = parser.parse_args()
    load_dotenv()

    if args.command == 'backtest':
        API_KEY = os.environ.get('APCA_API_KEY_ID')
        API_SECRET = os.environ.get('APCA_API_SECRET_KEY')
        BASE_URL = os.environ.get('APCA_API_BASE_URL', 'https://paper-api.alpaca.markets')
        api = REST(API_KEY, API_SECRET, BASE_URL)

        strategy_cls = STRATEGIES.get(args.strategy)
        if not strategy_cls:
            print(f"Unknown strategy: {args.strategy}")
            exit(1)
        strategy = strategy_cls(api, symbol=args.symbol, trail_percent=args.trail_percent)

        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=args.days)
        strategy.backtest(start=start_date.isoformat(), end=end_date.isoformat())

if __name__ == '__main__':
    main()
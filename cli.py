#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot — CLI
Usage: python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
"""

import argparse
import sys

from bot.client import get_client
from bot.orders import place_market_order, place_limit_order, place_stop_market_order
from bot.exceptions import ValidationError, BinanceClientError, OrderPlacementError


DIVIDER = "=" * 52


def print_order_request(args: argparse.Namespace) -> None:
    print(f"\n{DIVIDER}")
    print("ORDER REQUEST")
    print("=============\n")
    print(f"  Symbol      : {args.symbol.upper()}")
    print(f"  Side        : {args.side.upper()}")
    print(f"  Type        : {args.type.upper()}")
    print(f"  Quantity    : {args.quantity}")
    if args.price:
        print(f"  Price       : {args.price}")
    if args.stop_price:
        print(f"  Stop Price  : {args.stop_price}")
    print()


def print_order_result(result: dict) -> None:
    print("  Order placed successfully.\n")
    print(f"  Order ID      : {result['order_id']}")
    print(f"  Status        : {result['status']}")
    print(f"  Executed Qty  : {result['executed_qty']}")
    print(f"  Avg Price     : {result['avg_price']}")
    if result.get("time_in_force"):
        print(f"  Time in Force : {result['time_in_force']}")
    print(f"\n{DIVIDER}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet CLI — place MARKET, LIMIT, or STOP_MARKET orders.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument(
        "--side", required=True, choices=["BUY", "SELL"], type=str.upper, help="BUY or SELL"
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["MARKET", "LIMIT", "STOP_MARKET"],
        type=str.upper,
        dest="type",
        help="Order type",
    )
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, default=None, help="Limit price (required for LIMIT)")
    parser.add_argument(
        "--stop-price", type=float, default=None, dest="stop_price",
        help="Stop price (required for STOP_MARKET)"
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    print_order_request(args)
    print("  Submitting order to Binance Futures Testnet...\n")

    try:
        client = get_client()

        if args.type == "MARKET":
            result = place_market_order(client, args.symbol, args.side, args.quantity)

        elif args.type == "LIMIT":
            if not args.price:
                parser.error("--price is required for LIMIT orders.")
            result = place_limit_order(client, args.symbol, args.side, args.quantity, args.price)

        elif args.type == "STOP_MARKET":
            if not args.stop_price:
                parser.error("--stop-price is required for STOP_MARKET orders.")
            result = place_stop_market_order(
                client, args.symbol, args.side, args.quantity, args.stop_price
            )

        print_order_result(result)

    except ValidationError as e:
        print(f"  [Validation Error] {e}\n{DIVIDER}\n", file=sys.stderr)
        sys.exit(1)
    except BinanceClientError as e:
        print(f"  [Connection Error] {e}\n{DIVIDER}\n", file=sys.stderr)
        sys.exit(1)
    except OrderPlacementError as e:
        print(f"  [Order Failed] {e}\n{DIVIDER}\n", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n  Cancelled by user.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()

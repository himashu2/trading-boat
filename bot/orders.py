import time
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

from bot.exceptions import OrderPlacementError
from bot.validators import validate_order_params
from bot.logging_config import setup_logger

logger = setup_logger()

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


def _execute_with_retry(fn, *args, **kwargs):
    """Retry an API call up to MAX_RETRIES times on transient failures."""
    last_exc = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return fn(*args, **kwargs)
        except BinanceAPIException as e:
            # Don't retry on client-side errors (4xx)
            if e.status_code and 400 <= e.status_code < 500:
                raise
            last_exc = e
            logger.warning(f"API call failed (attempt {attempt}/{MAX_RETRIES}): {e.message}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            last_exc = e
            logger.warning(f"Unexpected error on attempt {attempt}: {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    raise last_exc


def _format_response(raw: dict) -> dict:
    return {
        "order_id": raw.get("orderId"),
        "symbol": raw.get("symbol"),
        "side": raw.get("side"),
        "type": raw.get("type"),
        "status": raw.get("status"),
        "executed_qty": raw.get("executedQty"),
        "avg_price": raw.get("avgPrice") or raw.get("price"),
        "time_in_force": raw.get("timeInForce"),
    }


def place_market_order(client: Client, symbol: str, side: str, quantity: float) -> dict:
    symbol = symbol.upper()
    side = side.upper()

    validate_order_params(symbol, side, "MARKET", quantity)

    logger.info(f"Placing MARKET {side} order | {symbol} qty={quantity}")

    try:
        raw = _execute_with_retry(
            client.futures_create_order,
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
        result = _format_response(raw)
        logger.info(f"MARKET order placed | order_id={result['order_id']} status={result['status']}")
        return result
    except BinanceOrderException as e:
        logger.error(f"Order rejected by exchange: {e.message}")
        raise OrderPlacementError(f"Order rejected: {e.message}") from e
    except BinanceAPIException as e:
        logger.error(f"API error while placing order: {e.message}")
        raise OrderPlacementError(f"API error: {e.message}") from e


def place_limit_order(
    client: Client, symbol: str, side: str, quantity: float, price: float
) -> dict:
    symbol = symbol.upper()
    side = side.upper()

    validate_order_params(symbol, side, "LIMIT", quantity, price=price)

    logger.info(f"Placing LIMIT {side} order | {symbol} qty={quantity} price={price}")

    try:
        raw = _execute_with_retry(
            client.futures_create_order,
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC",
        )
        result = _format_response(raw)
        logger.info(f"LIMIT order placed | order_id={result['order_id']} status={result['status']}")
        return result
    except BinanceOrderException as e:
        logger.error(f"Order rejected by exchange: {e.message}")
        raise OrderPlacementError(f"Order rejected: {e.message}") from e
    except BinanceAPIException as e:
        logger.error(f"API error while placing order: {e.message}")
        raise OrderPlacementError(f"API error: {e.message}") from e


def place_stop_market_order(
    client: Client, symbol: str, side: str, quantity: float, stop_price: float
) -> dict:
    """Bonus: Stop-Market order — closes position when stop_price is hit."""
    symbol = symbol.upper()
    side = side.upper()

    validate_order_params(symbol, side, "STOP_MARKET", quantity, stop_price=stop_price)

    logger.info(
        f"Placing STOP_MARKET {side} order | {symbol} qty={quantity} stop_price={stop_price}"
    )

    try:
        raw = _execute_with_retry(
            client.futures_create_order,
            symbol=symbol,
            side=side,
            type="STOP_MARKET",
            quantity=quantity,
            stopPrice=stop_price,
        )
        result = _format_response(raw)
        logger.info(
            f"STOP_MARKET order placed | order_id={result['order_id']} status={result['status']}"
        )
        return result
    except BinanceOrderException as e:
        logger.error(f"Order rejected by exchange: {e.message}")
        raise OrderPlacementError(f"Order rejected: {e.message}") from e
    except BinanceAPIException as e:
        logger.error(f"API error while placing order: {e.message}")
        raise OrderPlacementError(f"API error: {e.message}") from e

from bot.exceptions import ValidationError

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT", "STOP_MARKET"}


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
    stop_price: float | None = None,
) -> None:
    if not symbol or not symbol.strip():
        raise ValidationError("Symbol cannot be empty.")

    if side.upper() not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be BUY or SELL.")

    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Supported: {', '.join(VALID_ORDER_TYPES)}"
        )

    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than 0. Got: {quantity}")

    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValidationError("LIMIT orders require a valid price > 0.")

    if order_type.upper() == "STOP_MARKET":
        if stop_price is None or stop_price <= 0:
            raise ValidationError("STOP_MARKET orders require a valid stop price > 0.")

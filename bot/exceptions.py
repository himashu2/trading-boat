class ValidationError(Exception):
    """Raised when user input fails validation."""
    pass


class BinanceClientError(Exception):
    """Raised when client initialization or authentication fails."""
    pass


class OrderPlacementError(Exception):
    """Raised when an order fails to place on Binance."""
    pass

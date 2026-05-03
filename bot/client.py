import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

from bot.exceptions import BinanceClientError
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()

TESTNET_FUTURES_URL = "https://testnet.binancefuture.com"


def get_client() -> Client:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise BinanceClientError(
            "BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file."
        )

    try:
        client = Client(api_key, api_secret, testnet=True)
        # Point to futures testnet explicitly
        client.FUTURES_URL = TESTNET_FUTURES_URL + "/fapi"
        client.futures_ping()
        logger.info("Binance Futures Testnet client initialized successfully.")
        return client
    except BinanceAPIException as e:
        logger.error(f"Authentication failed: {e.message}")
        raise BinanceClientError(f"Authentication failed: {e.message}") from e
    except Exception as e:
        logger.error(f"Failed to connect to Binance Testnet: {e}")
        raise BinanceClientError(f"Could not connect to Binance Testnet: {e}") from e

# Binance Futures Testnet Trading Bot

A lightweight CLI tool to place futures orders on Binance Testnet (USDT-M). Built for internal use — no GUI, no overhead.

---

## Features

- Place **MARKET**, **LIMIT**, and **STOP_MARKET** orders
- BUY / SELL support
- Input validation with clear error messages
- Retry mechanism for transient API failures
- Rotating file logs + console warnings
- Clean terminal output

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance client setup
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   ├── exceptions.py      # Custom exceptions
│   └── logging_config.py  # File + console logging
├── logs/
│   └── trading.log
├── cli.py                 # CLI entrypoint
├── .env.example
├── requirements.txt
└── .gitignore
```

---

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd trading_bot

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Binance Futures Testnet API keys

1. Go to [https://testnet.binancefuture.com](https://testnet.binancefuture.com)
2. Log in with your GitHub account
3. Generate API Key + Secret from the dashboard

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env and fill in your API key and secret
```

---

## Usage

### Market Order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit Order

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3200
```

### Stop-Market Order

```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 90000
```

---

## Example Output

```
====================================================
ORDER REQUEST
=============

  Symbol      : BTCUSDT
  Side        : BUY
  Type        : MARKET
  Quantity    : 0.001

  Submitting order to Binance Futures Testnet...

  Order placed successfully.

  Order ID      : 3847291038
  Status        : FILLED
  Executed Qty  : 0.001
  Avg Price     : 94512.30

====================================================
```

---

## Logging

All activity is logged to `logs/trading.log` with rotation (max 5MB, 3 backups).

Log includes: order requests, API responses, validation failures, retries, and errors.

Console only shows `WARNING` level and above — logs have full `DEBUG` detail.

---

## Assumptions

- Only USDT-M Futures Testnet is supported (not Spot, not Coin-M)
- `timeInForce` for LIMIT orders is hardcoded to `GTC` (Good Till Cancelled)
- Quantity precision must match the symbol's requirements on Binance — no auto-rounding
- STOP_MARKET orders use `closePosition=False` by default (quantity-based, not full close)

---

## Possible Improvements

- Auto-fetch symbol precision and round quantity accordingly
- Add `--dry-run` flag to validate without placing orders
- Support order cancellation via CLI
- Add position status check before placing orders
- Config file support (TOML/YAML) for default symbol/quantity

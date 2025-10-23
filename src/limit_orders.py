"""
Binance Futures Bot - Limit Orders Module
-----------------------------------------
Handles creation and validation of LIMIT orders on Binance Futures Testnet.
Includes intelligent input validation, symbol suggestions, retry loops,
and descriptive Binance API error handling.
"""

import os
import logging
import difflib
from binance.client import Client
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException, BinanceRequestException

# ---------------------------------------------------------------------------
# Load API Keys and Setup Logging
# ---------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ---------------------------------------------------------------------------
# Connect to Binance Testnet
# ---------------------------------------------------------------------------
client = Client(api_key, api_secret, testnet=True)

# ---------------------------------------------------------------------------
# Utility: Fetch and Display Valid Symbols
# ---------------------------------------------------------------------------
def show_available_symbols():
    """Fetches valid symbols and shows examples for user reference."""
    try:
        exchange_info = client.futures_exchange_info()
        symbols = [s["symbol"] for s in exchange_info["symbols"] if s["status"] == "TRADING"]
        print("\n📊 Example valid symbols:")
        print(", ".join(symbols[:10]) + ", ...")
        return symbols
    except Exception as e:
        print("⚠️ Unable to fetch symbol list from Binance. Please check connection.")
        logging.error(f"Error fetching symbol list: {e}")
        return []

# ---------------------------------------------------------------------------
# Utility: Suggest Closest Symbol
# ---------------------------------------------------------------------------
def suggest_symbol(input_symbol, valid_symbols):
    """Suggests the closest match when user enters a mistyped symbol."""
    suggestion = difflib.get_close_matches(input_symbol.upper(), valid_symbols, n=1)
    if suggestion:
        print(f"⚠️ Invalid symbol '{input_symbol}'. Did you mean {suggestion[0]}?")
    else:
        print("⚠️ Invalid symbol. Please check available trading pairs.")

# ---------------------------------------------------------------------------
# Input Validation Utilities
# ---------------------------------------------------------------------------
def get_valid_input(prompt, valid_func, error_msg):
    """Keeps prompting user until valid input is received."""
    while True:
        value = input(prompt).strip()
        if valid_func(value):
            return value
        print(f"⚠️ {error_msg}")

def is_valid_side(s):
    return s.upper() in ["BUY", "SELL"]

def is_positive_float(s):
    try:
        return float(s) > 0
    except ValueError:
        return False

# ---------------------------------------------------------------------------
# Core Function: Place LIMIT Order
# ---------------------------------------------------------------------------
def place_limit_order(symbol, side, quantity, price):
    """
    Places a LIMIT order with detailed validations and exception handling.
    Prevents invalid or too-small notional orders before sending to Binance.
    """
    try:
        symbol = symbol.upper()
        side = side.upper()
        quantity = float(quantity)
        price = float(price)
        notional = quantity * price

        if notional < 100:
            print(f"⚠️ Order value too small (${notional:.2f}). Must be ≥ $100.")
            return

        logging.info(f"Attempting {side} LIMIT order: {symbol} @ {price}, qty={quantity}")

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )

        logging.info(f"✅ Limit order placed successfully: {order}")
        print("✅ Limit order placed successfully!")

    except BinanceAPIException as e:
        logging.error(f"Binance API error: {e}")
        if e.code == -1121:
            print("❌ Error: Invalid symbol.")
        elif e.code == -4164:
            print("❌ Error: Order’s notional must be ≥ $100. Increase quantity or adjust price.")
        elif e.code == -2019:
            print("❌ Error: Insufficient margin. Add more funds to your testnet wallet.")
        elif e.code == -2015:
            print("❌ Error: Invalid API key or permissions. Check your .env.")
        else:
            print(f"❌ Binance API Error ({e.code}): {e.message}")

    except BinanceRequestException as e:
        logging.error(f"Network error: {e}")
        print("⚠️ Network issue: Binance server unreachable. Please retry shortly.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print("❌ Unexpected error:", e)

# ---------------------------------------------------------------------------
# Main Execution Flow
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n💹 Welcome to Binance Futures Limit Order Bot\n")
    valid_symbols = show_available_symbols()

    # Symbol validation with auto-suggestion
    while True:
        symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
        if symbol in valid_symbols:
            break
        suggest_symbol(symbol, valid_symbols)

    side = get_valid_input(
        "Enter side (BUY/SELL): ",
        is_valid_side,
        "Invalid side. Type BUY or SELL."
    ).upper()

    qty_str = get_valid_input(
        "Enter quantity: ",
        is_positive_float,
        "Invalid quantity. Must be a positive number."
    )

    price_str = get_valid_input(
        "Enter limit price: ",
        is_positive_float,
        "Invalid price. Must be a positive number."
    )

    quantity = float(qty_str)
    price = float(price_str)

    place_limit_order(symbol, side, quantity, price)

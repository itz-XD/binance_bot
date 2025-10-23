"""
Binance Futures Bot - Market Orders Module
------------------------------------------
Handles creation and validation of MARKET orders on Binance Futures Testnet.
Includes robust input validation, retry loops, intelligent symbol checking,
auto-suggestions for mistyped symbols, and detailed error handling.
"""

import os
import logging
import difflib
from binance.client import Client
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException, BinanceRequestException

# ---------------------------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

# ---------------------------------------------------------------------------
# Configure Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ---------------------------------------------------------------------------
# Initialize Binance Client (Testnet)
# ---------------------------------------------------------------------------
client = Client(api_key, api_secret, testnet=True)

# ---------------------------------------------------------------------------
# Utility: Fetch and display valid symbols
# ---------------------------------------------------------------------------
def show_available_symbols():
    """Displays a few valid symbols from Binance Futures."""
    try:
        exchange_info = client.futures_exchange_info()
        symbols = [s["symbol"] for s in exchange_info["symbols"] if s["status"] == "TRADING"]
        print("\n📊 Example valid symbols:")
        print(", ".join(symbols[:10]) + ", ...")
        return symbols
    except Exception as e:
        print("⚠️ Unable to fetch symbol list from Binance. Please check your internet.")
        logging.error(f"Error fetching symbols: {e}")
        return []

# ---------------------------------------------------------------------------
# Utility: Suggest symbol if mistyped
# ---------------------------------------------------------------------------
def suggest_symbol(input_symbol, valid_symbols):
    """Suggests closest matching symbol if user input is invalid."""
    suggestion = difflib.get_close_matches(input_symbol.upper(), valid_symbols, n=1)
    if suggestion:
        print(f"⚠️ Invalid symbol '{input_symbol}'. Did you mean {suggestion[0]}?")
    else:
        print("⚠️ Invalid symbol. Please check the available trading pairs.")

# ---------------------------------------------------------------------------
# Utility: Get validated input with retry logic
# ---------------------------------------------------------------------------
def get_valid_input(prompt, valid_func, error_msg):
    """Continuously prompts until valid input is entered."""
    while True:
        value = input(prompt).strip()
        if valid_func(value):
            return value
        print(f"⚠️ {error_msg}")

# ---------------------------------------------------------------------------
# Validation Functions
# ---------------------------------------------------------------------------
def is_valid_side(s):
    return s.upper() in ["BUY", "SELL"]

def is_positive_float(s):
    try:
        return float(s) > 0
    except ValueError:
        return False

# ---------------------------------------------------------------------------
# Core Function: Place MARKET Order
# ---------------------------------------------------------------------------
def place_market_order(symbol, side, quantity):
    """
    Attempts to place a MARKET order on Binance Futures Testnet.
    Includes detailed error handling and suggestions for invalid inputs.
    """
    try:
        logging.info(f"Attempting {side} MARKET order: {symbol}, qty={quantity}")

        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )

        logging.info(f"✅ Market order placed successfully: {order}")
        print("✅ Market order placed successfully!")

    except BinanceAPIException as e:
        logging.error(f"Binance API error: {e}")
        if e.code == -1121:  # Invalid symbol
            print("❌ Error: Invalid symbol.")
        elif e.code == -2019:
            print("❌ Error: Insufficient margin. Add more funds to your testnet wallet.")
        elif e.code == -2015:
            print("❌ Error: Invalid API key or permissions. Check your .env and API settings.")
        else:
            print(f"❌ Binance API Error ({e.code}): {e.message}")

    except BinanceRequestException as e:
        logging.error(f"Network error: {e}")
        print("⚠️ Network issue: Binance server unreachable. Please try again later.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print("❌ Unexpected error:", e)

# ---------------------------------------------------------------------------
# Main Program Execution
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n📈 Welcome to Binance Futures Market Order Bot\n")
    valid_symbols = show_available_symbols()

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
    quantity = float(qty_str)

    place_market_order(symbol, side, quantity)

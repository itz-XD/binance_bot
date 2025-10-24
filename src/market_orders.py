"""
market_orders.py
----------------
Handles MARKET order placement with validation, symbol suggestions,
margin asset detection, and detailed error handling.
"""

import difflib
import logging
from config import client

# Utility functions
def show_available_symbols():
    """Get and show a few tradable symbols."""
    try:
        info = client.futures_exchange_info()
        symbols = [s["symbol"] for s in info["symbols"] if s["status"] == "TRADING"]
        print("\n📊 Example valid symbols:")
        print(", ".join(symbols[:10]) + ", ...")
        return symbols
    except Exception as e:
        logging.error(f"Error fetching symbols: {e}")
        print("⚠️ Unable to fetch symbols.")
        return []

def suggest_symbol(user_input, valid_symbols):
    """Suggest closest symbol if mistyped."""
    suggestion = difflib.get_close_matches(user_input.upper(), valid_symbols, n=1)
    if suggestion:
        print(f"⚠️ Invalid symbol '{user_input}'. Did you mean {suggestion[0]}?")
    else:
        print("⚠️ Unknown symbol. Check available pairs.")

def get_valid_input(prompt, validate_fn, msg):
    while True:
        val = input(prompt).strip()
        if validate_fn(val):
            return val
        print(f"⚠️ {msg}")

def is_valid_side(s): return s.upper() in ["BUY", "SELL"]
def is_positive_float(s):
    try: return float(s) > 0
    except ValueError: return False

def place_market_order():
    """Place a MARKET order with margin detection and validation."""
    print("\n🟢 MARKET ORDER\n")
    valid_symbols = show_available_symbols()

    while True:
        symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
        if symbol in valid_symbols: break
        suggest_symbol(symbol, valid_symbols)

    side = get_valid_input("Side (BUY/SELL): ", is_valid_side, "Type BUY or SELL.").upper()
    qty = float(get_valid_input("Quantity: ", is_positive_float, "Enter a positive number."))

    try:
        # Check notional requirement
        mark_price = float(client.futures_mark_price(symbol=symbol)["markPrice"])
        if mark_price * qty < 100:
            print(f"⚠️ Order notional too small (${mark_price * qty:.2f}). Must be ≥ $100.")
            return

        order = client.futures_create_order(symbol=symbol, side=side, type="MARKET", quantity=qty)
        print("✅ Market order placed successfully!")
        logging.info(f"Market order: {symbol} {side} {qty}")

    except Exception as e:
        print("❌ Error:", e)
        logging.error(f"Order error: {e}")

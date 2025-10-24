"""
limit_orders.py
----------------
Places LIMIT orders with input validation, symbol suggestions,
and margin-based notional checks.
"""

import difflib
import logging
from config import client

def show_available_symbols():
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

def suggest_symbol(s, valid_symbols):
    suggestion = difflib.get_close_matches(s.upper(), valid_symbols, n=1)
    if suggestion:
        print(f"⚠️ Invalid symbol '{s}'. Did you mean {suggestion[0]}?")
    else:
        print("⚠️ Unknown symbol. Check available pairs.")

def get_valid_input(prompt, fn, msg):
    while True:
        val = input(prompt).strip()
        if fn(val): return val
        print(f"⚠️ {msg}")

def is_valid_side(s): return s.upper() in ["BUY", "SELL"]
def is_positive_float(s):
    try: return float(s) > 0
    except ValueError: return False

def place_limit_order():
    print("\n🟡 LIMIT ORDER\n")
    valid_symbols = show_available_symbols()

    while True:
        symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
        if symbol in valid_symbols: break
        suggest_symbol(symbol, valid_symbols)

    side = get_valid_input("Side (BUY/SELL): ", is_valid_side, "Type BUY or SELL.").upper()
    qty = float(get_valid_input("Quantity: ", is_positive_float, "Enter positive number."))
    price = float(get_valid_input("Limit Price: ", is_positive_float, "Enter positive number."))

    notional = qty * price
    if notional < 100:
        print(f"⚠️ Order too small (${notional:.2f}). Must be ≥ $100.")
        return

    try:
        client.futures_create_order(symbol=symbol, side=side, type="LIMIT", timeInForce="GTC", quantity=qty, price=price)
        print("✅ Limit order placed successfully!")
        logging.info(f"Limit order: {symbol} {side} {qty}@{price}")
    except Exception as e:
        print("❌ Error:", e)
        logging.error(f"Order error: {e}")

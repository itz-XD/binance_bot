"""
Binance Futures Bot - Interactive CLI Terminal
----------------------------------------------
A unified console interface for placing orders, viewing account info,
checking/cancelling orders, and managing testnet trading activity.
"""

import os
import logging
import time
from binance.client import Client
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException, BinanceRequestException

# ────────────────────────────────────────────────────────────────
# Load API Keys and Setup Logging
# ────────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

client = Client(api_key, api_secret, testnet=True)

# ────────────────────────────────────────────────────────────────
# Utility helpers
# ────────────────────────────────────────────────────────────────
def safe_input(prompt, valid_fn, msg):
    """Keep asking user until valid input is given."""
    while True:
        val = input(prompt).strip()
        if valid_fn(val):
            return val
        print(f"⚠️ {msg}")

def is_positive_float(s):
    try:
        return float(s) > 0
    except ValueError:
        return False

def is_valid_side(s):
    return s.upper() in ["BUY", "SELL"]

def is_valid_symbol(s):
    return s.isalnum() and len(s) >= 3

# ────────────────────────────────────────────────────────────────
# Trading actions
# ────────────────────────────────────────────────────────────────
def place_market_order():
    print("\n🟢 Market Order\n")
    symbol = safe_input("Symbol (e.g., BTCUSDT): ", is_valid_symbol, "Enter valid pair.")
    side = safe_input("Side (BUY/SELL): ", is_valid_side, "Enter BUY or SELL.").upper()
    qty = float(safe_input("Quantity: ", is_positive_float, "Must be positive number."))

    try:
        client.futures_create_order(symbol=symbol.upper(), side=side, type="MARKET", quantity=qty)
        print("✅ Market order placed successfully!")
        logging.info(f"Market order: {symbol} {side} {qty}")
    except BinanceAPIException as e:
        print(f"❌ API error ({e.code}): {e.message}")
    except BinanceRequestException:
        print("⚠️ Network issue.")
    except Exception as e:
        print("❌ Unexpected:", e)

def place_limit_order():
    print("\n🟡 Limit Order\n")
    symbol = safe_input("Symbol (e.g., BTCUSDT): ", is_valid_symbol, "Enter valid pair.")
    side = safe_input("Side (BUY/SELL): ", is_valid_side, "Enter BUY or SELL.").upper()
    qty = float(safe_input("Quantity: ", is_positive_float, "Must be positive number."))
    price = float(safe_input("Limit price: ", is_positive_float, "Must be positive number."))

    notional = qty * price
    if notional < 100:
        print(f"⚠️ Order value too small (${notional:.2f}). Must be ≥ $100.")
        return

    try:
        client.futures_create_order(
            symbol=symbol.upper(), side=side, type="LIMIT",
            timeInForce="GTC", quantity=qty, price=price)
        print("✅ Limit order placed successfully!")
        logging.info(f"Limit order: {symbol} {side} {qty}@{price}")
    except BinanceAPIException as e:
        print(f"❌ API error ({e.code}): {e.message}")
    except BinanceRequestException:
        print("⚠️ Network issue.")
    except Exception as e:
        print("❌ Unexpected:", e)

def show_account_info():
    print("\n💰 Account Info\n")
    try:
        bal = client.futures_account_balance()
        acct = client.futures_account()
        print("Balances:")
        for b in bal:
            if float(b["balance"]) > 0:
                print(f"  → {b['asset']}: {b['balance']}  (avail {b['withdrawAvailable']})")
        print("\nPositions:")
        for p in acct["positions"]:
            if float(p["positionAmt"]) != 0:
                side = "LONG" if float(p["positionAmt"]) > 0 else "SHORT"
                print(f"  → {p['symbol']} | {side} {p['positionAmt']} @ {p['entryPrice']} | PnL {p['unrealizedProfit']}")
    except Exception as e:
        print("❌ Error:", e)

def check_orders():
    print("\n📜 Check Orders\n")
    symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
    try:
        open_orders = client.futures_get_open_orders(symbol=symbol)
        if not open_orders:
            print("✅ No open orders.")
        else:
            for o in open_orders:
                print(f"→ {o['orderId']} | {o['side']} {o['type']} {o['origQty']} @ {o['price']} | {o['status']}")
    except Exception as e:
        print("❌ Error:", e)

def cancel_orders():
    print("\n🗑️ Cancel Orders\n")
    symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
    try:
        open_orders = client.futures_get_open_orders(symbol=symbol)
        if not open_orders:
            print("✅ No open orders.")
            return
        for o in open_orders:
            print(f"→ {o['orderId']} | {o['side']} {o['type']} | {o['status']}")
        choice = input("Enter order ID or 'ALL': ").strip().upper()
        if choice == "ALL":
            client.futures_cancel_all_open_orders(symbol=symbol)
            print("✅ All orders cancelled.")
        else:
            client.futures_cancel_order(symbol=symbol, orderId=int(choice))
            print(f"✅ Order {choice} cancelled.")
    except Exception as e:
        print("❌ Error:", e)

# ────────────────────────────────────────────────────────────────
# CLI Menu
# ────────────────────────────────────────────────────────────────
def main_menu():
    while True:
        print("""
═══════════════════════════════════════════
🧠  Binance Futures Testnet Terminal
═══════════════════════════════════════════
[1] Place MARKET Order
[2] Place LIMIT Order
[3] Check Orders
[4] Cancel Orders
[5] Account Info
[0] Exit
""")
        choice = input("Select option: ").strip()

        if choice == "1":
            place_market_order()
        elif choice == "2":
            place_limit_order()
        elif choice == "3":
            check_orders()
        elif choice == "4":
            cancel_orders()
        elif choice == "5":
            show_account_info()
        elif choice == "0":
            print("\n👋 Exiting bot. See you soon!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")
        time.sleep(1.5)

# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🚀 Binance Futures Trading CLI (Testnet)\n")
    main_menu()

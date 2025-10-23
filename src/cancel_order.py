"""
Binance Futures Bot - Cancel Orders Module
------------------------------------------
Allows user to cancel a specific order by ID or cancel all open orders.
"""

import os
import logging
from binance.client import Client
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException, BinanceRequestException

# ---------------------------------------------------------------------------
# Load Keys & Configure Client
# ---------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

client = Client(api_key, api_secret, testnet=True)

# ---------------------------------------------------------------------------
# Cancel Orders
# ---------------------------------------------------------------------------
def cancel_orders(symbol):
    """Cancel open orders for a specific symbol."""
    try:
        symbol = symbol.upper()
        open_orders = client.futures_get_open_orders(symbol=symbol)

        if not open_orders:
            print("✅ No open orders to cancel.")
            return

        print(f"\n📜 Open Orders for {symbol}:")
        for order in open_orders:
            print(f"→ ID: {order['orderId']} | {order['type']} | {order['side']} | {order['status']}")

        choice = input("\nEnter order ID to cancel (or type 'ALL' to cancel all): ").strip().upper()

        if choice == "ALL":
            client.futures_cancel_all_open_orders(symbol=symbol)
            print("✅ All open orders cancelled successfully!")
        else:
            client.futures_cancel_order(symbol=symbol, orderId=int(choice))
            print(f"✅ Order {choice} cancelled successfully!")

    except BinanceAPIException as e:
        print(f"❌ Binance API Error ({e.code}): {e.message}")
        logging.error(f"Binance API error: {e}")

    except BinanceRequestException as e:
        print("⚠️ Network issue: Binance server unreachable.")
        logging.error(f"Network error: {e}")

    except Exception as e:
        print("❌ Unexpected error:", e)
        logging.error(f"Unexpected error: {e}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n🗑️ Binance Futures - Cancel Orders\n")
    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
    cancel_orders(symbol)

"""
Binance Futures Bot - Check Orders Module
-----------------------------------------
Displays all open and recently filled orders for a given trading symbol.
Includes network error handling and descriptive output.
"""

import os
import logging
from binance.client import Client
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException, BinanceRequestException

# ---------------------------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

client = Client(api_key, api_secret, testnet=True)

# ---------------------------------------------------------------------------
# Display Open and Recent Orders
# ---------------------------------------------------------------------------
def check_orders(symbol):
    """Fetch and display open and filled orders for the given symbol."""
    try:
        symbol = symbol.upper()
        open_orders = client.futures_get_open_orders(symbol=symbol)
        all_orders = client.futures_get_all_orders(symbol=symbol, limit=5)

        print(f"\n📜 Open Orders for {symbol}:")
        if open_orders:
            for order in open_orders:
                print(f"→ ID: {order['orderId']} | Type: {order['type']} | Side: {order['side']} | Price: {order['price']} | Qty: {order['origQty']} | Status: {order['status']}")
        else:
            print("✅ No open orders found.")

        print(f"\n📈 Recent Orders for {symbol}:")
        if all_orders:
            for order in all_orders[-5:]:
                print(f"→ ID: {order['orderId']} | Status: {order['status']} | Type: {order['type']} | Qty: {order['origQty']} | Price: {order['price']}")
        else:
            print("No recent orders found.")

    except BinanceAPIException as e:
        print(f"❌ Binance API Error ({e.code}): {e.message}")
        logging.error(f"Binance API error: {e}")

    except BinanceRequestException as e:
        print("⚠️ Network issue: Unable to reach Binance server.")
        logging.error(f"Network error: {e}")

    except Exception as e:
        print("❌ Unexpected error:", e)
        logging.error(f"Unexpected error: {e}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n🧾 Binance Futures - Check Orders\n")
    symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
    check_orders(symbol)

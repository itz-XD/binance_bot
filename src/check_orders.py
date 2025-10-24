"""
check_orders.py
---------------
Displays all open and recent orders for a given symbol.
"""

import logging
from config import client

def check_orders(symbol):
    """Display open and recent futures orders."""
    try:
        open_orders = client.futures_get_open_orders(symbol=symbol)
        all_orders = client.futures_get_all_orders(symbol=symbol, limit=5)

        print(f"\n📜 Open Orders for {symbol}:")
        if open_orders:
            for o in open_orders:
                print(f"→ {o['orderId']} | {o['side']} {o['type']} {o['origQty']} @ {o['price']} | {o['status']}")
        else:
            print("✅ No open orders.")

        print(f"\n📈 Recent Orders for {symbol}:")
        for o in all_orders[-5:]:
            print(f"→ {o['orderId']} | {o['status']} | {o['type']} | {o['origQty']} @ {o['price']}")

    except Exception as e:
        print("❌ Error:", e)
        logging.error(f"Check orders error: {e}")

"""
cancel_orders.py
----------------
Cancel a specific order by ID or all open orders for a symbol.
"""

import logging
from config import client

def cancel_orders(symbol):
    """Cancel open futures orders."""
    try:
        open_orders = client.futures_get_open_orders(symbol=symbol)
        if not open_orders:
            print("✅ No open orders to cancel.")
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
        logging.error(f"Cancel error: {e}")




if __name__ == "__main__":
    cancel_orders(input("Symbol: "))
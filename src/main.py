"""
main.py
-------
Interactive CLI for Binance Futures Bot (Testnet)
Includes all trading actions: place orders, cancel, view, and account info.
"""

import time
from market_orders import place_market_order
from limit_orders import place_limit_order
from check_orders import check_orders
from cancel_orders import cancel_orders
from account_info import display_account_info

# CLI Menu
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
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            check_orders(symbol)
        elif choice == "4":
            symbol = input("Enter symbol (e.g., BTCUSDT): ").strip().upper()
            cancel_orders(symbol)
        elif choice == "5":
            display_account_info()
        elif choice == "0":
            print("\n👋 Exiting bot. See you soon!")
            break
        else:
            print("⚠️ Invalid choice. Try again.")
        time.sleep(1.2)


if __name__ == "__main__":
    print("\n🚀 Binance Futures Trading CLI (Pro Edition - Testnet)\n")
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n🛑 Gracefully shutting down. Bye!\n")

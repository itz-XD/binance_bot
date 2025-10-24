"""
account_info.py
---------------
Shows account balances, available margin, and open positions with leverage.
"""

import logging
from config import client

def display_account_info():
    """Show Futures balances and open positions."""
    try:
        account = client.futures_account()
        balances = client.futures_account_balance()

        print("\n💰 Binance Futures Account Summary:")
        print(f"{'Asset':<6} {'Balance':>12} {'Available':>12} {'Cross Wallet':>15}")
        print("-" * 50)
        for b in balances:
            bal = float(b.get("balance", 0))
            if bal > 0:
                print(f"{b['asset']:<6} {bal:>12} {b.get('availableBalance','-'):>12} {b.get('crossWalletBalance','-'):>15}")

        print("\n📊 Open Positions:")
        positions = [p for p in account["positions"] if float(p["positionAmt"]) != 0]
        if not positions:
            print("✅ No open positions.")
        else:
            for p in positions:
                amt = float(p["positionAmt"])
                side = "LONG" if amt > 0 else "SHORT"
                print(f"→ {p['symbol']} | {side} {amt} @ {p['entryPrice']} | Leverage: {p['leverage']}x | PnL: {p['unrealizedProfit']}")

    except Exception as e:
        print("❌ Error:", e)
        logging.error(f"Account info error: {e}")



if __name__ == "__main__":
    display_account_info()
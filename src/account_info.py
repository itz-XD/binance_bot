"""
Binance Futures Bot - Account Info Module
-----------------------------------------
Displays key account metrics including wallet balance, positions,
unrealized profit/loss, and margin usage for the Testnet account.
"""

import os
import logging
from binance.client import Client
from dotenv import load_dotenv
from binance.exceptions import BinanceAPIException, BinanceRequestException

# ---------------------------------------------------------------------------
# Load API Keys & Initialize Client
# ---------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_SECRET_KEY")

logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

client = Client(api_key, api_secret, testnet=True)

# ---------------------------------------------------------------------------
# Account Information
# ---------------------------------------------------------------------------
def display_account_info():
    """Fetch and display Futures account balances and positions."""
    try:
        account_info = client.futures_account()
        balance_info = client.futures_account_balance()

        print("\n💰 Binance Futures Account Summary:")
        for b in balance_info:
            if float(b["balance"]) > 0:
                print(f"→ {b['asset']}: Balance = {b['balance']} | Withdraw Available = {b['withdrawAvailable']}")

        print("\n📊 Open Positions:")
        positions = [p for p in account_info["positions"] if float(p["positionAmt"]) != 0]
        if not positions:
            print("✅ No open positions currently.")
        else:
            for p in positions:
                print(f"→ {p['symbol']} | Side: {'LONG' if float(p['positionAmt']) > 0 else 'SHORT'} "
                      f"| Size: {p['positionAmt']} | Entry: {p['entryPrice']} | Unrealized PnL: {p['unrealizedProfit']}")

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
    print("\n📈 Binance Futures - Account Information\n")
    display_account_info()

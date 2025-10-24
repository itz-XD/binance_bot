"""
config.py
---------
Centralized configuration for Binance Futures Bot.
Handles API key loading, client setup, logging, and timestamp sync.
"""

import os
import time
import logging
from dotenv import load_dotenv
from binance.client import Client

# Load keys
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

# Logging setup (shared)
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize Binance client
client = Client(API_KEY, API_SECRET, testnet=True)
client.RECV_WINDOW = 10000  # 10 seconds to tolerate drift

# Sync local time offset with Binance server
try:
    server_time = client.futures_time()
    local_time = int(time.time() * 1000)
    client.timestamp_offset = server_time["serverTime"] - local_time
    logging.info("✅ Binance time sync successful.")
except Exception as e:
    logging.warning(f"⚠️ Time sync failed: {e}")

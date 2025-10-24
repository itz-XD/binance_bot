# Binance Futures Order Bot 🪙

## Overview
This is a simple CLI-based Binance Futures trading bot written in Python.  
It allows you to place **Market** and **Limit** orders directly from your terminal.  
All actions are logged for easy troubleshooting, and the bot features robust input validation to keep your trading safe and reliable.

---

## 📦 Features

- ✅ Place Market Orders
- ✅ Place Limit Orders
- ✅ Input validation for symbol, quantity, side, and price
- ✅ Logging of all actions to `bot.log`
- ✅ Check orders, cancel orders, and view account info
- ✅ Modular code and professional error handling

---

## 🛠️ Setup Instructions

### 1. Install Dependencies
```
pip install python-binance python-dotenv
```
Or, if you have requirements.txt:
```
pip install -r requirements.txt
```

### 2. Clone the Repository
```
git clone https://github.com/itz-XD/binance_bot.git
cd binance_bot
```

### 3. Configure API Keys
Create a `.env` file in your project root with:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
```
**Note:** Use Binance Futures Testnet API keys for safe testing.

---

## ⚙️ File Structure

```
your_name_binance_bot/
│
├── src/
│   ├── main.py
│   ├── config.py
│   ├── market_orders.py
│   ├── limit_orders.py
│   ├── check_orders.py
│   ├── cancel_orders.py
│   ├── account_info.py
│   └── advanced/
│       ├── (oco.py)           # For OCO feature if implemented
│       └── (twap.py)          # For TWAP feature if implemented
├── bot.log           # All order actions and errors
├── .env              # API keys (not committed to git)
├── README.md
├── report.pdf        # Analysis, screenshots, error summary
├── requirements.txt
```

---

## 🚀 How to Run

#### 1. Interactive CLI Terminal
```
python src/main.py
```
You will see:
```
🚀 Binance Futures Trading CLI (Pro Edition - Testnet)


═══════════════════════════════════════════
🧠  Binance Futures Testnet Terminal
═══════════════════════════════════════════
[1] Place MARKET Order
[2] Place LIMIT Order
[3] Check Orders
[4] Cancel Orders
[5] Account Info
[0] Exit

Select option:
```
Follow interactive prompts for each feature.  
All logs and errors are saved to `bot.log` for review.

#### 2. Direct Module Testing

To run individual features, e.g., Market Orders:
```
python src/market_orders.py
```

---

## 🧩 Notes

- All filenames are descriptive — no hardcoded or generic names used.
- All API credentials are kept in `.env` for security.
- All user inputs are validated before making trading calls.
- Please use **Testnet only** for safe development.

---

## ⚡ Advanced Features

Advanced features such as OCO, TWAP, Stop-Limit, and Grid strategy can be added in `src/advanced/` as bonus modules if implemented.

---

## 📖 Resources

- [Binance Futures API Docs](https://binance-docs.github.io/apidocs/futures/en/)
- [python-binance library](https://github.com/sammchardy/python-binance)
- [Dotenv for Python](https://pypi.org/project/python-dotenv/)

---

## 📝 Report & Documentation

See `report.pdf` in the project for:
- Screenshots of CLI terminal in action
- Explanation of main modules and error handling
- Project architecture/flowchart

---

## Contact

For questions or support, contact: sornayan.x@gmail.com

---

**Happy Trading!**
# Crypto Price Alert Bot

A fast and lightweight Telegram bot that notifies you instantly when a cryptocurrency price crosses your target (using Binance USDT pairs).

## Features

- `/up BTC 65000` → alerts when price goes above 65,000
- `/down ETH 3000` → alerts when price drops below 3,000
- `/list` → show all your active alerts
- `/clear` → remove all alerts
- `/price SOL` → get current price
- Runs every 15 seconds, no heavy database

## Status

**In active development**
I'm currently learning and improving the bot every day — expect frequent commits!

## Requirements

* Python 3.10+
* Aiogram 3.x
* A Binance API endpoint (public market data)
* A Telegram Bot Token stored in `.env`

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your bot token:

   ```
   BOT_TOKEN=your_token_here
   ```
4. Run the bot:

   ```
   python bot.py
   ```

## Roadmap

- [X] Basic up/down alerts
- [X] Smart mistake detection
- [ ] Persistent alerts (SQLite)
- [ ] Bulk price fetching (one request instead of many)
- [ ] WebSocket support (real-time, no polling)
- [ ] Deploy on VPS / Docker

Contributions, suggestions and stars are very welcome!

---

## License

Distributed under the [MIT License](LICENSE).

---

Made with love while learning

---

*Last updated: Nov 2025*
